import os
import csv
import json
import time
import requests
from datetime import datetime
from typing import Any, Dict, List, Optional

# Agora aceitamos ORGS="org1,org2,org3"
ORGS_RAW = os.environ.get("ORGS", "").strip()
TOKEN = os.environ.get("GH_TOKEN", "").strip()

if not ORGS_RAW:
    raise SystemExit("Missing env ORGS (comma-separated list)")
if not TOKEN:
    raise SystemExit("Missing env GH_TOKEN")

ORGS = [o.strip() for o in ORGS_RAW.split(",") if o.strip()]
if not ORGS:
    raise SystemExit("ORGS is empty after parsing")

API = "https://api.github.com"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

REPORT_DIR = "reports"
os.makedirs(REPORT_DIR, exist_ok=True)


def gh_get(url: str, params: Optional[dict] = None) -> requests.Response:
    r = requests.get(url, headers=HEADERS, params=params, timeout=60)

    # rate limit handling (basic)
    if r.status_code == 403 and "rate limit" in r.text.lower():
        reset = r.headers.get("X-RateLimit-Reset")
        if reset:
            wait = max(0, int(reset) - int(time.time()) + 5)
            print(f"[rate-limit] sleeping {wait}s")
            time.sleep(wait)
            r = requests.get(url, headers=HEADERS, params=params, timeout=60)

    r.raise_for_status()
    return r


def list_org_repos(org: str) -> List[Dict[str, Any]]:
    repos = []
    page = 1
    while True:
        r = gh_get(f"{API}/orgs/{org}/repos", params={
            "per_page": 100,
            "page": page,
            "type": "all",     # public + private (depende do token ter acesso)
            "sort": "full_name",
            "direction": "asc",
        })
        batch = r.json()
        if not batch:
            break
        repos.extend(batch)
        page += 1
    return repos


def get_branch_head_sha(owner: str, repo: str, branch: str) -> Optional[str]:
    url = f"{API}/repos/{owner}/{repo}/git/ref/heads/{branch}"
    try:
        r = gh_get(url)
        return r.json().get("object", {}).get("sha")
    except requests.HTTPError as e:
        print(f"[warn] ref not found {owner}/{repo}@{branch}: {e}")
        return None


def get_tree(owner: str, repo: str, sha: str) -> Optional[List[Dict[str, Any]]]:
    url = f"{API}/repos/{owner}/{repo}/git/trees/{sha}"
    try:
        r = gh_get(url, params={"recursive": 1})
        data = r.json()
        return data.get("tree", [])
    except requests.HTTPError as e:
        print(f"[warn] tree not found {owner}/{repo}: {e}")
        return None


def analyze_tree(tree: List[Dict[str, Any]]) -> Dict[str, Any]:
    paths = [n.get("path", "") for n in tree if n.get("type") == "blob"]
    lower = [p.lower() for p in paths]

    has_gitignore = ".gitignore" in lower
    has_readme = any(p.startswith("readme") for p in lower)  # README, README.md, etc

    ipynb = sum(1 for p in lower if p.endswith(".ipynb"))
    py = sum(1 for p in lower if p.endswith(".py"))
    tex = sum(1 for p in lower if p.endswith(".tex"))
    md = sum(1 for p in lower if p.endswith(".md"))
    yml = sum(1 for p in lower if p.endswith(".yml") or p.endswith(".yaml"))

    return {
        "has_gitignore": has_gitignore,
        "has_readme": has_readme,
        "notebooks_ipynb": ipynb,
        "files_py": py,
        "files_tex": tex,
        "files_md": md,
        "files_yml": yml,
        "total_files": len(paths),
    }


def audit_one_org(org: str) -> List[Dict[str, Any]]:
    print(f"[audit] org={org}")
    repos = list_org_repos(org)

    rows: List[Dict[str, Any]] = []
    for repo in repos:
        name = repo["name"]
        full_name = repo["full_name"]
        html_url = repo["html_url"]
        archived = repo.get("archived", False)
        fork = repo.get("fork", False)
        private = repo.get("private", False)
        default_branch = repo.get("default_branch") or "main"
        pushed_at = repo.get("pushed_at") or ""

        owner = repo["owner"]["login"]

        sha = get_branch_head_sha(owner, name, default_branch)
        if not sha:
            stats = {
                "has_gitignore": False,
                "has_readme": False,
                "notebooks_ipynb": 0,
                "files_py": 0,
                "files_tex": 0,
                "files_md": 0,
                "files_yml": 0,
                "total_files": 0,
            }
        else:
            tree = get_tree(owner, name, sha) or []
            stats = analyze_tree(tree)

        rows.append({
            "org": org,
            "name": name,
            "full_name": full_name,
            "url": html_url,
            "private": private,
            "archived": archived,
            "fork": fork,
            "default_branch": default_branch,
            "pushed_at": pushed_at,
            **stats,
        })

    return rows


def write_reports_for_org(org: str, rows: List[Dict[str, Any]]) -> None:
    org_dir = os.path.join(REPORT_DIR, org)
    os.makedirs(org_dir, exist_ok=True)

    # JSON (para o audit.html consumir)
    json_path = os.path.join(org_dir, "org-audit.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

    # CSV
    csv_path = os.path.join(org_dir, "org-audit.csv")
    fieldnames = list(rows[0].keys()) if rows else []
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

    # Markdown summary
    md_path = os.path.join(org_dir, "org-audit.md")
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    total = len(rows)
    with_readme = sum(1 for r in rows if r["has_readme"])
    with_gitignore = sum(1 for r in rows if r["has_gitignore"])
    total_ipynb = sum(int(r["notebooks_ipynb"]) for r in rows)

    lines = []
    lines.append(f"# Org Audit Report: {org}\n\nGenerated: **{now}**\n\n")
    lines.append(f"- Repositories: **{total}**\n")
    lines.append(f"- With README: **{with_readme}/{total}**\n")
    lines.append(f"- With .gitignore: **{with_gitignore}/{total}**\n")
    lines.append(f"- Total notebooks (.ipynb): **{total_ipynb}**\n\n")

    lines.append("## Table (top 50)\n\n")
    lines.append("| Repo | README | .gitignore | ipynb | py | tex | files | updated |\n")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---|\n")
    for r in rows[:50]:
        lines.append(
            f"| [{r['name']}]({r['url']}) | "
            f"{'✅' if r['has_readme'] else '—'} | "
            f"{'✅' if r['has_gitignore'] else '—'} | "
            f"{r['notebooks_ipynb']} | {r['files_py']} | {r['files_tex']} | "
            f"{r['total_files']} | {r['pushed_at'][:10]} |\n"
        )

    with open(md_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"[ok] wrote {json_path}, {csv_path}, {md_path}")


def main():
    print(f"[audit] orgs={ORGS}")

    all_rows: List[Dict[str, Any]] = []
    for org in ORGS:
        try:
            rows = audit_one_org(org)
            write_reports_for_org(org, rows)
            all_rows.extend(rows)
        except Exception as e:
            # não derruba tudo se uma org falhar
            print(f"[error] org={org}: {e}")

    # opcional: um índice geral (útil pro audit.html ter dropdown depois)
    index_path = os.path.join(REPORT_DIR, "index.json")
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump({"orgs": ORGS, "generated_at": datetime.utcnow().isoformat() + "Z"}, f, indent=2)
    print(f"[ok] wrote {index_path}")

    # opcional: CSV geral consolidado
    if all_rows:
        csv_all_path = os.path.join(REPORT_DIR, "org-audit.ALL.csv")
        fieldnames = list(all_rows[0].keys())
        with open(csv_all_path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            w.writerows(all_rows)
        print(f"[ok] wrote {csv_all_path}")


if __name__ == "__main__":
    main()
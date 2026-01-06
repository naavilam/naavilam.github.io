#!/usr/bin/env python3
import sys, os, glob
import yaml

def safe(s: str) -> str:
    return (s or "").replace('"', "'")

def job_label(job_id, job):
    name = job.get("name") or job_id
    return f"{job_id}: {name}" if name != job_id else job_id

def step_label(step):
    if isinstance(step, str):
        return step
    if "name" in step:
        return step["name"]
    if "uses" in step:
        return f"uses {step['uses']}"
    if "run" in step:
        first = step["run"].strip().splitlines()[0]
        return f"run: {first[:60]}{'…' if len(first)>60 else ''}"
    return "step"

def emit_sequence(workflow_name, on_block, jobs):
    lines = []
    lines.append("sequenceDiagram")
    lines.append("autonumber")
    lines.append('participant Dev as Developer')
    lines.append('participant GH as GitHub Actions')
    lines.append('participant Runner as Runner')
    lines.append('participant Repo as Repo')
    lines.append("")

    # Trigger
    trig = []
    if isinstance(on_block, dict):
        trig = list(on_block.keys())
    elif isinstance(on_block, list):
        trig = on_block
    elif isinstance(on_block, str):
        trig = [on_block]
    t = ", ".join(trig) if trig else "manual/other"
    lines.append(f'Dev->>GH: triggers "{safe(workflow_name)}" ({safe(t)})')
    lines.append("GH->>Runner: dispatch workflow run")
    lines.append("Runner->>Repo: checkout (if configured)")
    lines.append("")

    # Jobs
    # Render dependencies with "needs"
    ordered = list(jobs.items())
    # keep simple: keep file order, but show needs arrows when present
    for job_id, job in ordered:
        jl = job_label(job_id, job)
        runs_on = job.get("runs-on", "runner")
        lines.append(f'Note over Runner: job {safe(jl)}\\nruns-on: {safe(str(runs_on))}')

        needs = job.get("needs")
        if needs:
            if isinstance(needs, list):
                for n in needs:
                    lines.append(f'GH-->>GH: needs {safe(n)} -> {safe(job_id)}')
            else:
                lines.append(f'GH-->>GH: needs {safe(str(needs))} -> {safe(job_id)}')

        steps = job.get("steps", [])
        if not steps:
            lines.append(f'Runner-->>GH: (no steps found) {safe(job_id)}')
            lines.append("")
            continue

        for idx, st in enumerate(steps, start=1):
            sl = step_label(st)
            lines.append(f'Runner->>Runner: {safe(sl)}')
            # heuristic: common interactions
            if isinstance(st, dict) and "uses" in st:
                uses = st["uses"]
                if "actions/checkout" in uses:
                    lines.append("Runner->>Repo: git checkout")
                elif "aws-actions" in uses or "configure-aws-credentials" in uses:
                    lines.append("Runner->>Runner: configure AWS creds")
                elif "github" in uses:
                    lines.append("Runner->>GH: call GitHub API")
            if isinstance(st, dict) and "run" in st:
                cmd = st["run"].strip().splitlines()[0]
                if "terraform" in cmd:
                    lines.append("Runner->>Runner: terraform (plan/apply)")
                if "curl" in cmd:
                    lines.append("Runner->>GH: HTTP request (curl)")
                if "python" in cmd:
                    lines.append("Runner->>Runner: python script")
                if "npm" in cmd or "pnpm" in cmd or "yarn" in cmd:
                    lines.append("Runner->>Runner: node build")
            lines.append("")

        lines.append(f'Runner-->>GH: job "{safe(job_id)}" complete')
        lines.append("")

    lines.append("GH-->>Dev: workflow finished (success/fail)")
    return "\n".join(lines)

def main():
    if len(sys.argv) != 3:
        print("usage: workflow_to_mermaid.py <workflow_dir> <out_dir>", file=sys.stderr)
        sys.exit(2)

    wf_dir, out_dir = sys.argv[1], sys.argv[2]
    os.makedirs(out_dir, exist_ok=True)

    for path in sorted(glob.glob(os.path.join(wf_dir, "*.yml")) + glob.glob(os.path.join(wf_dir, "*.yaml"))):
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        name = data.get("name") or os.path.basename(path)
        on_block = data.get("on") or data.get(True) or {}  # GH sometimes serializes weirdly
        jobs = data.get("jobs") or {}

        mmd = emit_sequence(name, on_block, jobs)
        base = os.path.splitext(os.path.basename(path))[0]
        out = os.path.join(out_dir, f"{base}.mmd")
        with open(out, "w", encoding="utf-8") as g:
            g.write(mmd + "\n")
        print(f"WROTE {out}")

if __name__ == "__main__":
    main()
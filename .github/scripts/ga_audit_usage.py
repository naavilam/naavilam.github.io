import json, os, re
from pathlib import Path
from collections import defaultdict

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    RunReportRequest,
    DateRange,
    Dimension,
    Metric,
    FilterExpression,
    Filter,
)

ROOT = Path(".")
REPORTS = ROOT / "reports"


def norm_org_to_env(org: str) -> str:
    # academic-codex -> ACADEMIC_CODEX
    return re.sub(r"[^A-Za-z0-9]+", "_", org).strip("_").upper()


def write_credentials_from_secret() -> str:
    s = os.environ.get("GA_CREDENTIALS_JSON", "").strip()
    if not s:
        raise SystemExit("Missing GA_CREDENTIALS_JSON secret in env")

    secrets_dir = ROOT / ".secrets"
    secrets_dir.mkdir(parents=True, exist_ok=True)
    cred_path = secrets_dir / "ga.json"
    cred_path.write_text(s, encoding="utf-8")
    return str(cred_path)


def run_report(
    client,
    property_id: str,
    days: int,
    dimensions: list[str],
    metrics: list[str],
    event_name: str | None = None,
    limit: int = 100000,
):
    dim_objs = [Dimension(name=d) for d in dimensions]
    met_objs = [Metric(name=m) for m in metrics]

    dim_filter = None
    if event_name:
        dim_filter = FilterExpression(
            filter=Filter(
                field_name="eventName",
                string_filter={"value": event_name, "match_type": "EXACT"},
            )
        )

    req = RunReportRequest(
        property=f"properties/{property_id}",
        date_ranges=[DateRange(start_date=f"{days}daysAgo", end_date="today")],
        dimensions=dim_objs,
        metrics=met_objs,
        dimension_filter=dim_filter,
        limit=limit,
    )
    return client.run_report(req)


def as_int(s: str) -> int:
    try:
        return int(float(s))
    except Exception:
        return 0


def as_float(s: str) -> float:
    try:
        return float(s)
    except Exception:
        return 0.0


def top_percent_dict(counts: dict[str, int], top_k: int = 1) -> dict[str, int]:
    """
    Retorna {key: pct_int} para os top_k, pct arredondado.
    Ex: {"BR": 62, "US": 18}
    """
    if not counts:
        return {}
    total = sum(counts.values())
    if total <= 0:
        return {}

    items = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:top_k]
    out = {}
    for k, v in items:
        pct = int(round(100.0 * v / total))
        out[k] = pct
    return out


def main():
    cred_path = write_credentials_from_secret()
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cred_path

    orgs_raw = os.environ.get("ORGS", "").strip()
    if not orgs_raw:
        raise SystemExit("Missing ORGS env")

    orgs = [x.strip() for x in orgs_raw.split(",") if x.strip()]
    client = BetaAnalyticsDataClient()

    DAYS = 30

    for org in orgs:
        env_key = f"GA_PROPERTY_ID_{norm_org_to_env(org)}"
        property_id = os.environ.get(env_key, "").strip()

        if not property_id:
            print(f"[ga] skip org={org} (missing {env_key})")
            continue

        print(f"[ga] org={org} property_id={property_id}")

        # 1) Métricas principais por pagePath (GA4 padrão)
        # - views: screenPageViews (page_view “equivalente”)
        # - sessions: sessions
        # - users: totalUsers
        # - engagementRate, averageEngagementTime
        base = run_report(
            client,
            property_id,
            days=DAYS,
            dimensions=["pagePath"],
            metrics=["screenPageViews", "sessions", "totalUsers", "engagementRate", "averageEngagementTime"],
        )

        metrics_by_path: dict[str, dict] = {}

        for row in base.rows:
            path = row.dimension_values[0].value

            views = as_int(row.metric_values[0].value)
            sessions = as_int(row.metric_values[1].value)
            users = as_int(row.metric_values[2].value)
            engagement_rate = as_float(row.metric_values[3].value)  # 0..1
            avg_eng_time = as_float(row.metric_values[4].value)     # segundos

            metrics_by_path[path] = {
                "views": views,
                "sessions": sessions,
                "users": users,
                "clicks": 0,  # preenche depois
                "engagement_rate": engagement_rate,
                "avg_engagement_time_sec": avg_eng_time,
                "countries": {},
                "sources": {},
            }

        # 2) Clicks por pagePath (evento "click" como você já fazia)
        clicks = run_report(
            client,
            property_id,
            days=DAYS,
            dimensions=["pagePath"],
            metrics=["eventCount"],
            event_name="click",
        )

        for row in clicks.rows:
            path = row.dimension_values[0].value
            cnt = as_int(row.metric_values[0].value)
            metrics_by_path.setdefault(path, {
                "views": 0, "sessions": 0, "users": 0, "clicks": 0,
                "engagement_rate": 0.0, "avg_engagement_time_sec": 0.0,
                "countries": {}, "sources": {}
            })
            metrics_by_path[path]["clicks"] = cnt

        # 3) Países: distribuição por pagePath (uso de countryId => BR, US...)
        # Métrica: screenPageViews (pra refletir “views”)
        countries_resp = run_report(
            client,
            property_id,
            days=DAYS,
            dimensions=["pagePath", "countryId"],
            metrics=["screenPageViews"],
            limit=100000,
        )

        countries_counts = defaultdict(lambda: defaultdict(int))  # path -> country -> count
        for row in countries_resp.rows:
            path = row.dimension_values[0].value
            country = row.dimension_values[1].value or "??"
            cnt = as_int(row.metric_values[0].value)
            if cnt > 0:
                countries_counts[path][country] += cnt

        # 4) Sources: distribuição por pagePath (sessionSource)
        # Métrica: sessions (pra refletir tráfego real)
        sources_resp = run_report(
            client,
            property_id,
            days=DAYS,
            dimensions=["pagePath", "sessionSource"],
            metrics=["sessions"],
            limit=100000,
        )

        sources_counts = defaultdict(lambda: defaultdict(int))  # path -> source -> count
        for row in sources_resp.rows:
            path = row.dimension_values[0].value
            source = (row.dimension_values[1].value or "unknown").strip().lower()
            cnt = as_int(row.metric_values[0].value)
            if cnt > 0:
                sources_counts[path][source] += cnt

        # aplica “Opção B”: top com porcentagem (ainda 1 linha no front)
        for path in set(list(metrics_by_path.keys()) + list(countries_counts.keys()) + list(sources_counts.keys())):
            metrics_by_path.setdefault(path, {
                "views": 0, "sessions": 0, "users": 0, "clicks": 0,
                "engagement_rate": 0.0, "avg_engagement_time_sec": 0.0,
                "countries": {}, "sources": {}
            })
            metrics_by_path[path]["countries"] = top_percent_dict(dict(countries_counts[path]), top_k=1)
            metrics_by_path[path]["sources"] = top_percent_dict(dict(sources_counts[path]), top_k=1)

        payload = {
            "org": org,
            "property_id": property_id,
            "range_days": DAYS,
            "metrics_by_path": metrics_by_path,
        }

        out_dir = REPORTS / org
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "ga-usage.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8"
        )


if __name__ == "__main__":
    main()
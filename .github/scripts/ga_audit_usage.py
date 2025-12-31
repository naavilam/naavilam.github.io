import json, os, re
from pathlib import Path

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

def run_report(client, property_id: str, event_name: str, days: int = 30, limit: int = 10000):
    req = RunReportRequest(
        property=f"properties/{property_id}",
        date_ranges=[DateRange(start_date=f"{days}daysAgo", end_date="today")],
        dimensions=[Dimension(name="pagePath")],
        metrics=[Metric(name="eventCount")],
        dimension_filter=FilterExpression(
            filter=Filter(
                field_name="eventName",
                string_filter={
                    "value": event_name,
                    "match_type": "EXACT"
                }
            )
        ),
        limit=limit,
    )
    resp = client.run_report(req)
    out = {}
    for row in resp.rows:
        page = row.dimension_values[0].value
        cnt = int(row.metric_values[0].value)
        out[page] = cnt
    return out

def main():
    # escreve credencial e exporta ADC path
    cred_path = write_credentials_from_secret()
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cred_path

    orgs_raw = os.environ.get("ORGS", "").strip()
    if not orgs_raw:
        raise SystemExit("Missing ORGS env")

    orgs = [x.strip() for x in orgs_raw.split(",") if x.strip()]
    client = BetaAnalyticsDataClient()

    for org in orgs:
        env_key = f"GA_PROPERTY_ID_{norm_org_to_env(org)}"
        property_id = os.environ.get(env_key, "").strip()

        # se não tiver property id, só pula (sem quebrar o workflow)
        if not property_id:
            print(f"[ga] skip org={org} (missing {env_key})")
            continue

        print(f"[ga] org={org} property_id={property_id}")

        pageviews = run_report(client, property_id, event_name="page_view", days=30)
        clicks   = run_report(client, property_id, event_name="click", days=30)

        payload = {
            "org": org,
            "property_id": property_id,
            "range_days": 30,
            "pageviews_by_path": pageviews,
            "clicks_by_path": clicks,
        }

        out_dir = REPORTS / org
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "ga-usage.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8"
        )

if __name__ == "__main__":
    main()
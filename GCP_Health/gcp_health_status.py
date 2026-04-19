"""
Google Cloud Service Health Status Checker
Uses the Cloud Service Health API to fetch live GCP service incidents and events.
Docs: https://cloud.google.com/service-health/docs/reference/rest
"""

import json
import os
import sys
from datetime import datetime, timezone

import requests
from google.auth import default
from google.auth.transport.requests import Request


# ── Auth ──────────────────────────────────────────────────────────────────────

def get_access_token() -> str:
    """Obtain a short-lived OAuth2 access token using ADC."""
    credentials, _ = default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    credentials.refresh(Request())
    return credentials.token


# ── Public status (no auth required) ─────────────────────────────────────────

PUBLIC_STATUS_URL = "https://status.cloud.google.com/incidents.json"


def fetch_public_incidents(limit: int = 10) -> list[dict]:
    """Fetch recent incidents from the public GCP status page (no credentials needed)."""
    resp = requests.get(PUBLIC_STATUS_URL, timeout=15)
    resp.raise_for_status()
    incidents = resp.json()
    return incidents[:limit]


def print_public_incidents(incidents: list[dict]) -> None:
    print("\n" + "=" * 60)
    print("  GCP PUBLIC STATUS — RECENT INCIDENTS")
    print("=" * 60)

    if not incidents:
        print("  No recent incidents found. All systems operational.")
        return

    for inc in incidents:
        severity = inc.get("severity", "unknown").upper()
        status   = inc.get("status_impact", "unknown")
        begin    = inc.get("begin", "N/A")
        end      = inc.get("end", "Ongoing")
        summary  = inc.get("external_desc", "No description")
        services = ", ".join(
            p.get("title", "") for p in inc.get("affected_products", [])
        ) or "N/A"

        print(f"\n  Incident : {inc.get('id', 'N/A')}")
        print(f"  Severity : {severity}")
        print(f"  Status   : {status}")
        print(f"  Services : {services}")
        print(f"  Begin    : {begin}")
        print(f"  End      : {end}")
        print(f"  Summary  : {summary[:120]}{'...' if len(summary) > 120 else ''}")
        print("  " + "-" * 56)


# ── Cloud Service Health REST API (requires auth) ─────────────────────────────

BASE_API = "https://servicehealth.googleapis.com/v1"


def list_events(project_id: str, token: str, page_size: int = 20) -> list[dict]:
    """List service health events for a GCP project."""
    url = f"{BASE_API}/projects/{project_id}/locations/global/events"
    headers = {"Authorization": f"Bearer {token}"}
    params  = {"pageSize": page_size}

    resp = requests.get(url, headers=headers, params=params, timeout=15)
    resp.raise_for_status()
    return resp.json().get("events", [])


def list_organization_events(org_id: str, token: str, page_size: int = 20) -> list[dict]:
    """List service health events for a GCP organization."""
    url = f"{BASE_API}/organizations/{org_id}/locations/global/organizationEvents"
    headers = {"Authorization": f"Bearer {token}"}
    params  = {"pageSize": page_size}

    resp = requests.get(url, headers=headers, params=params, timeout=15)
    resp.raise_for_status()
    return resp.json().get("organizationEvents", [])


def print_events(events: list[dict], label: str = "PROJECT EVENTS") -> None:
    print("\n" + "=" * 60)
    print(f"  GCP SERVICE HEALTH — {label}")
    print("=" * 60)

    if not events:
        print("  No active events. All services healthy.")
        return

    state_map = {
        "EVENT_STATE_UNSPECIFIED": "Unknown",
        "ACTIVE":                  "Active",
        "CLOSED":                  "Closed",
    }
    impact_map = {
        "SERVICE_IMPACT_UNSPECIFIED": "Unknown",
        "DISRUPTION":                 "Disruption",
        "DEGRADED":                   "Degraded",
        "SERVICE_INFORMATION":        "Informational",
    }

    for ev in events:
        name        = ev.get("name", "N/A")
        title       = ev.get("title", "No title")
        description = ev.get("description", {}).get("en", "N/A")
        state       = state_map.get(ev.get("state", ""), ev.get("state", "N/A"))
        impact      = impact_map.get(ev.get("eventImpact", ""), ev.get("eventImpact", "N/A"))
        start_time  = ev.get("startTime", "N/A")
        end_time    = ev.get("endTime", "Ongoing")
        products    = ", ".join(
            p.get("title", "") for p in ev.get("affectedProducts", [])
        ) or "N/A"

        print(f"\n  Event    : {name.split('/')[-1]}")
        print(f"  Title    : {title}")
        print(f"  State    : {state}  |  Impact: {impact}")
        print(f"  Services : {products}")
        print(f"  Start    : {start_time}")
        print(f"  End      : {end_time}")
        print(f"  Details  : {description[:120]}{'...' if len(description) > 120 else ''}")
        print("  " + "-" * 56)


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    project_id = os.environ.get("GCP_PROJECT_ID")
    org_id     = os.environ.get("GCP_ORG_ID")

    # 1. Always show public incidents (no credentials required)
    print("\n[1] Fetching public GCP incident feed...")
    try:
        incidents = fetch_public_incidents(limit=5)
        print_public_incidents(incidents)
    except requests.HTTPError as exc:
        print(f"  ERROR fetching public incidents: {exc}")

    # 2. Authenticated API calls (requires Application Default Credentials)
    if not project_id and not org_id:
        print(
            "\n[INFO] Set GCP_PROJECT_ID and/or GCP_ORG_ID env vars "
            "to query the authenticated Service Health API."
        )
        return

    print("\n[2] Authenticating with Google Cloud ADC...")
    try:
        token = get_access_token()
    except Exception as exc:
        print(f"  ERROR obtaining credentials: {exc}")
        print("  Run: gcloud auth application-default login")
        return

    if project_id:
        print(f"\n[3] Fetching Service Health events for project: {project_id}")
        try:
            events = list_events(project_id, token)
            print_events(events, label=f"PROJECT: {project_id}")
        except requests.HTTPError as exc:
            print(f"  ERROR: {exc}")

    if org_id:
        print(f"\n[4] Fetching Service Health events for org: {org_id}")
        try:
            org_events = list_organization_events(org_id, token)
            print_events(org_events, label=f"ORG: {org_id}")
        except requests.HTTPError as exc:
            print(f"  ERROR: {exc}")


if __name__ == "__main__":
    main()

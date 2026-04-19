# GCP Cloud Service Health Status

Fetches live Google Cloud service health data via two channels:

| Channel | Auth needed | What it shows |
|---------|-------------|---------------|
| Public JSON feed | None | All public incidents |
| Service Health REST API | ADC / Service Account | Project- or Org-scoped events |

## Quick start

```bash
pip install -r requirements.txt

# Public incidents only (no auth required)
python gcp_health_status.py

# With authenticated project-level events
export GCP_PROJECT_ID=my-gcp-project
gcloud auth application-default login
python gcp_health_status.py

# With org-level events too
export GCP_ORG_ID=123456789
python gcp_health_status.py
```

## Required IAM roles (authenticated mode)

| Scope | Role |
|-------|------|
| Project events | `roles/servicehealth.viewer` |
| Org events | `roles/servicehealth.organizationViewer` |

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GCP_PROJECT_ID` | No | GCP project ID for project-scoped events |
| `GCP_ORG_ID` | No | GCP org ID for org-scoped events |

## API reference

- Public status page: <https://status.cloud.google.com>
- Cloud Service Health REST API: <https://cloud.google.com/service-health/docs/reference/rest>

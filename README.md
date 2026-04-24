# Travel Buddy Agent

A multi-agent application built using the Google Cloud Agent Development Kit (ADK) and deployed to Vertex AI Reasoning Engine.

## Local Development & Installation

This project is configured using a modern `pyproject.toml` file, which manages all metadata and dependencies. To install the project locally, simply run:

```bash
pip install .
```

*(This command automatically reads the `pyproject.toml` file and installs necessary dependencies like `google-adk`, `pydantic`, and `google-cloud-aiplatform`, completely replacing the need for a manually maintained `requirements.txt` file setup).*

---

## Deployment & GCP Infrastructure

Deployment to the Vertex AI Reasoning Engine is fully automated via GitHub Actions using the `adk deploy` CLI.

### Steps to configure GitHub actions to deploy to GCP

<!-- create workload identity pool and provider -->

```bash
# Create the pool
gcloud iam workload-identity-pools create "github-pool" \
  --project="<YOUR_PROJECT_ID>" --location="global" \
  --display-name="GitHub Actions Pool"

# Create a workload identity provider, OIDC provider
gcloud iam workload-identity-pools providers create-oidc "github-provider" \
  --project="<YOUR_PROJECT_ID>" \
  --location="global" \
  --workload-identity-pool="github-pool" \
  --issuer-uri="https://token.actions.githubusercontent.com" \
  --attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository" \
  --attribute-condition="assertion.repository == '<YOUR_GITHUB_ORG>/<YOUR_REPO_NAME>'"

<!-- link the service account  -->

```bash
# Create the service account
gcloud iam service-accounts create "github-deployer" \
  --project="<YOUR_PROJECT_ID>" \
  --display-name="GitHub Actions Deployer"

# Grant the service account the Vertex AI Agent Admin role
gcloud projects add-iam-policy-binding "<YOUR_PROJECT_ID>" \
  --member="serviceAccount:<YOUR_SERVICE_ACCOUNT_EMAIL>" \
  --role="roles/aiplatform.agentAdmin"

# Grant the service account the Service Account Token Creator role
gcloud iam service-accounts add-iam-policy-binding "<YOUR_SERVICE_ACCOUNT_EMAIL>" \
  --member="serviceAccount:<YOUR_SERVICE_ACCOUNT_EMAIL>" \
  --role="roles/iam.serviceAccountTokenCreator"

# Link the service account to the workload identity pool

gcloud iam service-accounts add-iam-policy-binding \
  "<YOUR_SERVICE_ACCOUNT_EMAIL>" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/<YOUR_PROJECT_NUMBER>/locations/global/workloadIdentityPools/github-pool/attribute.repository/<YOUR_GITHUB_ORG>/<YOUR_REPO_NAME>"
```

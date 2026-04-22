<!-- create workload identity pool and provider -->

```bash
# Create the pool
gcloud iam workload-identity-pools create "github-pool" \
  --project="mydummy-1" --location="global" \
  --display-name="GitHub Actions Pool"

# Create a workload identity provider, OIDC provider
gcloud iam workload-identity-pools providers create-oidc "github-provider" \
  --project="mydummy-1" --location="global" \
  --workload-identity-pool="github-pool" \
  --issuer-uri="https://token.actions.githubusercontent.com" \
  --attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository"
```

<!-- link the service account  -->

```bash
# Create the service account
gcloud iam service-accounts create "github-deployer" \
  --project="mydummy-1" \
  --display-name="GitHub Actions Deployer"

# Grant the service account the Vertex AI Agent Admin role
gcloud projects add-iam-policy-binding "mydummy-1" \
  --member="serviceAccount:[EMAIL_ADDRESS]" \
  --role="roles/aiplatform.agentAdmin"

# Grant the service account the Service Account Token Creator role
gcloud iam service-accounts add-iam-policy-binding "[EMAIL_ADDRESS]" \
  --member="serviceAccount:[EMAIL_ADDRESS]" \
  --role="roles/iam.serviceAccountTokenCreator"

# Link the service account to the workload identity pool

gcloud iam service-accounts add-iam-policy-binding \
  "ag-cicd-deployer@mydummy-1.iam.gserviceaccount.com" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/172748774286/locations/global/workloadIdentityPools/github-pool/attribute.repository/rkolar19/entagnt_travelbuddy_3"

```

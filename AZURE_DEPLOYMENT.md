# Azure Container Deployment (Heartline Webapp)

This guide keeps the Heartline Webapp running 24/7 on **Azure Container Apps** with a custom domain and a single GitHub Actions workflow.

---

## 1. Provision Azure Resources (one time)

```bash
RG=portfolio
LOCATION=germanywestcentral
ACR_NAME=heartlineregistry
LOG_ANALYTICS=heartline-logs
CONTAINER_ENV=heartline-app-env
APP_NAME=heartline-webapp

# Resource group & registry
az group create -n $RG -l $LOCATION
az acr create -n $ACR_NAME -g $RG --sku Basic --location $LOCATION

# Logging + Container Apps environment
az monitor log-analytics workspace create -n $LOG_ANALYTICS -g $RG -l $LOCATION
WORKSPACE_ID=$(az monitor log-analytics workspace show -n $LOG_ANALYTICS -g $RG --query customerId -o tsv)
WORKSPACE_KEY=$(az monitor log-analytics workspace get-shared-keys -n $LOG_ANALYTICS -g $RG --query primarySharedKey -o tsv)
az containerapp env create \
  -g $RG \
  -n $CONTAINER_ENV \
  -l $LOCATION \
  --logs-workspace-id $WORKSPACE_ID \
  --logs-workspace-key $WORKSPACE_KEY

# (Optional) First-time app create – env vars can be added later in the portal
az containerapp create \
  -g $RG \
  -n $APP_NAME \
  --environment $CONTAINER_ENV \
  --image mcr.microsoft.com/azuredocs/containerapps-helloworld:latest \
  --ingress external --target-port 8000 \
  --min-replicas 1 --max-replicas 1
```

Add the required environment variables (DB credentials, `SECRET_KEY`, etc.) to the Container App under **Settings → Secrets & application settings**. Use `azure-env-variables.json` as the reference list.

---

## 2. Configure GitHub Actions deployment

Workflow file: `.github/workflows/deploy_container_app.yml`

Create the following repository secrets (Settings → Secrets and variables → Actions):

| Secret | Description |
| --- | --- |
| `AZURE_CLIENT_ID` | Service principal client ID with `Contributor` access |
| `AZURE_TENANT_ID` | Azure AD tenant ID |
| `AZURE_SUBSCRIPTION_ID` | Subscription ID where the resources live |

The workflow assumes the resource names listed in the `env:` block. If your Azure names differ, edit that block accordingly.

### Deploy from Azure Portal (Source: Code or Artifact)
When using **Deployment Center** in Azure Container Apps:
1. Choose **Source = Code (GitHub)**, **Project scope = Heartline Webapp**.
2. Select the existing workflow file `deploy_container_app.yml`.
3. Azure will reuse this workflow instead of generating a new one, so you keep a single source of truth.

Every push to `main` (or manual dispatch) will:
1. Build the Docker image.
2. Push it to Azure Container Registry.
3. Update the Container App with `min-replicas = 1` so the app is always warm.

---

## 3. Assign the main domain

1. In the Azure Portal → Container Apps → **heartline-webapp** → **Custom domains**, add your domain (e.g., `app.yourdomain.com` or apex).  
2. Create the required DNS records:
   - CNAME pointing to the Container App default FQDN (e.g., `heartline-webapp.francecentral.azurecontainerapps.io`), or
   - A/ TXT records if mapping the apex.
3. Choose **Managed certificate** so Azure issues and renews TLS automatically.
4. Set the new hostname as the default domain for the app.

📌 With ingress set to `external` and `min-replicas` pinned at 1, the container stays online without manual start/stop.

---

## 4. Operations quick reference

| Task | Command |
| --- | --- |
| Tail logs | `az containerapp logs show -n heartline-webapp -g portfolio --follow` |
| Restart app | `az containerapp restart -n heartline-webapp -g portfolio` |
| Scale (temporary) | `az containerapp revision set-mode --mode multiple --name heartline-webapp -g portfolio` |
| Update env vars | Portal → Container Apps → Settings → Secrets/App settings → `Revision management → Create revision` |

The app will now auto-build, auto-deploy, and remain reachable from your main portfolio link without any manual container start/stop. Keep this file as the single Azure deployment reference to avoid documentation sprawl.

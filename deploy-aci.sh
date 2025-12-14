#!/bin/bash
# Deploy Heartline Webapp to Azure Container Instances
# Pay-per-use: Only charged when container is running

set -e

# Configuration
RESOURCE_GROUP="portfolio"
CONTAINER_NAME="heartline-webapp"
REGISTRY_NAME="heartlineregistry"
IMAGE_NAME="heartline"
DNS_LABEL="heartline-demo"
LOCATION="germanywestcentral"

echo "=== Azure Container Instances Deployment ==="
echo ""

# Step 1: Create Azure Container Registry (if not exists)
echo "1. Creating Azure Container Registry..."
az acr create \
  --resource-group $RESOURCE_GROUP \
  --name $REGISTRY_NAME \
  --sku Basic \
  --location $LOCATION \
  --admin-enabled true \
  || echo "Registry already exists, continuing..."

# Step 2: Get ACR credentials
echo ""
echo "2. Getting ACR credentials..."
ACR_USERNAME=$(az acr credential show --name $REGISTRY_NAME --query username -o tsv)
ACR_PASSWORD=$(az acr credential show --name $REGISTRY_NAME --query passwords[0].value -o tsv)
ACR_LOGIN_SERVER=$(az acr show --name $REGISTRY_NAME --query loginServer -o tsv)

# Step 3: Build and push Docker image
echo ""
echo "3. Building Docker image..."
docker build -t $IMAGE_NAME:latest .

echo ""
echo "4. Tagging image for ACR..."
docker tag $IMAGE_NAME:latest $ACR_LOGIN_SERVER/$IMAGE_NAME:latest

echo ""
echo "5. Logging into ACR..."
az acr login --name $REGISTRY_NAME

echo ""
echo "6. Pushing image to ACR..."
docker push $ACR_LOGIN_SERVER/$IMAGE_NAME:latest

# Step 4: Deploy to ACI
echo ""
echo "7. Deploying to Azure Container Instances..."
az container create \
  --resource-group $RESOURCE_GROUP \
  --name $CONTAINER_NAME \
  --image $ACR_LOGIN_SERVER/$IMAGE_NAME:latest \
  --registry-login-server $ACR_LOGIN_SERVER \
  --registry-username $ACR_USERNAME \
  --registry-password $ACR_PASSWORD \
  --dns-name-label $DNS_LABEL \
  --ports 8000 \
  --cpu 2 \
  --memory 4 \
  --restart-policy OnFailure \
  --location $LOCATION \
  --environment-variables \
    SECRET_KEY="heartline-secret-key-change-in-production" \
    DB_ENGINE="mssql+pyodbc" \
    DB_HOST="blamairia.database.windows.net" \
    DB_PORT="1433" \
    DB_USERNAME="blamairia" \
    DB_PASSWORD="Billel159" \
    DB_NAME="heartline-webapp" \
    DB_DRIVER="ODBC Driver 18 for SQL Server" \
    DB_ENCRYPT="yes" \
    DB_TRUST_SERVER_CERTIFICATE="no" \
    FLASK_APP="app.py" \
    FLASK_ENV="production" \
    PYTHONUNBUFFERED="1"

# Get container URL
echo ""
echo "=== Deployment Complete! ==="
FQDN=$(az container show --resource-group $RESOURCE_GROUP --name $CONTAINER_NAME --query ipAddress.fqdn -o tsv)
echo ""
echo "🎉 Your app is running at: http://$FQDN:8000"
echo ""
echo "Health check: http://$FQDN:8000/health"
echo "Login page: http://$FQDN:8000/login"
echo ""
echo "💰 Cost: ~$0.045/hour when running (~$2.70/month for 2 hours/day)"
echo ""
echo "🛑 To STOP and save money:"
echo "   az container stop --resource-group $RESOURCE_GROUP --name $CONTAINER_NAME"
echo ""
echo "▶️  To START again:"
echo "   az container start --resource-group $RESOURCE_GROUP --name $CONTAINER_NAME"
echo ""
echo "📊 Check status:"
echo "   az container show --resource-group $RESOURCE_GROUP --name $CONTAINER_NAME --query instanceView.state"

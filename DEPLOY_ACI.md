# Deploy Heartline to Azure Container Instances (Pay-Per-Use)

## 💰 Cost Savings: $73/month → $3-8/month

Instead of paying for App Service 24/7, use Azure Container Instances and pay only when running!

---

## 🚀 Quick Start (One-Time Setup)

### Prerequisites
```bash
# Install Azure CLI if not already installed
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Login to Azure
az login

# Install Docker if not already installed
sudo apt-get update && sudo apt-get install docker.io
sudo usermod -aG docker $USER
# Logout and login again for docker group to take effect
```

### Deploy (First Time)
```bash
cd "/home/billell/Portfolio/projects/Hearline Webapp"

# Run deployment script
./deploy-aci.sh
```

This will:
1. ✅ Create Azure Container Registry
2. ✅ Build Docker image
3. ✅ Push image to registry
4. ✅ Deploy container with 4GB RAM, 2 vCPU
5. ✅ Give you a public URL

**Total time: ~5-10 minutes**

---

## 🎮 Daily Usage (Super Simple)

### Start Container (Before Demo)
```bash
./aci-management.sh start
```
⏱️ Ready in ~15-30 seconds  
💰 Starts charging $0.045/hour

### Stop Container (After Demo)
```bash
./aci-management.sh stop
```
💰 Stops charging immediately (saves $0.045/hour)

### Check Status
```bash
./aci-management.sh status
```

### View Logs
```bash
./aci-management.sh logs
```

### Get URL
```bash
./aci-management.sh url
```

---

## 📊 Cost Breakdown

### Scenario 1: Demo to Recruiters (Typical)
- **Usage**: 5 demos/week, 10 minutes each
- **Monthly runtime**: ~3.5 hours
- **Cost**: **$0.16/month** + storage

### Scenario 2: Regular Portfolio Visits
- **Usage**: 10 visitors/day, 5 min average
- **Monthly runtime**: ~25 hours
- **Cost**: **$1.13/month** + storage

### Scenario 3: Active Development
- **Usage**: 2 hours/day
- **Monthly runtime**: 60 hours
- **Cost**: **$2.70/month** + storage

### Plus:
- Azure SQL Database: $5/month (Basic tier)
- Container Registry: $5/month (Basic tier)
- **Total: $6-13/month** vs **$73/month** with App Service

**Savings: $60-67/month (85-92% reduction)**

---

## 🔄 Update Deployment (After Code Changes)

### Option A: Quick Update (Redeploy)
```bash
# Make your code changes, then:
./deploy-aci.sh
```
This rebuilds and redeploys everything (~5 min).

### Option B: Just Rebuild Image
```bash
# Build new image
docker build -t heartlineregistry.azurecr.io/heartline:latest .

# Push to registry
az acr login --name heartlineregistry
docker push heartlineregistry.azurecr.io/heartline:latest

# Restart container to pull new image
./aci-management.sh restart
```

---

## 🌐 Add Custom Domain (Optional)

Azure Container Instances don't support custom domains directly, but you can:

### Option 1: Use Azure Front Door (Free Tier Available)
```bash
# Create Front Door
az network front-door create \
  --resource-group portfolio \
  --name heartline-fd \
  --backend-address heartline-demo.germanywestcentral.azurecontainer.io:8000

# Point your domain to Front Door
```

### Option 2: Use Cloudflare (Free)
1. Add CNAME record: `heartline.yourdomain.com` → `heartline-demo.germanywestcentral.azurecontainer.io`
2. Enable proxy (orange cloud)
3. Done! Cloudflare handles SSL

---

## 🛠️ Troubleshooting

### Container won't start?
```bash
# Check logs
./aci-management.sh logs

# Check status
./aci-management.sh status

# Restart
./aci-management.sh restart
```

### Need more resources?
Edit `deploy-aci.sh` and change:
```bash
--cpu 2           # Change to 4 for more power
--memory 4        # Change to 8 for more RAM
```

### Database connection issues?
```bash
# Check environment variables are set
az container show \
  --resource-group portfolio \
  --name heartline-webapp \
  --query containers[0].environmentVariables
```

---

## 🔐 Security Notes

### Environment Variables
Currently hardcoded in `deploy-aci.sh`. For production:
```bash
# Use Azure Key Vault
az keyvault create --name heartline-vault --resource-group portfolio
az keyvault secret set --vault-name heartline-vault --name db-password --value "Billel159"

# Reference in container
--secure-environment-variables DB_PASSWORD=...
```

### Change Default Admin Password
After first login, change from `admin/admin`!

---

## 📈 Monitoring (Optional)

### Enable Application Insights
```bash
# Create App Insights
az monitor app-insights component create \
  --app heartline-insights \
  --location germanywestcentral \
  --resource-group portfolio

# Add connection string to container env vars
```

---

## 🎯 Comparison: ACI vs App Service

| Feature | ACI (Pay-per-use) | App Service B2 |
|---------|-------------------|----------------|
| Cost (idle) | $0/month | $73/month |
| Cost (2h/day) | $2.70/month | $73/month |
| RAM | 4GB (customizable) | 3.5GB (fixed) |
| CPU | 2 vCPU (customizable) | 2 cores |
| Startup | 15-30s cold start | Instant |
| Custom domain | Via proxy | Direct |
| SSL | Via proxy | Built-in |
| CI/CD | Manual/GitHub Actions | Built-in |
| Scaling | Manual start/stop | Always on |

**Verdict**: ACI is **85-92% cheaper** for portfolio projects with low traffic.

---

## 🚀 Next Steps

1. ✅ Run `./deploy-aci.sh` to deploy
2. ✅ Test at the provided URL
3. ✅ After testing, run `./aci-management.sh stop`
4. ✅ Before demos, run `./aci-management.sh start`
5. ✅ Update your portfolio with the URL
6. ✅ Save $60-67/month! 💰

---

## 📞 Support

If anything breaks:
```bash
# Full diagnostic
./aci-management.sh status
./aci-management.sh logs

# Nuclear option (delete and redeploy)
./aci-management.sh delete
./deploy-aci.sh
```

**Deployment time: 5-10 minutes**  
**Monthly cost: $6-13 (vs $73)**  
**Savings: 85-92%** 🎉

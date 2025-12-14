# Azure Deployment Cost Options - Heartline Webapp

## ⚠️ PROBLEM: Traditional App Service = Fixed Monthly Cost
- Basic B2 (4GB RAM): ~$73/month (always charged)
- Standard S1 (1.75GB RAM): ~$69/month (always charged)
- Not cost-effective for portfolio projects with low traffic

---

## ✅ SOLUTION: Pay-Per-Use Options

### **Option 1: Azure Container Instances (ACI)** ⭐ RECOMMENDED
**Perfect for your use case!**

#### Pricing (Pay only when running):
- **4GB RAM, 2 vCPU**: ~$0.045/hour = **$0.0018/minute**
- **Example cost**: 10 minutes/day usage = **$0.54/month**
- **Stopped = $0 cost** (only storage charges ~$0.01/month)

#### How it works:
1. Container runs only when accessed
2. Auto-stops after idle period (configurable)
3. Starts in ~15-30 seconds when needed
4. Perfect for demos/portfolio

#### Setup:
```bash
# Create container instance
az container create \
  --resource-group portfolio \
  --name heartline-webapp \
  --image <your-docker-image> \
  --cpu 2 \
  --memory 4 \
  --dns-name-label heartline-demo \
  --ports 8000 \
  --environment-variables \
    DB_HOST=blamairia.database.windows.net \
    DB_NAME=heartline-webapp \
    # ... other env vars
```

#### Pros:
✅ Pay only for compute time used
✅ 4GB RAM easily achievable
✅ Quick startup (15-30 sec)
✅ No monthly fees when stopped
✅ Easy auto-start/stop scripts

#### Cons:
❌ Requires Docker containerization
❌ No built-in CI/CD (manual or GitHub Actions)
❌ Cold start delay

---

### **Option 2: Azure Functions (Consumption Plan)** 
**Only if you refactor to serverless**

#### Pricing:
- **Free**: First 1 million requests/month
- After: $0.20 per million executions
- Memory: Scales automatically

#### Requirements:
- ⚠️ Major code refactoring needed
- No persistent storage (need external DB)
- Good for API-only, not full Flask app

#### Verdict: ❌ Not suitable for your Flask app

---

### **Option 3: Azure Container Apps (with scaling to zero)**
**Modern, but more complex**

#### Pricing:
- **Consumption plan**: Pay per vCPU-second + memory-GB-second
- **4GB, 2 vCPU running**: ~$0.046/hour
- **Scaled to zero**: Only storage charges
- **Per request**: $0.40 per million requests

#### Features:
✅ Auto-scales to zero (0 instances when idle)
✅ Auto-scales up when traffic comes
✅ Built-in HTTPS, custom domains
✅ Can integrate with GitHub Actions

#### Setup complexity: Medium (more than ACI, less than Functions)

---

### **Option 4: Azure App Service (Spot Instances)**
**Not available for App Service - only VMs**

❌ App Service doesn't support spot/reserved instances
❌ Always fixed monthly cost

---

## 🎯 RECOMMENDED SOLUTION: Azure Container Instances

### Why ACI is perfect for you:
1. **True pay-per-use**: Only pay when container is running
2. **4GB RAM**: Plenty for your ECG AI model
3. **Portfolio-friendly**: Stop when not demoing, pay pennies
4. **Simple**: No complex serverless refactoring

### Estimated monthly cost:
- **Scenario 1** (10 visitors/day, 5 min each): 
  - 50 min/day × 30 days = 1,500 min/month
  - Cost: **$2.70/month**

- **Scenario 2** (Low traffic, 2 hours/day):
  - 2 hours/day × 30 days = 60 hours/month
  - Cost: **$2.70/month**

- **Scenario 3** (Stopped 90% of time):
  - 3 hours/month running
  - Cost: **$0.15/month** + storage

### Plus:
- Azure SQL Database: ~$5/month (Basic tier)
- **Total: $3-8/month** vs $73/month with App Service

---

## 🛠️ IMPLEMENTATION OPTIONS

### A. Full Docker Containerization (Best)
```dockerfile
# Create Dockerfile in your project
FROM python:3.11-slim

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . /app
WORKDIR /app

# Expose port
EXPOSE 8000

# Start with gunicorn
CMD ["gunicorn", "--bind=0.0.0.0:8000", "--workers=2", "app:app"]
```

Build and push to Azure Container Registry:
```bash
az acr create --name heartlineregistry --sku Basic
docker build -t heartlineregistry.azurecr.io/heartline:latest .
docker push heartlineregistry.azurecr.io/heartline:latest
```

### B. Hybrid: App Service + Manual Stop/Start
- Keep current App Service setup
- Manually stop when not in use: `az webapp stop --name heartline`
- **Cost when stopped**: Storage only (~$5/month for DB)
- **Limitation**: Manual intervention required

### C. GitHub Actions + ACI Auto-Deploy
```yaml
# .github/workflows/deploy-aci.yml
name: Deploy to ACI
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: azure/docker-login@v1
      - run: docker build -t heartline .
      - run: docker push ...
      - uses: azure/aci-deploy@v1
```

---

## 📊 COST COMPARISON

| Solution | Fixed Cost | Variable Cost | 4GB RAM | Idle Cost | Startup Time |
|----------|------------|---------------|---------|-----------|--------------|
| App Service B2 | $73/month | N/A | ✅ | $73/month | Instant |
| Container Instances | $0 | $0.045/hour | ✅ | $0 | 15-30s |
| Container Apps | $0 | $0.046/hour | ✅ | $0 | 5-15s |
| Functions Consumption | $0 | $0.20/1M req | ❌ 1.5GB max | $0 | 1-5s |

---

## 🚀 NEXT STEPS - RECOMMENDED PATH

### Option A: Quick Win - Manual Stop/Start (Tonight)
1. Keep your current App Service setup
2. After demoing, run: `az webapp stop --name heartline-webapp`
3. Before demo: `az webapp start --name heartline-webapp` (takes ~30s)
4. **Savings**: Pay only when running

### Option B: Optimal - Container Instances (This Weekend)
1. I'll create a Dockerfile for your Flask app
2. Build and push to Azure Container Registry
3. Deploy to ACI with auto-stop after 30 min idle
4. Set up a simple "Wake Up" button on your portfolio
5. **Savings**: $65-70/month vs App Service

### Option C: Advanced - Container Apps (Later)
1. Similar to ACI but with auto-scaling
2. Better for future if traffic increases
3. Slightly more expensive but more features

---

## 💡 MY RECOMMENDATION

**For your portfolio use case:**

1. **NOW**: Deploy to App Service (already configured) - Test it works
2. **TONIGHT**: Manually stop it after testing - Save money immediately
3. **THIS WEEK**: I'll containerize it for ACI - Save $65/month permanently

**Best of both worlds:**
- Get it working now on App Service
- Migrate to ACI for cost savings
- Keep both configs in your repo

---

Want me to create the Dockerfile and ACI deployment scripts right now?

# Azure Deployment Guide - Heartline Webapp

## Prerequisites
- Azure SQL Database created: `heartline-webapp`
- Azure Web App created (Python 3.11 runtime)
- Git repository pushed to GitHub

## Step 1: Configure Azure App Service

### 1.1 Set Environment Variables
In Azure Portal → Your Web App → Configuration → Application Settings, paste the content from `azure-env-variables.json`:

```json
[Copy the content from azure-env-variables.json file]
```

**⚠️ IMPORTANT**: Change the `SECRET_KEY` to a secure random string!

### 1.2 Configure Startup Command
In Azure Portal → Configuration → General Settings:
- **Startup Command**: `/home/site/wwwroot/startup.sh`
- **Always On**: Enable (to prevent cold starts)

## Step 2: Deploy from GitHub

### 2.1 Set up Deployment
1. Go to Deployment Center in Azure Portal
2. Choose **GitHub** as source
3. Authorize and select:
   - Organization: `blamairia`
   - Repository: `Hearline-Webapp`
   - Branch: `master` or `main`

### 2.2 Deploy
- Click **Save** to trigger initial deployment
- Monitor logs in Deployment Center

## Step 3: Verify Deployment

### 3.1 Check Logs
```bash
# View application logs
az webapp log tail --name <your-app-name> --resource-group <your-rg>
```

### 3.2 Test Endpoints
- Health check: `https://your-app.azurewebsites.net/health`
- Login page: `https://your-app.azurewebsites.net/login`

### 3.3 Default Credentials
- Username: `admin`
- Password: `admin`

**⚠️ Change these immediately after first login!**

## Step 4: Database Connection

The app uses the SSL certificates included in the repository:
- `DigiCertGlobalRootG2.crt.pem`
- `Microsoft RSA Root Certificate Authority 2017.crt`

These are automatically used for secure Azure SQL connection.

## Troubleshooting

### 403 Forbidden
- Check file permissions in startup.sh
- Verify `www-data` or `nginx` user ownership

### 502 Bad Gateway
- Check if Gunicorn is running: `ps aux | grep gunicorn`
- Verify port 8000 is configured
- Check application logs for Python errors

### Database Connection Errors
- Verify firewall rules in Azure SQL allow Azure services
- Check connection string in environment variables
- Ensure SSL certificates are present

### Cold Start Issues
- Enable **Always On** in App Service plan (Basic or higher)
- The warmup page will show during cold starts

## Performance Optimization

1. **Enable Always On**: Prevents cold starts (requires Basic tier+)
2. **Scale Up**: For AI/ML workloads, consider B2 or higher
3. **Application Insights**: Enable for monitoring and diagnostics

## Security Checklist

- [ ] Change default admin password
- [ ] Update SECRET_KEY in environment variables
- [ ] Configure custom domain with SSL
- [ ] Enable Azure AD authentication (optional)
- [ ] Set up proper CORS if needed
- [ ] Review and restrict database firewall rules

## Maintenance

### Update Application
```bash
git push origin master
# Azure auto-deploys from GitHub
```

### View Logs
```bash
az webapp log tail --name heartline-webapp --resource-group <rg-name>
```

### Restart App
```bash
az webapp restart --name heartline-webapp --resource-group <rg-name>
```

## Cost Estimation

- **Basic B1 Plan**: ~$13/month (Always On included)
- **Azure SQL Basic**: ~$5/month
- **Total**: ~$18/month

## Support

For issues, check:
1. Application logs in Azure Portal
2. Deployment logs in Deployment Center
3. Database connectivity test in Azure SQL Query Editor

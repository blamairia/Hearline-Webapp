#!/bin/bash
# Azure Container Instances Management Script
# Easily start, stop, and check your container

RESOURCE_GROUP="portfolio"
CONTAINER_NAME="heartline-webapp"

case "$1" in
  start)
    echo "▶️  Starting Heartline container..."
    az container start --resource-group $RESOURCE_GROUP --name $CONTAINER_NAME
    echo "✅ Container started!"
    sleep 5
    FQDN=$(az container show --resource-group $RESOURCE_GROUP --name $CONTAINER_NAME --query ipAddress.fqdn -o tsv)
    echo "🌐 Access at: http://$FQDN:8000"
    ;;
    
  stop)
    echo "🛑 Stopping Heartline container..."
    az container stop --resource-group $RESOURCE_GROUP --name $CONTAINER_NAME
    echo "✅ Container stopped! (No charges while stopped)"
    ;;
    
  restart)
    echo "🔄 Restarting Heartline container..."
    az container restart --resource-group $RESOURCE_GROUP --name $CONTAINER_NAME
    echo "✅ Container restarted!"
    ;;
    
  status)
    echo "📊 Checking container status..."
    az container show \
      --resource-group $RESOURCE_GROUP \
      --name $CONTAINER_NAME \
      --query "{State:instanceView.state, FQDN:ipAddress.fqdn, IP:ipAddress.ip, CPU:containers[0].resources.requests.cpu, Memory:containers[0].resources.requests.memoryInGb}" \
      --output table
    ;;
    
  logs)
    echo "📜 Fetching container logs..."
    az container logs --resource-group $RESOURCE_GROUP --name $CONTAINER_NAME --follow
    ;;
    
  url)
    FQDN=$(az container show --resource-group $RESOURCE_GROUP --name $CONTAINER_NAME --query ipAddress.fqdn -o tsv)
    echo "🌐 App URL: http://$FQDN:8000"
    echo "🔍 Health: http://$FQDN:8000/health"
    echo "🔑 Login: http://$FQDN:8000/login"
    ;;
    
  delete)
    echo "⚠️  WARNING: This will DELETE the container!"
    read -p "Are you sure? (yes/no): " confirm
    if [ "$confirm" = "yes" ]; then
      az container delete --resource-group $RESOURCE_GROUP --name $CONTAINER_NAME --yes
      echo "🗑️  Container deleted!"
    else
      echo "Cancelled."
    fi
    ;;
    
  *)
    echo "Heartline Webapp - ACI Management"
    echo ""
    echo "Usage: $0 {start|stop|restart|status|logs|url|delete}"
    echo ""
    echo "Commands:"
    echo "  start    - Start the container (begins charging)"
    echo "  stop     - Stop the container (stops charging)"
    echo "  restart  - Restart the container"
    echo "  status   - Show container status and details"
    echo "  logs     - View container logs (live)"
    echo "  url      - Show access URLs"
    echo "  delete   - Delete the container completely"
    echo ""
    echo "💰 Cost: ~$0.045/hour when running, $0 when stopped"
    exit 1
    ;;
esac

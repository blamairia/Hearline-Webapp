#!/bin/bash
docker stop heartline-webapp || true
docker rm heartline-webapp || true
docker run -d \
  --name heartline-webapp \
  -p 8090:8000 \
  -e SECRET_KEY="heartline-secret-key-change-this-in-production-2024" \
  -e DB_ENGINE="mssql+pyodbc" \
  -e DB_HOST="blamairia.database.windows.net" \
  -e DB_PORT="1433" \
  -e DB_USERNAME="blamairia" \
  -e DB_PASSWORD="Billel159" \
  -e DB_NAME="heartline-webapp" \
  -e DB_DRIVER="ODBC Driver 18 for SQL Server" \
  -e DB_ENCRYPT="yes" \
  -e DB_TRUST_SERVER_CERTIFICATE="no" \
  -e FLASK_APP="app.py" \
  -e FLASK_ENV="production" \
  -e PYTHONUNBUFFERED="1" \
  -e SCM_DO_BUILD_DURING_DEPLOYMENT="false" \
  -e WEBSITES_PORT="8080" \
  heartline-webapp:local

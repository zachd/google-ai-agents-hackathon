#!/bin/bash

# Cloud Run deployment script for Mystery Trip Planner
# This script deploys the backend to Google Cloud Run

set -e

# Configuration
PROJECT_ID=${GOOGLE_CLOUD_PROJECT:-"your-project-id"}
SERVICE_NAME="mystery-trip-planner"
REGION=${GOOGLE_CLOUD_REGION:-"us-central1"}
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo "🚀 Deploying Mystery Trip Planner to Cloud Run"
echo "Project: ${PROJECT_ID}"
echo "Service: ${SERVICE_NAME}"
echo "Region: ${REGION}"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found"
    echo "Please create .env file from .env.example and add your GOOGLE_API_KEY"
    exit 1
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Check if GOOGLE_API_KEY is set
if [ -z "$GOOGLE_API_KEY" ]; then
    echo "❌ Error: GOOGLE_API_KEY not set in .env file"
    exit 1
fi

# Build and push Docker image
echo "📦 Building Docker image..."
docker build -t ${IMAGE_NAME} .

echo "📤 Pushing image to Google Container Registry..."
docker push ${IMAGE_NAME}

# Deploy to Cloud Run
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy ${SERVICE_NAME} \
    --image ${IMAGE_NAME} \
    --platform managed \
    --region ${REGION} \
    --allow-unauthenticated \
    --memory 512Mi \
    --timeout 300 \
    --max-instances 10 \
    --set-env-vars "GOOGLE_API_KEY=${GOOGLE_API_KEY},PORT=8080" \
    --project ${PROJECT_ID}

# Get the service URL
SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} --region=${REGION} --project=${PROJECT_ID} --format="value(status.url)")

echo "✅ Deployment complete!"
echo "Service URL: ${SERVICE_URL}"
echo ""
echo "Test the deployment:"
echo "curl ${SERVICE_URL}/health"
echo ""
echo "Update your frontend .env.production with:"
echo "VITE_API_URL=${SERVICE_URL}"

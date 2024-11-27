#!/bin/bash

# Set variables
REGION="us-east-1"  # Change to your desired region
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)
LAMBDA_REPO_NAME="lambda-repo"  # ECR repository name for Lambda image
ECS_REPO_NAME="ecs-repo"  # ECR repository name for ECS image
LAMBDA_FUNCTION_NAME="MyLambdaFunction"  # Name of your Lambda function
IMAGE_TAG="latest"
DOCKERFILE_LAMBDA="Dockerfile.lambda"  # Dockerfile for Lambda
DOCKERFILE_MONITORING="Dockerfile.monitoring"  # Dockerfile for MLFlow
LAMBDA_ECR_URI="${AWS_ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${LAMBDA_REPO_NAME}:${IMAGE_TAG}"
ECS_ECR_URI="${AWS_ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${ECS_REPO_NAME}:${IMAGE_TAG}"

# Step 1: Authenticate Docker to Amazon ECR
echo "Authenticating Docker to Amazon ECR..."
aws ecr get-login-password --region ${REGION} | docker login --username AWS --password-stdin ${LAMBDA_ECR_URI}
aws ecr get-login-password --region ${REGION} | docker login --username AWS --password-stdin ${ECS_ECR_URI}

# Step 2: Check if the ECR repositories exist for Lambda and ECS, create them if not
echo "Checking if the ECR repositories exist..."

LAMBDA_REPO_EXISTS=$(aws ecr describe-repositories --region ${REGION} --repository-names ${LAMBDA_REPO_NAME} --query 'repositories[0].repositoryName' --output text 2>/dev/null)

if [[ "$LAMBDA_REPO_EXISTS" == "None" || -z "$LAMBDA_REPO_EXISTS" ]]; then
  echo "Lambda ECR repository does not exist. Creating repository..."
  aws ecr create-repository --repository-name ${LAMBDA_REPO_NAME} --region ${REGION}
else
  echo "Lambda ECR repository already exists."
fi

# ECS ECR Repository check
ECS_REPO_EXISTS=$(aws ecr describe-repositories --region ${REGION} --repository-names ${ECS_REPO_NAME} --query 'repositories[0].repositoryName' --output text 2>/dev/null)

if [[ "$ECS_REPO_EXISTS" == "None" || -z "$ECS_REPO_EXISTS" ]]; then
  echo "ECS ECR repository does not exist. Creating repository..."
  aws ecr create-repository --repository-name ${ECS_REPO_NAME} --region ${REGION} --output json | jq '.repository.repositoryUri'
  echo "ECS ECR repository already exists."
fi

# Step 3: Build Docker images for Lambda and MLFlow
# Build Docker image for Lambda
echo "Building Docker image for Lambda..."
docker build -f ${DOCKERFILE_LAMBDA} -t ${LAMBDA_ECR_URI} .

# Build Docker image for ECS
echo "Building Docker image for ECS..."
docker build -f ${DOCKERFILE_MONITORING} -t ${ECS_ECR_URI} .

# Step 4: Push Docker images to ECR repositories
# Push Lambda Docker image to ECR
echo "Pushing Lambda Docker image to ECR..."
docker push ${LAMBDA_ECR_URI}

# Push ECS Docker image to ECR
echo "Pushing ECS Docker image to ECR..."
docker push ${ECS_ECR_URI}

# Step 5: Deploy the Lambda function using the Docker image
echo "Deploying Lambda function using the Docker image..."

# Check if Lambda function exists
#LAMBDA_EXISTS=$(aws lambda get-function --function-name ${LAMBDA_FUNCTION_NAME} --region ${REGION} --query 'Configuration.FunctionName' --output text)

# if [[ "$LAMBDA_EXISTS" == "${LAMBDA_FUNCTION_NAME}" ]]; then
#   echo "Lambda function exists. Updating function..."
#   aws lambda update-function-code --function-name ${LAMBDA_FUNCTION_NAME} \
#     --image-uri ${LAMBDA_ECR_URI} --region ${REGION}
# else
#   echo "Lambda function does not exist. Creating a new Lambda function..."
#   aws lambda create-function --function-name ${LAMBDA_FUNCTION_NAME} \
#     --package-type Image \
#     --code ImageUri=${LAMBDA_ECR_URI} \
#     --role arn:aws:iam::${AWS_ACCOUNT_ID}:role/service-role/YOUR_LAMBDA_EXECUTION_ROLE \
#     --region ${REGION}
# fi

echo "Lambda function deployment complete."

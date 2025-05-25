#!/bin/bash

# IAM-HR Integration Setup Script
# This script sets up the complete environment for IAM-HR integration demo

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Docker is installed
echo -e "${BLUE}Checking prerequisites...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Docker Compose is not installed. Please install Docker Compose first.${NC}"
    exit 1
fi

# Create necessary directories
echo -e "${BLUE}Creating directory structure...${NC}"
mkdir -p nginx/conf.d nginx/certs
mkdir -p scripts

# Copy configuration files
echo -e "${BLUE}Copying configuration files...${NC}"
cp nginx-config nginx/conf.d/default.conf
cp sync_users.py scripts/
chmod +x scripts/sync_users.py

# Start the environment
echo -e "${BLUE}Starting the environment...${NC}"
docker-compose up -d

# Wait for services to be ready
echo -e "${BLUE}Waiting for services to initialize (this may take a few minutes)...${NC}"
# Wait for Keycloak
attempt=0
max_attempts=30
until $(curl --output /dev/null --silent --head --fail http://localhost:8080); do
    if [ ${attempt} -eq ${max_attempts} ]; then
        echo -e "${RED}Timed out waiting for Keycloak to start${NC}"
        exit 1
    fi
    printf '.'
    attempt=$(($attempt+1))
    sleep 10
done

# Wait for OrangeHRM
attempt=0
until $(curl --output /dev/null --silent --head --fail http://localhost:8081); do
    if [ ${attempt} -eq ${max_attempts} ]; then
        echo -e "${RED}Timed out waiting for OrangeHRM to start${NC}"
        exit 1
    fi
    printf '.'
    attempt=$(($attempt+1))
    sleep 10
done

echo -e "\n${GREEN}All services are up and running!${NC}"

# Install Python dependencies for the sync script
echo -e "${BLUE}Setting up Python environment for sync script...${NC}"
docker run --rm -v "$(pwd)/scripts:/scripts" --network iam-hr-network python:3.9-slim pip install requests -t /scripts

echo -e "${GREEN}Environment setup completed successfully!${NC}"
echo -e "${GREEN}---------------------------------------------${NC}"
echo -e "${GREEN}Access Keycloak at: http://localhost:8080${NC}"
echo -e "${GREEN}- Username: admin${NC}"
echo -e "${GREEN}- Password: admin${NC}"
echo -e "${GREEN}Access OrangeHRM at: http://localhost:8081${NC}"
echo -e "${GREEN}- Username: admin${NC}"
echo -e "${GREEN}- Password: admin123${NC}"
echo -e "${GREEN}---------------------------------------------${NC}"
echo -e "${BLUE}To run the sync script:${NC}"
echo -e "${BLUE}docker run --rm -v \"\$(pwd)/scripts:/scripts\" --network iam-hr-network python:3.9-slim python /scripts/sync_users.py${NC}"
echo -e "${GREEN}---------------------------------------------${NC}"
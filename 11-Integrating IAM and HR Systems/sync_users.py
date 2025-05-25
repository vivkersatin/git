#!/usr/bin/env python3
"""
IAM-HR Integration Demo Script
This script demonstrates how to sync user data between OrangeHRM and Keycloak.
"""

import requests
import json
import os
import logging
import time
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("sync.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("iam-hr-sync")

# Configuration
ORANGEHRM_BASE_URL = os.getenv("ORANGEHRM_BASE_URL", "http://localhost:8081")
ORANGEHRM_USERNAME = os.getenv("ORANGEHRM_USERNAME", "admin")
ORANGEHRM_PASSWORD = os.getenv("ORANGEHRM_PASSWORD", "admin123")

KEYCLOAK_BASE_URL = os.getenv("KEYCLOAK_BASE_URL", "http://localhost:8080")
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM", "master")
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID", "admin-cli")
KEYCLOAK_USERNAME = os.getenv("KEYCLOAK_USERNAME", "admin")
KEYCLOAK_PASSWORD = os.getenv("KEYCLOAK_PASSWORD", "admin")

# Keycloak auth token
keycloak_token = None

def get_keycloak_token():
    """Get an access token from Keycloak"""
    global keycloak_token
    
    token_url = f"{KEYCLOAK_BASE_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token"
    payload = {
        'client_id': KEYCLOAK_CLIENT_ID,
        'username': KEYCLOAK_USERNAME,
        'password': KEYCLOAK_PASSWORD,
        'grant_type': 'password'
    }
    
    try:
        response = requests.post(token_url, data=payload)
        response.raise_for_status()
        keycloak_token = response.json()['access_token']
        logger.info("Successfully obtained Keycloak token")
        return keycloak_token
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to get Keycloak token: {e}")
        return None

def get_orangehrm_token():
    """Get an access token from OrangeHRM API (simplified for demo)"""
    # Note: OrangeHRM doesn't have a standard API, this is a simplified example
    # In a real implementation, you would need to use OrangeHRM's specific API or database
    
    # Simulating OrangeHRM login - in real implementation this would be actual API call
    logger.info("Successfully authenticated with OrangeHRM (simulated)")
    return "simulated-orangehrm-token"

def get_employees_from_orangehrm():
    """Get employee data from OrangeHRM"""
    # In a real implementation, this would call the OrangeHRM API
    # For demonstration, we'll return sample data
    
    # Simulated response
    employees = [
        {
            "id": "E001",
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@example.com",
            "username": "john.doe",
            "position": "System Administrator",
            "department": "IT",
            "status": "Active",
            "hireDate": "2023-01-15"
        },
        {
            "id": "E002", 
            "firstName": "Jane",
            "lastName": "Smith",
            "email": "jane.smith@example.com",
            "username": "jane.smith",
            "position": "HR Manager",
            "department": "Human Resources",
            "status": "Active",
            "hireDate": "2022-11-01"
        },
        {
            "id": "E003",
            "firstName": "Michael",
            "lastName": "Johnson",
            "email": "michael.johnson@example.com",
            "username": "michael.johnson",
            "position": "Software Engineer",
            "department": "Development",
            "status": "Active",
            "hireDate": "2023-03-10"
        }
    ]
    
    logger.info(f"Retrieved {len(employees)} employees from OrangeHRM")
    return employees

def get_users_from_keycloak():
    """Get users from Keycloak"""
    if not keycloak_token:
        get_keycloak_token()
        
    headers = {
        'Authorization': f'Bearer {keycloak_token}',
        'Content-Type': 'application/json'
    }
    
    users_url = f"{KEYCLOAK_BASE_URL}/admin/realms/{KEYCLOAK_REALM}/users"
    
    try:
        response = requests.get(users_url, headers=headers)
        response.raise_for_status()
        users = response.json()
        logger.info(f"Retrieved {len(users)} users from Keycloak")
        return users
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to get users from Keycloak: {e}")
        return []

def create_user_in_keycloak(employee):
    """Create a new user in Keycloak based on employee data"""
    if not keycloak_token:
        get_keycloak_token()
        
    headers = {
        'Authorization': f'Bearer {keycloak_token}',
        'Content-Type': 'application/json'
    }
    
    users_url = f"{KEYCLOAK_BASE_URL}/admin/realms/{KEYCLOAK_REALM}/users"
    
    # Map employee data to Keycloak user format
    user_data = {
        "username": employee["username"],
        "email": employee["email"],
        "firstName": employee["firstName"],
        "lastName": employee["lastName"],
        "enabled": employee["status"] == "Active",
        "emailVerified": True,
        "attributes": {
            "employeeId": [employee["id"]],
            "department": [employee["department"]],
            "position": [employee["position"]],
            "hireDate": [employee["hireDate"]]
        },
        "credentials": [
            {
                "type": "password",
                "value": "TemporaryPassword123!",  # In production, use random passwords or implement SMTP for reset
                "temporary": True
            }
        ]
    }
    
    try:
        response = requests.post(users_url, headers=headers, data=json.dumps(user_data))
        response.raise_for_status()
        logger.info(f"Created user {employee['username']} in Keycloak")
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to create user in Keycloak: {e}")
        if hasattr(e.response, 'text'):
            logger.error(f"Response: {e.response.text}")
        return False

def update_user_in_keycloak(user_id, employee):
    """Update existing user in Keycloak with employee data"""
    if not keycloak_token:
        get_keycloak_token()
        
    headers = {
        'Authorization': f'Bearer {keycloak_token}',
        'Content-Type': 'application/json'
    }
    
    user_url = f"{KEYCLOAK_BASE_URL}/admin/realms/{KEYCLOAK_REALM}/users/{user_id}"
    
    # Map employee data to Keycloak user format for update
    user_data = {
        "firstName": employee["firstName"],
        "lastName": employee["lastName"],
        "email": employee["email"],
        "enabled": employee["status"] == "Active",
        "attributes": {
            "employeeId": [employee["id"]],
            "department": [employee["department"]],
            "position": [employee["position"]],
            "hireDate": [employee["hireDate"]],
            "lastUpdated": [datetime.now().isoformat()]
        }
    }
    
    try:
        response = requests.put(user_url, headers=headers, data=json.dumps(user_data))
        response.raise_for_status()
        logger.info(f"Updated user {employee['username']} in Keycloak")
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to update user in Keycloak: {e}")
        return False

def assign_roles(user_id, department):
    """Assign roles based on department"""
    if not keycloak_token:
        get_keycloak_token()
        
    headers = {
        'Authorization': f'Bearer {keycloak_token}',
        'Content-Type': 'application/json'
    }
    
    # Map departments to roles (simplified example)
    role_mapping = {
        "IT": ["admin", "user"],
        "Human Resources": ["hr-manager", "user"],
        "Development": ["developer", "user"],
        # Add more mappings as needed
    }
    
    # Get default roles for unknown departments
    roles_to_assign = role_mapping.get(department, ["user"])
    
    # Get available roles
    roles_url = f"{KEYCLOAK_BASE_URL}/admin/realms/{KEYCLOAK_REALM}/roles"
    
    try:
        response = requests.get(roles_url, headers=headers)
        response.raise_for_status()
        available_roles = response.json()
        
        # Find matching roles and assign them
        for role in available_roles:
            if role["name"] in roles_to_assign:
                role_url = f"{KEYCLOAK_BASE_URL}/admin/realms/{KEYCLOAK_REALM}/users/{user_id}/role-mappings/realm"
                role_data = [role]
                
                try:
                    response = requests.post(role_url, headers=headers, data=json.dumps(role_data))
                    response.raise_for_status()
                    logger.info(f"Assigned role {role['name']} to user {user_id}")
                except requests.exceptions.RequestException as e:
                    logger.error(f"Failed to assign role {role['name']}: {e}")
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to get roles from Keycloak: {e}")

def sync_users():
    """Main function to sync users between OrangeHRM and Keycloak"""
    logger.info("Starting user synchronization")
    
    # Get authentication tokens
    get_keycloak_token()
    orangehrm_token = get_orangehrm_token()
    
    if not keycloak_token or not orangehrm_token:
        logger.error("Failed to authenticate with one or both systems")
        return
    
    # Get data from both systems
    employees = get_employees_from_orangehrm()
    keycloak_users = get_users_from_keycloak()
    
    # Create a map of Keycloak users by email for easy lookup
    keycloak_users_map = {user.get('email', ''): user for user in keycloak_users}
    
    # Process each employee
    for employee in employees:
        email = employee['email']
        
        if email in keycloak_users_map:
            # User exists, update
            user = keycloak_users_map[email]
            update_user_in_keycloak(user['id'], employee)
            assign_roles(user['id'], employee['department'])
        else:
            # New user, create
            created = create_user_in_keycloak(employee)
            if created:
                # Get the new user to assign roles
                updated_users = get_users_from_keycloak()
                for user in updated_users:
                    if user.get('email') == email:
                        assign_roles(user['id'], employee['department'])
                        break
    
    logger.info("User synchronization completed")

if __name__ == "__main__":
    # Run the sync process
    sync_users()
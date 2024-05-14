# User Guide

This user guide provides instructions for setting up and using the Account Manager application.

## Installation

1. Clone the repository from GitHub:
   ```
   git clone https://github.com/motestw64631/Account_manager/edit/main/README.md
   ```

2. Use Docker Compose to start the application:
   ```
   docker-compose up --build
   ```

## Usage

### Create User API

To test the Create User API, use the following `curl` command:
```bash
curl -X 'POST' \
  'http://localhost:8087/users' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "string",
  "password": "String123"
}'
```

### Verify API

To test the Verify API, use the following `curl` command:
```bash
curl -X 'POST' \
  'http://localhost:8087/verify' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "string",
  "password": "String123"
}'
```

#### API Docs

You can view the documentation below or connect to http://localhost:8087/docs after starting the container to view the API documentation.



***
# API document
## Introduction

This two APIs show how to create accounts and verify a account. 

## Endpoints

### Create User

- **URL**: `/users`
- **Method**: `POST`
- **Summary**: Create User
- **Request Body**:
  - Content-Type: `application/json`
  - Schema:
    ```json
    {
      "properties": {
        "username": {
          "type": "string",
          "maxLength": 32,
          "minLength": 3,
          "title": "Username",
          "description": "a string representing the desired username for the account, with a minimum length of 3 characters and a maximum length of 32 characters."
        },
        "password": {
          "type": "string",
          "maxLength": 32,
          "minLength": 8,
          "title": "Password",
          "description": "a string representing the desired password for the account, with aminimum length of 8 characters and a maximum length of 32 characters, containing at least 1 uppercase letter, 1 lowercase letter, and 1 number."
        }
      },
      "type": "object",
      "required": [
        "username",
        "password"
      ],
      "title": "UserCreate"
    }
    ```
  - Required: Yes
- **Responses**:
  - `200`: Successful Response
    - Content-Type: `application/json`
    - Schema:
      ```json
      {
        "properties": {
          "success": {
            "type": "boolean",
            "title": "Success",
            "default": true
          }
        },
        "type": "object",
        "title": "ResponseModel"
      }
      ```
  - `400`: Bad Request
    - Content-Type: `application/json`
    - Schema:
      ```json
      {
        "properties": {
          "success": {
            "type": "boolean",
            "title": "Success",
            "default": false
          },
          "reason": {
            "type": "string",
            "title": "Reason"
          }
        },
        "type": "object",
        "required": [
          "reason"
        ],
        "title": "ErrorResponse"
      }
      ```
  - `422`: Unprocessable Entity
    - Content-Type: `application/json`
    - Schema:
      ```json
      {
        "properties": {
          "success": {
            "type": "boolean",
            "title": "Success",
            "default": false
          },
          "reason": {
            "type": "string",
            "title": "Reason"
          }
        },
        "type": "object",
        "required": [
          "reason"
        ],
        "title": "ErrorResponse"
      }
      ```

### Verify User

- **URL**: `/verify`
- **Method**: `POST`
- **Summary**: Verify User
- **Request Body**:
  - Content-Type: `application/json`
  - Schema:
    ```json
    {
      "properties": {
        "username": {
          "type": "string",
          "title": "Username",
          "description": "a string representing the username of the account being accessed."
        },
        "password": {
          "type": "string",
          "title": "Password",
          "description": "a string representing the password being used to access the account."
        }
      },
      "type": "object",
      "required": [
        "username",
        "password"
      ],
      "title": "UserVerify"
    }
    ```
  - Required: Yes
- **Responses**:
  - `200`: Successful Response
    - Content-Type: `application/json`
    - Schema:
      ```json
      {
        "properties": {
          "success": {
            "type": "boolean",
            "title": "Success",
            "default": true
          }
        },
        "type": "object",
        "title": "ResponseModel"
      }
      ```
  - `401`: Unauthorized
    - Content-Type: `application/json`
    - Schema:
      ```json
      {
        "properties": {
          "success": {
            "type": "boolean",
            "title": "Success",
            "default": false
          },
          "reason": {
            "type": "string",
            "title": "Reason"
          }
        },
        "type": "object",
        "required": [
          "reason"
        ],
        "title": "ErrorResponse"
      }
      ```
  - `422`: Unprocessable Entity
    - Content-Type: `application/json`
    - Schema:
      ```json
      {
        "properties": {
          "success": {
            "type": "boolean",
            "title": "Success",
            "default": false
          },
          "reason": {
            "type": "string",
            "title": "Reason"
          }
        },
        "type": "object",
        "required": [
          "reason"
        ],
        "title": "ErrorResponse"
      }
      ```
  - `429`: Too Many Requests
    - Content-Type: `application/json`
    - Schema:
      ```json
      {
        "properties": {
          "success": {
            "type": "boolean",
            "title": "Success",
            "default": false
          },
          "reason": {
            "type": "string",
            "title": "Reason"
          }
        },
        "type": "object",
        "required": [
          "reason"
        ],
        "title": "ErrorResponse"
      }
      ```

## Data Models

### ErrorResponse

- **Properties**:
  - `success`: (boolean, default: `false`) Indication of success.
  - `reason`: (string) Reason for the error.
- **Required Fields**: `reason`

### ResponseModel

- **Properties**:
  - `success`: (boolean, default: `true`) Indication of success.

### UserCreate

- **Properties**:
  - `username`: (string) Username for the account. Must be between 3 to 32 characters.
  - `password`: (string) Password for the account. Must be between 8 to 32 characters and contain at least 1 uppercase letter, 1 lowercase letter, and 1 number.
- **Required Fields**: `username`, `password`

### UserVerify

- **Properties**:
  - `username`: (string) Username of the account being accessed.
  - `password`: (string) Password being used to access the account.
- **Required Fields**: `username`, `password`
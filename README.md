
***
# FastAPI
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
      "$ref": "#/components/schemas/UserCreate"
    }
    ```
  - Required: Yes
- **Responses**:
  - `200`: Successful Response
    - Content-Type: `application/json`
    - Schema:
      ```json
      {
        "$ref": "#/components/schemas/ResponseModel"
      }
      ```
  - `400`: Bad Request
    - Content-Type: `application/json`
    - Schema:
      ```json
      {
        "$ref": "#/components/schemas/ErrorResponse"
      }
      ```
  - `422`: Unprocessable Entity
    - Content-Type: `application/json`
    - Schema:
      ```json
      {
        "$ref": "#/components/schemas/ErrorResponse"
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
      "$ref": "#/components/schemas/UserVerify"
    }
    ```
  - Required: Yes
- **Responses**:
  - `200`: Successful Response
    - Content-Type: `application/json`
    - Schema:
      ```json
      {
        "$ref": "#/components/schemas/ResponseModel"
      }
      ```
  - `401`: Unauthorized
    - Content-Type: `application/json`
    - Schema:
      ```json
      {
        "$ref": "#/components/schemas/ErrorResponse"
      }
      ```
  - `422`: Unprocessable Entity
    - Content-Type: `application/json`
    - Schema:
      ```json
      {
        "$ref": "#/components/schemas/ErrorResponse"
      }
      ```
  - `429`: Too Many Requests
    - Content-Type: `application/json`
    - Schema:
      ```json
      {
        "$ref": "#/components/schemas/ErrorResponse"
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

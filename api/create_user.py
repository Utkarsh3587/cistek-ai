import json
import os
import boto3
import uuid
import re

dynamodb = boto3.resource("dynamodb", endpoint_url=os.environ.get("DYNAMODB_ENDPOINT"))
table_name = os.environ.get("TABLE_NAME")
table = dynamodb.Table(table_name)

EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

def validate_email(email):
    """Validate email format"""
    if not re.match(EMAIL_REGEX, email):
        return False
    return True

def validate_phone_number(phone_number):
    """Validate phone number: must be numeric and have a length between 10 and 15 characters."""
    if not phone_number.isdigit() or len(phone_number) < 10 or len(phone_number) > 15:
        return False
    return True

def lambda_handler(event, context):
    try:
        # Parse request body
        body = json.loads(event["body"])
        
        # Validate email format
        email = body.get("email")
        if not email or not validate_email(email):
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Invalid email format"}),
                "headers": {
                    "Content-Type": "application/json"
                }
            }

        # Validate phone number length
        phone_number = body.get("phone_number")
        if not phone_number or not validate_phone_number(phone_number):
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Phone number must be numeric and between 10 and 15 characters"}),
                "headers": {
                    "Content-Type": "application/json"
                }
            }

        # Generate UUID for user_id
        user_id = str(uuid.uuid4())
        
        # Prepare user data
        user_data = {
            "user_id": user_id,
            "firstname": body["firstname"],
            "lastname": body["lastname"],
            "dob": body["dob"],
            "address": body["address"],
            "gender": body["gender"],
            "email": email,
            "phone_number": phone_number
        }
        
        # Insert data into DynamoDB
        table.put_item(Item=user_data)
        
        # Return success response with 201 Created status
        return {
            "statusCode": 201,
            "body": json.dumps({"message": "User created successfully", "user_id": user_id}),
            "headers": {
                "Content-Type": "application/json"
            }
        }
        
    except KeyError as e:
        # Handle missing fields with a 400 Bad Request error
        return {
            "statusCode": 400,
            "body": json.dumps({"error": f"Missing required field: {str(e)}"}),
            "headers": {
                "Content-Type": "application/json"
            }
        }
    except Exception as e:
        # Handle unexpected errors with a 500 Internal Server Error
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {
                "Content-Type": "application/json"
            }
        }

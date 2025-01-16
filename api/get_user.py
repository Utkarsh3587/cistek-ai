import json
import os
import boto3

dynamodb = boto3.resource("dynamodb", endpoint_url=os.environ.get("DYNAMODB_ENDPOINT"))
table_name = os.environ.get("TABLE_NAME")
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    user_id = event["pathParameters"]["user_id"]
    
    try:
        # Retrieve user data from DynamoDB
        response = table.get_item(Key={"user_id": user_id})
        
        if "Item" not in response:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "User not found"}),
                "headers": {
                    "Content-Type": "application/json"
                }
            }

        user = response["Item"]
        
        # Return user data with 200 OK
        return {
            "statusCode": 200,
            "body": json.dumps(user),
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

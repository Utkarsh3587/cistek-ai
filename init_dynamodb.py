import boto3

def create_users_table():
    dynamodb = boto3.client("dynamodb", endpoint_url="http://localhost:8000")

    try:
        dynamodb.create_table(
            TableName="Users",
            KeySchema=[
                {"AttributeName": "user_id", "KeyType": "HASH"}
            ],
            AttributeDefinitions=[
                {"AttributeName": "user_id", "AttributeType": "S"}
            ],
            ProvisionedThroughput={
                "ReadCapacityUnits": 5,
                "WriteCapacityUnits": 5
            }
        )
        print("Table 'Users' created successfully.")
    except dynamodb.exceptions.ResourceInUseException:
        print("Table 'Users' already exists.")

if __name__ == "__main__":
    create_users_table()

import json
import boto3

# Initialize a DynamoDB resource
dynamodb = boto3.resource('dynamodb')

# Replace 'Movies' with the name of your DynamoDB table
table = dynamodb.Table('Movies')

def lambda_handler(event, context):
    try:
        # Scan the DynamoDB table to retrieve all movie entries
        response = table.scan()
        movies = response.get('Items', [])
        
        # Return the list of movies in the response
        return {
            'statusCode': 200,
            'body': json.dumps(movies)
        }
        
    except Exception as e:
        # Return a 500 status code if there's an internal server error
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error retriving the mo: {str(e)}')
        }

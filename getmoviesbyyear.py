import json
import boto3
from boto3.dynamodb.conditions import Attr

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Movies')

def lambda_handler(event, context):
    try:
        # Safely extract the 'year' path parameter from the event
        if 'pathParameters' not in event or 'year' not in event['pathParameters']:
            return {
                'statusCode': 400,
                'body': json.dumps('Year parameter is missing from the request.')
            }
        
        # Get the year from pathParameters (as a string, since 'releaseYear' is a string)
        year = event['pathParameters']['year']

        # Query DynamoDB for movies with the specified 'releaseYear'
        response = table.scan(
            FilterExpression=Attr('releaseYear').eq(year)
        )
        
        # Get the movies from the response
        movies = response.get('Items', [])
        
        # Return the list of movies as a response
        return {
            'statusCode': 200,
            'body': json.dumps(movies)
        }
    
    except Exception as e:
        # Return internal server error if something goes wrong
        return {
            'statusCode': 500,
            'body': json.dumps(f'Internal server error: {str(e)}')
        }

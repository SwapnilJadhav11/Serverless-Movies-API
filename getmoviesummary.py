import json
import boto3
import os
import requests

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Movies')

# OpenAI API endpoint and headers
openai_api_key = os.getenv('OPENAI_API_KEY')  # Retrieve the OpenAI API key from environment variables
openai_url = "https://api.openai.com/v1/chat/completions"  # Updated endpoint for gpt-3.5-turbo

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {openai_api_key}"  # Add the API key to the authorization header
}

def lambda_handler(event, context):
    try:
        # Safely extract the 'movieTitle' path parameter from the event
        if 'pathParameters' not in event or 'movieTitle' not in event['pathParameters']:
            return {
                'statusCode': 400,
                'body': json.dumps('Movie title parameter is missing from the request.')
            }
        
        # Get the movie title from pathParameters
        movie_title = event['pathParameters']['movieTitle']

        # Query DynamoDB for the movie with the specified title
        response = table.get_item(
            Key={'moviesTitle': movie_title}
        )
        
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'body': json.dumps('Movie not found.')
            }
        
        movie = response['Item']

        # Generate a prompt for GPT based on the movie information
        prompt = f"Summarize the movie '{movie['moviesTitle']}', a {movie['genre']} film released in {movie['releaseYear']}."
        
        # Request GPT-3.5-turbo for a summary
        data = {
            "model": "gpt-3.5-turbo",  # Use the newer model
            "messages": [{"role": "system", "content": "You are a helpful assistant."},
                         {"role": "user", "content": prompt}],  # Updated to match the new chat format
            "max_tokens": 150  # Limit the response length
        }
        openai_response = requests.post(openai_url, headers=headers, json=data)
        
        if openai_response.status_code != 200:
            return {
                'statusCode': 500,
                'body': json.dumps(f"OpenAI API request failed: {openai_response.text}")
            }
        
        # Parse the GPT response and extract the summary
        gpt_summary = openai_response.json()['choices'][0]['message']['content'].strip()

        # Add the generated summary to the movie details
        movie['generatedSummary'] = gpt_summary
        
        # Return the movie details with the generated summary
        return {
            'statusCode': 200,
            'body': json.dumps(movie)
        }

    except Exception as e:
        # Return internal server error if something goes wrong
        return {
            'statusCode': 500,
            'body': json.dumps(f'Internal server error: {str(e)}')
        }

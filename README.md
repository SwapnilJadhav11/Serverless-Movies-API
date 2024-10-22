# **Serverless Movies API - Capstone Project**

This project is a **Serverless Movies API** that allows users to retrieve movie information and generate movie summaries using OpenAI's GPT-3.5 model. The API is built with **AWS Lambda**, **API Gateway**, and **DynamoDB** for a fully serverless architecture. It includes endpoints to retrieve a list of movies, search for movies by year, and generate AI-based movie summaries.

## **Table of Contents**
- [Overview](#overview)
- [API Endpoints](#api-endpoints)
- [Technologies Used](#technologies-used)
- [Setup and Installation](#setup-and-installation)
  - [Prerequisites](#prerequisites)
  - [Terminal Commands](#terminal-commands)
  - [AWS Lambda Configuration](#aws-lambda-configuration)
  - [OpenAI API Integration](#openai-api-integration)
  - [API Gateway Setup](#api-gateway-setup)
- [Authentication](#authentication)
- [Usage](#usage)
- [Testing](#testing)
- [Future Enhancements](#future-enhancements)

## **Overview**

The Serverless Movies API allows users to:
- Retrieve a list of movies stored in a DynamoDB table.
- Search for movies based on release year.
- Generate movie summaries using OpenAI's GPT model.

The API uses **AWS Lambda** functions for serverless execution, **DynamoDB** for storing movie details, and **API Gateway** to expose the functions as REST API endpoints. Movie covers are stored in **AWS S3**, and the OpenAI GPT-3.5 model generates summaries dynamically.

## **API Endpoints**

### 1. **GetMovies**
- **Endpoint**: `/getmovies`
- **Description**: Returns a list of all movies in the database.
- **Response Example**:
  ```json
  [
    {
      "moviesTitle": "Inception",
      "releaseYear": "2010",
      "genre": "Science Fiction, Action",
      "coverUrl": "https://moviecoversbucket.s3.amazonaws.com/Inception.jpg"
    },
    ...
  ]
  ```

### 2. **GetMoviesByYear**
- **Endpoint**: `/getmoviesbyyear/{year}`
- **Description**: Returns movies released in the specified year.
- **Response Example**:
  ```json
  [
    {
      "moviesTitle": "Inception",
      "releaseYear": "2010",
      "genre": "Science Fiction, Action",
      "coverUrl": "https://moviecoversbucket.s3.amazonaws.com/Inception.jpg"
    }
  ]
  ```

### 3. **GetMovieSummary**
- **Endpoint**: `/getmoviesummary/{movieTitle}`
- **Description**: Retrieves movie details and generates an AI-based summary.
- **Response Example**:
  ```json
  {
    "moviesTitle": "Inception",
    "releaseYear": "2010",
    "genre": "Science Fiction, Action",
    "coverUrl": "https://moviecoversbucket.s3.amazonaws.com/Inception.jpg",
    "generatedSummary": "A mind-bending sci-fi thriller about dream manipulation and corporate espionage, where a skilled thief enters the dreams of others to steal secrets."
  }
  ```

## **Technologies Used**

- **AWS Lambda**: Serverless compute for executing functions.
- **AWS API Gateway**: Exposes Lambda functions as REST APIs.
- **AWS DynamoDB**: NoSQL database to store movie details.
- **AWS S3**: For storing and retrieving movie cover images.
- **OpenAI API**: Used to generate AI-based movie summaries using GPT-3.5.
- **Python**: Programming language for Lambda functions.
- **`requests`** Library: To interact with the OpenAI API.
- **AWS Lambda Layers**: Used to include additional Python packages like `requests`.

## **Setup and Installation**

### **Prerequisites**
- **AWS Account**: Required to set up Lambda, API Gateway, DynamoDB, and S3.
- **OpenAI API Key**: Obtain your API key from [OpenAI](https://platform.openai.com/account/api-keys).
- **Python 3.x** installed locally.
- **AWS CLI** (optional but recommended).

### **Terminal Commands**

These are the steps and commands we executed on the terminal:

#### 1. **Install the `requests` library for Lambda Layer**:
We installed the `requests` library in a local directory, zipped it, and uploaded it as a Lambda layer.

```bash
# Create a directory for the Python packages
mkdir python
cd python

# Install requests in the directory
pip install requests -t .

# Zip the directory
cd ..
zip -r requests-layer.zip python/
```

#### 2. **Upload the Layer to AWS Lambda**:
1. Go to the **AWS Lambda Console**.
2. In the left-hand menu, select **Layers**.
3. Click **Create Layer**, upload the `requests-layer.zip` file, and select the appropriate runtime (e.g., Python 3.12).
4. Attach the layer to your Lambda function.

---

### **AWS Lambda Configuration**

1. **Create Lambda Functions** for:
   - `GetMovies`
   - `GetMoviesByYear`
   - `GetMovieSummary`

2. **Add Environment Variables**:
   - Go to the **Configuration** tab of the Lambda function.
   - Add an environment variable for the **OpenAI API Key**:
     - **Key**: `OPENAI_API_KEY`
     - **Value**: Your OpenAI API Key (e.g., `sk-xxxxxxxxxxxxxxxx`).

3. **IAM Roles**:
   - Ensure your Lambda functions have the correct permissions to access **DynamoDB** and **S3**.
   - Attach the `AWSLambdaBasicExecutionRole` and any other relevant policies for DynamoDB and S3 access.

### **OpenAI API Integration**

The OpenAI API is used to generate movie summaries dynamically. To integrate it into the Lambda function:

1. Install the `requests` library as shown above.
2. Use the `gpt-3.5-turbo` model for generating the summary, as `text-davinci-003` has been deprecated.

### **API Gateway Setup**

1. **Create a new API Gateway** with the following endpoints:
   - `/getmovies`
   - `/getmoviesbyyear/{year}`
   - `/getmoviesummary/{movieTitle}`

2. **Enable Lambda Proxy Integration** to pass path parameters correctly to Lambda.

3. **Deploy the API** to a stage (e.g., `prod`).

---

## **Authentication**

We did not implement full authentication in this project, but to secure the API further, you can:
- **Add API Keys**: Set up API keys in API Gateway.
- **Use AWS Cognito**: Implement user authentication for more robust security.
- **Attach Permissions**: Use IAM roles to restrict access to resources like DynamoDB and S3.

---

## **Usage**

1. **GetMovies**:
   - To retrieve all movies, make a `GET` request to:
     ```
     GET /getmovies
     ```

2. **GetMoviesByYear**:
   - To search for movies released in a specific year, make a `GET` request to:
     ```
     GET /getmoviesbyyear/2010
     ```

3. **GetMovieSummary**:
   - To generate a summary for a movie, make a `GET` request to:
     ```
     GET /getmoviesummary/Inception
     ```

---

## **Testing**

You can test the API using tools like **Postman**, **curl**, or **AWS API Gateway Test Console**.

---

## **Future Enhancements**

- **Authentication**: Add user authentication using AWS Cognito or API keys.
- **Rate Limiting**: Implement rate limiting to avoid overuse of the OpenAI API.
- **Search by Genre**: Add the ability to search movies by genre.
- **Additional Movie Details**: Include more detailed movie information (e.g., cast, director).

---

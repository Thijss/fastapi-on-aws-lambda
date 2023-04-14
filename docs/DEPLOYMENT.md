# Deployment on AWS lambda

This document describes how to deploy the API on AWS Lambda.
If you do not want to use AWS S3, you can skip the final section about linking the API to AWS S3.

## Setting up the API on your AWS account

Prerequisites:
- Python 3.9 on your local machine (AWS Lambda runs on Python 3.9)
- poetry installed (https://python-poetry.org/)
- AWS Account (https://aws.amazon.com/)
- AWS CLI installed (https://aws.amazon.com/cli/). Alternatively you can do everything manually on the [AWS console](https://console.aws.amazon.com/).


## API (AWS Lambda)

### Creating a Lambda function on your AWS account
Create a Lambda function on your AWS account to run the API.
You can use the console to create your lambda function. This will automatically link a AWSLambdaBasicExecutionRole to it.

After creation, alter the following for your lambda function:
- Set Runtime to `Python 3.9` (Code > Runtime Settings)
- Set the Runtime Handler to `app.main.handler` (Code > Runtime Settings)
- Enable function URL with Auth type `NONE` (Configuration > Function URL)
  - Explanation: authentication will be done by FastAPI


### Configure environment variables for your lambda function
On the lambda console of your function, head over to 'Configuration -> Environment variables' and add the following:

- set `API_KEY_READ_ACCESS` to `<a_random_string>`
- set `API_KEY_WRITE_ACCESS` to `<a_different_random_string>`

For now, we will allow all origins, methods and headers. You can restrict this later on.

- set `HTTP_ALLOWED_METHODS` to `*` 
- set `HTTP_ALLOWED_HEADERS` to `*`
- set `HTTP_ALLOWED_ORIGINS` to `*` 


### Install the dependencies on your local machine using poetry
Create a python 3.9 environment:
```
poetry env use 3.9
```
Then install the dependencies:
```
poetry install
```
Since `in-project = true` is configured in `poetry.toml`, this will create a virtual environment within the project folder.


### Build the lambda package
From the root of the project, run:
```bash
./lambda_zip.sh
```
This script will zip the whole project into `package.zip` in the root of the project.

### Upload the lambda package to your lambda function

From the root of the project, run:
```bash
./lambda_deploy.sh
```
- Note: This script assumes you have a lambda function on AWS with the same name as the current directory. 
  
Alternatively, you can use the AWS console to upload the zip file.

### Done
You can now test your API on AWS Lambda. The URL of your API is available on the lambda console under 'Configuration > Function URL'.

Visit `https://<your_function_url>/docs` to see the Swagger page of your API.


## Linking your API to AWS S3

### Bucket creation
Create a S3 Bucket on your AWS account to store the json files in. Either use the console or AWS CLI:
```
aws s3 mb s3://<your_unique_bucket_name>
```

### Extra environment variables for your lambda function
On the lambda console of your function, head over to 'Configuration -> Environment variables' and add the following:

- set `S3_ACCESS` to `write`
- set `S3_BUCKET_NAME` to `<your_unique_bucket_name>`


### Extending the linked IAM role with S3 permissions
Next, head to 'Configuration > Permissions' and click the link to the IAM role.

Attach the following S3 policy to the role:
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "s3:*",
            "Resource": [
                "arn:aws:s3:::<your_unique_bucket_name>/assets",
                "arn:aws:s3:::<your_unique_bucket_name>/assets/*"
            ]
        }
    ]
}
```

### Done
Your API now has read/write access to your S3 bucket.
You can now test your API on AWS Lambda. The URL of your API is available on the lambda console under 'Configuration > Function URL'.

Visit `https://<your_function_url>/docs` to see the Swagger page of your API.
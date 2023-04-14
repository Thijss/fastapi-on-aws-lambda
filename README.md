# FastAPI on AWS Lambda (with AWS S3)
Welcome to my template repository for running FastAPI on AWS Lambda with an optional link to AWS S3.

## AWS deployment
Checkout [DEPLOYMENT](docs/DEPLOYMENT.md) for a detailed guide on how to deploy the project on AWS Lambda and link with AWS S3.


## Local installation
The project's Python version is currently locked to python 3.9 to keep it compatible with AWS Lambda. 
If you want to run the API locally, you need to have python 3.9 installed.

If you do not plan to deploy the API on AWS Lambda, you can update the python version constraint in `pyproject.toml` and use any python version >= 3.6.

### Install dependencies
```
poetry env use 3.9
poetry install
```

### Set environment variables
copy .env.example to .env and fill in the values
```
cp .env.example .env
```

## Roadmap/ToDo
- [ ] Add integration with AWS Cognito for authentication
- [ ] Move setup to an AWS Cloudformation Template
- [ ] Split JSON files of each model into multiple files to allow concurrent writes.
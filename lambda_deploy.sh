# Note: This script assumes you have a lambda function on AWS with the same name as the current directory
# You can alter "${PWD##*/}" to a fixed name if this is not the case
aws lambda update-function-code --function-name "${PWD##*/}" --zip-file fileb://package.zip

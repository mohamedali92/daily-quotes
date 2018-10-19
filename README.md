[![CircleCI](https://circleci.com/gh/mohamedali92/daily-quotes/tree/master.svg?style=svg)](https://circleci.com/gh/mohamedali92/daily-quotes/tree/master)
# Daily-quotes  

Simple service to send myself daily motivational quotes. Over the last year I have collected quotes that I enjoy and can relate to. The purpose of this project is to deliver these one of these quotes daily to myself in the form of an sms message.

## Why am I building this project?

 - Deliver daily motivational quotes to myself
 - Understand and gain experience building serverless applications using [AWS lambda](https://aws.amazon.com/lambda/)
 - Gain experience writting integration & acceptance tests for serverless applications
 - Learn how to build a CI/CD pipeline using [CirleCI](https://circleci.com/)
 - Learn how to use AWS resources such as SNS, DynamoDB and Cloudwatch
 - Gain experience with the [serverless framework](https://github.com/serverless/serverless)

## What marks the project as done?

 - [x] Integration and acceptance tests
 - [x] CI/CD pipeline for testing and deploying
 - [x] Secret management via AWS ssm
 - [x] Command line application to add new quotes

## Architecture 
![daily-quotes-arch](https://user-images.githubusercontent.com/8728962/46260974-f42a6d00-c4a1-11e8-9ae9-7072fcccf6fb.png)

## Usage instructions
### Setup
 1. [Setup an AWS account](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/)
 2. [Install and configure the serverless framework](https://serverless.com/framework/docs/providers/aws/guide/quick-start/)
 3. [Configure credentials](https://serverless.com/framework/docs/providers/aws/guide/credentials/)

 ### Setup secrets
Add PhoneNumber secret to SSM. 
Originally I used environment variables to pass my phone number to the handler function, but that means putting my personal phone number on the internet when I add my code to git. Yikes! After reading this [article](https://serverless.com/blog/serverless-secrets-api-keys/)  about secrets management I switched over to the AWS Systems Manager Parameter Store to store secrets. Refer to the above article or this [AWS document](https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-paramstore-su-create.html)  to add a parameter with the name ```PhoneNumber``` to the parameter store.

### Deployment
Deploy using  ``` sls deploy -v --stage STAGENAME --region REGIONNAME ```
This should create the cloudwatch event, lambda function, DynamoDB table and the required iam role and permissions.

### Seeding  data
After deployment you should have an empty DynamoDB table in ```REGIONNAME``` . In order to recieve daily quotes you need to seed the table with data. At a minimum the following is required:
```
{
  "NumberOfQuotes": 3,
  "PhoneNumber": "+17785558888",
  "Quotes": [
    "Discipline equals freedom",
    "A life of no regrets",
    "Ego is enemy"
  ]
}
```

### Testing
To test that your function works you can invoke it from the aws console/cli or using the serverless framework as follows
```sls invoke --function daily-quote --stage dev --region us-west-2 --log```
### Adding new quotes
To add a new quote, create a new virtualenv. Activate your virtualenv and cd into the add_new_quotes directory. Then run ```pip install --editable .```
Make sure you have aws credentials setup with enough permissions to udpate items in dynamoDB table. You also need to set your table name in parameter store.
After that you should be able to add quotes; the ```PHONENUMBER``` is the primary key Id for the dynamoDB table. 
```add_new_quotes PHONENUMBER [QUOTES]...```

For Example:
```add_new_quotes +17781112222 "Like attracts like" "You attract what you are."```

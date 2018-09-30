# Daily-quotes  

Simple service to send myself daily motivational quotes. Over the last year I have collected quotes that I enjoy and can relate to. The purpose of this project is to deliver these one of these quotes daily to myself in the form of an sms message.

## Why am I building this project?

 - Deliver daily motivational quotes to myself
 - Understand and gain experience building serverless applications using [AWS lambda](https://aws.amazon.com/lambda/)
 - Gain experience writting integration & acceptance tests for serverless applications
 - Learn how to build a CI/CD pipeline using [CirleCI](https://circleci.com/)
 - Learn how to use AWS resources such as SNS, DynmaoDB and Cloudwatch
 - Gain experience with the [serverless framework](https://github.com/serverless/serverless)

## What marks the project as done?

 - [x] Integration and acceptance tests
 - [x] CI/CD pipeline for testing and deploying
 - [x] Secret management via AWS ssm
 - [ ] Command line application to add new quotes

## Architecture 
![daily-quotes-arch](https://user-images.githubusercontent.com/8728962/46260974-f42a6d00-c4a1-11e8-9ae9-7072fcccf6fb.png)

## Usage instructions
### Setup
 1. [Setup an AWS account](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/)
 2. [Install and configure the serverless framework](https://serverless.com/framework/docs/providers/aws/guide/quick-start/)
 3. [Configurecredentials](https://serverless.com/framework/docs/providers/aws/guide/credentials/)

 ### Setup secrets
Add PhoneNumber secret to SSM. 
Originally I used environment variables to pass my phone number to the handler function, but that means putting my personal phone number on the internet when I add my code to git. Yikes! After reading this [article](https://serverless.com/blog/serverless-secrets-api-keys/)  about secrets management I switched over to the AWS Systems Manager Parameter Store to store secrets. Refer to the above article or this [AWS document](https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-paramstore-su-create.html)  to add a parameter with the name ```PhoneNumber``` to the parameter store.

### Deployment
Deploy using  ``` sls deploy --stage STAGENAME --region REGIONNAME ```
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
### Adding new quotes

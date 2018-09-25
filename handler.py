import json
import logging
import boto3
from botocore.exceptions import ClientError
from random import randrange
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

clientSNS = boto3.client("sns")
dynamodb = boto3.resource("dynamodb")


# Temp code while I refactor to pull dynamically from ssm
if "DYNAMODB_TABLE" and "PHONE_NUMBER" in os.environ:
    tableName = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    phoneNumber = os.environ['PHONE_NUMBER']
else:
    pass


def get_number_of_quotes(tableName, phoneNumberPrimaryId):
    try:
        numberOfQuotes = tableName.get_item(
            Key={
                "PhoneNumber": phoneNumberPrimaryId
            },
            ProjectionExpression="NumberOfQuotes"
        )
    except ClientError as e:
        logging.error(e.response['Error']['Message'])
    else:
        numberOfQuotesStripped = int(numberOfQuotes['Item']['NumberOfQuotes'])
        logging.info(numberOfQuotesStripped)
        return numberOfQuotesStripped


def get_random_quote(tableName, phoneNumberPrimaryId, quoteNumber):
    projectionExpressionString = f"Quotes[{quoteNumber}]"
    logging.info(projectionExpressionString)
    try:
        randomQuote = tableName.get_item(
            Key={
                "PhoneNumber": phoneNumberPrimaryId
            },
            ProjectionExpression=projectionExpressionString
        )
    except ClientError as e:
        logging.error(e.response['Error']['Message'])
    else:
        randomQuoteStripped = randomQuote['Item']['Quotes'][0]
        logging.info(randomQuoteStripped)
        return randomQuoteStripped


def send_random_quote_sms(phoneNumber, randomQuote):
    clientSNS.publish(
        PhoneNumber=phoneNumber,
        Message=randomQuote
    )


def send_daily_quote(event, context):
    numberOfQuotes = get_number_of_quotes(tableName, phoneNumber)
    randomNumber = randrange(numberOfQuotes - 1)
    randomQuote = get_random_quote(tableName, phoneNumber, randomNumber)
    send_random_quote_sms(phoneNumber, randomQuote)

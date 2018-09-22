import boto3
import logging
from botocore.exceptions import ClientError
from random import randrange

logging.basicConfig(level=logging.INFO)

session = boto3.Session(profile_name="daily-quotes")

clientSNS = session.client("sns")
dynamodb = session.resource("dynamodb")
table = dynamodb.Table("DailyQuotes")
phoneNumber = ""


def get_number_of_quotes(phoneNumberPrimaryId):
    try:
        numberOfQuotes = table.get_item(
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


def get_random_quote(phoneNumberPrimaryId, quoteNumber):
    projectionExpressionString = f"Quotes[{quoteNumber}]"
    logging.info(projectionExpressionString)
    try:
        randomQuote = table.get_item(
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

numberOfQuotes = get_number_of_quotes(phoneNumber)
randomNumber = randrange(numberOfQuotes - 1)
randomQuote = get_random_quote(phoneNumber, randomNumber)
send_random_quote_sms(phoneNumber, randomQuote)


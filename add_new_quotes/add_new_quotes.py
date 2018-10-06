import boto3
import click
import logging
from click import echo

logger = logging.getLogger()
logger.setLevel(logging.INFO)

clientSSM = boto3.client('ssm')
dynamodb = boto3.resource("dynamodb")


def get_secret(key):
    resp = clientSSM.get_parameter(
        Name=key,
        WithDecryption=True
        )
    return resp['Parameter']['Value']


tableName = dynamodb.Table(get_secret('DYNAMODB_TABLE'))

def process_quotes(quotes):
    valid_quotes = []
    for quote in quotes:
        if len(quote) < 160:
            valid_quotes.append(quote)
        else:
            echo (f'This quote: {quote}"" exceeds 160 characters and is going to be discarded.')
    return valid_quotes, len(valid_quotes)
    

@click.command()
@click.argument('phone_number')
@click.argument('quotes', nargs=-1)
def add_new_quote(phone_number, quotes):
    new_quotes, number_of_new_quotes = process_quotes(quotes)
    if number_of_new_quotes > 0:
        try:
            response = tableName.update_item(
                Key={
                    "PhoneNumber": phone_number
                },
                UpdateExpression="SET Quotes = list_append(Quotes, :i), NumberOfQuotes = NumberOfQuotes + :n",
                ExpressionAttributeValues={
                    ':i': new_quotes,
                    ':n': number_of_new_quotes,
                },
                ReturnValues="UPDATED_NEW"
            )
        except ClientError as e:
            logging.error(e.response['Error']['Message'])
        else: 
            click.echo(response)
    else:
        click.echo("No new quotes added.")
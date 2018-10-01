import boto3
import click
import logging

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


phoneNumber = get_secret('PhoneNumber')
tableName = dynamodb.Table(get_secret('DYNAMODB_TABLE'))

@click.command()
@click.argument('phone_number')
@click.argument('quote')
def add_new_quote(phone_number, quote):
    """Example script."""
    click.echo('Hello World!')
    click.echo(phone_number)
    click.echo(quote)


@click.command()
@click.argument('phone_number')
def get_number_of_quotes(phone_number):
    try:
        numberOfQuotes = tableName.get_item(
            Key={
                "PhoneNumber": phone_number
            },
            ProjectionExpression="NumberOfQuotes"
        )
    except ClientError as e:
        logging.error(e.response['Error']['Message'])
    else:
        numberOfQuotesStripped = int(numberOfQuotes['Item']['NumberOfQuotes'])
        click.echo(numberOfQuotesStripped)

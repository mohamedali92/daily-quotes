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


tableName = dynamodb.Table(get_secret('DYNAMODB_TABLE'))


@click.command()
@click.argument('phone_number')
@click.argument('quote')
def add_new_quote(phone_number, quote):
    """Example script."""
    click.echo('Hello World!')
    click.echo(phone_number)
    click.echo(quote)
    try:
        response = tableName.update_item(
            Key={
                "PhoneNumber": phone_number
            },
            UpdateExpression="SET Quotes = list_append(Quotes, :i), NumberOfQuotes = NumberOfQuotes + :n",
            ExpressionAttributeValues={
                ':i': [quote],
                ':n': 1,
            },
            ReturnValues="UPDATED_NEW"
        )
    except ClientError as e:
        logging.error(e.response['Error']['Message'])
    else: 
        click.echo(response)
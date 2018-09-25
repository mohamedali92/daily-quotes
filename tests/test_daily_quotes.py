# Path hack.
import sys
import os
import boto3
from handler import get_number_of_quotes, get_random_quote
from random import randrange

clientSNS = boto3.client("sns")
dynamodb = boto3.resource("dynamodb")
clientSSM = boto3.client('ssm')


def get_secret(key):
    resp = clientSSM.get_parameter(
        Name=key,
        WithDecryption=True
        )
    return resp['Parameter']['Value']


phoneNumber = get_secret('PhoneNumber')
table = dynamodb.Table(get_secret('DYNAMODB_TABLE'))


def test_number_of_quotes():
    numberOfQuotes = get_number_of_quotes(table, phoneNumber)
    assert numberOfQuotes > 0


def test_get_random_quote():
    numberOfQuotes = get_number_of_quotes(table, phoneNumber)
    randomNumber = randrange(numberOfQuotes - 1)
    randomQuote = get_random_quote(table, phoneNumber, randomNumber)
    assert len(randomQuote) > 0


import boto3


session = boto3.Session(profile_name='sns-sms')

client = session.client("sns")


client.publish(
    PhoneNumber="+17785524618",
    Message="Hello World!!"
)
import json
import boto3
from botocore.exceptions import ClientError

def send_email(to_email, subject, body_text, body_html):
    client = boto3.client('ses', region_name='us-east-1')
    sender_email = "your_verified_sender@example.com"
    
    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    to_email,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': "UTF-8",
                        'Data': body_html,
                    },
                    'Text': {
                        'Charset': "UTF-8",
                        'Data': body_text,
                    },
                },
                'Subject': {
                    'Charset': "UTF-8",
                    'Data': subject,
                },
            },
            Source=sender_email,
        )
    except ClientError as e:
        return e.response['Error']['Message']
    else:
        return response['MessageId']

def lambda_handler(event, context):
    required_keys = ['to_email', 'subject', 'body_text', 'body_html']
    
    for key in required_keys:
        if key not in event:
            return {
                'statusCode': 400,
                'body': json.dumps(f"Missing required key: {key}")
            }

    to_email = event['to_email']
    subject = event['subject']
    body_text = event['body_text']
    body_html = event['body_html']
    
    email_response = send_email(to_email, subject, body_text, body_html)
    
    if isinstance(email_response, str) and 'Error' in email_response:
        return {
            'statusCode': 500,
            'body': json.dumps(email_response)
        }
    else:
        return {
            'statusCode': 200,
            'body': json.dumps(f"Email sent! Message ID: {email_response}")
        }


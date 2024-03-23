import traceback
import json
import boto3
from openai import OpenAI
from config import Config

BUCKET_NAME = "openmeeting-serverless-mp3"


# SNS, SQS for data in transit, S3, Aurora, DynamoDB for persistence
def speech_to_text(client, config, file_key):

    response = client.get_object(Bucket=BUCKET_NAME, Key=file_key)
    audio_file = response['Body'].read()

    try:
        transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
        )
    except Exception as ex:
        print(f"Unable to transcribe audio: {ex}")
        traceback.print_exc()
        return {"statusCode": 500, 
                "body": f"Unable to transcribe audio: {ex}"}

    print(transcription.text)

    return transcription


def text_to_summary(client, content, summary_size=150):

    try:
        response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", 
             "content": f"Summarize the following text within {summary_size}: "},
        ]
        )
    except Exception as ex:
        print(f"Unable to summarize text: {ex}")
        traceback.print_exc()
        return {"statusCode": 500, 
                "body": f"Unable to summarize text: {ex}"}
    
    return response

## uploads mp3 to bucket and returns object name ##
## is this a frontend process? ##
def upload_audio_file(file, config):
    bucket = boto3.client("s3")

    response = bucket.put_object(Bucket=config["BUCKET_NAME"], Key=config["BUCKET_KEY"], Body=file)
    return response



## if uploading mp3, then activating summarizer, 
## then we would put MP3 into S3 or DynamoDB
## return a UUID for that item
## and use that UUID when trying to access the item again

## When do we clear out old MP3 files?
def lambda_handler(event, context):
    print(f"request event: {event}")
    client = OpenAI()

    config = Config()

    
    if 'body'in event and 'id' in event['body']['id']:
        audio_file_key = event['body']['key']
    else:
        print("Invalid input: Incorrect format.")
        return {"statusCode": 401, "body": "Invalid input: Incorrect format."}
    
    ## endpoint for processing speech to text ##
    response = speech_to_text(client, config, audio_file_key)

    if not response:

    if 'status' == 

    ## endpoint for summarizing ##
    text_to_summary(client, content=)


    return resp


if __name__ == "__main__":
    id = upload_audio_file(path)
    # return {"statusCode": 200, "body": {"audio_path": path}}
    
import traceback
from io import BytesIO
import boto3
from openai import OpenAI
from config import Config

BUCKET_NAME = "openmeeting-serverless-mp3"


# SNS, SQS for data in transit, S3, Aurora, DynamoDB for persistence
def speech_to_text(client, file_key):
    response = download_audio_file(file_key=file_key)
    audio_file = response['Body'].read()
    # print(audio_file)

    try:
        transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=("recording.mp3", audio_file, "audio/mp3")
        )
    except Exception as ex:
        print(f"Unable to transcribe audio: {ex}")
        traceback.print_exc()
        return {"statusCode": 500, 
                "body": f"Unable to transcribe audio: {ex}"}

    print(transcription.text)

    return transcription.text


def text_to_summary(client, content, summary_size=150):

    try:
        response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "assistant", 
             "content": f"Summarize the following text within {summary_size} words: {content}"},
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
def upload_audio_file(filename):
    s3 = boto3.resource("s3")
    try:
        s3.Object(BUCKET_NAME, f'media/{filename}').put(Body=open(f'./media/{filename}', 'rb'))
    except:
        traceback.print_exc()

def download_audio_file(file_key):
    s3 = boto3.client("s3")
    response = s3.get_object(Bucket=BUCKET_NAME, Key=file_key)
    return response

## if uploading mp3, then activating summarizer, 
## then we would put MP3 into S3 or DynamoDB
## return a UUID for that item
## and use that UUID when trying to access the item again

## When do we clear out old MP3 files?
def lambda_handler(event, context):
    print(f"request event: {event}")
    config = Config()
    client = OpenAI(api_key=config.secret)
    
    if 'body'in event and 'key' in event['body']:
        audio_file_key = event['body']['key']
    else:
        print("Invalid input: Incorrect format.")
        return {"statusCode": 401, "body": "Invalid input: Incorrect format."}
    
    ## endpoint for processing speech to text ##
    response = speech_to_text(client, audio_file_key)

    ## endpoint for summarizing ##
    resp = text_to_summary(client, content=response)

    return resp.choices[0].message.content


if __name__ == "__main__":
    file_name = 'math_problem.mp3'
    upload_audio_file(file_name)
    request = {
        "body": {
            "key": f'media/{file_name}'
        }
    }
    response = lambda_handler(request, None)
    print(response)
    
    
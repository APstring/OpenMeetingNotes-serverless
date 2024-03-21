from openai import OpenAI
import traceback
import json

# SNS, SQS for data in transit, S3, Aurora, DynamoDB for persistence
def speech_to_text(client, audio_path):


    audio_file= open(audio_path, "rb")

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


def upload_audio_file():
    return


def retrieve_audio_path():
    return


## if uploading mp3, then activating summarizer, 
## then we would put MP3 into S3 or DynamoDB
## return a UUID for that item
## and use that UUID when trying to access the item again

## When do we clear out old MP3 files?
def lambda_handler(event, context):
    print(f"request event: {event}")
    client = OpenAI()

    if :
        id = upload_audio_file(path)
        return {"statusCode": 200, "body": {"audio_path": path}}
    else:
        


    if 'body'in event and 'id' in event['body']['id']:
        audio_id = event['body']['id']
    else:
        print("Invalid input: Incorrect format.")
        return {"statusCode": 401, "body": "Invalid input: Incorrect format."}
    
    ## endpoint for uploading mp3 ##

    ## endpoint for summarizing ##


    return resp

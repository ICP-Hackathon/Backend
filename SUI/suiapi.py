import requests
from Walrus import walrus
from DB import models, schemas

BASE_URL = "http://localhost:8080"
RAGCOON_STAGE_ID = "0x68e7482eb88d2bfe57481a8078ed447bc50c00f7487d9484bc00b9e49c0c7986"
headers = {"Content-Type": "application/json"}

def add_user_creator_consumser(user_address: str):
    creator_url = BASE_URL + "/movecall/add_creator"
    consumer_url = BASE_URL + "/movecall/add_consumer"
    creator_params = {
        "ragcoonStageId": RAGCOON_STAGE_ID,
        "creatorAddress": user_address,
    }
    consumer_paramse = {
        "ragcoonStageId": RAGCOON_STAGE_ID,
        "consumerAddress": user_address,
    }
    # Make the POST request to another API with the received data
    creator_response = requests.get(creator_url, params=creator_params, headers=headers).json()
    consumer_response = requests.get(consumer_url, params=consumer_paramse, headers=headers).json()

    print("Creator Response")
    print(creator_response)
    
    print("Consumer Response")
    print(consumer_response)

def add_ai(ai_id: str, creator_address: str):
    url = BASE_URL + "/movecall/add_ai"  # The URL of the REST API you want to call
    headers = {"Content-Type": "application/json"}
    params = {
        "ragcoonStageId": RAGCOON_STAGE_ID,
        "creatorAddress": creator_address,
        "AIID" : ai_id,
    }

    response = requests.get(url, params=params, headers=headers).json()
    digest = response.get('digest')
    return digest


def add_blob(ai: schemas.AITableCreate ,ai_id : str, embed: str):
    url = BASE_URL + "/movecall/add_blob_id"  # The URL of the REST API you want to call
    res = walrus.send_data(str(embed))

    blob_id = ''
    if 'newlyCreated' in res :
        blob_id = res['newlyCreated']['blobObject']['blobId']
    elif 'alreadyCertified' in res :
        blob_id = res['alreadyCertified']['blobId']

    headers = {"Content-Type": "application/json"}
    params = {
        "ragcoonStageId": RAGCOON_STAGE_ID,
        "creatorAddress": ai.creator_address,
        "AIID" : ai_id,
        "blobID" : blob_id
    }
    # Make the POST request to another API with the received data
    response = requests.get(url, params=params, headers=headers).json()
    digest = response.get('digest')
    return digest

def pay_usage(ai: models.AITable, tokens: int):
    url = BASE_URL + "/movecall/pay_usage"  # The URL of the REST API you want to call
    params = {
        "ragcoonStageId": RAGCOON_STAGE_ID,
        "creatorAddress": ai.creator_address,
        "AIID" : ai.ai_id,
        "consumerAddress": ai.creator_address,
        "amount" : tokens
    }
    response = requests.get(url, params=params, headers=headers).json()

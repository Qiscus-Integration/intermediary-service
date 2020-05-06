from chalice import Chalice, Response
# from botocore.vendored import requests
import requests
import json
import os

app = Chalice(app_name='WallsDefaultAgentAllocation')
app.debug = True

QISCUS_BASE_URL = os.getenv("QISCUS_BASE_URL")
QISMO_BASE_URL = os.getenv("QISMO_BASE_URL")
QISMO_APP_ID = os.getenv("QISMO_APP_ID")
QISMO_AUTH_TOKEN = os.getenv("QISMO_AUTH_TOKEN")
QISMO_ADMIN_EMAIL = os.getenv("QISMO_ADMIN_EMAIL")

LINK_PAYMENT = "Link_Payment"

@app.route('/', methods=['POST'])
def index():
    body = app.current_request.json_body
    room = body['room_id']
    agent = body['candidate_agent']['id']
    allocation =  allocate(room,agent)
    print(f"allocation: {body}")
    print("==============================")
    email = body['email']
    name = body['name']
    payload = [
        { 
            "key": "Nama",
            "value": name
        },
        { 
            "key": "Alamat",
            "value": "-"
        },
        { 
            "key": "No Hp",
            "value": email
        },
        { 
            "key": "Order",
            "value": "-"
        },
        { 
            "key": "Jumlah",
            "value": "-"
        },
        { 
            "key": "Biaya",
            "value": "-"
        },
        { 
            "key": LINK_PAYMENT,
            "value": "https://invoice.bayardulu.com/"
        },
        { 
            "key": "No. Resi",
            "value": "-"
        }
    ]

    info = additionalInformation(room, payload)
    print(f"room: {room}")
    print(f"agent: {agent}")
    print(f"userInfo: {info.text}")
    if info.status_code == 200:
        print("success add info")

    return allocation.json()

def allocate(room_id, agent_id):
    url = f"{QISMO_BASE_URL}/api/v1/admin/service/assign_agent"
    payload = {
            'room_id':room_id,
            'agent_id':int(agent_id)
        }
    headers = {
        'Authorization': QISMO_AUTH_TOKEN,
        }
    
    response = requests.request("POST", url, data=payload, headers=headers)
    return response

def additionalInformation(room_id, userInfo):
    payload = {
        "user_properties": userInfo
    }
    print(f"send additionalInformation {payload}")
    url = f"{QISMO_BASE_URL}/api/v1/qiscus/room/{room_id}/user_info"
    headers = {
        'Authorization': QISMO_AUTH_TOKEN,
    }
    response = requests.post(url, headers=headers, json=payload)
    return response

@app.route('/ticket', methods=['POST'])
def submitTicket():
    body = app.current_request.json_body
    print(f"body: {body}")

    add_info = body['additional_info']
    room_id = body['room_id']
    message = f"Berikut e-invoice anda \nOrder ID: {room_id}\n"
    payment = ""
    for i in add_info:
        print(f"additional_info {i}")
        key =  i['key']
        value = i['value']
        if LINK_PAYMENT in key:
            payment = f"Silahkan melalukan pembayaran pada link berikut {value}"
        else:
            new = f"{key} : {value} \n"
            message = message + new
    message = f"{message} \n{payment}"
    tag = addTag(room_id)
    send = sendMessage(room_id, message)
    return send

def sendMessage(room_id, message):
    print(f"send {message} \nto {room_id}")
    
    url = f"{QISMO_BASE_URL}/{QISMO_APP_ID}/bot"
    payload = {
        "sender_email": QISMO_ADMIN_EMAIL, 
        "message": message,
        "type": "text",
        "room_id": room_id
    }
    headers = {
        'Authorization': QISMO_AUTH_TOKEN,
        }
    
    response = requests.request("POST", url, data=payload, headers=headers)
    print(f"send Message: {response.text}")
    return Response(body={"url": response.text},
                    status_code=200,
                    headers={'Content-Type': 'application/json'})

def addTag(room_id):
    print(f"add room tag {room_id}")
    url = f"{QISMO_BASE_URL}/api/v1/room_tag/create"
    payload = {
        "tag": room_id,
        "room_id": room_id
    }
    headers = {
        'Authorization': QISMO_AUTH_TOKEN,
        'Qiscus-App-Id': QISMO_APP_ID
    }
    
    response = requests.request("POST", url, data=payload, headers=headers)
    print(f"add tag: {response.text}")
    return Response(body={"url": response.text},
                    status_code=200,
                    headers={'Content-Type': 'application/json'})



from chalice import Chalice
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
            "key": "Link Payment",
            "value": "https://invoice.bayardulu.com/"
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
    message = f"""
    Order ID: {room_id}
    """
    for i in add_info:
        new = f"{i['key']} : {i['value']} \n"
        message = message + new
    
    sendMessage(room_id, message)

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
    return response




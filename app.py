from chalice import Chalice
# from botocore.vendored import requests
import requests
import json
import os

app = Chalice(app_name='WallsDefaultAgentAllocation')
app.debug = True

base_url = "https://multichannel.qiscus.com"
admin_token = "N4tYDSlsJNc9VvNLcr2d"

@app.route('/', methods=['POST'])
def index():
    body = app.current_request.json_body
    room = body['room_id']
    agent = body['candidate_agent']['id']
    allocation =  allocate(room,agent)

    payload = [
        { 
            "key": "Nama",
            "value": "-"
        },
        { 
            "key": "Alamat",
            "value": "-"
        },
        { 
            "key": "No Hp",
            "value": "-"
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
            "value": "-"
        }
    ]

    info = additionalInformation(room, payload)
    print(f"room: {room}")
    print(f"agent: {agent}")
    print(f"userInfo: {info}")
    if info.status_code == 200:
        print("success add info")

    return allocation.json()

def allocate(room_id, agent_id):
    url = f"{base_url}/api/v1/admin/service/assign_agent"
    payload = {
            'room_id':room_id,
            'agent_id':int(agent_id)
        }
    headers = {
        'Authorization': admin_token,
        }
    
    response = requests.request("POST", url, data=payload, headers=headers)
    return response

def additionalInformation(room_id, userInfo):
    payload = {
        "user_properties": userInfo
    }
    url = f"{base_url}/api/v1/qiscus/room/{room_id}/user_info"
    headers = {
        'Authorization': admin_token,
        }
    
    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
    return response
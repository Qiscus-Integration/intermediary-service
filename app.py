from chalice import Chalice
# from botocore.vendored import requests
import requests
import json
import os

app = Chalice(app_name='CustomAgentAllocation')
app.debug = True

base_url = "https://qismo.qiscus.com"

@app.route('/', methods=['POST'])
def index():

    room = event['room_id']
    agent = event['candidate_agent']['id']
    allocation =  allocate(room,agent)

    payload = [
        { 
            "key": "Contact",
            "value": "https://"
        }
    ]

    info = additionalInformation(room, payload)
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
        'Authorization': "5Y3P3TiuAjJSVSJm8hH8",
        }
    
    response = requests.request("POST", url, data=payload, headers=headers)
    return response

def additionalInformation(room_id, userInfo):
    payload = {
        "user_properties": userInfo
    }
    url = f"{base_url}/api/v1/qiscus/room/{room_id}/user_info"
    headers = {
        'Authorization': "5Y3P3TiuAjJSVSJm8hH8",
        }
    
    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
    return response
from chalice import Chalice
from botocore.vendored import requests
import json

app = Chalice(app_name='CustomAgentAllocation')
app.debug = True

@app.route('/', methods=['POST'])
def index():
    event = app.current_request.json_body
    room = event['room_id']
    agent = event['candidate_agent']['id']
    return allocate(room,agent)

def allocate(room_id, agent_id):
    url = "https://qismo.qiscus.com/api/v1/admin/service/assign_agent"
    payload = {
            'room_id':room_id,
            'agent_id':int(agent_id)
        }
    headers = {
        'Authorization': "5Y3P3TiuAjJSVSJm8hH8",
        }
    
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)
    print(payload)
    return response.json()
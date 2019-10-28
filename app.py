from chalice import Chalice
import requests
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
            'agent_id':agent_id
        }
    headers = {
        'Authorization': "IBGXsgr0FMrr0ThbC6DE",
        }
    
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)
    return response.json()
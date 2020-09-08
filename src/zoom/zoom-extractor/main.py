from dotenv import load_dotenv
import os
import json
from zoomus import ZoomClient

load_dotenv()

client = ZoomClient(os.getenv('API_KEY'), os.getenv('API_SECRET'))

user_list_response = client.user.list()
user_list = json.loads(user_list_response.content)

print(user_list)

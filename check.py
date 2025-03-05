import os
from dotenv import load_dotenv
import requests

load_dotenv()

url = os.getenv("BASE_URL")[:-2] + "/user/credit"
headers = {
    "Content-Type": "application/json",
    "Authorization": os.getenv("AVALAI_API_KEY")
}
response = requests.get(url, headers=headers)
print(response.json())
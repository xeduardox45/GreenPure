import requests

def generate_request():
   	response = requests.get('http://127.0.0.1:8000/dato')
   	elementos = response.json()
   	return elementos
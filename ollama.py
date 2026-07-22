import requests
import json
public_url='https://perplexed-stack-revocable.ngrok-free.dev'
# Define the URL and headers
# Use the dynamically generated public_url from ngrok
url = f"{public_url}/api/generate"
headers = {
    "Content-Type": "application/json",
    "ngrok-skip-browser-warning": "true"  # Bypass ngrok's interstitial warning page
}

# Define the data (payload) to send in the POST request
data = {
    "model": "gemma4:latest",
    "prompt": "Who is sundar picchai?",
    "stream": False
}

# Send the POST request
try:
    response = requests.post(url, headers=headers, data=json.dumps(data))
    # Check if the request was successful and print the response
    if response.status_code == 200:
        print("Response:", response.json().get('response'))
    else:
        print(f"Failed to get a response. Status code: {response.status_code}")
        print("Body:", response.text)
except Exception as e:
    print(f"An error occurred: {e}")
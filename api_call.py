import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Base URL of your deployed API (update with your actual Render URL)
BASE_URL = "https://datareq.onrender.com/"

# Endpoint for financial summary
endpoint = "/health-summary"
url = BASE_URL + endpoint

# Headers with the API token (replace with your actual token)
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer mjSO8mdx4MVJ7kYip1Jok0_K8cnGLJ6s1rDYTyKbQfU"
}

# The data to summarize (replace with your actual financial data)
payload = {
    "data": "Job & Career: Satisfaction = 5, Importance = 8; Physical Health: Satisfaction = 6, Importance = 7; Mental Health: Satisfaction = 4, Importance = 9; Significant Other: Satisfaction = 7, Importance = 5; Family: Satisfaction = 8, Importance = 7; Friendship: Satisfaction = 6, Importance = 6; Community: Satisfaction = 5, Importance = 5; Spirituality & Faith: Satisfaction = 3, Importance = 7; Physiological Needs: Satisfaction = 9, Importance = 8; Finances: Satisfaction = 4, Importance = 10; Education & Learning: Satisfaction = 6, Importance = 6; Hobbies & Entertainment: Satisfaction = 5, Importance = 6"
}

# Make the POST request to your API endpoint
response = requests.post(url, json=payload, headers=headers, verify=False)

# Check the response
if response.status_code == 200:
    print("Summary:", response.json())
else:
    print("Error:", response.status_code, response.text)

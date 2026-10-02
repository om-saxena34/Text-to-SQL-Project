import requests 
response = requests.get("https://mail.google.com/mail/u/0/#inbox/FMfcgzQhWfXrQKZFXLlBCfBqPBmssTsz")

print(response.status_code)
print(response.json())
import requests 
from requests.auth import HTTPBasicAuth 
import time
# Making a get request 
c=0
for i in range(60):

    response = requests.get('https://IP:8080/', auth = HTTPBasicAuth('sammy', 'sammy'), verify=False) 
    time.sleep(1)
    if response.status_code == 200:
        c += 1
    
    print(f'the number of 200 response: {c}\n\n')

print(c)
#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import matplotlib.pyplot as plt
import pandas as pd


# In[ ]:


username = "dat.daouy2003@gmail.com"
password = "daodat2k3"

# Create a session to persistently store the headers
s = requests.Session()

# Save credentials into session
s.auth = (username, password)

# Send a POST request to the /authentication API
response = s.post('https://api.worldquantbrain.com/authentication')


# In[ ]:


from urllib.parse import urljoin
# Check status code for next action
if response.status_code == requests.status_codes.codes.unauthorized:
    if response.headers["WWW-Authenticate"] == "persona":
        # Outputs the URL to access through the browser to complete biometrics authenticationd
        input("Complete biometrics authentication and press any key to continue: " + urljoin(response.url, response.headers["Location"]))
        s.post(urljoin(response.url, response.headers["Location"]))
    else:
        print("incorrect email and password")    


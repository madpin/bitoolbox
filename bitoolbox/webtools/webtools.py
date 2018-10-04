# -*- coding: utf-8 -*-
import requests
import os

def download(url, fulllfile, overwrite=True):
    # open in binary mode
    if(not overwrite and os.path.isfile(fulllfile)):
        return 1
    with open(fulllfile, "wb") as file:
        # get request
        response = requests.get(url)
        # write to file
        file.write(response.content)
        return 0
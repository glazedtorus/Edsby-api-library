import sys
import os

class Edsby():
    def __init__(self, **kwargs):
       self.serverAddress = kwargs['host'] 
       
       if 'headers' in kwargs:
           self.headers = kwargs['headers']
       else:
           self.headers = { 
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36','referer' : 'https://' + self.serverAddress + '/',
                'accept': '*/*',
                'accept-language':'en-US,en',
                'dnt': '1',
                'x-requested-with':'XMLHttpRequest'
           }

       if 'meta' in kwargs:
           self.instanceMeta = kwargs['meta']  
       else:
           self.instanceMeta = self.parseInstanceMetadata()

       if 'session' in kwargs:
           self.session = kwargs['session'] 
       else:
           self.session = self.getSession() 
       if 'username' in kwargs & 'password' in kwargs:
        self.login(username = kwargs['username'], password = kwargs['password'])

    
class Error(Exception):
    pass

class LoginError(Error):
    def __init__(self, message):
        self.message = message
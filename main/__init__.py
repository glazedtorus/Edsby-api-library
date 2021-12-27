import sys

#for help use -h command line argument
if sys.argv[1]=="-h"or"-help"or"--h"or"--help":
    print("usage: <python __init__.py [-h]> or  <from__init__.py import Edsby>")
    print("optional args:")
    print("-h,--h,-help,--help : prints this help message")
    print("description: ")
    print("This is a python library to interact with the Edsby student database directly from Python to help build useful apps around it simpler, faster and easier.")
    print("notice: ")
    print("To pass the necessary parameters to the Edsby class(in this file), you can pass identifiers like your username, password, session id, and more (in dict format) as needed for your session.")

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
import sys
import json
import requests
from datetime import date

class Edsby():
    def __init__(self, **kwargs):
       self.edsbyHost = kwargs['host'] 
       
       if 'headers' in kwargs:
           self.headers = kwargs['headers']
       else:
           self.headers = { 
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',                    'referer' : 'https://' + self.edsbyHost + '/',
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
        self.login (username = kwargs['username'], password = kwargs['password'])
    
    def login(self, **kwargs):
        self.authData = self.getauthData((kwargs['username'], kwargs['password']))
        self.studentdata = self.sendAuthenticationData()
        return True
        
    def getauthData(self, logindata):
        self.authData = requests.get('https://'+self.edsbyHost+"/core/node.json/"+str(self.instanceMeta['nid'])+"?xds=fetchcryptdata&type=Plaintext-LeapLDAP",cookies=self.getCookies(),headers=self.getHeaders()).json()["slices"][0]
        return {
            '_formkey': self.authData["_formkey"],
            'sauthdata': self.authData['data']["sauthdata"],
            'crypttype': 'LeapLDAP',
            'login-userid' : logindata[0],
            'login-password' : logindata[1],
            'login-host' : self.edsbyHost,
            'remember' : 1
        }
    
    def sendauthenticaonData(self):
        studentData = requests.post('https://'+self.edsbyHost+'/core/login/'+str(self.instanceMeta['nid'])+'?xds=loginform&editable=true',data=self.authData,cookies=self.getCookies(),headers=self.getHeaders())
        cookies = {
            'session_id_edsby': dict(studentData.cookies)['session_id_edsby'],
            '__cfduid': dict(self.getCookies())['__cfduid'],
        }
        self.setCookies(cookies)
        studentData = studentData.json()
        if 'error' in studentData:
            raise LoginError(studentData['errorstr'])
        return {
          'unid': studentData['unid'],
          'compiled': studentData['compiled'],
          'nid': studentData['slices'][0]['nid'],
          'name': studentData['slices'][0]['data']['name'],
          'guid': studentData['slices'][0]['data']['guid'],
          'formkey': studentData['slices'][0]['data']['formkey']
        }

    def setHeaders(self, headers):
        self.headers = headers  

    def getHeaders(self):
        return self.headers
       
    def parseInstanceMetadata(self):
            rawPage = requests.get('https://'+self.edsbyHost,headers=self.getHeaders()).text
            meta = rawPage[rawPage.find('openSesame(')+12:] 
            meta = meta[:meta.find('}')].split(',') 

            metaTuples = list()
            for prop in meta: 
                key = prop[0:prop.find(":")].strip() 
                key = key.replace('"',"")
                value = prop[len(key)+3:].replace("'", "") 
                metaTuples.append((key, value)) 

            return dict(metaTuples)  

    def getinstanceMetadata(self):
        return self.instanceMeta

    def getSession(self):
        return requests.Session.get('https://' + self.edsbyHost + "/core/login"+str(self.instanceMeta['nid'])+"?xds=loginform&editable=true",headers=self.getHeaders())
    
class Error(Exception):
    pass

class LoginError(Error):
    def __init__(self, message):
        self.message = message
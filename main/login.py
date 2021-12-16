import requests
from requests.api import get
from __init__ import LoginError

def login(self, **kwargs):
    self.authdata = self.getauthdata((kwargs['username'], kwargs['password']))
    self.studentdata = self.sendauthenticationData()
    return True

def getauthdata(self, logindata):
    self.authdata = requests.get('https://' + self.edsbyhost + '.edsby.com/core/node.json/' + str(self.instanceMeta['nid']) + '?xds=fetchcryptdata&type=Plaintext-LeapLDAP', cookies=self.getCookies(), headers=self.getHeaders()).json()["slices"][0]
    return {
        '_formkey': self.authData["_formkey"],
        'sauthdata': self.authData['data']["sauthdata"],
        'crypttype': 'LeapLDAP',
        'login-userid' : logindata[0],
        'login-password' : logindata[1],
        'login-host' : self.edsbyHost,
        'remember' : 1
    }


def sendauthenticationData(self):
    studentData = requests.post('https://'+self.edsbyHost+'.edsby.com/core/login/'+str(self.instanceMeta['nid'])+'?xds=loginform&editable=true',data=self.authData,cookies=self.getCookies(),headers=self.getHeaders())
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
        rawPage = requests.get('https://'+self.edsbyHost+'.edsby.com',headers=self.getHeaders()).text
        meta = rawPage[rawPage.find('openSesame(')+12:] 
        if meta == -1:
            raise Exception("There was an error parsing the metadata")
        else:
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
    return requests.Session.get('https://' + self.edsbyHost + "edsby.com/core/login"+str(self.instanceMeta['nid'])+"?xds=loginform&editable=true",headers=self.getHeaders())

def endSession(self):
    self.session = self.getSession()

def clearData(self):
    self.authdata = None
    self.studentdata = None
    return True
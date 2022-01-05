import main.login as login
import requests

def getRawCurrentClassData(self):
    return requests.get('https://'+self.serverAddress+'/core/node.json/'+str(self.studentData['nid'])+'?xds=BaseStudentClasses&match=multi',cookies=self.getCookies(),headers=self.getHeaders()).json()['slices'][0]['data']['classesContainer']['classes']

def getCurrentClasses(self):
    rawCurrentClasses = self.getRawCurrentClassData()
    currentClasses = dict()
    for className in rawCurrentClasses:
        NID = rawCurrentClasses[className]['nid']
        humanName = rawCurrentClasses[className]['class']['details']['course']
        RID = rawCurrentClasses[className]['rid']
        courseCode = rawCurrentClasses[className]['class']['details']['info']['teachernid']

        currentClasses[NID] = dict()
        currentClasses[NID]['human_name'] = humanName
        currentClasses[NID]['rid'] = RID
        currentClasses[NID]['course_code'] = courseCode

        teacherName = rawCurrentClasses[className]['class']['details']['info']['param']
        teacherNID = rawCurrentClasses[className]['class']['details']['info']['teachernid']

        currentClasses[NID]['teacher'] = dict()
        currentClasses[NID]['teacher']['name'] = teacherName
        currentClasses[NID]['teacher']['nid'] = teacherNID

    return currentClasses

def getCurrentClassNIDList(self):
    classNIDs = list()
    for NID in self.getCurrentClasses():
        classNIDs.append(NID)
    return classNIDs

def getRawClassData(self):
    return requests.get('https://'+self.serverAddress+'/core/node.json/'+str(self.studentData['nid'])+'?xds=ClassPicker&match=multi',cookies=self.getCookies(),headers=self.getHeaders()).json()['slices'][0]['data']['classes']

def getAllClasses(self):
    rawClassData = requests.get('https://'+self.serverAddress+'/core/node.json/'+str(self.studentData['nid'])+'?xds=ClassPicker&match=multi',cookies=self.getCookies(),headers=self.getHeaders()).json()['slices'][0]['data']['classes']
    classDict = dict()
    for className in rawClassData:
        NID = rawClassData[className]['nid']
        humanName = rawClassData[className]['course']['class']['text']['line1']
        RID = rawClassData[className]['rid']
        courseCode = rawClassData[className]['course']['class']['text']['line2']['code']

        classDict[NID] = dict()
        classDict[NID]['human_name'] = humanName
        classDict[NID]['rid'] = RID
        classDict[NID]['course_code'] = courseCode

        classDict[NID]['teacher'] = dict()
        classDict[NID]['teacher']['name'] = rawClassData[className]['course']['class']['text']['line2']['name']
        classDict[NID]['teacher']['nid'] = None

    return classDict

def getClassIDList(self):
    return self.getAllClasses()

def getAllClassNIDList(self):
    classNIDs = list()
    for NID in self.getAllClasses():
        classNIDs.append(NID)
    return classNIDs

def getPastClasses(self):
    currentClasses = self.getCurrentClassNIDList()
    allClasses = self.getAllClasses()
    for classNID in list(allClasses):
        if classNID in currentClasses:
            del allClasses[classNID]
    return allClasses

def getAllClassAverages(self):
    classes = self.getAllClasses()
    for key in classes:
        classes[key]['average'] = self.getClassAverage(key)
    return classes

def getClassAssignmentMetadata(self, classNID):
    return requests.get('https://'+self.serverAddress+'/core/node.json/'+str(classNID)+'?xds=MyWork&student='+str(self.studentData['unid']),cookies=self.getCookies(),headers=self.getHeaders()).json()['slices'][0]['data']['loaddata']['gradebook']['terms']

def getClassAssignmentScores(self, classNID, classRID):
    return requests.get('https://'+self.serverAddress+'/core/node.json/'+str(classNID)+'/'+str(classRID)+'/'+str(classNID)+'?xds=MyWorkAssessmentPane&unit=all&student='+str(self.studentData['unid'])+'&model=24605449',cookies=self.getCookies(),headers=self.getHeaders()).json()["slices"][0]["data"]['grades']

def getMixedFormatClassAssignmentScores(self, classNID, classRID):
    return requests.get('https://'+self.serverAddress+'/core/node.json/'+str(classNID)+'/'+str(classRID)+'/'+str(classNID)+'?xds=MyWorkChart&student='+str(self.studentData['unid']),cookies=self.getCookies(),headers=self.getHeaders()).json()['slices'][0]['data']['loaddata']['grades']

def getClassPublishedAssignments(self, classNID, classRID):
    return requests.get('https://'+self.serverAddress+'/core/node.json/'+str(classNID)+'/'+str(classRID)+'/'+str(classNID)+'?xds=MyWorkChart&student='+str(self.studentData['unid']),cookies=self.getCookies(),headers=self.getHeaders()).json()['slices'][0]['data']['bubbles']['publishedAssessments'].split(',')

def getHumanReadableAssignmentSummary(self, classNID, classRID):
    assignments = self.getClassAssignmentList(classNID, classRID)
    humanList = dict()
    for key in assignments['assignments']:
        if 'scorePercentage' in assignments['assignments'][key]:
            humanList[assignments['assignments'][key]['name']] = assignments['assignments'][key]['scorePercentage']
        else:
            humanList[assignments['assignments'][key]['name']] = assignments['assignments'][key]['score'].upper()
    return humanList

def getRawClassAttendanceRecords(self, classID):
    return requests.get('https://'+self.serverAddress+'/core/node.json/'+str(classID)+'?xds=MyWorkChart&student='+str(self.studentData['unid']),cookies=self.getCookies(),headers=self.getHeaders()).json()['slices'][0]['data']['chartContainer']['chart']['attendanceRecords']['data']['right']['records']['incident']

def getClassmates(self, classNID):
    classMates = requests.get('https://'+self.serverAddress+'/core/node.json/'+str(classNID)+'?xds=ClassStudentList',cookies=self.getCookies(),headers=self.getHeaders()).json()
    if 'slices' in classMates: 
        if 'places' in classMates['slices'][0]['data'] and 'item' in classMates['slices'][0]['data']['places']:
            return classMates['slices'][0]['data']['places']['item']
    else:
        return ''

def getClassFeed(self, classNID):
    feed = requests.get('https://'+self.serverAddress+'/core/node.json/'+str(classNID)+'?xds=CourseFeed',cookies=self.getCookies(),headers=self.getHeaders()).json()['slices'][0]['data']
    return feed if 'item' in feed else ''

def getClassCalendar(self, classNID):
    return requests.get('https://'+self.serverAddress+'/core/node.json/'+str(classNID)+'?xds=CalendarPanel_Class',cookies=self.getCookies(),headers=self.getHeaders()).json()['slices'][0]['data']

def getStudentNotifications(self):
    return requests.get('https://'+self.serverAddress+'/core/node.json/'+str(self.studentData['unid'])+'?xds=notifications',cookies=self.getCookies(),headers=self.getHeaders()).json()['slices'][0]['data']

def getCalendarDueAssignments(self):
    return self.getCalendarData()['due']

def getCalendarOverdueAssignments(self):
    return self.getCalendarData()['overdue']

def getCalendarEvents(self):
    calendar = self.getCalendarData()
    for key in list(calendar['common']):
        if str(key + '.0') in list(calendar['events']):
            calendar['common'][str(key)] = calendar['events'][str(key + '.0')]
    return calendar['common']

def getCalendarSchedules(self):
    return self.getCalendarData()['schedules']

def getDMs(self):
    return requests.get('https://'+self.serverAddress+'/core/node.json/'+str(self.studentData['unid'])+'?xds=Messages&_context=1',cookies=self.getCookies(),headers=self.getHeaders()).json()["slices"][0]["data"]["body"]["left"]["items"]["item"]

def sendDM(self, message):
    Body = {
        '_formkey':self.studentData['formkey'],
        'form-composeBody': str(message['text']),
        'form-media-fill-addresources-integrations-integrationfiledata': message['filedata'],
        'form-media-fill-addresources-integrations-integrationfiles': message['files'],
        'nodetype': message['nodetype'],
    }

    return requests.post('https://'+self.serverAddress+'/core/create/'+str(message['to'])+'?xds=MessagesCompose&permaLinkKey=false&scopeState=true&_processed=true',data=Body,cookies=self.getCookies(),headers=self.getHeaders()).json() 
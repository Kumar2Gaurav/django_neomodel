import requests
import json

from EventEngine.models import *
from ActionEngine.models import *
from datetime import datetime, timedelta

class ServiceDeskimpl():
    # data = None
    # def __init__(self,data=none):
    #     self.data=data


    def getIncidentDetails(self,type):
        try:
            querySet = serviceNowInfo.objects.filter(name=type)
            if querySet:
                return querySet[0]
            else: return {"Status": False, "msg": "unable to fetch querySet"}
        except Exception as e:
            return {"Status": False, "msg": e}

    def execute_request_post(self,url,dic):
        try:
            r = requests.post(url,params=dic)
            return r
        except Exception as e:
            return {"Status": False, "msg": e}

    def map_attribute(self,subj,desc,ci,state):
        try:
            type=OutputType.objects.get(code='MNG')
            allkey=UserConfig.objects.filter(output_ass=type)
            map_dic = {
                "subject": subj,
                "description": desc,
                "category": None,
                "subcategory": None,
                "technician": "technician",
                "status": "Open",
                "priority": None,
                "requestType": "Incident",
                "ASSET": ci

            }

            for item in allkey:
                if state == "CRITICAL" and item.key == "PRIORITY_CRITICAL":
                    map_dic['priority'] = item.value
                elif state == "MAJOR" and item.key == "PRIORITY_MAJOR":
                    map_dic['priority'] = item.value
                elif item.key == "CATAGORY":
                    map_dic['category'] = item.value
                elif item.key=="SUBCATEGORY":
                    map_dic['subcategory'] = item.value



            in_dic = {"operation": {
                "details": map_dic
            }}
            return in_dic

        except Exception as e:
            return {"Status": False, "msg": e}

    def map_attribute_for_update(self,subj,desc,ci, state):
        try:
            map_dic = {
                    "category": "Network",
                    "priority":"High",
                    "requestType":"High",
            }
            if subj:
                map_dic["subject"] = subj
            if desc:
                map_dic["description"] = desc
            if ci:
                map_dic["ASSET"] = ci
            if state:
                map_dic["status"] = state
            in_dic = {"operation": {
                "details": map_dic
            }}
            return in_dic

        except Exception as e:
            return {"Status": False, "msg": e}


    def map_attribute_for_resoultion(self,desc):
        try:
            map_dic =  {
                            "resolutiontext": desc
                        }
            in_dic = {
                "operation": {
                    "details": {
                        "resolution": map_dic
                    }
                }
            }

            return in_dic
        except Exception as e:
            return {"Status": False, "msg": e}

    def map_attribute_for_worklog(self,desc):
        try:
            date = datetime.now()
            strtDate = date.strftime('%d %b %Y, %H:%M:%S')
            endDate = datetime.now() + timedelta(hours=9)
            endDate = endDate.strftime('%d %b %Y, %H:%M:%S')
            in_dic = {
                "operation": {
                    "details": {
                        "worklogs": {
                            "worklog": {
                                "description": desc,
                                "starttime": strtDate,
                                "endtime": endDate,
                            }
                        }
                    }
                }
            }

            return in_dic
        except Exception as e:
            return {"Status": False, "msg": e}

    def getSDinfo(self,ticketno):
        try:
            incidentDetails = OutputConfig.objects.get(host="172.16.10.56")
            incidentUrl = UserConfig.objects.get(key="mngincident")
            url = "http://" + incidentDetails.host + ":" + str(incidentDetails.port) + incidentUrl.value+"/"+str(ticketno)
            dic = {"OPERATION_NAME":"GET_REQUEST","TECHNICIAN_KEY": incidentDetails.techKey, "format": "json",}
            result = self.execute_request_post(url, dic)
            if result.status_code == requests.codes.ok:
                json_data = json.loads(result.text)
                if 'operation' not in json_data:
                    ts_resolve = int(json_data['RESOLVEDTIME'])/1000
                    resolvedate = datetime.utcfromtimestamp(ts_resolve).strftime('%Y-%m-%d %H:%M:%S')
                    ts_duebytime = int(json_data['DUEBYTIME']) / 1000
                    duebytime = datetime.utcfromtimestamp(ts_duebytime).strftime('%Y-%m-%d %H:%M:%S')
                    return {"Status": False,
                            "incident_no": json_data['WORKORDERID'],
                            "incident_subject": json_data['SUBJECT'],
                            "incident_status": json_data['STATUS'],
                            "incident_desc": json_data['DESCRIPTION'],
                            "incident_category": json_data['CATEGORY'],
                            "incident_priority": json_data['PRIORITY'],
                            "incident_requestType": json_data['REQUESTTYPE'],
                            "incident_asset": json_data['ASSET'],
                            "incident_sla": json_data['SLA'],
                            "incident_technician": json_data['TECHNICIAN'],
                            "incident_resolvedate": resolvedate,
                            "incident_duebytime": duebytime,
                            "incident_responseduebytime": json_data['RESPONSEDUEBYTIME'],
                            }
                return  {"Status": False, "msg": "operation not in json_data"}
            else:
                print(result.text)
                return {"Status": False, "msg": "status_code is false"}
        except Exception as e:
            return {"Status": False, "msg": e}


    def _createIncident(self,sub,ci,desc,state):
        try:
            incidentDetails=OutputConfig.objects.get(outType__code="MNG")
            incidentUrl= UserConfig.objects.get(key="mngincident")
            url = "http://"+incidentDetails.host+":"+str(incidentDetails.port)+incidentUrl.value
            in_dic = self.map_attribute(sub,desc,ci,state)
            techkey = incidentDetails.techKey
            dic = {"OPERATION_NAME": "ADD_REQUEST", "TECHNICIAN_KEY": techkey
                , "format": "json", "INPUT_DATA": json.dumps(in_dic)}
            result = self.execute_request_post(url, dic)
            if result.status_code == requests.codes.ok:
                json_data = json.loads(result.text)
                print(json_data)
                resut_obj = json_data['operation']['Details']
                return {"Status":True,"data":resut_obj}
            else:
                return {"Status": False, "msg": "status_code is false"}
        except Exception as e:
            return {"Status": False, "msg": e}

    def _updateIncident(self,sub,ci,desc, state, ticketNo):
        #incidentDetails = getIncidentDetails(CONFIG.ServiceDesk)
        incidentDetails = OutputConfig.objects.get(host="172.16.10.56")
        incidentUrl = UserConfig.objects.get(key="mngincident")
        try:
            #url = incidentDetails.host_url+incidentUrl.value+"/"+ str(ticketNo)
            url = "http://" + incidentDetails.host + ":" + str(incidentDetails.port) + incidentUrl.value+"/"+ str(ticketNo)
            in_dic = self.map_attribute_for_update(sub,desc,ci, state)
            techkey = incidentDetails.techKey
            dic = {"OPERATION_NAME": "EDIT_REQUEST", "TECHNICIAN_KEY": techkey
                , "format": "json", "INPUT_DATA": json.dumps(in_dic)}
            result = self.execute_request_post(url, dic)
            if result.status_code == requests.codes.ok:
                json_data = json.loads(result.text)
                incident_no = json_data['operation']['Details']['WORKORDERID']
                incident_subject = json_data['operation']['Details']['SUBJECT']
                incident_status = json_data['operation']['Details']['STATUS']
                return incident_no,incident_subject,incident_status
            else:
                return {"Status": False, "msg": "status_code is false"}
        except Exception as e:
            return {"Status": False, "msg": e}

    def _AddToResolution(self,desc, workorderId):
        #incidentDetails = getIncidentDetails(CONFIG.ServiceDesk)
        incidentDetails = OutputConfig.objects.get(host="172.16.10.56")
        incidentUrl = UserConfig.objects.get(key="mngincident")
        try:
            url = "http://" + incidentDetails.host + ":" + str(incidentDetails.port) + incidentUrl.value+"/"+ str(workorderId)+"/resolution"
            in_dic = self.map_attribute_for_resoultion(desc)
            techkey = incidentDetails.techKey
            dic = {"OPERATION_NAME": "ADD_RESOLUTION", "TECHNICIAN_KEY": techkey
                , "format": "json", "INPUT_DATA": json.dumps(in_dic)}
            result = self.execute_request_post(url, dic)
            if result.status_code == requests.codes.ok:
                json_data = json.loads(result.text)
                if 'status' in json_data['operation']['result']:
                    success = json_data['operation']['result']['status']
                    return success
                else:
                    return {"Status": False, "msg": "status not in json_data"}
            else:
                return {"Status": False, "msg": "status_code is false"}
        except Exception as e:
            return {"Status": False, "msg": e}


    def _AddWorklog(self,desc, ticketNo):
        incidentDetails = OutputConfig.objects.get(host="172.16.10.56")
        incidentUrl = UserConfig.objects.get(key="mngincident")
        try:
            url="http://" + incidentDetails.host + ":" + str(incidentDetails.port) + incidentUrl.value+"/"+ str(ticketNo)+"/worklogs"
            #url = incidentDetails.host_url+incidentUrl.value+"/"+ str(ticketNo)+"/worklogs"
            in_dic = self.map_attribute_for_worklog(desc)
            techkey = incidentDetails.techKey
            dic = {"OPERATION_NAME": "ADD_WORKLOG", "TECHNICIAN_KEY": techkey
                , "format": "json", "INPUT_DATA": json.dumps(in_dic)}
            result = self.execute_request_post(url, dic)
            if result.status_code == requests.codes.ok:
                json_data = json.loads(result.text)
                if 'status' in json_data['operation']['result']:
                    success = json_data['operation']['result']['status']
                    return success
                else:
                    return  {"Status": False, "msg": "status not in json_data"}
            else:
                return {"Status": False, "msg": "status_code is false"}
        except Exception as e:
            return {"Status": False, "msg": e}


    def _AllWorklogs(self,ticketNo):
        #incidentDetails = getIncidentDetails(CONFIG.ServiceDesk)
        incidentDetails = OutputConfig.objects.get(host="172.16.10.56")
        incidentUrl = UserConfig.objects.get(key="mngincident")
        try:
            url="http://" + incidentDetails.host + ":" + str(incidentDetails.port) + incidentUrl.value+"/"+ str(ticketNo)+"/worklogs"
            #url = incidentDetails.host_url+incidentUrl.value+"/"+ str(ticketNo)+"/worklogs"
            # in_dic = map_attribute_for_worklog()
            techkey = incidentDetails.techKey
            dic = {"OPERATION_NAME": "GET_WORKLOGS", "TECHNICIAN_KEY": techkey
                , "format": "json"}
            result = self.execute_request_post(url, dic)
            if result.status_code == requests.codes.ok:
                json_data = json.loads(result.text)
                if 'status' in json_data['operation']['result']:
                    success = json_data['operation']['result']['status']
                    data = json_data['operation']['Details']
                    return data
                else:
                    return {"Status": False, "msg": "status not in json_data"}
            else:
                return  {"Status": False, "msg": "status code false"}

        except Exception as e:
            return {"Status": False, "msg": e}




    def GetIncident(self,data):
        try:
            ticketno = data['workorder_id']
            querySetIncidentInfo = manageEngineInfo.objects.get(ticketNo=ticketno)
            resultDic = self.getSDinfo(ticketno)
            if resultDic:
                querySetIncidentInfo.ticketState = resultDic["incident_status"]
                querySetIncidentInfo.subject = resultDic["incident_subject"]
                querySetIncidentInfo.desc = resultDic["incident_desc"]
                querySetIncidentInfo.save()
                return {"Status": True, "data": resultDic}
            return {"Status": False, "msg": "Not able to Get incident in Service Desk"}
        except manageEngineInfo.DoesNotExist:
            return {"Status": False, "msg": "Incident Info does't exsist in DB"}
        except:
            return {"Status": False, "msg": "Not able to Get Details from server."}

    def getallIncident(self,data):
        #import ipdb;ipdb.set_trace()
        try:
            allobj=manageEngineInfo.objects.all()
            objlist=[]
            for i in allobj:
                dic={}
                dic['ticketNo']=i.ticketNo
                dic['subject']=i.subject
                dic['status']=i.status
                dic['event']=i.event
                dic['createTime']=i.createTime
                objlist.append(dic)
            return {"Status": True, "data": objlist}

        except manageEngineInfo.DoesNotExist:
            return {"Status": False, "msg": "Incident Info does't exsist in DB"}
        except:
            return {"Status": False, "msg": "Not able to Get Details from server."}

    def CreateIncident(self,data):

        try:
            sub = data["subject"]
            ci = data["ci"]
            dec = data["description"]
            state = data["state"]
            event_id=data["event_id"]
            eventObj = Events.objects.get(id=event_id)
            result = self._createIncident(sub,ci,dec,state)
            import ipdb;
            ipdb.set_trace()
            if result['Status'] == True:
                try:
                    datares = result['data']
                    incidentObj = manageEngineInfo(ticketNo=datares['WORKORDERID'],
                                                   ticketState=datares['STATUS'],
                                                   subject=datares['SUBJECT'],
                                                   desc=dec,
                                                   priority=datares['PRIORITY'],
                                                   technician=datares['TECHNICIAN'],
                                                   sla=datares['SLA'],
                                                   responseduebytime=datares['RESPONSEDUEBYTIME'],
                                                   event=eventObj)
                    incidentObj.save()

                    return {"Status":True,"incident_id":incidentObj.id, "WorkId": datares['WORKORDERID']}
                except manageEngineInfo.DoesNotExist:
                    return {"Status":False,"msg":"Not able to Create incident in Service Desk"}
                except Exception as e:
                    return {"Status": False, "msg": e}
            else:
                return {"Status":False,"msg":"Not able to create incident"}
        except Exception as e:
            return {"Status": False, "msg": e}


    def UpdateIncident(self,data):
        try:
            sub = data["subject"] if "subject" in data else None
            ci = data["ci"] if "ci" in data else None
            dec = data["description"] if "description" in data else None
            state = data["state"] if "state" in data else None
            ticketNo = data["workorderId"]
            result = self._updateIncident(sub,ci,dec, state, ticketNo)
            if result[0]:
                try:
                    incidentObj = manageEngineInfo.objects.filter(ticketNo=ticketNo)
                    incidentObj.update(subject=sub,ticketState= result[2], desc=dec)
                    return {"Status":True,"WorkId":result[0],'msg':"incident updated succesfully"}
                except:
                    return {"Status":False,"msg":"Not able to fetch incident from DB"}
            else:
                return {"Status":False,"msg":"Not able to update incident"}
        except Exception as e:
            return {"Status": False, "msg": e}

    def AddToResolution(self,data):
        try:
            desc = data["description"]
            ticketNo = data["workorderId"]
            result = self._AddToResolution(desc, ticketNo)
            if result[0]:
                return {"Status":True,"msg":"Success"}
            else:
                return {"Status":False,"msg":"Not able to add request in resolution state"}
        except Exception as e:
            return {"Status": False, "msg": e}

    def AddWorklog(self,data):
        try:
            desc = data["description"]
            ticketNo = data["workorderId"]
            result = self._AddWorklog(desc,  ticketNo)
            if result[0]:
                return {"Status": True, "msg": "Success"}
            else:
                return {"Status": False, "msg": "Not able to add request in resolution state"}
        except Exception as e:
            return {"Status": False, "msg": e}

    def AllWorklogs(self,data):
        try:
            ticketNo = data["workorderId"]
            result = self._AllWorklogs(ticketNo)
            if result:
                result_list = []
                for data in result:
                    ts_start = int(data['startTime']) / 1000
                    starttime = datetime.utcfromtimestamp(ts_start).strftime('%Y-%m-%d %H:%M:%S')
                    ts_end = int(data['endTime']) / 1000
                    endtime = datetime.utcfromtimestamp(ts_end).strftime('%Y-%m-%d %H:%M:%S')
                    result_dic = {
                        "starttime": starttime,
                        "endtime": endtime,
                        "description": data['description'],
                        "technician": data['technician'],
                        "cost": data['cost'],
                        "workHours": data['workHours'],
                        "workMinutes": data['workMinutes'],
                        "otherCharge": data['otherCharge']
                    }
                    result_list.append(result_dic)
                return {"Status": True, "msg": "Success", "data": result_list}
            else:
                return {"Status": False, "msg": "Not able to add request in resolution state"}
        except Exception as e:
            return {"Status": False, "msg": e}

# ================================== service desk ==================================================== #
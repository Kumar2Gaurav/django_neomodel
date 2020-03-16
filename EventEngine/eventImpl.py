from django.conf import settings
from Hosts.models import Hosts
from django.db.models import Count
from EventEngine import CONFIG
from EventEngine.models import (
    InputSourceType,
    InputSource,
    Events)

from ActionEngine.models import (
    mailInfo,
    manageEngineInfo,
    serviceNowInfo,OutputType
)

class EventInfo():
    data = None

    def __init__(self, data):
        self.data = data

    def eventTableField(self,eventlist, res):
        try:
            headers  = ['code', 'Event Id', 'Host', 'Service/Interface','Event State',
                        'Message', 'Parent', 'Children',
                        'NMS', 'Event Time']
            eventresList = []
            count = 0
            for item in eventlist:
                dic = {}
                dic['code'] = item.id
                dic['Event Id'] = "CATS-" + str(item.id)
                dic['Host'] = item.ci.name if item.ci else ""
                dic['Service/Interface'] = item.interface

                dic['Event State'] = item.state
                dic['Message'] = item.description

                dic['Parent'] = item.parent
                dic['Children'] = item.count

                dic['NMS'] = item.alertSource.name if item.alertSource else ""
                dic['NMS Id'] = item.alertSource.id if item.alertSource else ""

                dic['Event Time'] = str(item.eventTime).split(".")[0]
                eventresList.append(dic)

            res['headers'] = headers
            res['count'] = count
            res['data'] = eventresList
            return res
        except Exception as e:
            return {"Status":False,"msg":e}

    def getChildEvent(self):
        try:
            #import ipdb;ipdb.set_trace()
            eventId = self.data['eventId']
            eventlist = Events.objects.filter(parent=eventId).order_by('-id')

            res = {"headers": None,
                   "data": None}

            result = self.eventTableField(eventlist, res)
            return {"Status": True, "data": result}
        except Exception as e:
            return {"Status": False, "msg": str(e)}

    def getAllEvents(self):
        try:
            page = self.data.get('page', 1)
            state = self.data.get("state", None)
            hostId = self.data.get("hostId", None)
            hostType = self.data.get("hostType", None)
            nmsId = self.data.get("nmsId", None)

            firstLimt = settings.PER_PAGE_DATA_PAGINATION * (int(page) - 1) + 0
            secondLimt = settings.PER_PAGE_DATA_PAGINATION * int(page)
            # import ipdb;ipdb.set_trace()
            eventlist = Events.objects.filter(parent=0)
            count = eventlist.count()
            if state:
                eventlist =eventlist.filter(state=state)
                count = eventlist.count()
            if hostId:
                eventlist =eventlist.filter(ci__id=hostId)
                count = eventlist.count()
            if hostType:
                eventlist =eventlist.filter(ci__hostType=hostType)
                count = eventlist.count()
            if nmsId:
                eventlist =eventlist.filter(alertSource__id=nmsId)
                count = eventlist.count()

            count_critical = eventlist.filter(state="CRITICAL").count()
            count_down = eventlist.filter(state="DOWN").count()
            count_warning = eventlist.filter(state="WARNING").count()

            eventlist = eventlist.order_by('-id')[firstLimt:secondLimt]

            total_pages = count / settings.PER_PAGE_DATA_PAGINATION
            total_pages = int(total_pages) if float(total_pages).is_integer() else int(total_pages) + 1

            res = {"headers": None,
                   "data": None,
                   "total_pages": total_pages,
                   "count_critical": count_critical,
                   "count_down": count_down,
                   "count_warning": count_warning}
            reslt = self.eventTableField(eventlist, res)
            result = {"Status": True, "data": reslt}
        except Exception as e:
            result = {"Status": False, "msg": str(e)}
        return result

    def getEventsWithCITypeCount(self):
        try:
            ciTypes = Hosts.objects.values('hostType').annotate(dcount=Count('hostType'))
            count = Events.objects.filter(parent=0).count()
            mainDict = []
            for ciType in ciTypes:
                resultDic = {}
                eventHostCounts = Events.objects.filter(parent=0, ci__hostType=ciType['hostType']).values(
                    'ci_id').annotate(dcount=Count('ci_id'))
                eventresList = []
                totalCount = 0
                for CiCounts in eventHostCounts:
                    ciObj = Hosts.objects.get(pk=CiCounts['ci_id'])
                    dic = {
                        'ci_id': ciObj.id,
                        'ci_name': ciObj.name,
                        'count': CiCounts['dcount']
                    }
                    eventresList.append(dic)
                    totalCount = totalCount + CiCounts['dcount']
                resultDic['device'] = ciType['hostType']
                resultDic['objList'] = eventresList
                resultDic['totalCount'] = totalCount
                mainDict.append(resultDic)
            result = {"Status": True, "count": count, "data": mainDict}
        except Events.DoesNotExist:
            result = {"Status": False, "msg": "Event Does not exists"}
        except Hosts.DoesNotExist:
            result = {"Status": False, "msg": "Host Does not exists"}
        except Exception as e:
            result = {"Status": False, "msg": str(e)}
        return result

    def getDailyEventsAndIncidentCountChart(self):
        try:
            eventList = Events.objects.extra(select={'day': 'date( "eventengine_Events"."createdTime" )'}).values('day') \
                .annotate(available=Count('createdTime'))
            # print (eventList.query)
            category = []
            event_count = []
            # incident_count = []
            result=[]
            for event in eventList:
                # incidentInfoObj = Hosts.objects.filter(created_at__contains=str(event["day"]))
                # incidentInfoCount = incidentInfoObj.count()
                # category.append({"label": str(event["day"])})
                # event_count.append({"value": event["available"]})
                result.append({"label": str(event["day"]),"value": str(event["available"])})
                # incident_count.append({"value": incidentInfoCount})


            result = {"Status": True, "data": result}
        except Exception as e:
            result = {"Status": False, "msg": str(e)}
        return result

    def getEventData(self):
        try:
            #need to update get latest result
            # event_id = int(self.data['event_id'])
            event_id = 168
            eventlist = Events.objects.filter(id=event_id)
            # event_id = int(self.data['event_id'])
            event_id = 168
            eventlist = Events.objects.filter(id=event_id)
            event_id = int(self.data['event_id'])
            event = Events.objects.get(pk=event_id)
            dic = {}
            result = {}
            manage_dic = {}
            servicenow_dic = {}
            mail_dic = {}

            dic['Event Id'] = "CATS-" + str(event.id)
            dic['State'] = event.state
            dic['Alarm Name'] = event.alarmName
            dic['Alarm Type'] = event.alarmType
            dic['Description'] = event.description
            dic['Host'] = event.ci.name if event.ci else ""
            dic['NMS'] = event.alertSource.name if event.alertSource else ""
            # dic['NMS Id'] = event.alertSource.id if event.alertSource else ""
            dic['Event Time'] = str(event.eventTime).split(".")[0]
            dic['Created Time'] = str(event.eventTime).split(".")[0]
            dic['Parent'] = event.parent
            dic['Children'] = event.count
            dic['Assigned'] = event.assigned
            dic['Service/Interface'] = event.interface

            manageEngineObj = manageEngineInfo.objects.filter(event__id=event_id)
            serviceNowObj = serviceNowInfo.objects.filter(event__id=event_id)
            mailObj = mailInfo.objects.filter(event__id=event_id)
            if manageEngineInfo:
                for data in manageEngineObj:
                    # manage_dic['id'] = data.id
                    manage_dic['Ticket No'] = data.ticketNo
                    manage_dic['Subject'] = data.subject
                    manage_dic['Ticket State'] = data.ticketState
                    # manage_dic['Status'] = data.status
                    manage_dic['Create Time'] = data.createTime
                    manage_dic['Description'] = data.desc
                    manage_dic['SLA'] = data.sla
                    manage_dic['Technician'] = data.technician
                    manage_dic['Resolve Date'] = data.resolvedate
                    manage_dic['Due By Time'] = data.duebytime
                    manage_dic['Response Due By Time'] = data.responseduebytime


            elif serviceNowObj:
                for data in serviceNowObj:
                    # servicenow_dic['id'] = data.id
                    servicenow_dic['Ticket No'] = data.ticketNo
                    servicenow_dic['Subject'] = data.subject
                    servicenow_dic['Ticket State'] = data.ticketState
                    servicenow_dic['Create Time'] = data.createTime

            elif mailObj:
                for data in mailObj:
                    # mail_dic['id'] = data.id
                    mail_dic['Send Date'] = data.sendDate
                    mail_dic['User Mail Id'] = data.userMailId
                    mail_dic['Ack Now'] = data.ackNow
                    mail_dic['Subject'] = data.subject

            result['event'] = dic
            result['manageengine_data'] = manage_dic
            result['servicenow_data'] = servicenow_dic
            result['mail_data'] = mail_dic
            typedic = {"manageengine_data":"",
                                       "servicenow_data":"",
                                       "mail_data":"",}

            outputtype = OutputType.objects.all()
            for out in outputtype:
                if out.code == CONFIG.MANAGEENGINE:
                    typedic['manageengine_data'] = out.code
                elif out.code == CONFIG.SERVICENOW:
                    typedic['servicenow_data'] = out.code
                elif out.code == CONFIG.EMAIL:
                    typedic['mail_data'] = out.code

            result['type_code'] = typedic
            return result

        except manageEngineInfo.DoesNotExist:
            result = {"Status": False, "msg": "Manage Engine value error "}

        except serviceNowInfo.DoesNotExist:
            result = {"Status": False, "msg": "Service Now value error"}

        except mailInfo.DoesNotExist:
            result = {"Status": False, "msg": "Mail info value error"}

        except Exception as e:
            return {"Status":False,"msg":e}




class InputSourceTypeInfo():
    data = None

    def __init__(self, data):
        self.data = data

    def getAllInputSourceType(self):
        try:
            iptSrcTypeSet = InputSourceType.objects.all()
            iptSrcTypeList = []
            for iptSrcType in iptSrcTypeSet:
                dic = {}
                dic['id'] = iptSrcType.id
                dic['name'] = iptSrcType.name
                dic['code'] = iptSrcType.code
                iptSrcTypeList.append(dic)
            result = {"Status": True, "data": iptSrcTypeList}
        except InputSourceType.DoesNotExist:
            result = {"Status": False, "msg": "Input source type does not exists."}
        except Exception as e:
            result = {"Status": False, "msg": str(e)}
        return result

    def createInputSourceType(self):
        try:
            iptSrcType = InputSourceType(name=self.data['name'], code=self.data['code'])
            iptSrcType.save()
            result = {"Status": True, "msg": "Input Source Type " + iptSrcType.name + " created successfully",
                      "id": iptSrcType.id}
        except Exception as e:
            result = {"Status": False, "msg": str(e)}
        return result

    def updateInputSourceType(self):
        try:
            iptSrcType_id = self.data['inputsourcetype_id']
            iptSrcTypeObj = InputSourceType.objects.get(pk=iptSrcType_id)
            if "name" in self.data:
                iptSrcTypeObj.name = self.data["name"]
            if "code" in self.data:
                iptSrcTypeObj.code = self.data["code"]
            iptSrcTypeObj.save()
            result = {"Status": True, "msg": "Input Source Type " + iptSrcTypeObj.name + " updated successfully"}
        except InputSourceType.DoesNotExist:
            result = {"Status": False, "msg": "Input Source Type " + self.data['name'] + " does not exists"}
        except Exception as e:
            result = {"Status": False, "msg": str(e)}
        return result

    def deleteInputSourceType(self):
        try:
            iptSrcType_id = self.data['inputsourcetype_id']
            iptSrcTypeObj = InputSourceType.objects.get(pk=iptSrcType_id)
            iptSrcType_name = iptSrcTypeObj.name
            iptSrcTypeObj.delete()
            result = {"Status": True, "msg": "Input Source Type " + iptSrcType_name + " deleted successfully"}
        except InputSourceType.DoesNotExist:
            result = {"Status": False, "msg": "Input Source Type Does not exists"}
        except Exception as e:
            result = {"Status": False, "msg": str(e)}
        return result


class InputSourceInfo():
    data = None

    def __init__(self, data):
        self.data = data

    def getAllInputSource(self):
        try:
            iptSrcSet = InputSource.objects.all()
            iptSrcList = []
            for iptSrc in iptSrcSet:
                dic = {}
                dic['id'] = iptSrc.id
                dic['name'] = iptSrc.name
                dic['description'] = iptSrc.description
                dic['serverIp'] = iptSrc.serverIp
                dic['iptSrcType_name'] = iptSrc.inputSourceType.name
                iptSrcList.append(dic)
            result = {"Status": True, "data": iptSrcList}
        except InputSourceType.DoesNotExist:
            result = {"Status": False, "msg": "Input source does not exist."}
        except Exception as e:
            result = {"Status": False, "msg": str(e)}
        return result

    def createInputSource(self):
        try:
            inputSourceTypeObj = InputSourceType.objects.get(pk=self.data['inputsourcetype_id'])
            inputSourceObj = InputSource(name=self.data['name'], inputSourceType=inputSourceTypeObj,
                                         description=self.data['description'], serverIp=self.data['serverIp'])
            inputSourceObj.save()
            result = {"Status": True, "msg": "Input Source " + inputSourceObj.name + " created successfully",
                      "id": inputSourceObj.id}
        except Exception as e:
            result = {"Status": False, "msg": str(e)}
        return result

    def updateInputSource(self):
        try:
            iptSrcObj = InputSource.objects.get(pk=self.data['inputsource_id'])
            inputSourceTypeObj = InputSourceType.objects.get(pk=self.data['inputsourcetype_id'])
            if "name" in self.data:
                iptSrcObj.name = self.data["name"]
            if "description" in self.data:
                iptSrcObj.description = self.data["description"]
            if "inputsourcetype_id" in self.data:
                iptSrcObj.inputSourceType = inputSourceTypeObj
            if "serverIp" in self.data:
                iptSrcObj.serverIp = self.data["serverIp"]
            iptSrcObj.save()
            result = {"Status": True, "msg": "Input Source " + iptSrcObj.name + " updated successfully"}
        except InputSource.DoesNotExist:
            result = {"Status": False, "msg": "Input Source " + self.data['name'] + " does not exist"}
        except InputSourceType.DoesNotExist:
            result = {"Status": False, "msg": "Input Source Type" + self.data['inputsourcetype_id'] + " does not exist"}
        except Exception as e:
            result = {"Status": False, "msg": str(e)}
        return result

    def deleteInputSource(self):
        try:
            iptSrc_id = self.data['inputsource_id']
            iptSrcObj = InputSource.objects.get(pk=iptSrc_id)
            iptSrc_name = iptSrcObj.name
            iptSrcObj.delete()
            result = {"Status": True, "msg": "Input Source " + iptSrc_name + " deleted successfully"}
        except InputSourceType.DoesNotExist:
            result = {"Status": False, "msg": "Input Source Does not exists"}
        except Exception as e:
            result = {"Status": False, "msg": str(e)}
        return result
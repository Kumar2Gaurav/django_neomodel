
from EventEngine.models import Events
from ActionEngine.sdimpl import ServiceDeskimpl
from RuleEngine.models import (
    HostRuleInfo,

)
from RuleEngine.models import (

    Action_rule_association
)
from ActionEngine.models import (

    manageEngineInfo,
    serviceNowInfo
)
from EventEngine import  CONFIG
from datetime import datetime, timedelta


class CommonUtil():

    def RuleOnEventCI(self, ci, state):
        try:
            ci_asslist = HostRuleInfo.objects.filter(host_name=ci.name).filter(rule__event_status__state=state)
            for ci_ass in ci_asslist:  # Need to change
                # if ci_ass.rule.event_status == state:
                return ci_ass.rule
            return None

        except HostRuleInfo.DoesNotExist:
            print("WARNING :: No Rule for " + ci.name)
            return None
        except:
            return None

    def isParentOpenforCI(self,ci,interface, state, alarm_name):
        isInterface,isAlarm,actionCodeList = self._checkInterfaceAlarm(ci,state)
        eventList = Events.objects.filter(ci=ci).filter(parent=0).filter(state=state)
        if isInterface and not isAlarm:
            eventList = eventList.filter(interface=interface)
        elif isAlarm and not isInterface:
            eventList = eventList.filter(alarmName=alarm_name)
        elif isInterface and isAlarm:
            eventList = eventList.filter(interface=interface).filter(alarmName=alarm_name)
        for event in eventList:
            # incident on sd is closed or not
            if self._checkIncidentState(event,actionCodeList):
                return event
        return None

    def executeRuleOnCi(self, rule, ci, interface_name, alarm_name, description, message,state):
        time = rule.rule_time
        count = rule.rule_count
        status = rule.event_status
        try:
            time_threshold = datetime.utcnow() - timedelta(minutes=time)
            isInterface,isAlarm,actionList = self._checkInterfaceAlarm(ci,state)

            eventList = Events.objects.filter(ci=ci).filter(parent=0).filter(state=status).filter(createdTime__gt=time_threshold)

            if isInterface and not isAlarm:
                eventList = eventList.filter(interface=interface_name)
            elif isAlarm and not isInterface:
                eventList = eventList.filter(alarmName=alarm_name)
            elif isInterface and isAlarm:
                eventList = eventList.filter(interface=interface_name).filter(alarmName=alarm_name)

            print("Total events : ",len(eventList))
            action = False
            if count <= len(eventList):
                for assc in actionList:
                    if assc == CONFIG.MANAGEENGINE:
                        state = state
                        incidentObj = ServiceDeskimpl()
                        dic = {"subject": description, "ci": ci.name,
                             "description": message,
                             "state":state, "event_id": eventList[0].id}
                        result = incidentObj.CreateIncident(dic)
                        action = True
                        print ("creation result ==", result)
                    elif assc.action.code == CONFIG.SERVICENOW:
                        ""
                    elif assc.action.code == CONFIG.EMAIL:
                        ""
                parentEvent = eventList[0]
                parentEvent.count = len(eventList)-1
                parentEvent.save()

                for event in eventList[1:]:
                    event.parent =  parentEvent.id
                    event.save()
                if action:
                    return {"Status":True,"msg":"Successfully logged event with rule and incident created successfully."}
                else:
                    return {"Status":True,"msg":"Successfully logged event with rule, but no action performed."}

            return {"Status":True,"msg":"Successfully logged event not eligible for rule count"}
        except Exception as e:
            return {"Status":False,"msg":e}

    def _checkInterfaceAlarm(self,ci,state):
        try:
            hostRuleObj = HostRuleInfo.objects.filter(host_name=ci.name).filter(rule__event_status__state=state)
            for hosRule in hostRuleObj:
                isInterface = hosRule.rule.isInterface
                isAlarm = hosRule.rule.isAlarmType
                actionassobjlist = Action_rule_association.objects.filter(rule=hosRule)
                actioncodeList = []
                for ass in actionassobjlist:
                    actioncodeList.append(ass.action.code)
                return isInterface,isAlarm,actioncodeList
            return None,None,None
        except HostRuleInfo.DoesNotExist:
            print("WARNING :: No Rule for " + ci.name)
            return None,None,None
        except Exception as e:
            print("ERROR "+str(e))
            return None,None,None

    def _updateMETicketInfo(self,actionObj,result):
        actionObj.ticketState = result['incident_status']
        actionObj.status = result['incident_status']
        actionObj.technician = result['incident_technician']
        actionObj.sla = result['incident_sla']
        actionObj.resolvedate = result['incident_resolvedate']
        actionObj.responseduebytime = result['incident_responseduebytime']
        actionObj.priority = result['incident_priority']
        actionObj.update()

    def _checkIncidentState(self, event,actionCodeList):
        if CONFIG.SERVICENOW in actionCodeList:
            try:
                eventExistSN = serviceNowInfo.objects.filter(event=event)
                #code to check with service now manager to incident state
                if eventExistSN:
                    if eventExistSN[0].status not in CONFIG.INCIDENT_STATE_DIC:
                        return event
                    return None
            except serviceNowInfo.DoesNotExist:
                return None
        elif CONFIG.MANAGEENGINE in actionCodeList:
            try:
                eventExistME = manageEngineInfo.objects.get(event=event)
                ticketno = eventExistME.ticketNo
                sdiml = ServiceDeskimpl()
                response = sdiml.getSDinfo(ticketno)
                if response["Status"]== True:
                    print("Service Desk status for ticket " + response['incident_status'])
                    if response['incident_status'] == eventExistME.status and \
                            response['incident_status'] not in CONFIG.INCIDENT_STATE_DIC_ME:
                        return event
                    elif response['incident_status'] != eventExistME.status and \
                            response['incident_status'] not in CONFIG.INCIDENT_STATE_DIC_ME:
                        self._updateMETicketInfo(eventExistME,response)
                        return event
                    else:
                        self._updateMETicketInfo(eventExistME,response)
                        return None
            except Exception as e:
                return None


        return None
from EventEngine.models import Events
from Hosts.models import Hosts
from EventEngine.commonEventUtil import CommonUtil
from EventEngine import  CONFIG

from EventEngine.models import InputSource

hour_data = 48


class NagionsProcessEvent():
    data = None
    util = None

    def __init__(self, data):
        self.data = data
        self.util = CommonUtil()

    def processlogEvent(self):
        event_type = self.data['type']
        server_ip = self.data['host']
        print(server_ip,event_type)
        try:
            server = InputSource.objects.filter(inputSourceType__code=event_type).filter(serverIp=server_ip)
            # print("server length ",len(server))
            if(len(server))==1:
                print(server[0].name)
                if event_type == CONFIG.NAGIOS_EVENT:  # Need to change of config
                    return self._processNagiosLog(server[0])
                else:
                    return {"Status": False, "msg": "UNKNOWN state"}
            else:
                return {"Status":False,"msg":"couldnot find server details from db"}
        except InputSource.DoesNotExist:
            return {"Status":False,"msg":"server config not available"}
        except Exception as e:
            return {"Status": False, "msg": str(e)}


    def _processNagiosLog(self,server):
        if self._iseventloggable():

            print("INFO: event is loggable")
            hostname = self.data['data']['CI_hostname']
            try:
                try:
                    ci = Hosts.objects.get(name = hostname)
                except:
                    try:
                        # inputTypeObj = InputSource.objects.get(inputSourceType__code=self.data['type'])
                        ciInfoObj = Hosts(name=hostname, ipAddress="", hostType="UNKNOWN", inputType=server)
                        ciInfoObj.save()
                        ci = Hosts.objects.get(name=self.data['data']['CI_hostname'])
                    except:
                        return {"Status": False, "msg": "Input source does not exist for make auto host"}
                    # self._associate_ci_rule(self.data['data']['CI_hostname'])

                interface_name = self.data['data']['CI_service']
                alarm_name = self.data['data']['CI_alert_name']
                alarm_type = self.data['data']['CI_alarm_type']
                state = self.data['data']['CI_state']
                eventTimeObj = self.data['data']['time_obj']
                incident_description = str(ci.name)+" : "+str(interface_name)+" : "+str(alarm_name) \
                    if interface_name.strip() else str(ci.name)+" : "+str(alarm_name)

                parent_event = self.util.isParentOpenforCI(ci,interface_name,state,alarm_name)

                if parent_event != None:
                    event = Events(description=self.data['data']['CI_message'], alertSource=server, ci=ci,
                                   eventTime=eventTimeObj, parent=parent_event.id, state =state,
                                   interface=interface_name, alarmName=alarm_name, alarmType=alarm_type)
                    event.save()

                    parent_event.count = parent_event.count+1
                    parent_event.save()

                    return {"Status":True,"msg":"event is logged under event "+str(parent_event.id)}
                else:
                    event = Events(description=self.data['data']['CI_message'], alertSource=server, ci=ci,
                                   eventTime=eventTimeObj, state=state,
                                   interface=interface_name, alarmName=alarm_name,
                                   alarmType=alarm_type)
                    event.save()
                    rule = self.util.RuleOnEventCI(ci, state)
                    if rule != None:
                        return self.util.executeRuleOnCi(rule,ci,interface_name,alarm_name, incident_description,
                                                     self.data['data']['CI_message'],self.data['data']['CI_state'])
                    else:
                        return {"Status": True, "msg": "event is logged without rule"}


            except Hosts.DoesNotExist:
                return {"Status":False,"msg":"CI Details not available "+self.data['data']['CI_hostname']}


    def _iseventloggable(self):
        if self.data['data']['CI_state'] in CONFIG.LOGGABLE:
            return True
        return False
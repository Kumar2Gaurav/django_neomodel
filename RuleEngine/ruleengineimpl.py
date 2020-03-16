from RuleEngine.models import (Rule,
                        HostRuleInfo,
                        Action,
                        Action_rule_association,
                               RuleState)
from Hosts.models import Hosts
from datetime import datetime


class Rules():

    data=None

    def __init__(self,data=None):
        self.data=data

    def str_to_bool(self,s):
        if s == 'True':
            return True
        elif s == 'False':
            return False

    def create_rule(self):
        try:
            timestmp=self.data['creation_time']
            time=str(datetime.fromtimestamp((int(timestmp))/1000))
            # time=time.strftime('%m/%d/%Y %H:%M')
            rule_state=RuleState.objects.get(pk=self.data['state_id'])
            rule = Rule(rule_name= self.data['rule_name'],rule_time = int(self.data['rule_time']),
                        rule_count=int(self.data['rule_count']),
                        event_status = rule_state,created_time=time,created_by = self.data['user_name'],
                        isInterface=self.data['isInterface'],isAlarmType=self.data['isAlarmType'])
            rule.save()
            return {"Status":True,"msg":"Rule "+rule.rule_name+" created successfully"}
        except RuleState.DOESNOTEXIST:
            return {"Status": False,"msg":"RuleState Doesn't exist"}
        except Exception as ae:
            return {"Status": False, "msg": ae}


    def update_rule(self):
        
        # ipdb.set_trace()

        rule_id = self.data['rule_id']
        timestmp = self.data['creation_time']
        time = str(datetime.fromtimestamp((int(timestmp))/1000))
        try:
            rule = Rule.objects.get(pk=int(rule_id))
            rule_state = RuleState.objects.get(pk=self.data['state_id'])
            rule.rule_name = self.data['rule_name']
            rule.rule_time = int(self.data['rule_time'])
            rule.rule_count = int(self.data['rule_count'])
            rule.created_time=time
            rule.created_by = self.data['user_name']
            rule.isInterface=self.data['isInterface']
            rule.isAlarmType=self.data['isAlarmType']
            rule.event_status=rule_state
            rule.save()
            return {"Status":True,"msg":"Rule updated successfully"}
        except Rule.DoesNotExist:
            return {"Status": False, "msg": "Rule  does not exsist"}
        except RuleState.DoesNotExist:
            return {"Status": False, "msg": "RuleState  does not exsist"}
        except Exception as ae:
            return {"Status": False, "msg": str(ae)}

    def delete_rule(self):
        rule_id = self.data['rule_id']
        try:
            # import ipdb;ipdb.set_trace()
            rule = Rule.objects.get(pk=int(rule_id))
            rule_name = rule.rule_name
            # Ci_rule_info.objects.filter(rule=rule).delete()
            rule.delete()
            return {"Status": True, "msg": "Rule " + rule_name + " deleted successfully"}
        except Rule.DoesNotExist:
            return {"Status": False, "msg": "Rule Does not exsists"}
        except Exception as ae:
            return {"Status": False, "msg": "Delete operation failed "+str(ae)}


    def getall_rules(self):
        try:
            
            rule_list = Rule.objects.all()
            rule_list_res = []
            for rule in rule_list:
                # state = RuleState.objects.get(pk=self.data['state_id'])
                dic ={}
                dic['rule_id'] = rule.id
                dic['rule_name']= rule.rule_name
                dic['rule_time'] = rule.rule_time
                dic['rule_count'] = rule.rule_count
                dic['creation_time']=(rule.created_time).strftime('%m/%d/%Y %H:%M')
                dic['user_name'] = rule.created_by
                dic['isInterface']=rule.isInterface
                dic['isAlarmType']=rule.isAlarmType
                dic['event_status'] = rule.event_status.state
                rule_list_res.append(dic)
            return {"Status": True, 'Rule_list':rule_list_res}
        except Exception as ae:
            return {"Status": False, "msg": str(ae)+" get all rules operation failed"}


    def get_rule_details(self):
        try:
            # import ipdb;ipdb.set_trace()
            rule = Rule.objects.get(pk=int(self.data))
            dic = {}
            dic['rule_id'] = rule.id
            dic['rule_name'] = rule.rule_name
            dic['rule_time'] = rule.rule_time
            dic['rule_count'] = rule.rule_count
            dic['creation_time'] = (rule.created_time).strftime('%m/%d/%Y %H:%M')
            dic['user_name'] = rule.created_by
            dic['isInterface'] = rule.isInterface
            dic['isAlarmType'] = rule.isAlarmType
            dic['event_status']=rule.event_status
            return {"Status":True,"rule_details":dic}
        except Rule.DoesNotExist:
            return {"Status": False, "msg": "Rule does not exsist"}
        except Exception as ae:
            return {"status":False,"msg":ae}


    def associate_host_rule(self):
        try:
            rule_id = self.data['rule_id']
            host_ids = eval(self.data['host_id'])
            desc = self.data['desc']
            rule = Rule.objects.get(pk=rule_id)
            status = rule.event_status
            for host_id in host_ids:
                host=Hosts.objects.get(pk=host_id)
                host_name=host.name
                try:
                    host_rule_ass = HostRuleInfo.objects.get(host_name=host_name)
                    host_rule_ass.rule=rule
                    host_rule_ass.save()
                except HostRuleInfo.DoesNotExist:
                    host=HostRuleInfo(host_name=host_name,desc=desc,rule=rule)
                    host.save()
            return {"status": True,
                    "msg": "Created new association rule with Rule " + rule.rule_name + " for host " + host_name}
        except Hosts.DoesNotExist:
            return {"status": False, "msg": "Not able to retrive Host Details"}
        except Rule.DoesNotExist:
            return {"status": False, "msg": "Not able to retrive Rule Details"}
        except Exception as ae:
            return {"status": False, "msg": str(ae)+" Not able to Create association"}


    def get_host_rule(self):
        # import ipdb;ipdb.set_trace()
        try:
            host_ass_list = HostRuleInfo.objects.all()
            host_ass_list_res = []
            for host_ass in host_ass_list:
                dic ={}
                dic['assc_id']=host_ass.id
                dic['rule_id'] = host_ass.rule.id
                dic['rule_name'] = host_ass.rule.rule_name
                dic['desc'] = host_ass.desc
                dic['host_name'] = host_ass.host_name

                host_ass_list_res.append(dic)
            return {"Status":True,"list":host_ass_list_res}
        except :
            return {"Status": False, "msg": "Not Able to fetch information"}


    def delete_association(self):
        assc_id = self.data['assc_id']
        try:
            assc = HostRuleInfo.objects.get(pk=assc_id)
            assc_name = assc.host_name
            assc.delete()
            return {"Status": "Sucess", "msg": "Association " + assc_name + " deleted successfully"}
        except HostRuleInfo.DoesNotExist:
            return {"Status": "Failed", "msg": "Association Does not exists"}
        except Exception as ae:
            return {"Status": "Failed", "msg": str(ae)+" Delete operation failed"}

    def get_status(self):
        try:
            states=RuleState.objects.all()
            list=[]
            for x in states:
                dic={}
                dic['id']=x.id
                dic['name']=x.state
                list.append(dic)
            return {"Status": "True", "msg":list}
        except Exception as ae:
            return {"Status": "False", "msg": "can not get status details"}

    def associate_action(self):
        try:
            ruleaction=Action_rule_association.objects.all()
            list=[]
            for ruleactions in ruleaction:
                    dic={}
                    dic["id"]=ruleactions.id
                    dic["rule_id"]=ruleactions.rule.id
                    dic["action_id"]=ruleactions.action.id
                    dic['rule']=ruleactions.rule.rule_name
                    dic['action']=ruleactions.action.name
                    list.append(dic)
            return {"status": True,"data":list}
        except Action_rule_association.DoesNotExist:
            return {"status": False, "msg": "Rule doesnot exist"}
        except Exception as ae:
            return {"status":False,"msg":"can't associate action"+str(ae)}

    def delete_action(self):
        try:
            #import ipdb;ipdb.set_trace()
            print(self.data["id"])
            action_delete= Action_rule_association.objects.filter(id=int(self.data["id"])).delete()
            return {"status": True, "msg":"Rule and action successfully deleted",  }

        except Action_rule_association.DoesNotExist:
            return {"status": False, "msg": "Action doesnot exist"}
        except Exception as ae:
            return {"status":False,"msg":"can't associate action"+str(ae)}


    def create_action(self):
        try:
            ruleobj=Rule.objects.get(id=self.data['rule_id'])
            id=eval(self.data["action_id"])
            print(id)
            desc= self.data["desc"]
            #import ipdb;ipdb.set_trace()
            flag = False
            for i in id:
                actionobj = Action.objects.get(id=i)
                obj = Action_rule_association.objects.filter(rule=ruleobj, action=actionobj)
                if obj :
                    continue
                else:
                  flag =True
                  obj = Action_rule_association(rule=ruleobj, action=actionobj)
                  obj.save()

            if flag : return {"status": True, "msg": "rule and action succusefully created"}
            else: return {"status": False, "msg": "not updated"}
        except Action_rule_association.DoesNotExist:
            return {"status": False, "msg": "Rule doesnot exist"}
        except Exception as ae:
            return {"status":False,"msg":"can't associate action"+str(ae)}



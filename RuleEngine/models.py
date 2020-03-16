from django.db import models
# from EventEngine.models import InputSourceType
from django.utils import timezone
from  ActionEngine.models import OutputConfig


class RuleState(models.Model):
    state = models.CharField(max_length=1024, blank=True, null=True)

    def __str__(self):
        return self.state

    class Meta:
        db_table = "Status"


class Rule(models.Model):
   rule_name = models.CharField(max_length=255,blank=False)
   rule_time = models.IntegerField()
   rule_count = models.IntegerField()
   created_time = models.DateTimeField(default=timezone.now)
   created_by = models.CharField(max_length=256)
   isInterface = models.BooleanField()
   isAlarmType = models.BooleanField()
   event_status = models.ForeignKey(RuleState, on_delete=models.SET_NULL, blank=True, null=True)


   def __str__(self):
       return self.rule_name

   class Meta:
       db_table = "rule"




class Action(models.Model):
    name = models.CharField(max_length=100,blank=True,null=True)
    code = models.CharField(max_length=50,blank=True,null=True)
    output_ass= models.ForeignKey(OutputConfig,on_delete=models.CASCADE,null=True )
    rule = models.ManyToManyField(Rule,blank=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "actions"


class HostRuleInfo(models.Model):
    host_name=models.CharField(max_length=1024,blank=True,null=True)
    rule=models.ForeignKey(Rule,on_delete=models.SET_NULL,blank=True,null=True)
    created_date=models.DateTimeField(default=timezone.now)
    desc=models.CharField(max_length=1024)
    def __str__(self):
        return self.host_name

    class Meta:
        db_table = "HostRuleInfo"


class Action_rule_association(models.Model):
    rule = models.ForeignKey(Rule, on_delete = models.SET_NULL, blank=True, null=True)
    action = models.ForeignKey(Action, on_delete = models.SET_NULL, blank=True, null=True)

    class Meta:
        db_table = "rule_actions"

from django.db import models
from Hosts.models import *




# Create your models here.

class InputSourceType(models.Model):
    name = models.CharField(max_length=150, blank=True)
    code = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "eventengine_InputSourceType"


class InputSource(models.Model):
    name = models.CharField(max_length=100, blank=True)
    serverIp = models.CharField(max_length=50, blank=True)
    inputSourceType = models.ForeignKey(InputSourceType, on_delete = models.SET_NULL, blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "eventengine_InputSource"


class Events(models.Model):
    state = models.CharField(max_length=256, blank=True)
    alarmName = models.CharField(max_length=256, blank=True)
    alarmType = models.CharField(max_length=256, blank=True)
    description = models.TextField(max_length=256,blank=True)
    ci = models.ForeignKey('Hosts.Hosts', on_delete = models.SET_NULL, blank=True, null=True)
    alertSource = models.ForeignKey(InputSource, on_delete = models.SET_NULL, blank=True, null=True)
    eventTime = models.DateTimeField(null=True)
    createdTime = models.DateTimeField(auto_now_add=True)
    parent = models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    assigned = models.CharField(max_length=256,blank=True)
    interface = models.CharField(max_length=1024, blank=True)

    def __str__(self):
        return self.description

    class Meta:
        db_table = "eventengine_Events"

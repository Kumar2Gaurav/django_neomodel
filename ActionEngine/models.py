from django.db import models
from EventEngine.models import Events
# Create your models here.


class OutputType(models.Model):
    name = models.CharField(max_length=32 ,blank=False)
    code = models.CharField(max_length=32 ,blank=False,unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "actionengine_OutputType"

class UserConfig(models.Model):
    key=models.CharField(max_length=32 ,blank=False)
    value=models.CharField(max_length=32 ,blank=True)
    output_ass=models.ForeignKey(OutputType,on_delete=models.CASCADE)

    def __str__(self):
        return self.key

    class Meta:
        db_table = "actionengine_UserConfig"

class OutputConfig(models.Model):
    name = models.CharField(max_length=128 ,blank=False)
    outType = models.ForeignKey(OutputType,on_delete=models.CASCADE)
    host = models.CharField(max_length=128 , unique=False)
    port = models.IntegerField()
    username = models.CharField(max_length=32 ,blank=True,unique=False)
    password = models.CharField(max_length=32 ,blank=True)
    techKey = models.CharField(max_length=128 ,blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "actionengine_OutputConfig"

class serviceNowInfo(models.Model):
    ticketNo = models.CharField(max_length=32 ,blank=False)
    subject = models.CharField(max_length=32 ,blank=False)
    ticketState = models.CharField(max_length=32 ,blank=False)
    createTime = models.DateTimeField()
    event = models.ForeignKey(Events , on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.subject

    class Meta:
        db_table = "actionengine_serviceNowInfo"

class mailInfo(models.Model):
    sendDate = models.DateTimeField()
    userMailId = models.CharField(max_length=32 ,blank=False)
    ackNow = models.CharField(max_length=32 ,blank=False)
    subject = models.CharField(max_length=32 ,blank=False)
    event = models.ForeignKey(Events ,on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.userMailId

    class Meta:
        db_table = "actionengine_mailInfo"

class manageEngineInfo(models.Model):
    ticketNo = models.CharField(max_length=32, blank=False)
    subject = models.CharField(max_length=1024, blank=False)
    ticketState = models.CharField(max_length=32, blank=False)
    status = models.CharField(max_length=32, blank=True)
    priority = models.CharField(max_length=32, blank=True)
    createTime = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(Events , on_delete=models.SET_NULL, null=True, blank=True)
    desc = models.CharField(max_length=2048, blank=True)
    sla = models.CharField(max_length=1024, blank=False, default='')
    technician = models.CharField(max_length=256, blank=False, default='')
    resolvedate = models.CharField(max_length=512, blank=False, default='')
    duebytime = models.CharField(max_length=1024, blank=True, default='')
    responseduebytime = models.CharField(max_length=2048, blank=True, default='')


    def __str__(self):
        return self.subject

    class Meta:
        db_table = "actionengine_manageEngineInfo"
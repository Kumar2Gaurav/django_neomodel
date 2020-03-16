from django.db import models
from EventEngine.models import InputSourceType
from EventEngine.models import InputSource
from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
                      UniqueIdProperty, RelationshipTo, RelationshipFrom,StructuredRel)



config.DATABASE_URL = 'bolt://neo4j:12345@localhost:7687'
#config.DATABASE_URL = 'bolt://neo4j:newpass@172.16.10.89:7687'

class Interfaces(StructuredRel):
    interface=StringProperty()

class HostsGraph(StructuredNode):
    service = RelationshipFrom('ServicesGraph', 'SERVICE_OFF')
    link=RelationshipTo('HostsGraph','LINKED_TO',model=Interfaces)
    alias = StringProperty(required=True)
    ip = StringProperty(required=True)
    name = StringProperty(required=True)
    type=StringProperty(required=True)

    def __str__(self):
        return self.name

class ServicesGraph(StructuredNode):
    name = StringProperty(required=True)
    host_name=StringProperty(required=True)
    type=StringProperty(required=True)
    host = RelationshipTo(HostsGraph, 'SERVICE_OFF')

    def __str__(self):
        return self.name


class Hosts(models.Model):
    name = models.CharField(max_length=128,unique=True)
    ipAddress = models.CharField(max_length=30)
    hostType = models.CharField(max_length=30)
    inputType=models.ForeignKey(InputSource, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "hosts_Hosts"


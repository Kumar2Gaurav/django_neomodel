NAGIOS_EVENT = 'nagios_log'
U2000_EVENT ="u2000_snmp"
M2000_EVENT ="m2000_snmp"


LOGGABLE = ['CRITICAL', 'MAJOR']

INCIDENT_OPEN = 'Open'

INCIDENT_STATE_DIC_ME = ['Resolved', 'Closed']

AUTO_TICKETING = True
INCIDENT_ACTION_CODE = "create_incident"
STATUSOK=['OK', 'UP', 'CLEARED']
RESOLVED = "Resolved"
ACKURL = 'http://172.16.10.95:9000/acknowledge/'
CRITICAL = "CRITICAL"
MAJOR = 'MAJOR'

PRIORITY_STATE = {"CRITICAL": "Core Priority 1",
                    "MAJOR": "Core Priority 2",
                  "UNKNOWN": "Core Priority 3"}

DATA_HOST_LIST =["GBN-0003_TRC-CR_X8-01"]


# ======================== Action Codes ================================ #
MANAGEENGINE = "MNG"
SERVICENOW = "SNOW"
EMAIL = "MAIL"


#==========================MIB CONSTANT U2000 HUWAIE======================
mib_11={"1":"Critical","2":"Major","3":"Minor","4":"Warning","5":"Indeterminate","6":"Clear"}
mib_10 ={"1":"Power System","2":"Environment System","3":"Signaling System","4":"Trunk System","5":"Hardware System",
"6":"Software System","7":"Running System","8":"Communication System","9":"QoS","10":"Processing error","11":"OMC","12":"Integrity Violation",
"13":"Operational Violation","14":"Physical Violation","15":"Security Service Or Mechanism Violation","16":"Time Domain Violation"}

mib_2= {"1":"Fault","2":"Clear","3":"Event","4":"Acknowledge","5":"Unacknowledge","9":"Change"}

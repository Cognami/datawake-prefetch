import os


"""
All configuration for the datawake web server.
To change the configuration you should set the appropriate environment variables.
Environment variables are used to set conf to conform to standard docker practices.

REQUIRED ENVIRONMENT VARIABLES

DW_DB: database name
DW_DB_USER: database username
DW_DB_PASSWORD: database password
DW_DB_HOST: database ip address or hostname
DW_DB_PORT: database port
DW_KAFKA_CONN_POOL: comma seperated list of kafka brokers ip:port,..
DW_KAFKA_PUB_TOPIC: kafka topic to publish visited urls for processing.


OPTIONAL ENVIRONMENT VARIABLES

DW_GOOGLE_CLIENT_IDS: list of client ids used for google user authentication
DW_MOCK_AUTH:  If set actual user authentication is bypassed. (for dev / demos only)
DW_CONN_TYPE:  Determines mysql is used to store the generated web index data. default=mysql. can by mysql or cluster
DW_EXTERNAL_LINK_NAMES: Comma separated list of links names to provide for extracted features found in the domain index.
DW_EXTERNAL_LINK_VALUES: Comma separated list of links to provide for extracted features found in the domain index.
    The link text may contain "$ATTR" and/or "$VALUE", which will be replaced with an extracted type and value such as "phone" and "5555555555"


"""

VERSION_NUMBER="0.5_testing"

# enforce requirement for all required paramaters to be set

REQUIRED_PARAMS = [
    'DW_DB',
    'DW_DB_USER',
    'DW_DB_PASSWORD',
    'DW_DB_HOST',
    'DW_DB_PORT',
    'DW_KAFKA_CONN_POOL',
    'DW_KAFKA_PUB_TOPIC',
]
not_found = []
for param in REQUIRED_PARAMS:
    if param not in os.environ:
        not_found.append(param)
if len(not_found) > 0:
    raise ValueError("Datawake required environment variables not set: "+str(not_found))




# read required params

DATAWAKE_CORE_DB = {
    'database': os.environ['DW_DB'],
    'user': os.environ['DW_DB_USER'],
    'password':os.environ['DW_DB_PASSWORD'],
    'host': os.environ['DW_DB_HOST'],
    'port': os.environ['DW_DB_PORT']
}

KAFKA_CONN_POOL=os.environ['DW_KAFKA_CONN_POOL']
KAFKA_PUBLISH_TOPIC=os.environ['DW_KAFKA_PUB_TOPIC']
KAFKA_TRAIL_TOPIC=os.environ['DW_KAFKA_TRAIL_TOPIC']


# read optional params


CLIENT_IDS = []
if 'DW_GOOGLE_CLIENT_IDS' in os.environ:
    CLIENT_IDS = os.environ['DW_GOOGLE_CLIENT_IDS'].strip().split(',')


MOCK_AUTH = 'DW_MOCK_AUTH' in os.environ


# can be "cluster" or "mysql"
ENTITY_CONNECTION = 'mysql'
if 'DW_CONN_TYPE' in os.environ:
    ENTITY_CONNECTION = os.environ['DW_CONN_TYPE'].lower()
if ENTITY_CONNECTION != 'mysql':
    raise ValueError("DW_CONN_TYPE must be 'mysql' if set. ")


#
# Link to external tools.  provide a list of links in the form:
#   {'display':'display name','link':"..."}
# The link text may contain "$ATTR" and/or "$VALUE"
# which will be replaced with an extracted type and value such as "phone" and "5555555555"
#
EXTERNAL_LINKS = []
if 'DW_EXTERNAL_LINK_NAMES' in os.environ or 'DW_EXTERNAL_LINK_VALUES' in os.environ :
    try:
        linkNames = os.environ['DW_EXTERNAL_LINK_NAMES'].strip().split(',')
        linkValues = os.environ['DW_EXTERNAL_LINK_VALUES'].strip().split(',')
        for i in range( max (len(linkNames),len(linkValues))):
            EXTERNAL_LINKS.append({'display':linkNames[i],'link':linkValues[i]})
    except:
        raise ValueError("if DW_LINK_NAMES or DW_LINK_VALUES are set, both must be set and of equal length")

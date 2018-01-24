"""
Script name: lab1-2-get-host.py
Get all hosts connected to DNAC
"""

from dnac import *


# Controller ip, username and password are defined in dnac_config.py
# The get() function is defined in dnac.py
# Get token function is called in get() function
try:
    resp= get(api="host")
    response_json = resp.json() # Get the json-encoded content from response
    print (json.dumps(response_json,indent=4),'\n') # Convert "response_json" object to a JSON formatted string and print it out
except:
    print ("Something wrong with GET /host request")
    sys.exit()

# Parsing raw response to list out all users and their role
for host in response_json["response"]:
    if 'connectedInterfaceName' in host:
        interface = host['connectedInterfaceName']
    else:
        interface = None

    print ("Host '%s': Connected to %s/%s"%(host['hostIp'], 
                                            host["connectedNetworkDeviceName"], 
                                            interface ))


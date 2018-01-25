"""
This script prints out IOS config by deviceId:
User select a device from the list and script retrieve device ID according to user's selection
then calls - GET /network-device/{id}/config - to print out IOS configuration
"""
from dnac import * # DNAC IP is assigned in dnac_config.py
from tabulate import *

# Print out device list for user to select
device = []
try:
    resp= get(api="network-device") # The response (result) from "GET /network-device" request
    status = resp.status_code
    response_json = resp.json() # Get the json-encoded content from response
    device = response_json["response"] # Network-device
except:
    print ("Something wrong, cannot get network device information")
    sys.exit()

if status != 200:
    print (resp.text)
    sys.exit()

# Make sure there is at least one network device
if device == [] :   # if response is not empty
    print ("No network device was found !")
    sys.exit()

# Device found
device_list = []
# Extracting attributes
# Add a counter to an iterable
i=0
for item in device:
    i+=1
    device_list.append([i,item["hostname"],item["managementIpAddress"],item["type"],item["instanceUuid"]])
# Show all network devices under this DNAC's management
# Pretty print tabular data, needs 'tabulate' module
print (tabulate(device_list, headers=['number','hostname','ip','type'],tablefmt="rst"),'\n')

print ("*** Please note that some devices may not be able to show configuration for various reasons. ***\n")

# Ask user input
# Find out network device id for network device with ip or hostname, index 4 is the device id
# In the loop until 'id' is assigned or user select 'exit'

id = ""
device_id_idx = 4
while True:
    user_input = input('=> Select a number for the device from above to show IOS config: ')
    user_input= user_input.lstrip() # Ignore leading space
    if user_input.lower() == 'exit':
        sys.exit()
    if user_input.isdigit():
        if int(user_input) in range(1,len(device_list)+1):
            id = device_list[int(user_input)-1][device_id_idx]
            break
        else:
            print ("Oops! number is out of range, please try again or enter 'exit'")
    else:
        print ("Oops! input is not a digit, please try again or enter 'exit'")
# End of while loop

# Get IOS configuration API
try:
    resp = get(api="network-device/"+id+"/config")
    status = resp.status_code
except:
    print ("Something wrong with GET network-device/"+id+"/config !\n")
    sys.exit()
try:
    response_json = resp.json()
    # Replace "\r\n" to "\n" to remove extra space line (Carriage Return)
    print (response_json["response"].replace("\r\n","\n"))
except:
    # For some reason IOS configuration is not returned
    if status == 204:
        print ("No Content in response of GET /network-device/id/config !")
    else:
        print ("Something wrong in response of GET /network-device/id/config!\n")
        print ("Response:\n",json.dumps(response_json,indent = 4))

"""
This script prints out IOS config or interface info by deviceId:
User select a device from the list and script retrive device ID according to user's selection
then calls - GET /network-device/{id}/config or GET /interface/network-device/"+id
to print out IOS configuration or interface information
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
if device == []:
    print ("No network device found !")
    print (resp.text)

# Ask user's input - What to display ? Interfaces list(1) or IOS config(2) ?
while True:
    user_input = input('=> Please enter \n1: To get list of interfaces for the given device ID\n2: To get IOS configuration for the given device ID\nEnter your selection: ' )
    user_input= user_input.lstrip() # ignore leading space
    if user_input.lower() == 'exit':
        sys.exit()
    if user_input.isdigit():
        if user_input in {'1','2'}:
            break
        else:
            print ("Sorry, wrong selection, please try again to select 1 or 2 or enter 'exit'!")
    else:
       print ("Oops! input is not a digit, please try again or enter 'exit'")
# End of while loop

# Device found
device_list = []
# Extracting attributes
# Add a counter to an iterable
i=0
for item in device:
    i+=1
    device_list.append([i,item["hostname"],item["managementIpAddress"],item["type"],item["instanceUuid"]])
    #Not showing id to user, it's just a hex string

# Show all network devices under this DNAC's management
# Pretty print tabular data, needs 'tabulate' module
# Not showing id to user, it's just a hex string
print (tabulate(device_list, headers=['number','hostname','ip','type'],tablefmt="rst"),'\n')

# Ask user's input
# Find out network device id for network device with ip or hostname, index 4 is device id
# In the loop until 'id' is assigned or user select 'exit'
id = ""
device_id_idx = 4
while True:
    if user_input == '1':
        print ("*** Please note that some devices may not be able to show interface info for various reasons. ***\n")
        user_input2 = input('=> Select a number for the device from above to show Interface: ')
    else:
        print ("*** Please note that some devices may not be able to show configuration for various reasons. ***\n")
        user_input2 = input('=> Select a number for the device from above to show IOS config: ')
    user_input2= user_input2.lstrip() # Ignore leading space
    if user_input2.lower() == 'exit':
        sys.exit()
    if user_input2.isdigit(): # Check if the user's input is a digit
        if int(user_input2) in range(1,len(device_list)+1): # Check if input is within range
            id = device_list[int(user_input2)-1][device_id_idx]
            break
        else:
            print ("Oops! number is out of range, please try again or enter 'exit'")
    else:
        print ("Oops! input is not a digit, please try again or enter 'exit'")
# End of while loop

# Show interface or IOS config
if user_input == '1':
    # Get interface list
    selected_api  =  "interface/network-device/"+id
else:
    # Get IOS configuration
    selected_api =  "network-device/"+id+"/config"
# GET api request
try:
    resp = get(api=selected_api)
    status = resp.status_code
except:
    print ("Something wrong with GET %s\n"%s)
    sys.exit()

try:
    response_json = resp.json()
    if user_input == '1': # Interface list
        print ("Response:\n",json.dumps(response_json,indent = 4))
    if user_input == '2': # IOS configuration
        # Replace "\r\n" to "\n" to remove extra space line (Carriage Return)
        print (response_json["response"].replace("\r\n","\n"))
except:
    if status == 204:
        print ("No Content in response of GET %s"%selected_api)
    else:
        print ("Something wrong in response of GET %s!\n"%selected_api)
        print ("Response:\n",json.dumps(response_json,indent = 4))

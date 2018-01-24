"""
Script name: lab1-1-get-host.py
This script prints out all hosts that are connected to DNAC network devices in a tabular list format.
"""

from dnac import *

def get_host():
    """
    This function returns a tabular list of all hosts that are connected to DNAC network devices.
    Return:
    ------
    list: a list of all hosts and network devices with a number tag
    """
    host_list=[]
    try:
        resp = get(api="host") # The get() function is the simplified version for "get" function in requests module, defined in dnac.py
        response_json = resp.json() # Get the json-encoded content from response
        print ("Status: ",resp.status_code)  # This is the http request status
    except:
        print ("Something wrong with GET /host request!")
        return host_list
    # Now create a list of host summary
    i=0
    for item in response_json["response"]:
        i+=1
        host_list.append([i,item["hostIp"],item["hostType"],item["connectedNetworkDeviceIpAddress"]])
    return host_list

if __name__ == "__main__": # Execute only if run as a script
    host=get_host()
    # We use tabulate module here to print a nice table format. You should use "pip" tool to install in your local machine
    # The tabulate module is imported in dnac.py
    # For the simplicity we just copy the source code in working directory without installing it
    print (tabulate(host,headers=['number','host IP','type','connected to network device'],tablefmt="rst"))





"""
Script name: lab2-1-get-host-network-device-iplist.py
This script return all hosts and network devices in a tabular list.

dnac.py has functions for REST request and obtain token
dnac_config.py is the central place to change the dnac IP, username, password ...etc
"""

from dnac import * # The dnac_config.py is the central place to change the dnac IP, username, password ...etc

def get_host_and_device():
    """
    This function returns a list of all hosts and network devices with a number tag.

    Return:
    -------
    list: a list of all hosts and network devices with a number tag
    """
    ip_list=[]
    idx=0
    # Get host
    try:
        resp= get(api="host")
        print ("Status of GET /host: ",resp.status_code)  # This is the http request status
        response_json = resp.json() # Get the json-encoded content from response
        if response_json["response"] !=[]:
            i=0
            for item in response_json["response"]:
                i+=1
                ip_list.append([i,"host",item["hostIp"]])
            idx=i # idx(sequential number) will be used to tag host and network device
    except:
        print ("Something wrong, cannot get host IP list")
    # So far "ip_list" contains all hosts

    # Now get network device and append it to the list
    try:
        resp= get(api="network-device")
        print ("Status: of GET /network-device ",resp.status_code)  # This is the http request status
        response_json = resp.json() # Get the json-encoded content from response
        if response_json["response"] !=[]:
            for item in response_json["response"]:
                idx+=1
                ip_list.append([idx,"network device",item["managementIpAddress"]])
    except:
        print ("Something wrong ! Cannot get network-device IP list !")
    # Now "ip_list" should have hosts and network-devices

    if ip_list !=[]:
        return ip_list
    else:
        print ("There is no any host or network device !")
        sys.exit()

if __name__ == "__main__": # execute only if run as a script
    # We use tabulate module here to print a nice table format. You should use "pip" tool to install in your local machine
    # The tabulate module is imported in dnac.py
    # For the simplicity we just copy the source code in working directory, without installing it
    print (tabulate(get_host_and_device(),headers=['number','type','ip'],tablefmt="rst"))



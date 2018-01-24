"""
Script name: lab2-2-get-path-trace-with-flowAnalysisId.py
This script prints outA DNAC path trace information between the source and destination host(network device).
"""

from dnac import *
import threading,time # Need it for delay - sleep() function

def check_status(arg,arg1):
    """
    Non-blocking wait function to check POST /flow-analysis status:
    INPROGRESS, COMPLETED, FAILED

    Parameters
    ----------
    arg (str) : status of POST /flow-analysis
    arg1 (str): flowAnalysisId from POST /flow-analysis
    Return:
    -------
    None
    """
    status = arg
    flowAnalysisId = arg1
    count = 0
    while status != "COMPLETED":
        if status == "FAILED":
            print("Unable to find full path. No traceroute or netflow information found. Failing path calculation.")
            print("\n------ End of path trace ! ------")
            sys.exit()
        print ("\nTask is not finished yet, sleep 1 second then try again")
        time.sleep(1)
        count += 1
        if count > 20: # timeout after ~ 20 seconds
            print ("\nScript time out, no routing path was found. Please try using different source and destination !")
            print("\n------ End of path trace ! ------")
            sys.exit()
        try:
            r = get(api="flow-analysis/"+flowAnalysisId)
            response_json = r.json()
            # print ("Response from GET /flow-analysis/"+flowAnalysisId,json.dumps(response_json,indent=4))
            status = response_json["response"]["request"]["status"]
            print ("\n**** Check status here: ",status," ****\n")
        except:
            # Something is wrong
            print ("\nSomething is wrong when executing get /flow-analysis/{flowAnalysisId}")
            sys.exit()
    print ("Response from GET /flow-analysis/"+flowAnalysisId,json.dumps(response_json,indent=4))
    print("\n------ End of path trace ! ------")

def get_host_and_device():
    """
    This function returns a list of all hosts and network devices with a number tag.

    Return:
    ------
    list: a list of all hosts and network devices with a number tag
    """
    ip_list=[]
    idx=0
    # Create a list of host and network device
    # Get host
    try:
        resp= get(api="host")
        response_json = resp.json() # Get the json-encoded content from response
        i=0
        if response_json["response"] !=[]:
            for item in response_json["response"]:
                i+=1
                ip_list.append([i,"host",item["hostIp"]])
            idx=i # This idx(sequential number) will be used to tag host and network device
                  # So far this number = the number of hosts
    except:
        print ("Something wrong, cannot get host IP list")

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
    return ip_list

def select_ip(prompt,ip_list,idx):
    """
    This function return a element that user selected from a tabular list

    Parameters
    ----------
    prompt: str
        message to prompt user
    ip_list: list
        a list with idx that user can make a selection
    idx: int
        position of element to retrieve from list

    Return:
    -------
    str: user selected IP address
    """

    ip =""
    while True:
        user_input = input(prompt)
        user_input= user_input.lstrip() # Ignore leading space
        if user_input.lower() == 'exit':
            sys.exit()
        if user_input.isdigit():
            if int(user_input) in range(1,len(ip_list)+1):
                ip = ip_list[int(user_input)-1][idx] # The idx is the position of IP
                return ip
            else:
                print ("Oops! number is out of range, please try again or enter 'exit'")
        else:
            print ("Oops! input is not a digit, please try again or enter 'exit'")
    # End of while loop

if __name__ == "__main__": # execute only if run as a script
    ip_idx = 2
    nd_list = get_host_and_device()
    if len(nd_list) < 2:
        print ("We need at least 2 host or network-device to perform path trace!")
        sys.exit()

    print (tabulate(nd_list,headers=['number','type','ip'],tablefmt="rst"))
    print ("*** Please note that not all source/destination ip pair will return a path - no route. ! *** \n")
    s_ip = select_ip('=> Select a number for the source IP from above list: ',nd_list,ip_idx) # ip_idx (=2) is the position of IP in the list
    d_ip = select_ip('=> Select a number for the destination IP from above list: ',nd_list,ip_idx) # ip_idx (=2) is the position of IP in the list
    # Now we have the souce and destination IPs we can use them to POST /flow-analysis
    path_data = {"sourceIP": s_ip, "destIP": d_ip} # JSON input for POST /flow-analysis - simplify one
    # path_data= {"sourceIP":s_ip,"destIP":d_ip,"periodicRefresh":False,"inclusions":["QOS-STATS","INTERFACE-STATS","DEVICE-STATS","PERFORMANCE-STATS","ACL-TRACE"]}
    # above JSON will trigger the respone to include stats of QoS, interface, device and ACL trace
    r = post(api="flow-analysis",data=path_data) # Execute POST /flow-analysis
    response_json = r.json()
    print ("Response from POST /flow-analysis:\n",json.dumps(response_json,indent=4))
    try:
       flowAnalysisId = response_json["response"]["flowAnalysisId"]
    except:
        print ("\n For some reason cannot get flowAnalysisId")
        sys.exit()

    ###########################################################
    # Check status of POST /flow-analysis - non-blocking wait #
    ###########################################################
    thread = threading.Thread(target=check_status, args=('',flowAnalysisId,)) # Passing <status = ''>
    thread.start()


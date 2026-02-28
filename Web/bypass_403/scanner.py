# This file contains the logic of bypassing 403 
'''
Docstring for bypass403
This script is for bypassin 403 forbidden errors on web servers.
The goal is to automate testing all approaches to bypass it including but not limited to:
1. Headers 
2. Path normalization -- done
3. HTTP Methods -- done 
4. User Agents -- done
5. Other headers such as Content-Type -- done 
6. Append IP addresses -- next step
7. Optimize code. -- next step
8. ASN/Geo
9. Refererer Headers
10. Test on valid valid scenarios. -- next step.
12. Send them via burp? -- done
13. Tailor the args to be more customizable (e.g., if the user does not want to add these lists);--> next step.
14. Try to conquer it if some of the methods or techniques does not make difference. -- next step.
15. Add auth header and see if it makes difference (403 test instead of 401) -- done
16. Display the request arch (to make sure it is structured correctly). -- next step.
17 leveraging `curl` command to perform requests with different techniques.
'''
import requests
import sys
from payloads import *

## Helper Methods

def read_file(file_path):
    with open(file_path, 'r') as file:
        agents = file.readlines()
    return agents



# I cannot make it optional since bypassing depends on passing those parameters
if len(sys.argv) < 4:
    print(f"[!] Incorrect number of arguments.")
    print(f"[!] Usage: {sys.argv[0]} <full_target_url> <agent_wordlist_file> <headers_wordlists> <ip_header_wordlist> <auth token>[optional]")
    sys.exit(1)

# Read wordlists
agents = read_file(sys.argv[2])
forwarded_headers = read_file(sys.argv[3])
ips = read_file(sys.argv[4])


# I want to get the last endpoint to add the path norm char before it, given the url from the user
# For example if the user is providing: http://example.com/api/v1/get-passcode
# I want to get that get-passcode part to add the path norm chars before it.
# We can split via / and get the last part. 
splited_url = sys.argv[1].split('/')
last_segment= splited_url[-1]

## Shift the model from looping over all cases to "generating testcases and then executing them"
## Test case: 
    ## Method = GET
    ## User-Agent = X
    ## Content-Type = Y
    ## Forwarded-Header = Z
    ## IP = 1.2.3.4
    ## Auth = present/ absent

## Design optimization:
  ## Questions to ask myself:
    ## 1. Which dimensions should be paired (e.g., forwarder headers and IPs)
    ## 2. Do I need to test every combination?
    ## 3. What varies, what stays constant? (e.g., URL usually constant)
    ## 4. What should be a single test case? 
    ## 5. What fields does it have or should have? What are optional fields? 

  ## Design considerations:
    ## 1. Execution logic remain clean and flat; One loop for generating test cases, one for executing them. 
    ## 2. Reduce combinations without loosing coverage.

  ## Test case design:
    ## A test case is a one concrete HTTP request .
    ## <Method, Endpoint, Authentication/NoAuth, Extra-headers (User-Agent, Content-Type, Forwarded-Header + IP)>

for char in PATH_NORM:

    if (char == ''):
        modified_url = sys.argv[1]
    else: 
        modified_url = '/'.join(splited_url[:-1] + [char] + [last_segment])
    
    print(f"[*] Trying URL: {modified_url}")

    for agent in agents:
        
        agent = agent.strip()
        for content_type in CONTENT_TYPES:
            
            content_type = content_type.strip()

            for forwarded_header in forwarded_headers:

                forwarded_header = forwarded_header.strip()
                for ip in ips:

                    ip = ip.strip()
                    for i in range(len(HTTP_METHODS)):
                        
                        method = HTTP_METHODS[i]
                        
                        if sys.argv[5]:
                            authorization_token = sys.argv[5]
                            response = requests.request(method, modified_url, headers =  {"User-Agent": agent, "Content-Type" :content_type, forwarded_header: ip, "Authorization": authorization_token}, proxies=PROXIES, verify=False)
                        else:
                            response = requests.request(method, modified_url, headers =  {"User-Agent": agent, "Content-Type" :content_type, forwarded_header: ip}, proxies=PROXIES, verify=False)

                        print(f"[*] appedning results to the file....")
                        
                        # Update result path with your path
                        with open("/Users/kholoudahmed/Downloads/Clones/Automation/web/bypass_403/bypass_403_results.txt", 'w') as result_file:
                            result_file.write(f"[*] Trying url {modified_url}, Method {method} with User-Agent:{agent} with Content-Type : {content_type} with header {forwarded_header} with ip value {ip})\n")
                            result_file.write("\n")
                            result_file.write(f"Response : {response.text}\n")
                            result_file.write("\n************************************************************\n")
    
    print(f"[*] Finished appending results to the file. ")

# Test logic happens here
def generate_test_case(method, url, headers, auth=None):
    return 0 


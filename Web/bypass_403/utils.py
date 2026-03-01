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


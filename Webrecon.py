import socket 
import argparse
from concurrent.futures import ThreadPoolExecutor
import requests 

parser = argparse.ArgumentParser()

parser.add_argument('--url')

arg = parser.parse_args()

Ports = []

#---------------------------
#Port scanning function 
#---------------------------
def check_port(port):
    url = arg.url.replace("http://", "").replace("https://", "")
    s = socket.socket()
    s.settimeout(3)
    try:
        s.connect((url, port))
        try:

            banner = s.recv(1024)
            decode = banner.decode(errors='ignore').strip()

            Ports.append(f'Ports: {port} | Banner: {decode} + \n')
        except:
            pass


    except: 
        pass

    finally:

        s.close()



wordlist = ["admin", "login", "backup", "uploads", "config", "dashboard", "api", "test"]
url_found = []

def dir_scanner(word):
    url = arg.url + "/" + word 
    s = requests.Session()
    response = s.get(url)

    status = response.status_code
    if status == 200:
        url_found.append(url)





headers = []

def get_headers():
    response = requests.get(arg.url)
    for key, value in response.headers.items():
        headers.append(f"{key}: {value}") 
        print(f"{key}: {value}")          

    


def save_report():
    with open("report.txt", "w") as f:
        f.write("=== PORT SCAN ===\n")
        for port in Ports:
            f.write(port + "\n")
        f.write("\n=== DIRECTORIES ===\n")
        for url in url_found:
            f.write(url + "\n")
        f.write("\n=== HEADERS ===\n")    
        for header in headers:
            f.write(header + "\n")
        


with ThreadPoolExecutor(max_workers=50) as e:
    e.map(check_port, range(1, 81))

with ThreadPoolExecutor(max_workers=50) as e:
    e.map(dir_scanner, wordlist)


print("\n---Open Ports---")
print(Ports)

print("\n----Found URLs---")
print(url_found)

print("\n---Header found")
get_headers()          

save_report() 
print("Report saved!")
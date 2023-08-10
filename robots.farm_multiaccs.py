import random
import time
import requests
from web3 import Web3
from datetime import datetime
from colorama import init, Fore
from eth_account.messages import encode_defunct
init()

ref_code = '2ecd8'
retry_count = 2
use_proxy = True

w3 = Web3(Web3.HTTPProvider("https://bsc.blockpi.network/v1/rpc/public"))

headers = {
    'authority': 'robots.farm',
    'accept': '*/*',
    'cookie': f'_by={ref_code}; _ga=GA1.1.319997992.1691686083; _ga_J1EV6ZYFX7=GS1.1.1691686083.1.1.1691686114.0.0.0',
    'referer': 'https://robots.farm/airdrop/quests',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
}

items = {
    'Common Item': [100, 101, 102, 103, 104, 105],
    'Rare Item': [110, 111, 112, 113, 114],
    'Epic Item': [120, 121, 122, 123],
    'Legendary Item': [130, 131, 132],
    'Crate small chance': [201, 202, 203, 204, 205],
    'Crate avg chance': [206, 207, 208, 209, 210],
    'Crate good chance': [211, 212, 213, 214, 215],
    'Crate high chance': [216, 217, 218, 219],
    'Crate very high chance': [220],
    'Egg': [301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320],
    'Discount Rare Item 1 NFT': [400],
    'Discount Rare Item 3 NFT': [401],
    'Discount Rare Item 5 NFT': [402],
    'Legendary Item Free Mint NFT': [403],
}


def read_file(filename):
    result = []
    with open(filename, 'r') as file:
        for tmp in file.readlines():
            result.append(tmp.replace('\n', ''))

    return result


def write_to_file(filename, text):
    with open(filename, 'a') as file:
        file.write(f'{text}\n')


def sign_signature(private_key, message):
    message_hash = encode_defunct(text=message)
    signed_message = w3.eth.account.sign_message(message_hash, private_key)

    signature = signed_message.signature.hex()
    return signature


def login(address):
    params = {
        'address': address,
    }

    requests.get(
        'https://robots.farm/api/account',
        params=params,
        headers=headers,
        proxies=random.choice(proxies)
    ).json()


def is_available(address, private):
    params = {
        'address': address,
    }

    response = requests.get(
        'https://robots.farm/api/next-free',
        params=params,
        headers=headers,
        proxies=random.choice(proxies)
    ).json()

    if response['Next'] == '0001-01-02T00:00:00Z' and not response['Available']:
        write_to_file("does not have eth transaction.txt", f"{private};{address}")
        return False, 1
    elif int(response['Next'].split("T")[0].split("-")[-1]) > int(datetime.now().strftime('%d')):
        write_to_file('not_qualified.txt', f"{private};{address};{response['Next']}")
        return False, 0
    else:
        return (True,)


def get_reward(private):
    ts = int(time.time())
    message = f'Robots.farm play Quest 1 {ts}'
    signed_message = sign_signature(private, message)[2:]

    params = {
        'timestamp': ts,
        'quest': '1',
        'signature': signed_message,
    }

    response = requests.get(
        'https://robots.farm/api/play-quest',
        params=params,
        headers=headers,
        proxies=random.choice(proxies)
    )
    try:
        for item_id, count in response.json().items():
            for item_name, item_ids in items.items():
                if int(item_id) in item_ids:
                    print(f'\tItem rare: {item_name}; Count: {count}')
                    write_to_file('REWARDS.txt', f'{private};{item_name};{count}')
    except Exception as e:
        write_to_file('ERROR.txt', f'{private};{e}')
        print(f"\t{response.text}")


def main(private):
    address = w3.eth.account.from_key(private).address

    login(address)
    is_available_list = is_available(address, private)
    if is_available_list[0]:
        print(f"{Fore.MAGENTA}{datetime.now().strftime('%d %H:%M:%S')}{Fore.RESET} | {Fore.CYAN}{address}{Fore.RESET} "
              f"| {Fore.BLUE}Rewards:")
        get_reward(private)
    else:
        err_text = ['Retry tomorrow', "robots.farm doesn't see ethereum transaction."]
        print(f"{Fore.MAGENTA}{datetime.now().strftime('%d %H:%M:%S')}{Fore.RESET} | {Fore.CYAN}{address}{Fore.RESET} "
              f"| {Fore.RED}Address not qualified. {err_text[is_available_list[1]]}"
              f"{' Added to the end of the list.' if privates.count(private) <= retry_count and is_available_list[1] else ''}")
        if privates.count(private) <= retry_count:
            privates.append(private)


if __name__ == '__main__':
    privates = read_file('privates.txt')
    if use_proxy:
        proxies = []
        for proxy in read_file('proxies.txt'):
            proxies.append({"http": f"http://{proxy}", "https": f"http://{proxy}"})
    else:
        proxies = [None, None, None]
    for p in privates:
        main(p)

import requests

address = '0x0000000000000000000000000123123' # сюда адрес акка, на котором нужно клеймить поинты за рефов

cookies = {
    '_ga': 'GA1.1.994808847.1691609354',
    '_by': '2ed2e',
    '_ga_J1EV6ZYFX7': 'GS1.1.1691692737.6.1.1691692911.0.0.0',
}

headers = {
    'authority': 'robots.farm',
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uk;q=0.6',
    # 'cookie': '_ga=GA1.1.994808847.1691609354; _by=2ed2e; _ga_J1EV6ZYFX7=GS1.1.1691692737.6.1.1691692911.0.0.0',
    'referer': 'https://robots.farm/dashboard',
    'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
}

params = {
    'address': address,
}

response = requests.get('https://robots.farm/api/account', params=params, cookies=cookies, headers=headers).json()
account_id = response['ID']
print(f'На аккаунте {address} есть {response["Points"]} Points\n\n')

params = {
    'id': account_id,
}

response = requests.get('https://robots.farm/api/referrals', params=params, cookies=cookies, headers=headers)

ref_list = response.json()
for ref in ref_list:
    ref = ref['ID']

    params = {
        'side': 'ref',
        'id': ref,
    }

    response = requests.get('https://robots.farm/api/claim-referral', params=params, cookies=cookies, headers=headers)
    print(response.json())
    if 'message' in responce.json():
        print(f'Уже заклеймлено, ref_id :{ref}')
    else:
        print(f'Заклеймил 1 поинт, ref_id :{ref}')

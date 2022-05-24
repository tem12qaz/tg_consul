import requests

cookies = {
    '_ga': 'GA1.2.1541250795.1652893431',
    '_gid': 'GA1.2.1139223970.1652893431',
    '_gat': '1',
    '_yatri_session': 'cVFRQUpSTEpXZVdCR1lHNWpxUFZ5SStDYkxtYWtmZFVQU3Q0NmRYWjZhR0k4ZFFtRXhtWFRTVlNaQllOd0dpWVlIKzlSSDNWb2UzMnlQdGIxbGxSRVoxQ2lxMUxaQm1hZ3kvaDdUOURaQ3J5YnFVVFlvbjhnOUtHWmRwL3ZBRkNDeWViVjk5SVlWK0t6UlZtMElkZ2dUdnU4TEZraWxtT042KzdLUGhUQWIwbE9mQ3pwdHg3N0lTVkdwN0ZMcW1OV3JYYnliZGdxcmFaYnlvVUlreUZtdEJZL3lSVUdxeGlRdFByNVpReGk2aEN1Z0xZOTcvZ2FUUmYzcEIyUWJTVUJEUEJkTXd3U0VtckZhMkZoeGdYT0RlbjZXVDUzWmZERm9YeXIvdjNhejJRZjlzcnJHbzJtaEVJRDl5dDUxMnJHcThNbGhreFB4V2ViNVVac09ReW9wL3hXZzUyZHR6Z3c0RW00cEdtVmxyK2V0cTdqNGlPYlJBL2NPaFlxZ3ZDMFlGaTU1V2JJcHBOQ3ozOEZuSFpPelk2M1A4UVVlMDFJTEg0dlZqUGhva3BPc1hERjlXZy9oczJZMzhSK2h1SVNXN3NqYjZYcEt0eFlGdHhkL1JBOEhFcnd2SktNaDZtNDgxajFQZkgva0kreEswZ0VpaE8rQmE5V1BYVDZqNmpGOHdzOFpNQjhBakwrbmJTTVBHSjJOL1pZR0RGeWZWV3ZJcFB6MDhPSkdnPS0tWVdJRTc4WHdDMWpoQUZ4MnlSckhFZz09--0af03e53edba4f57357085412c051c743039ec01',
}

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'ru-RU,ru;q=0.9,en;q=0.8,es;q=0.7',
    'Connection': 'keep-alive',
    # Requests sorts cookies= alphabetically
    # 'Cookie': '_ga=GA1.2.1541250795.1652893431; _gid=GA1.2.1139223970.1652893431; _gat=1; _yatri_session=cVFRQUpSTEpXZVdCR1lHNWpxUFZ5SStDYkxtYWtmZFVQU3Q0NmRYWjZhR0k4ZFFtRXhtWFRTVlNaQllOd0dpWVlIKzlSSDNWb2UzMnlQdGIxbGxSRVoxQ2lxMUxaQm1hZ3kvaDdUOURaQ3J5YnFVVFlvbjhnOUtHWmRwL3ZBRkNDeWViVjk5SVlWK0t6UlZtMElkZ2dUdnU4TEZraWxtT042KzdLUGhUQWIwbE9mQ3pwdHg3N0lTVkdwN0ZMcW1OV3JYYnliZGdxcmFaYnlvVUlreUZtdEJZL3lSVUdxeGlRdFByNVpReGk2aEN1Z0xZOTcvZ2FUUmYzcEIyUWJTVUJEUEJkTXd3U0VtckZhMkZoeGdYT0RlbjZXVDUzWmZERm9YeXIvdjNhejJRZjlzcnJHbzJtaEVJRDl5dDUxMnJHcThNbGhreFB4V2ViNVVac09ReW9wL3hXZzUyZHR6Z3c0RW00cEdtVmxyK2V0cTdqNGlPYlJBL2NPaFlxZ3ZDMFlGaTU1V2JJcHBOQ3ozOEZuSFpPelk2M1A4UVVlMDFJTEg0dlZqUGhva3BPc1hERjlXZy9oczJZMzhSK2h1SVNXN3NqYjZYcEt0eFlGdHhkL1JBOEhFcnd2SktNaDZtNDgxajFQZkgva0kreEswZ0VpaE8rQmE5V1BYVDZqNmpGOHdzOFpNQjhBakwrbmJTTVBHSjJOL1pZR0RGeWZWV3ZJcFB6MDhPSkdnPS0tWVdJRTc4WHdDMWpoQUZ4MnlSckhFZz09--0af03e53edba4f57357085412c051c743039ec01',
    'If-None-Match': 'W/"a96d28dfa64d718cee862570c1fc5600"',
    'Referer': 'https://ais.usvisa-info.com/en-ca/niv/schedule/38770842/appointment?utf8=%E2%9C%93&applicants%5B%5D=45853796&applicants%5B%5D=45853930&applicants%5B%5D=45854052&applicants%5B%5D=45854131&applicants%5B%5D=45854300&confirmed_limit_message=1&commit=Continue',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Mobile Safari/537.36',
    'X-CSRF-Token': 'tweXzSnrqvtX2DhGdZU0zEux+z0aPEGxFjfeKsYkx/AGa8C1tfyTKU4kQmqXq0/PhKnaGgLjBSxbBDye+ABpbw==',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
}



class Prx:
    def __init__(self):
        self.ip = '138.59.207.172'
        self.port = '9068'
        self.user = 'UonNTz'
        self.password = '1tfyat'

    @property
    def http(self):
        return f'http://{self.user}:{self.password}@{self.ip}:{self.port}'

    @property
    def https(self):
        return f'https://{self.user}:{self.password}@{self.ip}:{self.port}'


prx = Prx()
proxies = {
    "http": prx.http,
    "https": prx.https,
}

response = requests.get('https://ais.usvisa-info.com/en-ca/niv/schedule/38770842/appointment/days/94.json?appointments\\[expedite\\]=false', cookies=cookies, headers=headers)
print(response.content)

# response = requests.get(
#     'http://ais.usvisa-info.com/en-ca/niv/schedule/38770842/appointment/days/94.json?appointments\\[expedite\\]=false',
#     cookies=cookies, headers=headers, proxies=proxies
# )
# print(response.content)
#
# response = requests.get(
#     'http://ais.usvisa-info.com/en-ca/niv/schedule/38770842/appointment/times/94.json?date=2023-07-18&appointments\\[expedite\\]=false',
#     cookies=cookies, headers=headers, proxies=proxies
# )
# print(response.content)

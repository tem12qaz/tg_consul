import requests

cookies = {
    '_ga': 'GA1.2.1541250795.1652893431',
    '_gid': 'GA1.2.1139223970.1652893431',
    '_yatri_session': 'Vm42WVZJSVNQOEpPWTVqeXJBSlFlYW9PWklzVVhRR2g1REljeWllMlc0ZjdCMDZkRlVpTUtjbEF2NTE3QXg1RHd0WDZkTFlHVmZibG9VU0FWRDlmVjBaU1kyejNJb3c3MC9wZ1E2YWVRdVlYbE9JOHFPRkQzTmRsSFZkUlRWeXdReklGb3ZQSVF1QmFndWltN2dFRmkvWXlTVHV6VTRmcUpSQUpqT09HQ3B0WHBFZkxJYjYzVXBSSS9IOHFRb2dwZ1dIcjNUVDZXVGxlc1U0ZTNpVUZ0RVp0Uk5tV3FwUGFSSUI1Rms5eldIM0ROTFpCYzUwVWh4bmRKK3FzbFFaVC9adWJ0M0tXZkN3Si9vV0RLODRrOEZheFZuMkVzZXNOaXM5djZSb25rWmxrRGtTRENJaVNuSmtCS1BRdlNvRFY3VURmTnpIRFlKSjJ3QmNLbFM1ODJJcVNZS1ByUGI4N1NtcXhieXgzNktPelJxb1FzcmtCTHFIVVlFSHFGV3M3RFlpZk9hclF6U2t2V1N2a2ZrRU1kdEh1dmRtZlBxWnp4bTNwcjlYc2VmSStsQzFNTmVqaDZINVFvOXc2QjBXbmZLM2RrVnNaa3llakl1RWlwL0RZVjZQVXlrcjQ3ZnA1Q0s0YTdPSnRaMnJGd1ZubGZSS2E3eHl2cDJQKzVoTlJENForYmdLNjV2MjlrLzZWZDdjaWN2OWEzQ0Rzb3d6RFQ5cDhrK2I2bUpvPS0tL2R1YzV6cXZXOUVzQWRJVCtvYURZdz09--c1d79bcec503536a90c5f485c87810b227560ff7',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'ru-RU,ru;q=0.9,en;q=0.8,es;q=0.7',
    'Connection': 'keep-alive',
    # Requests sorts cookies= alphabetically
    # 'Cookie': '_ga=GA1.2.1541250795.1652893431; _gid=GA1.2.1139223970.1652893431; _yatri_session=Vm42WVZJSVNQOEpPWTVqeXJBSlFlYW9PWklzVVhRR2g1REljeWllMlc0ZjdCMDZkRlVpTUtjbEF2NTE3QXg1RHd0WDZkTFlHVmZibG9VU0FWRDlmVjBaU1kyejNJb3c3MC9wZ1E2YWVRdVlYbE9JOHFPRkQzTmRsSFZkUlRWeXdReklGb3ZQSVF1QmFndWltN2dFRmkvWXlTVHV6VTRmcUpSQUpqT09HQ3B0WHBFZkxJYjYzVXBSSS9IOHFRb2dwZ1dIcjNUVDZXVGxlc1U0ZTNpVUZ0RVp0Uk5tV3FwUGFSSUI1Rms5eldIM0ROTFpCYzUwVWh4bmRKK3FzbFFaVC9adWJ0M0tXZkN3Si9vV0RLODRrOEZheFZuMkVzZXNOaXM5djZSb25rWmxrRGtTRENJaVNuSmtCS1BRdlNvRFY3VURmTnpIRFlKSjJ3QmNLbFM1ODJJcVNZS1ByUGI4N1NtcXhieXgzNktPelJxb1FzcmtCTHFIVVlFSHFGV3M3RFlpZk9hclF6U2t2V1N2a2ZrRU1kdEh1dmRtZlBxWnp4bTNwcjlYc2VmSStsQzFNTmVqaDZINVFvOXc2QjBXbmZLM2RrVnNaa3llakl1RWlwL0RZVjZQVXlrcjQ3ZnA1Q0s0YTdPSnRaMnJGd1ZubGZSS2E3eHl2cDJQKzVoTlJENForYmdLNjV2MjlrLzZWZDdjaWN2OWEzQ0Rzb3d6RFQ5cDhrK2I2bUpvPS0tL2R1YzV6cXZXOUVzQWRJVCtvYURZdz09--c1d79bcec503536a90c5f485c87810b227560ff7',
    'If-None-Match': 'W/"211e76e65a3cf7059ed6a6ba4c331e37"',
    'Referer': 'https://ais.usvisa-info.com/en-ca/niv/schedule/38770842/appointment?utf8=%E2%9C%93&applicants%5B%5D=45853796&applicants%5B%5D=45853930&applicants%5B%5D=45854052&applicants%5B%5D=45854131&applicants%5B%5D=45854300&confirmed_limit_message=1&commit=Continue',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Mobile Safari/537.36',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
}

response = requests.get('https://ais.usvisa-info.com/en-ca/niv/schedule/38770842/appointment/days/94.json?appointments\\[expedite\\]=false', cookies=cookies, headers=headers)
print(response.content)

response = requests.get('https://ais.usvisa-info.com/en-ca/niv/schedule/38770842/appointment/times/94.json?date=2023-07-18&appointments\\[expedite\\]=false', cookies=cookies, headers=headers)
print(response.content)
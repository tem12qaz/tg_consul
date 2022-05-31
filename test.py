import requests

cookies = {
    '_ga': 'GA1.2.1541250795.1652893431',
    '_gid': 'GA1.2.2009656092.1653660797',
    '_yatri_session': 'akp0Q293NnREeTQyN0o3c2pNNUJXckNKL2VEUS8vTHpZaGFWQ2xBc3F4MU4yMkliam12YlZmeG03UmFnWGUzMUpaYWpzVU1hOHlMaTlnemUzRGtVTjFoZjVyMjQ3T3VodkM4MExDMkxBNHJJSmNZT0lyYzNyZHNTQ1pHTDRMTW5wdzJJVkYvSUZLdStTZXZPMHFPemxjZkxwRzl2OUVCZ2lRTkdQV05VaVB2WGRZVWVFQzQ0S29JVm1MemZ4Zm9rQnRrQlhzRUxxT1V0OEpoMGdUczM5bFozUzlQbEF2blBUNXJOUnovMVJQS01uc0NpQU94aGJBemlmb3ZHRVNMaCtIQjR2dmJPdk9zQi9xRkpuN1dxT2xzQ2hQcTNnQzBwRTZrdUdMV3pSQS85VVUwbDI2NlJtem9YSVp6aFNWTXlaTnJRVVhCVkJaQTdDdnBZc0xuVVU0b1NjUUlKT2N0eDd4UUdSMDVRSngveW8xZ3NTQkFjRm0xNHNIUzRCODBJMUZsK1h5cUZ3eGdLaWdCSldoL3RpcjRWTmkxcitiK1Exc2M0b2xyMWV3QnVIQyttMmFwTFJMNFBSRHNQbFdpeGsreGw1WEh5TXJnVWFxbS9jVC81enlUY1gxWXNqSG5uazQ5L3dPY0QvSnF0V2JsMnRVTDh3ZERFNHc4S1M5Y2hMK3ZRcXI0MXdTS1F4UEtFZXdDbVR6c3VjZ3psaWdsaHR5MU1LNWU3NHJrPS0tdk56YlhkdDlJRVEySVpSQ0JOZTYzdz09--a25e0740c6878c4386f2b9f5220f7f5d9564fe7a',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'ru-RU,ru;q=0.9,en;q=0.8,es;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # Requests sorts cookies= alphabetically
    # 'Cookie': '_ga=GA1.2.1541250795.1652893431; _gid=GA1.2.2009656092.1653660797; _yatri_session=akp0Q293NnREeTQyN0o3c2pNNUJXckNKL2VEUS8vTHpZaGFWQ2xBc3F4MU4yMkliam12YlZmeG03UmFnWGUzMUpaYWpzVU1hOHlMaTlnemUzRGtVTjFoZjVyMjQ3T3VodkM4MExDMkxBNHJJSmNZT0lyYzNyZHNTQ1pHTDRMTW5wdzJJVkYvSUZLdStTZXZPMHFPemxjZkxwRzl2OUVCZ2lRTkdQV05VaVB2WGRZVWVFQzQ0S29JVm1MemZ4Zm9rQnRrQlhzRUxxT1V0OEpoMGdUczM5bFozUzlQbEF2blBUNXJOUnovMVJQS01uc0NpQU94aGJBemlmb3ZHRVNMaCtIQjR2dmJPdk9zQi9xRkpuN1dxT2xzQ2hQcTNnQzBwRTZrdUdMV3pSQS85VVUwbDI2NlJtem9YSVp6aFNWTXlaTnJRVVhCVkJaQTdDdnBZc0xuVVU0b1NjUUlKT2N0eDd4UUdSMDVRSngveW8xZ3NTQkFjRm0xNHNIUzRCODBJMUZsK1h5cUZ3eGdLaWdCSldoL3RpcjRWTmkxcitiK1Exc2M0b2xyMWV3QnVIQyttMmFwTFJMNFBSRHNQbFdpeGsreGw1WEh5TXJnVWFxbS9jVC81enlUY1gxWXNqSG5uazQ5L3dPY0QvSnF0V2JsMnRVTDh3ZERFNHc4S1M5Y2hMK3ZRcXI0MXdTS1F4UEtFZXdDbVR6c3VjZ3psaWdsaHR5MU1LNWU3NHJrPS0tdk56YlhkdDlJRVEySVpSQ0JOZTYzdz09--a25e0740c6878c4386f2b9f5220f7f5d9564fe7a',
    'Origin': 'https://ais.usvisa-info.com',
    'Referer': 'https://ais.usvisa-info.com/en-ca/niv/schedule/39276393/appointment',
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

data = {
    'utf8': '✓',
    'authenticity_token': 'mdh/ObX6Ee797k7oAyZ7WEPOKjITUDCgGvtsQ5u3pOl6DuV517ktOXd+l2OUv8eQwMnbJJadv5exvojtHlNzkg==',
    'confirmed_limit_message': '1',
    'use_consulate_appointment_capacity': 'true',
    'appointments[consulate_appointment][facility_id]': '94',
    'appointments[consulate_appointment][date]': '2023-02-21',
    'appointments[consulate_appointment][time]': '08:45',
}

response = requests.post('https://ais.usvisa-info.com/en-ca/niv/schedule/39276393/appointment', cookies=cookies, headers=headers, data=data)
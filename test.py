import requests

cookies = {
    '_ga': 'GA1.2.1541250795.1652893431',
    '_gid': 'GA1.2.1139223970.1652893431',
    '_yatri_session': 'YjJBZVA1Ly9FY1ZGdURHVy9reTdhS3I1WnRVNnVXVkdsOUorcW9MV21NL3JMRzlWeGl5ZzBDRnB2aS9hZzV0MjBsTk54aUFrRHZBbkJZZWQ3RVllaGRvS3FHeGZTSTdyQXJBQ0FWUFA4Nmg0VHRGWEx0K0ZIQksyYWc4SUM3MVMwYzF2bVNMR0lObnUySnJaMEdqR090REtlcGp6NnBQUUw4RHhpVXZuTmo0OHczT2VvWUt3cjJwVTN3L2krUEczUGZtT3lnWEpxbmVnYXJmNG9HYzhSOEZMdlkvaUU0Ly9IL1VmV3lxdWc0bisxdUt6bjJjSW94bVBmVzdKR2xtNUtDd3hCRTFkTDNNNlJEbHNhR3pycGFXTEtFZE9wU3BwTno2dFBaYUxucytkNzZqTFZNcjM5empnbGVCdU1CdFR3ZGpaYVJYZ2x3cmQxOVhYRlFHWUs3aGZvenI0djM1eEtDNXF2RW5NUXdvR3EzWWVaaEZhQWQvRC9RWGxoeEg2S2x1cHpIQUNNQ0taWDNxUEUxZTlnMGwyMkxreExxekxKMEtGODN6dkV3RmVXU0VqYWxqU3BSdndTY29XcU1GTkQrMkJ3bHNCVmU5dzhqUlRwSU5SMXJxajY0Yy9WL0FZY3FiUDhValZ1Zm5PWWRPK2F1MnB2ZlYxSmRxNUszNzh6Z2RwbDFTR3d2cTVORUJyNXgyZ21jald2OFpHMmF3OTEreWMvL1A4c3dzPS0tdjgzM25XVDVYNngzd1hKRVNEYnYwQT09--aaf9980a1c564e39fe73111f06faff88c97ea552',
    '_gat': '1',
}



response = requests.get('https://ais.usvisa-info.com/en-ca/niv/schedule/38770842/appointment/days/94.json?appointments\\[expedite\\]=false', cookies=cookies, headers=headers)
print(response.content)

response = requests.get('https://ais.usvisa-info.com/en-ca/niv/schedule/38770842/appointment/times/94.json?date=2023-07-18&appointments\\[expedite\\]=false', cookies=cookies, headers=headers)
print(response.content)
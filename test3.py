import asyncio

import aiohttp
import requests

cookies = {
    '_gat': '1',
    '_yatri_session': 'aUVodjFkdG5YYTZNTm5NWUhsb2VDTUYxdGJXV1hZcXJoVm4rdVZYcnNsZ0QzT2FKNUpUalZoR1ZaVm5YZnU2QVRyZU5menF2aENXNzZselZXU3I3a1hKSWFzSmQyelVvY2YvQWZ2MGdSc3hXMHE2dmhzd0h2cEU4VW8rVlFOc0xhWlhkeEw1cXMvZXRJdWM3dXpJNVY4ODk2VUFlWmR3eTVOamdzVElQOEpFTTVHR3hodXlja2p6T3NYRGlRMytvNWhFb2drYTFtL1B1dVdNZWs1UHJDd1Q4b1FrU0lIakwxdkpuWnpnV2xYZG9lQUR5TUJYQW9kRWZjUC9ONm0wSmFvYVRZQlQ3UWNvUXlvVjNKUlp6b1NJbkcrRlRJUkpzSitIekhHSHh5WnVtSkhtdE1QMjlFQ3R6dUZJRmsraHEzSGovL3R5aTk2UnYya0hwazlyTTBidTVSbm81R3BVT1F3ZEpWNThJMVVEZzZoZCt2SkgxTS9Dcytuc2lqc1RvT0dxRkd1RStlaVVpKy9idndvNFZ5RFZhSWpacGFMV3l6N2FxMCtpMTJ6NkZ4MlJlSGJ4S0phM05SLzlEcndXeVZzZFZLS2FGUFZiaVN5V1RKUTMyTjJ4cC9hSzhPVEpxbE5aaW5kS0NFMWVKVkNmbCtIcFlSRzE2ME51Q05naVFmTklCa1g5TlZYSTBIam0zNHgzNS9RaGRlbzdmL1AwbHlZWnB1Qlp2M1BBPS0tcCtxZXhwL2NMMWg3YzM0Uk5yTVpKdz09--e282749062a356849d9c4c17d1b4a1d0b17b2620',
    '_ga': 'GA1.2.1735939955.1653064144',
    '_gid': 'GA1.2.971806773.1653064144'
}

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'ru-RU,ru;q=0.9,en;q=0.8,es;q=0.7',
    'Connection': 'keep-alive',
    # Requests sorts cookies= alphabetically
    # 'Cookie': '_ga=GA1.2.1541250795.1652893431; _gid=GA1.2.1139223970.1652893431; _yatri_session=TGpJcnl2NWF0V1JETXhrTmZwaFZ6ZVpWNlBGV3Z4RmZYK250MmVsaWlIK0VYS05zeVpWa21lWjZZUSs0dWZWbWZudVpZU05OWXAvenJZYWJ3S1dkQmpKdlBoMmVaMEpMSXMrYi8yd0theXZDV2tyUjkxZ1dtaWswTVFKdHNJZzNyTzg0RythMkZmQnYxMzJNYlNSd2F1bEZLTVBWTmhOUCtrYitEN3FpWlpucnNkeUpBOXgwQ1lkRGVXUkpsOXptQXlGMmFONjZMVElsb1p5TlZIcW8wRUZtRnF0ZFNsRWNNdGRobGZtamhjSHRJQWdCa3ZOS1Bha1hjNTVTd1oyNWprNDVZQlFzYXM4UUt1N1laZGZjaWtWd0FXMW1wOW0vUWR3M1E2cUZ4bGl5bWNleUR4MzY1NTQwNTVJM3N1TWc2QjYyTEc4SWdRN0MzYy8wcEJzUHI0OTZ4OTB4TTlTbExiMk51Y2RESmxvcUVrbWZqenpDd1EvbDhmZEV2VlpYQzRKRUN6Y1dGaDJNVVVQUUZvWlBPMXlnUG9zOFRkRWE3eUIvV1VHNC9pb0ZLYm9YcENrVU1KSktBZkplWGlqQ2F6djRSTnJzVW16OVpiYng4THZxRHc0aVhmYS92clVEczFaVGgrd0lDUTdUSWhpeVJwYlJHRmtGcHVaa3h6Q1FPekR3cHlUcnJRN1hGUjRpNkYzRHpST0JlVHp4ZDJsK1BWanVicGFyL2FrPS0tTkpKSC9nbmErVHcxbUJobEtZeGxmUT09--d3fa47363713b47b6698b869385b24c7dc7829b9',
    'If-None-Match': 'W/"a96d28dfa64d718cee862570c1fc5600"',
    'Referer': 'https://ais.usvisa-info.com/en-ca/niv/schedule/38770842/appointment?utf8=%E2%9C%93&applicants%5B%5D=45853796&applicants%5B%5D=45853930&applicants%5B%5D=45854052&applicants%5B%5D=45854131&applicants%5B%5D=45854300&confirmed_limit_message=1&commit=Continue',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Mobile Safari/537.36',
    'X-CSRF-Token': 'jYPdO/irS0VRzzGfTSvxt9VFhDpv0T241HzpLhHkuK5KHFfbCtbhRZ5uheYGg4oW1MdCxhSdCXHOT6Zjq/bx+w==',
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


async def main():
    print('--------------')
    async with aiohttp.ClientSession(cookies=cookies) as session:
        resp = await session.get(
            url='https://ais.usvisa-info.com/en-ca/niv/schedule/38770842/appointment/days/94.json?appointments\\[expedite\\]=false',
            headers=headers,
            proxy=str(prx.http)
        )
        data = (await resp.read())
        print (resp)
        print(data)
        print('----------------------')

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.create_task(main())
    loop.run_forever()
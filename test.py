
at = 'Gme/U8ngwUqADDOgUgk2QIbSydNbiLG3mN4b0NzTwHz5NIpIWES/anBsqr4qCcsS3EFgl8krhmj1XoRxljGtyw=='
city_id = '94'
date='2022-07-01'
time='11:00'
user_id = '39407085'
'''var xhr = new XMLHttpRequest();xhr.open("POST", "https://ais.usvisa-info.com/en-ca/niv/schedule/39407085/appointment", false);xhr.send(JSON.stringify({'utf8': '✓', 'authenticity_token': 'Gme/U8ngwUqADDOgUgk2QIbSydNbiLG3mN4b0NzTwHz5NIpIWES/anBsqr4qCcsS3EFgl8krhmj1XoRxljGtyw==', 'confirmed_limit_message': '1', 'use_consulate_appointment_capacity': 'true', 'appointments[consulate_appointment][facility_id]': '94', 'appointments[consulate_appointment][date]': '2022-07-01', 'appointments[consulate_appointment][time]': '11:00'}));while (xhr.readyState != 4){} return [xhr.responseText, xhr.status];
'''
data = {
                'utf8': '-',
                'authenticity_token': at,
                'confirmed_limit_message': '1',
                'use_consulate_appointment_capacity': 'true',
                'appointments[consulate_appointment][facility_id]': city_id,
                'appointments[consulate_appointment][date]': date,
                'appointments[consulate_appointment][time]': time,
            }
script = '''var xhr = new XMLHttpRequest();xhr.open("POST", "https://ais.usvisa-info.com/en-ca/niv/schedule/{user_id}/appointment", false);xhr.send(JSON.stringify({data}));while (xhr.readyState != 4){empty} return [xhr.responseText, xhr.status];'''
script = script.format(user_id=user_id, data=data, empty='{}')
print(str(script))

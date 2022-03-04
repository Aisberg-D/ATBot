import requests

open_weather_token = '0a2abb1451e2be7d79d70e0139f75663'
city_name = 'Irkutsk'


def get_weather(city_name):
    res = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&lang=ru&appid={open_weather_token}')
    # todo check response status cod
    cur_weather = res.json()
    #print(type(cur_weather))
    #print(cur_weather["main"]["temp"])
    #print(cur_weather["weather"][0]["description"])
    return f'Температура: {cur_weather["main"]["temp"]}, на улице {cur_weather["weather"][0]["description"]}'

if __name__ == '__main__':
    print(get_weather(city_name))

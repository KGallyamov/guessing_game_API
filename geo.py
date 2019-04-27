import requests
import sys


def get_photos(city):
    response = None
    try:
        point_array = get_coordinates(city)
        map_request = "http://static-maps.yandex.ru/1.x/?ll=", point_array[0], ",", point_array[1],\
                      "&spn=0.002,0.002&l=map"
        response = requests.get(map_request)
        if not response:
            print("Ошибка выполнения запроса")
            sys.exit(1)
    except Exception:
        print("Запрос не удалось выполнить. Проверьте наличие сети Интернет.")
        sys.exit(1)
    return response.content


def get_coordinates(city):
    url = "https://geocode-maps.yandex.ru/1.x/"
    params = {
        'geocode': city,
        'format': 'json'
    }
    response = requests.get(url, params)
    json = response.json()
    point_str = json['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
    point_array = [float(x) for x in point_str.split(' ')]
    return point_array


def get_country(city):
    url = "https://geocode-maps.yandex.ru/1.x/"
    params = {
        'geocode': city,
        'format': 'json'
    }
    response = requests.get(url, params)
    json = response.json()
    return json['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['AddressDetails']['Country']['CountryName']

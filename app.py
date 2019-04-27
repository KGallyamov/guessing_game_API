from flask import Flask, request
import logging
import json
import random
from geo import get_country, get_coordinates, get_photos

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, filename='app.log',
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')


@app.route('/post', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    logging.info('Request: %r', response)
    return json.dumps(response)


def handle_dialog(res, req):
    user_id = req['session']['user_id']
    city = random.choice('Москва', 'Санкт-Петербург', 'Казань', 'Самара', 'Бостон', 'Стокгольм', 'Нью-Йорк', 'Гонконг',
                         'Лондон', 'Уэльс')

    if req['session']['new']:
        res['response']['text'] = \
            'Привет! Я могу показать фотографии города а ты попытаешься отгадать что это за город!'
        res['response']['image'] = get_photos(city)
        return
    cities = get_cities(req)
    if not cities:
        res['response']['text'] = 'Ты не написал название не одного города!'
    elif len(cities) == 1 and cities[0] == city:
        res['response']['text'] = 'Верно! Этот город в стране - ' + \
                                  get_country(cities[0])
    else:
        res['response']['text'] = 'Неправильно!'


def get_cities(req):
    cities = []
    for entity in req['request']['nlu']['entities']:
        if entity['type'] == 'YANDEX.GEO':
            if 'city' in entity['value']:
                cities.append(entity['value']['city'])
    return cities


if __name__ == '__main__':
    app.run()

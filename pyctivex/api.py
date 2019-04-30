# -*- coding: utf-8 -*-
import logging
import requests
from django.conf import Settings


class ActiveDirectoryApi(object):
    ENDPOINT = getattr(Settings, 'AUTH_URL', 'http://10.1.1.243:8888')

    USER_DATA = ('client_email', 'profile', 'position', 'direction', 'type_position', 'employees_boss', 'boss')

    @staticmethod
    def login(user, password):
        """
        Permite autenticar contra el directorio activo y a su vez retorna informacion laboral del usuario
        :param user: str
        :param password: str
        :return: dict. int
        """

        payload = {'user': user, 'password': password}
        response = requests.post('{}/{}'.format(ActiveDirectoryApi.ENDPOINT, 'login'), data=payload)

        if response.status_code != requests.codes.ok:
            logging.exception('Error consulting auth url {} with response data: {}'
                              .format(ActiveDirectoryApi.ENDPOINT, response.content))

        return response.json(), response.status_code

    @staticmethod
    def user_data(user, fields):
        """
        Permite autenticar contra el directorio activo y a su vez retorna informacion laboral del usuario
        :param user: str
        :param fields: str, array, tuple
        :return: dict. int
        """
        
        if isinstance(fields, tuple):
            fields = list(fields)
        elif isinstance(fields, str):
            fields = str(fields).split(",")

        values = fields.__str__().replace("'", '"')

        endpoint = '{}/{}?user={}&fields={}'.format(ActiveDirectoryApi.ENDPOINT, 'user_data', user, values)

        response = requests.post(endpoint)

        if response.status_code == requests.codes.ok:
            return response.json(), response.status_code
        logging.error(response)
        return {'error': response.text}, response.status_code

import requests
from pathlib import Path

class DataBase:
    def __init__(self,url):
        self.url = 'http://localhost/Proyecto-UPTAEB-T2/'

        self.prepared_session = requests.session()

        # pr = self.prepared_session.prepare_request(requests.Request(
        #     'GET',
        #     self.url + 'apiasd',
        #     params={'randomnautica': 'productos'}
        # )
        # )
        # response = self.prepared_session.send(
        #     pr,
        #     timeout=15
        # )

    def login(self, correo, contraseña):
        try:
            r = False
            response = self.prepared_session.send(requests.Request(
                'POST', self.url + 'api_login',
                data={'correo': correo, 'contraseña': contraseña}
            ).prepare(), timeout=15)
            if response.text == '1':
                r = True
        finally:
            return r

    def buscar(self, **kwargs) -> list:
        pr = self.prepared_session.prepare_request(requests.Request(
            'GET',
            self.url + 'api_search',
            params=kwargs
            )
        )
        response = self.prepared_session.send(
            pr,
            timeout=15
        )
        return response.json()['lista']
    def download_image(self,name):
        pr = self.prepared_session.prepare_request(requests.Request(
            'GET',
            self.url + 'api_get_image',
            params={'img':name}
            )
        )
        response = self.prepared_session.send(
            pr,
            timeout=15,
            allow_redirects=True
        )

        if Path(f'cache/{name}').is_file() and Path(f'cache/{name}').stat().st_size == int(response.headers['content-length']):
            return f'cache/{name}'
        if 'image' not in response.headers['content-type']:
            return 'cache/banner_productos.png'
        with open(f'cache/{name}', 'wb') as file:
            file.write(response.content)
        return f'cache/{name}'
        # if stream:
        #     return response.iter_content(chunk)
        # else:
        #     return response.content

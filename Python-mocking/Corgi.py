from flask import request_started
import requests

class ApiCorgi(object):
    url = "http://api.corgidata.com"
    version = "v1"

    def make_url(self, resource):
        return "/".join([self.url, self.version, resource])

    def get(self, url, retries=3):
        while retries > 0:
            try:
                response = requests.get(url=url)
                try:
                    response.raise_for_status()
                    return response.json()
                except requests.exceptions.HTTPError as e:
                    self.handle_http_error(e)
            except (requests.exceptions.ConnectionError,
                    requests.exceptions.Timeout) as e:
                retries -= 1
                if not retries:
                    self.handle_connection_error(e)

    def breed_info(self, breed):
        resource = "/".join(['breeds', breed])
        url = self.make_url(resource = resource)
        response = self.get(url=url)
        return response
    
    def handle_http_error(self, e):
        pass

    def handle_connection_error(self, e):
        raise requests.exceptions.ConnectionError
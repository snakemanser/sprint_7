import constants
import requests

class CourierAPI:

    # создание курьера
    def api_v1_courier(self, data):
        path = "/api/v1/courier"
        url = f"{constants.URL}{path}"
        return requests.post(url, data=data)

    # логин курьера
    def api_v1_courier_login(self, data):
        path = "/api/v1/courier/login"
        url = f"{constants.URL}{path}"
        return requests.post(url, data=data)

    # удаление курьера
    def api_v1_courier_id(self, data):
        courier_id = self.api_v1_courier_login(data).json()['id']
        path = f"/api/v1/courier/{courier_id}"
        url = f"{constants.URL}{path}"
        return requests.delete(url)
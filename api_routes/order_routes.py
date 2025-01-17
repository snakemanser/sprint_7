import constants
import requests

class OrderAPI:

    # создание заказа
    def api_v1_orders(self, data):
        path = "/api/v1/orders"
        url = f"{constants.URL}{path}"
        return requests.post(url, data=data)

    # отмена заказа
    def api_v1_orders_cancel(self, params, data=None):
        path = "/api/v1/orders/cancel"
        url = f"{constants.URL}{path}"
        return requests.put(url, data=data, params=params)

    # получение списка заказов
    def api_v1_orders_get(self, params=None):
        path = "/api/v1/orders"
        url = f"{constants.URL}{path}"
        return requests.get(url, params=params)


    # получение инфо о заказе по трек номеру
    def api_v1_orders_track(self, data):
        path = "/api/v1/orders/track"
        url = f"{constants.URL}{path}"
        order_track = self.api_v1_orders(data=data).json()['track']
        params = {"t": order_track}
        return requests.get(url, params=params)


    # принять заказ
    def api_v1_orders_accept_id(self, order_id, params):
        path = f"/api/v1/orders/accept/{order_id}"
        url = f"{constants.URL}{path}"
        return requests.put(url, params=params)

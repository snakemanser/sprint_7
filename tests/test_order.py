import allure
import pytest
import constants
from api_routes.order_routes import OrderAPI
from api_routes.courier_routes import CourierAPI


class TestCreateOrder:
    @allure.title('Проверки создания заказа с разным параметром color и без него')
    @allure.description(
        'создает заказ с черным, серым, черным и серым, без параметра color, проверяет код и наличие track в теле, удаляет заказ')
    @pytest.mark.parametrize('data', [
        constants.ORDER_BLACK_DATA,
        constants.ORDER_GREY_DATA,
        constants.ORDER_BLACK_AND_GREY_DATA,
        constants.ORDER_NO_COLOR_DATA])
    def test_create_order_diff_color(self, data):
        resp = OrderAPI().api_v1_orders(data=data)
        assert resp.status_code == 201
        assert 'track' in resp.text
        order_track = resp.json()['track']
        params = {"track": order_track}
        OrderAPI().api_v1_orders_cancel(params)


class TestGetOrders:
    @allure.title('Проверка получения списка заказов для курьера')
    @allure.description(
        'создает курьера, создает заказ, привязывает заказ к курьеру, получает список заказов курьера,'
        'проверяет код ответа и что id созданного заказа равен id заказа в ответе, отменяет заказ, удаляет курьера')
    @pytest.mark.parametrize('order_data', [constants.ORDER_TEST_DATA])
    def test_get_orders_list_for_courier(self, prepare_courier, order_data):
        courier_id = CourierAPI().api_v1_courier_login(data=constants.LOGIN_COURIER_1_DATA).json()['id']
        order_info = OrderAPI().api_v1_orders_track(data=order_data)
        order_id = order_info.json()['order']['id']
        params = {"courierId": courier_id}
        OrderAPI().api_v1_orders_accept_id(order_id, params=params)
        resp = OrderAPI().api_v1_orders_get(params=params)
        assert resp.status_code == 200
        assert order_id == resp.json()['orders'][0]['id']
        params_2 = {"track": order_info.json()['order']['track']}
        OrderAPI().api_v1_orders_cancel(params_2)

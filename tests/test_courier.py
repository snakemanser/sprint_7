import allure
import pytest
import constants
from api_routes.courier_routes import CourierAPI


class TestCreateCourier:

    @allure.title('Проверка создания курьера')
    @allure.description(
        'создает курьера, проверяет статус код и тело ответа, удаляет курьера')
    def test_create_courier(self, del_courier):
        resp = CourierAPI().api_v1_courier(data=constants.CREATE_COURIER_1_DATA)
        assert resp.status_code == 201
        assert resp.json() == {'ok': True}

    @allure.title('Ошибка при создании двух одинаковых курьеров')
    @allure.description(
        'пытается создать 2ух одинаковых курьеров, проверяет код и текст ошибки, удаляет курьера')
    def test_create_two_identical_courier_error(self, prepare_courier):
        resp = CourierAPI().api_v1_courier(data=constants.CREATE_COURIER_1_DATA)
        assert resp.status_code == 409
        assert resp.json() == {"code": 409,"message": "Этот логин уже используется. Попробуйте другой."}

    @allure.title('Ошибка при создании курьера без пароля')
    @allure.description(
        'запрос на создание курьера без пароля, проверяет код и текст ошибки')
    def test_create_courier_without_pass_error(self):
        data = {
        "login": "pidjukpidja4ok",
        "firstName": "medoviymedovi4ek"}
        resp = CourierAPI().api_v1_courier(data=data)
        assert resp.status_code == 400
        assert resp.json() == {"code": 400,"message": "Недостаточно данных для создания учетной записи"}

    @allure.title('Ошибка при создании двух курьеров с одинаковым логином')
    @allure.description(
        'пытается создать 2ух курьеров с одинаковым логином и разным пасс+имя, проверяет код и текст ошибки, удаляет курьера')
    def test_create_courier_only_login_duplicate_error(self, prepare_courier):
        data = {
        "login": "pidjukpidja4ok",
        "password": "qwe322qwe",
        "firstName": "qwe322qwe"}
        resp = CourierAPI().api_v1_courier(data=data)
        assert resp.status_code == 409
        assert resp.json() == {"code": 409, "message": "Этот логин уже используется. Попробуйте другой."}



class TestLoginCourier:
    @allure.title('Проверка логина курьера')
    @allure.description(
        'создает курьера, выполняет логин, проверяет код и наличие параметра id в ответе, удаляет курьера')
    def test_courier_login(self, prepare_courier):
        resp = CourierAPI().api_v1_courier_login(data=constants.LOGIN_COURIER_1_DATA)
        assert resp.status_code == 200
        assert 'id' in resp.text

    @allure.title('Ошибка при логине с неправильным паролем/логином')
    @allure.description(
        'создает курьера, выполняет логин с неправильным логином, затем паролем, проверяет код и текст ошибки, удаляет курьера')
    @pytest.mark.parametrize('data', [{"login": "qwezxcqwe","password": "singapurJ "},
                                      {"login": "pidjukpidja4ok","password": "qwezxcqwe"}])
    def test_courier_login_with_wrong_login_then_pass_error(self, prepare_courier, data):
        resp = CourierAPI().api_v1_courier_login(data=data)
        assert resp.status_code == 404
        assert resp.json() == {"code": 404,"message": "Учетная запись не найдена"}

    @allure.title('Ошибка при логине без логина')
    @allure.description(
        'создает курьера, выполняет логин без передачи логина, проверяет код и текст ошибки, удаляет курьера')
    def test_courier_login_no_login_error(self, prepare_courier):
        data = {"password": "singapurJ "}
        resp = CourierAPI().api_v1_courier_login(data=data)
        assert resp.status_code == 400
        assert resp.json() == {"code": 400,"message": "Недостаточно данных для входа"}

    @allure.title('Ошибка при логине с несуществующими данными')
    @allure.description(
        'логин с несуществующими данными, проверяет код и текст ошибки')
    def test_courier_login_nonexistent_courier_error(self):
        data = {
            "login": "qqqqqqqqqq",
            "password": "qqqqqqqqqq"}
        resp = CourierAPI().api_v1_courier_login(data=data)
        assert resp.status_code == 404
        assert resp.json() == {"code": 404, "message": "Учетная запись не найдена"}
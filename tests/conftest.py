import pytest
import constants
from api_routes.courier_routes import CourierAPI


# создает курьера с CREATE_COURIER_1_DATA затем удаляет его
@pytest.fixture(scope='function')
def prepare_courier():
    courier = CourierAPI().api_v1_courier(data=constants.CREATE_COURIER_1_DATA)
    yield courier
    CourierAPI().api_v1_courier_id(data=constants.LOGIN_COURIER_1_DATA)


# удаляет курьера с CREATE_COURIER_1_DATA
@pytest.fixture(scope='function')
def del_courier():
    yield
    CourierAPI().api_v1_courier_id(data=constants.LOGIN_COURIER_1_DATA)
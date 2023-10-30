import pytest

from api.schemas.order import Order
from repositories.orders import OrderRepository


@pytest.mark.usefixtures('db_for_test', 'created_multiple_orders')
def test_get_average_order_amount():
    average = OrderRepository.get_average_order_amount()
    assert average >= 0


@pytest.mark.usefixtures('db_for_test', 'created_multiple_orders')
def test_get_popular_products_list():
    popular = OrderRepository.get_popular_products_list()
    print(popular)


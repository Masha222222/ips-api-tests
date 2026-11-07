import allure
from pydantic import TypeAdapter

from api_tests.models.pumps import AlertResponse


@allure.title("Получение списка предупреждений помпы")
def test_get_pump_alerts(pumps_client):
    response = pumps_client.get_alerts("pump-1")

    assert response.status_code == 200, (
        f"Ожидался код 200, получен {response.status_code}. "
        f"Ответ: {response.text}"
    )

    TypeAdapter(list[AlertResponse]).validate_json(response.text, strict=True)
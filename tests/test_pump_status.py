import allure

from api_tests.models.pumps import PumpStateResponse


@allure.title("Получение статуса помпы pump-1")
def test_get_pump_status(pumps_client):
    response = pumps_client.get_status("pump-1")

    assert response.status_code == 200, (
        f"Ожидался код 200, получен {response.status_code}. "
        f"Ответ: {response.text}"
    )

    content_type = response.headers.get("Content-Type", "")
    assert content_type.startswith("application/json"), (
        f"Ожидался JSON, получен Content-Type: {content_type!r}"
    )

    PumpStateResponse.model_validate(response.json(), strict=True)
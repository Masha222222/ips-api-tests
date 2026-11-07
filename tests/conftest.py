import pytest
from api_tests.client import PumpsClient
from uuid import uuid4
from datetime import datetime, timezone
from api_tests.models.pumps import TelemetryRequest
@pytest.fixture
def pumps_client():
    return PumpsClient("https://ips.alexgallax-edu.ru")

@pytest.fixture
def test_pump_id():
    return f"api-tests-{uuid4().hex}"

@pytest.fixture
def pump_alerts(pumps_client, test_pump_id):
    telemetry = TelemetryRequest(
        glucose_value=1.0,
        glucose_unit="mmol/L",
        timestamp=datetime.now(timezone.utc),
    )
    response = pumps_client.send_telemetry(
        test_pump_id, telemetry.model_dump(mode="json")
    )
    assert response.status_code == 200, (
        f"Не удалось отправить измерение: {response.status_code}, {response.text}"
    )

    response = pumps_client.get_alerts(test_pump_id)
    assert response.status_code == 200, (
        f"Не удалось получить предупреждения: {response.status_code}, {response.text}"
    )

    alerts = response.json()
    assert alerts, "После отправки измерения ожидалось хотя бы одно предупреждение"

    return alerts
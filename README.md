# IPS API Tests

API-тесты раздела Pumps учебного симулятора инфузионной помпы.

Swagger: https://ips.alexgallax-edu.ru/docs

## Запуск

```powershell
python -m pip install -r requirements.txt
python -m pytest -q
```

## Отчёт Allure

Собранный отчёт находится в папке `allure-report`. Для открытия нужна Allure CLI:

```powershell
allure open allure-report
```

## Особенности стенда

- `POST /api/v1/pumps/{pump_id}/alerts/all` указан в задании, но отсутствует в Swagger. Стенд возвращает `405 Method Not Allowed` с заголовком `Allow: DELETE`. Тест проверяет этот ответ. Позитивный сценарий для POST недоступен.
- `POST /api/v1/pumps/{pump_id}/block/reset` при отказе возвращает HTTP `403` и `status: "FAILED"`. Ответ `403` в Swagger не описан.
- После успешного сброса `manual_action_required` становится `false`. В первом запросе статуса после сброса поле `bolus_status` ещё может оставаться `blocked`, поэтому тест проверяет изменение `manual_action_required`.
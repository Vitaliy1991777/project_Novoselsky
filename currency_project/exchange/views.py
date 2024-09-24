import requests
from django.http import JsonResponse
from .models import ExchangeRate  # Не забудьте создать модель ExchangeRate
import time
from django.shortcuts import render

# Функция для получения курса USD к RUB через API ЦБ РФ
def fetch_usd_to_rub():
    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    response = requests.get(url)
    data = response.json()
    return data['Valute']['USD']['Value']

# Представление для обработки запроса
def get_current_usd(request):
    # Пауза 10 секунд
    time.sleep(10)

    # Получение курса и сохранение в базе данных
    rate = fetch_usd_to_rub()
    ExchangeRate.objects.create(rate=rate)

    # Получение последних 10 запросов
    last_10 = ExchangeRate.objects.all().order_by('-timestamp')[:10]

    # Возвращаем данные в формате JSON
    return JsonResponse({
        'current_rate': rate,
        'last_10_requests': [
            {'rate': obj.rate, 'timestamp': obj.timestamp} for obj in last_10
        ]
    })

# Представление для главной страницы
def index(request):
    return render(request, 'exchange/index.html')

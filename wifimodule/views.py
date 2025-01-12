from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
'''
def home(request):
    received_text = None

    if request.method == "POST":
        received_text = request.POST.get('text_input')  # Formdan gelen veriyi al

    return render(request, 'home.html', {'received_text': received_text})
'''
from django.shortcuts import render
from django.http import JsonResponse
'''
@csrf_exempt
def home(request):
    received_text = None
    if request.method == "POST":
        received_text = request.POST.get('text_input')  # Formdan gelen veriyi al

    return render(request, 'home.html', {'received_text': received_text})
@csrf_exempt
def get_text(request):
    # ESP8266 bu yola GET isteği yaparak veriyi alacak
    received_text = request.GET.get('text', '')
    return JsonResponse({'text': received_text})
'''

# views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse

from django.shortcuts import render
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

from .models import TextData
from django.shortcuts import render
from django.http import JsonResponse
from .models import TextData
from django.views.decorators.csrf import csrf_exempt
from .models import DistanceData
from .models import TemperatureData, HumidityData, DistanceData
# Verileri kaydetme ve gösterme fonksiyonu
@csrf_exempt
def home(request):
    received_text = None
    if request.method == "POST":
        # Formdan gelen verileri al
        text_input = request.POST.get('text_input')
        sayi_input = request.POST.get('sayi_input')
        selected_button = request.POST.get('button')

        # Veritabanına metin ve sayı değerini kaydet
        if text_input:
            TextData.objects.create(text_input=text_input)
            received_text = text_input
        elif sayi_input:
            TextData.objects.create(text_input=f"asayi:{sayi_input}")
            received_text = f"asayi:{sayi_input}"
        elif selected_button:
            TextData.objects.create(text_input=selected_button)
            received_text = selected_button

    return render(request, 'home.html', {'received_text': received_text})

# ESP8266'nın veriyi çekeceği fonksiyon
@csrf_exempt
def get_text(request):
    # En son kaydedilen text verisini al
    latest_text = TextData.objects.last()
    if latest_text:
        return JsonResponse({'text': latest_text.text_input})
    else:
        return JsonResponse({'text': 'Veri yok'})




import datetime
last_data_time = None

@csrf_exempt
def uzaklik_olcumu(request):
    global last_data_time

    # Eğer istek AJAX isteği ise sadece yeni veriyi kontrol edip JSON yanıt dön
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        latest_data = DistanceData.objects.last()
        if latest_data and latest_data.timestamp != last_data_time:
            last_data_time = latest_data.timestamp
            return JsonResponse({'new_data': True})
        return JsonResponse({'new_data': False})

    # Normal GET isteğiyle sayfayı yüklemek için
    all_data = DistanceData.objects.all().order_by('timestamp')
    latest_data = all_data.last()
    if latest_data:
        last_data_time = latest_data.timestamp

    return render(request, 'uzaklik_olcumu.html', {
        'all_data': all_data,
        'latest_data': latest_data.distance if latest_data else "Veri yok",
    })

@csrf_exempt
def add_distance_data(request):
    if request.method == "POST":
        distance = request.POST.get('distance')
        if distance:
            DistanceData.objects.create(distance=float(distance), timestamp=datetime.datetime.now())
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})



last_temp_time = None
last_humidity_time = None

@csrf_exempt
def sicaklik_olcumu(request):
    global last_temp_time

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        latest_data = TemperatureData.objects.last()
        if latest_data and latest_data.timestamp != last_temp_time:
            last_temp_time = latest_data.timestamp
            return JsonResponse({'new_data': True})
        return JsonResponse({'new_data': False})

    all_data = TemperatureData.objects.all().order_by('timestamp')
    latest_data = all_data.last()
    if latest_data:
        last_temp_time = latest_data.timestamp

    return render(request, 'sicaklik_olcumu.html', {
        'all_data': all_data,
        'latest_data': latest_data.temperature if latest_data else "Veri yok",
    })

@csrf_exempt
def nem_olcumu(request):
    global last_humidity_time

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        latest_data = HumidityData.objects.last()
        if latest_data and latest_data.timestamp != last_humidity_time:
            last_humidity_time = latest_data.timestamp
            return JsonResponse({'new_data': True})
        return JsonResponse({'new_data': False})

    all_data = HumidityData.objects.all().order_by('timestamp')
    latest_data = all_data.last()
    if latest_data:
        last_humidity_time = latest_data.timestamp

    return render(request, 'nem_olcumu.html', {
        'all_data': all_data,
        'latest_data': latest_data.humidity if latest_data else "Veri yok",
    })

@csrf_exempt
def add_temperature_data(request):
    if request.method == "POST":
        temperature = request.POST.get('temperature')
        if temperature:
            TemperatureData.objects.create(temperature=float(temperature), timestamp=datetime.datetime.now())
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

@csrf_exempt
def add_humidity_data(request):
    if request.method == "POST":
        humidity = request.POST.get('humidity')
        if humidity:
            HumidityData.objects.create(humidity=float(humidity), timestamp=datetime.datetime.now())
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})



# views.py
from .models import BuzzerData

@csrf_exempt
def toggle_buzzer(request):
    if request.method == "POST":
        status = request.POST.get('status')
        if status:
            BuzzerData.objects.create(status=status)
            return JsonResponse({'status': 'success', 'current_status': status})
    else:
        # En son buzzer durumunu döndür
        latest_status = BuzzerData.objects.last()
        if latest_status:
            return JsonResponse({'status': 'success', 'current_status': latest_status.status})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})



# views.py
from django.shortcuts import render
from .models import Location

def show_map(request):
    # Veritabanındaki en son eklenmiş konumu al
    latest_location = Location.objects.last()
    context = {
        "latitude": latest_location.latitude if latest_location else 0,
        "longitude": latest_location.longitude if latest_location else 0,
    }
    return render(request, 'show_map.html', context)




# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Location

@csrf_exempt
def save_location(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        # Veritabanına konum kaydet
        Location.objects.create(latitude=latitude, longitude=longitude)
        return JsonResponse({"status": "success", "message": "Konum kaydedildi."})

    return JsonResponse({"status": "fail", "message": "Geçersiz istek."})




import requests
from django.shortcuts import render
from .models import Location

def get_weather_icon(weathercode):
    """Hava durumu koduna göre uygun Font Awesome ikon sınıfını döndür."""
    if weathercode == 0:
        return "fas fa-sun"
    elif weathercode == 1:
        return "fas fa-cloud"
    elif weathercode == 2:
        return "fas fa-cloud-sun"
    elif weathercode == 3:
        return "fas fa-cloud-showers-heavy"
    elif weathercode in [45, 48]:
        return "fas fa-smog"
    elif weathercode in [51, 53, 55]:
        return "fas fa-cloud-rain"
    elif weathercode in [61, 63, 65]:
        return "fas fa-cloud-showers-heavy"
    elif weathercode in [71, 73, 75]:
        return "fas fa-snowflake"
    elif weathercode == 95:
        return "fas fa-bolt"
    else:
        return "fas fa-cloud"

def hava_durumu(request):
    # Veritabanındaki son konumu al
    latest_location = Location.objects.last()

    # Eğer konum yoksa varsayılan enlem ve boylam
    latitude = latest_location.latitude if latest_location else 0
    longitude = latest_location.longitude if latest_location else 0

    # Open-Meteo API isteği
    api_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true&daily=temperature_2m_max,temperature_2m_min,windspeed_10m_max,weathercode&timezone=auto"
    response = requests.get(api_url)
    weather_data = response.json()

    # API'den gelen hava durumu bilgisi
    current_weather = weather_data.get("current_weather", {})
    daily_forecast = weather_data.get("daily", {})

    # 5 günlük tahmin için veri hazırlama
    forecast = []
    for i in range(len(daily_forecast.get("time", []))):
        forecast.append({
            "date": daily_forecast["time"][i],
            "temperature": daily_forecast["temperature_2m_max"][i],
            "windspeed": daily_forecast["windspeed_10m_max"][i],
            "weather_icon": get_weather_icon(daily_forecast["weathercode"][i])
        })

    context = {
        "latitude": latitude,
        "longitude": longitude,
        "temperature": current_weather.get("temperature", "Bilinmiyor"),
        "windspeed": current_weather.get("windspeed", "Bilinmiyor"),
        "weather_icon": get_weather_icon(current_weather.get("weathercode", 0)),
        "forecast": forecast,
    }

    return render(request, 'havadurumu.html', context)
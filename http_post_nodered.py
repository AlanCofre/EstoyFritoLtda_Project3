import requests
import time
from generate_json import generate_sensor_data
from datetime import datetime

NODERED_URL = "http://localhost:1880/sensor_data"

print("=" * 60)
print("Enviando datos a NodeRed vía HTTP POST")
print(f"URL: {NODERED_URL}")
print("=" * 60)
print("Presiona Ctrl+C para detener\n")

try:
    while True:
        sensor_data = generate_sensor_data()
        
        response = requests.post(
            NODERED_URL,
            json=sensor_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✓ Datos enviados exitosamente")
            print(f"  Temp: {sensor_data['dUMA']['environment']['temperature']}°C")
            print(f"  Humidity: {sensor_data['dUMA']['environment']['humidity']}%")
            print(f"  IAQ: {sensor_data['dUMA']['air_quality']['iaq_index']}")
            print(f"  PM 2.5: {sensor_data['dUMA']['air_quality']['pm25']} μg/m³")
        else:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✗ Error: {response.status_code}")
        
        time.sleep(5)
        
except KeyboardInterrupt:
    print("\n\nEnvío detenido por el usuario")
except Exception as e:
    print(f"\n✗ Error: {e}")

import json
import time
from datetime import datetime
import paho.mqtt.client as mqtt
from generate_json import generate_sensor_data  

# ==========================
# CONFIG MQTT
# ==========================

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "sensores"
MQTT_USERNAME = "publisher"   
MQTT_PASSWORD = "pub123"      

INTERVALO_SEGUNDOS = 5

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[MQTT PUBLISHER] Conectado al broker")
    else:
        print(f"[MQTT PUBLISHER] Error de conexión. Código: {rc}")

def main():
    # Crear cliente MQTT
    client = mqtt.Client(client_id="demo_publisher", clean_session=True)
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_connect = on_connect

    print("=" * 60)
    print("MQTT Publisher - Enviando datos de sensores al tópico 'sensores'")
    print(f"Broker: {MQTT_BROKER}:{MQTT_PORT}")
    print(f"Usuario: {MQTT_USERNAME}")
    print("=" * 60)

    # Conectar al broker
    client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
    client.loop_start()

    try:
        while True:
            data = generate_sensor_data()
            payload_str = json.dumps(data)
            result = client.publish(MQTT_TOPIC, payload=payload_str, qos=1)
            status = result[0]

            if status == mqtt.MQTT_ERR_SUCCESS:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ✓ Publicado en '{MQTT_TOPIC}'")
                env = data["dUMA"]["environment"]
                aq = data["dUMA"]["air_quality"]
                print(f"   Temp: {env['temperature']} °C | Hum: {env['humidity']} % | IAQ: {aq['iaq_index']}")
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ✗ Error al publicar (code={status})")

            time.sleep(INTERVALO_SEGUNDOS)

    except KeyboardInterrupt:
        print("\n[MQTT PUBLISHER] Detenido por el usuario")
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()

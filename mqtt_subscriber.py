import json
from datetime import datetime
import paho.mqtt.client as mqtt
import requests

# ==========================
# CONFIG MQTT
# ==========================

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "sensores"

MQTT_USERNAME = "subscriber"   
MQTT_PASSWORD = "sub123"     

# ==========================
# CONFIG NODE-RED
# ==========================

NODERED_URL = "http://localhost:1880/sensor_data_mqtt"  


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[MQTT SUBSCRIBER] Conectado al broker, suscribiéndose a 'sensores'...")
        client.subscribe(MQTT_TOPIC, qos=1)
    else:
        print(f"[MQTT SUBSCRIBER] Error de conexión. Código: {rc}")


def on_message(client, userdata, msg):
    try:
        payload_str = msg.payload.decode("utf-8")
        data = json.loads(payload_str)

        # Log en consola
        env = data["dUMA"]["environment"]
        aq = data["dUMA"]["air_quality"]

        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 📥 Mensaje MQTT recibido en '{msg.topic}':")
        print(f"   Temp: {env['temperature']} °C | Hum: {env['humidity']} % | IAQ: {aq['iaq_index']}")

        # Reenvío a Node-RED (mismo formato original)
        response = requests.post(
            NODERED_URL,
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=3
        )

        if response.status_code == 200:
            print(f"   ✓ Reenviado a Node-RED ({NODERED_URL})")
        else:
            print(f"   ✗ Error HTTP Node-RED: {response.status_code} -> {response.text}")

    except Exception as e:
        print(f"[MQTT SUBSCRIBER] Error procesando mensaje: {e}")


def main():
    client = mqtt.Client(client_id="demo_subscriber", clean_session=True)
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message

    print("=" * 60)
    print("MQTT Subscriber - Recibiendo de 'sensores' y reenviando a Node-RED")
    print(f"Broker: {MQTT_BROKER}:{MQTT_PORT}")
    print(f"Usuario: {MQTT_USERNAME}")
    print(f"Node-RED URL: {NODERED_URL}")
    print("=" * 60)

    client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
    client.loop_forever()


if __name__ == "__main__":
    main()

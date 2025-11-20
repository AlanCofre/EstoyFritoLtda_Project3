import json  # Importa módulo para trabajar con datos JSON
from datetime import datetime  # Importa para obtener fecha/hora actual
import paho.mqtt.client as mqtt  # Importa cliente MQTT de Paho
import requests  # Importa módulo para hacer peticiones HTTP

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

NODERED_URL = "http://localhost:1880/sensor_data_mqtt"  # URL endpoint de Node-RED

def on_connect(client, userdata, flags, rc):
    # Función callback que se ejecuta al conectar al broker MQTT
    if rc == 0:
        # Conexión exitosa - suscribirse al tópico
        print("[MQTT SUBSCRIBER] Conectado al broker, suscribiéndose a 'sensores'...")
        # Suscribirse al tópico con QoS 1
        client.subscribe(MQTT_TOPIC, qos=1)
    else:
        # Error en la conexión
        print(f"[MQTT SUBSCRIBER] Error de conexión. Código: {rc}")

def on_message(client, userdata, msg):
    # Función callback que se ejecuta cuando llega un mensaje MQTT
    try:
        # Decodificar el payload del mensaje de bytes a string UTF-8
        payload_str = msg.payload.decode("utf-8")
        # Convertir string JSON a diccionario Python
        data = json.loads(payload_str)

        # Extraer datos específicos para mostrar en consola
        env = data["dUMA"]["environment"]
        aq = data["dUMA"]["air_quality"]

        # Mostrar información del mensaje recibido
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 📥 Mensaje MQTT recibido en '{msg.topic}':")
        print(f"   Temp: {env['temperature']} °C | Hum: {env['humidity']} % | IAQ: {aq['iaq_index']}")

        # Reenviar los datos a Node-RED via HTTP POST
        response = requests.post(
            NODERED_URL,  # URL destino
            json=data,  # Datos a enviar en formato JSON
            headers={"Content-Type": "application/json"},  # Cabecera indicando tipo de contenido
            timeout=3  # Timeout de 3 segundos para la petición
        )

        # Verificar respuesta de Node-RED
        if response.status_code == 200:
            print(f"   ✓ Reenviado a Node-RED ({NODERED_URL})")
        else:
            print(f"   ✗ Error HTTP Node-RED: {response.status_code} -> {response.text}")

    except Exception as e:
        # Capturar cualquier error durante el procesamiento del mensaje
        print(f"[MQTT SUBSCRIBER] Error procesando mensaje: {e}")

def main():
    # Función principal del suscriptor
    
    # Crear cliente MQTT con ID específico
    client = mqtt.Client(client_id="demo_subscriber", clean_session=True)
    # Configurar credenciales de autenticación
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    # Asignar funciones callback para eventos
    client.on_connect = on_connect
    client.on_message = on_message

    # Mostrar información de configuración
    print("=" * 60)
    print("MQTT Subscriber - Recibiendo de 'sensores' y reenviando a Node-RED")
    print(f"Broker: {MQTT_BROKER}:{MQTT_PORT}")
    print(f"Usuario: {MQTT_USERNAME}")
    print(f"Node-RED URL: {NODERED_URL}")
    print("=" * 60)

    # Conectar al broker y mantener conexión activa
    client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
    # Loop infinito que maneja la comunicación MQTT
    client.loop_forever()

if __name__ == "__main__":
    # Punto de entrada del script
    main()
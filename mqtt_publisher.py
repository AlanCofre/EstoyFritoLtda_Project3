import json  # Importa módulo para trabajar con datos JSON
import time  # Importa módulo para manejar tiempos y delays
from datetime import datetime  # Importa para obtener fecha/hora actual
import paho.mqtt.client as mqtt  # Importa cliente MQTT de Paho
from generate_json import generate_sensor_data  # Importa función generadora de datos

# ==========================
# CONFIG MQTT
# ==========================

MQTT_BROKER = "localhost"  # Dirección IP o hostname del broker MQTT
MQTT_PORT = 1883  # Puerto del broker MQTT (1883 es el puerto por defecto)
MQTT_TOPIC = "sensores"  # Nombre del tópico donde se publicarán los mensajes
MQTT_USERNAME = "publisher"  # Nombre de usuario para autenticación en el broker
MQTT_PASSWORD = "pub123"  # Contraseña para autenticación en el broker

INTERVALO_SEGUNDOS = 5  # Tiempo en segundos entre cada publicación

def on_connect(client, userdata, flags, rc):
    # Función callback que se ejecuta cuando se conecta al broker
    # rc = result code (código de resultado de la conexión)
    if rc == 0:
        # Código 0 significa conexión exitosa
        print("[MQTT PUBLISHER] Conectado al broker")
    else:
        # Otros códigos indican diferentes tipos de errores
        print(f"[MQTT PUBLISHER] Error de conexión. Código: {rc}")

def main():
    # Función principal del programa
    
    # Crear cliente MQTT con ID específico y sesión limpia
    client = mqtt.Client(client_id="demo_publisher", clean_session=True)
    # Configurar usuario y contraseña para autenticación
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    # Asignar la función callback para manejar eventos de conexión
    client.on_connect = on_connect

    # Mostrar información de configuración en consola
    print("=" * 60)
    print("MQTT Publisher - Enviando datos de sensores al tópico 'sensores'")
    print(f"Broker: {MQTT_BROKER}:{MQTT_PORT}")
    print(f"Usuario: {MQTT_USERNAME}")
    print("=" * 60)

    # Conectar al broker MQTT con keepalive de 60 segundos
    client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
    # Iniciar loop en segundo plano para manejar comunicación MQTT
    client.loop_start()

    try:
        # Bucle infinito para publicar datos continuamente
        while True:
            # Generar datos de sensores simulados
            data = generate_sensor_data()
            # Convertir diccionario de datos a string JSON
            payload_str = json.dumps(data)
            # Publicar mensaje en el tópico con QoS 1 (calidad de servicio)
            result = client.publish(MQTT_TOPIC, payload=payload_str, qos=1)
            # Obtener código de resultado de la publicación
            status = result[0]

            if status == mqtt.MQTT_ERR_SUCCESS:
                # Si la publicación fue exitosa (código 0)
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ✓ Publicado en '{MQTT_TOPIC}'")
                # Extraer datos específicos para mostrar en consola
                env = data["dUMA"]["environment"]
                aq = data["dUMA"]["air_quality"]
                # Mostrar valores de sensores en consola
                print(f"   Temp: {env['temperature']} °C | Hum: {env['humidity']} % | IAQ: {aq['iaq_index']}")
            else:
                # Si hubo error en la publicación
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ✗ Error al publicar (code={status})")

            # Esperar el intervalo configurado antes de siguiente publicación
            time.sleep(INTERVALO_SEGUNDOS)

    except KeyboardInterrupt:
        # Capturar interrupción por teclado (Ctrl+C) para salir elegantemente
        print("\n[MQTT PUBLISHER] Detenido por el usuario")
    finally:
        # Bloque que siempre se ejecuta, asegura limpieza de recursos
        client.loop_stop()  # Detener el loop de MQTT
        client.disconnect()  # Desconectar del broker

if __name__ == "__main__":
    # Punto de entrada del script - ejecuta la función main
    main()
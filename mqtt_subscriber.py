#!/usr/bin/env python3
"""
mqtt_subscriber.py - Suscriptor MQTT
Proyecto #3 Dashboard Ambiental - INFO1128
"""

import json
import paho.mqtt.client as mqtt
import requests
import sys

# Configuración MQTT
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "sensores"
MQTT_USERNAME = "subscriber"
MQTT_PASSWORD = "sub123"

# Configuración Node-RED
NODERED_URL = "http://localhost:1880/sensores-mqtt"

def on_connect(client, userdata, flags, rc):
    """Callback cuando se conecta al broker"""
    if rc == 0:
        print("✓ Conectado al Broker MQTT")
        client.subscribe(MQTT_TOPIC)
        print(f"✓ Suscrito al tópico: '{MQTT_TOPIC}'")
    else:
        print(f"✗ Error de conexión. Código: {rc}")

def on_message(client, userdata, msg):
    """Callback cuando se recibe un mensaje"""
    try:
        datos = json.loads(msg.payload.decode())
        
        print(f"\n📥 Mensaje recibido:")
        print(f"  Timestamp:     {datos.get('timestamp', 'N/A')}")
        print(f"  Temperatura:   {datos.get('temperatura', 'N/A')}°C")
        print(f"  Humedad:       {datos.get('humedad', 'N/A')}%")
        print(f"  Presión:       {datos.get('presion', 'N/A')} hPa")
        print(f"  Cal. Aire:     {datos.get('calidad_aire', 'N/A')} AQI")
        print(f"  Luminosidad:   {datos.get('luminosidad', 'N/A')} lux")
        print(f"  CO2:           {datos.get('co2', 'N/A')} ppm")
        
        # Reenviar a Node-RED
        try:
            response = requests.post(NODERED_URL, json=datos, timeout=3)
            if response.status_code == 200:
                print("  ✓ Reenviado a Node-RED")
            else:
                print(f"  ⚠ Node-RED: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print("  ✗ Error: Node-RED no está disponible")
        except Exception as e:
            print(f"  ✗ Error al reenviar: {e}")
            
    except Exception as e:
        print(f"Error al procesar mensaje: {e}")

def main():
    """Función principal"""
    print("╔════════════════════════════════════════════════════════╗")
    print("║         MQTT SUBSCRIBER - Dashboard Ambiental          ║")
    print("╚════════════════════════════════════════════════════════╝")
    print()
    
    client = mqtt.Client(client_id="python_subscriber")
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        print(f"Conectando a {MQTT_BROKER}:{MQTT_PORT}...")
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        
        print("Presiona Ctrl+C para detener\n")
        client.loop_forever()
        
    except KeyboardInterrupt:
        print("\n\nDeteniendo suscriptor...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.disconnect()
        print("Desconectado del broker\n")

if __name__ == "__main__":
    main()
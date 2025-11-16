#!/usr/bin/env python3
"""
JSON.py - Generador de datos JSON con envío HTTP POST
Proyecto #3 Dashboard Ambiental - INFO1128

Este script genera datos aleatorios de sensores ambientales
y los envía mediante HTTP POST a Node-RED y Grafana.

Autor: [Tu Nombre]
Fecha: Noviembre 2024
"""

import json
import random
import time
import requests
from datetime import datetime
import sys
import os

# ============================================================
# CONFIGURACIÓN
# ============================================================

# URLs de destino
URL_NODERED = "http://localhost:1880/sensores"
URL_GRAFANA = "http://localhost:3000/api/datasources/proxy/1/write"

# Intervalo de envío (segundos)
INTERVALO_ENVIO = 5

# Rangos de valores para sensores
RANGOS = {
    'temperatura': (15.0, 35.0),    # °C
    'humedad': (30.0, 90.0),        # %
    'presion': (950.0, 1050.0),     # hPa
    'calidad_aire': (0, 500),       # AQI
    'luminosidad': (0, 1000),       # lux
    'co2': (400, 2000)              # ppm
}

# Colores para terminal
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# ============================================================
# FUNCIONES
# ============================================================

def limpiar_pantalla():
    """Limpia la pantalla de la terminal"""
    os.system('clear' if os.name != 'nt' else 'cls')

def imprimir_banner():
    """Muestra el banner inicial del programa"""
    limpiar_pantalla()
    print(f"{Colors.HEADER}{Colors.BOLD}")
    print("╔════════════════════════════════════════════════════════╗")
    print("║     DASHBOARD AMBIENTAL - Generador JSON HTTP          ║")
    print("║              INFO1128 - Proyecto #3                    ║")
    print("╚════════════════════════════════════════════════════════╝")
    print(f"{Colors.ENDC}")

def generar_datos_json():
    """
    Genera el JSON con datos aleatorios de sensores ambientales
    
    Returns:
        dict: Diccionario con los datos de sensores
    """
    datos = {
        "timestamp": datetime.now().isoformat(),
        "temperatura": round(random.uniform(*RANGOS['temperatura']), 2),
        "humedad": round(random.uniform(*RANGOS['humedad']), 2),
        "presion": round(random.uniform(*RANGOS['presion']), 2),
        "calidad_aire": round(random.uniform(*RANGOS['calidad_aire']), 2),
        "luminosidad": round(random.uniform(*RANGOS['luminosidad']), 2),
        "co2": round(random.uniform(*RANGOS['co2']), 2)
    }
    return datos

def enviar_a_nodered(datos):
    """
    Envía datos a Node-RED via HTTP POST
    
    Args:
        datos (dict): Diccionario con los datos a enviar
        
    Returns:
        bool: True si el envío fue exitoso, False en caso contrario
    """
    try:
        response = requests.post(
            URL_NODERED, 
            json=datos,
            timeout=3,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            print(f"{Colors.OKGREEN}  ✓ Node-RED: OK ({response.status_code}){Colors.ENDC}")
            return True
        else:
            print(f"{Colors.WARNING}  ⚠ Node-RED: {response.status_code}{Colors.ENDC}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"{Colors.FAIL}  ✗ Node-RED: Error de conexión (¿está corriendo?){Colors.ENDC}")
        return False
    except requests.exceptions.Timeout:
        print(f"{Colors.FAIL}  ✗ Node-RED: Timeout{Colors.ENDC}")
        return False
    except Exception as e:
        print(f"{Colors.FAIL}  ✗ Node-RED: {str(e)}{Colors.ENDC}")
        return False

def enviar_a_grafana(datos):
    """
    Envía datos a Grafana via HTTP POST
    
    Args:
        datos (dict): Diccionario con los datos a enviar
        
    Returns:
        bool: True si el envío fue exitoso, False en caso contrario
    """
    try:
        # Nota: La URL de Grafana debe configurarse según tu instalación
        # Este es un ejemplo genérico
        response = requests.post(
            URL_GRAFANA, 
            json=datos,
            timeout=3,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code in [200, 204]:
            print(f"{Colors.OKGREEN}  ✓ Grafana: OK ({response.status_code}){Colors.ENDC}")
            return True
        else:
            print(f"{Colors.WARNING}  ⚠ Grafana: {response.status_code}{Colors.ENDC}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"{Colors.WARNING}  ⚠ Grafana: No disponible (opcional){Colors.ENDC}")
        return False
    except requests.exceptions.Timeout:
        print(f"{Colors.FAIL}  ✗ Grafana: Timeout{Colors.ENDC}")
        return False
    except Exception as e:
        print(f"{Colors.WARNING}  ⚠ Grafana: {str(e)}{Colors.ENDC}")
        return False

def mostrar_datos(datos, contador):
    """
    Muestra los datos generados en la consola
    
    Args:
        datos (dict): Datos de sensores
        contador (int): Número de envío
    """
    print(f"\n{Colors.OKCYAN}{Colors.BOLD}─────────────────────────────────────────────────────────{Colors.ENDC}")
    print(f"{Colors.BOLD}📊 Envío #{contador} - {datos['timestamp']}{Colors.ENDC}")
    print(f"{Colors.OKCYAN}─────────────────────────────────────────────────────────{Colors.ENDC}")
    
    # Mostrar valores con colores según umbrales
    temp = datos['temperatura']
    temp_color = Colors.OKGREEN if 18 <= temp <= 26 else Colors.WARNING
    print(f"  🌡️  Temperatura:     {temp_color}{temp:>7.2f}°C{Colors.ENDC}")
    
    hum = datos['humedad']
    hum_color = Colors.OKGREEN if 40 <= hum <= 70 else Colors.WARNING
    print(f"  💧 Humedad:         {hum_color}{hum:>7.2f}%{Colors.ENDC}")
    
    pres = datos['presion']
    pres_color = Colors.OKGREEN if 980 <= pres <= 1020 else Colors.WARNING
    print(f"  🔽 Presión:         {Colors.OKBLUE}{pres:>7.2f} hPa{Colors.ENDC}")
    
    aqi = datos['calidad_aire']
    if aqi <= 50:
        aqi_color = Colors.OKGREEN
    elif aqi <= 100:
        aqi_color = Colors.OKCYAN
    elif aqi <= 150:
        aqi_color = Colors.WARNING
    else:
        aqi_color = Colors.FAIL
    print(f"  🏭 Calidad Aire:    {aqi_color}{aqi:>7.2f} AQI{Colors.ENDC}")
    
    lux = datos['luminosidad']
    lux_color = Colors.OKGREEN if lux > 300 else Colors.WARNING
    print(f"  💡 Luminosidad:     {lux_color}{lux:>7.2f} lux{Colors.ENDC}")
    
    co2 = datos['co2']
    co2_color = Colors.OKGREEN if co2 < 800 else Colors.WARNING if co2 < 1500 else Colors.FAIL
    print(f"  🌫️  CO2:             {co2_color}{co2:>7.2f} ppm{Colors.ENDC}")
    
    print(f"\n{Colors.BOLD}📤 Enviando datos...{Colors.ENDC}")

def verificar_conexiones():
    """
    Verifica que los servicios estén disponibles antes de iniciar
    
    Returns:
        bool: True si al menos Node-RED está disponible
    """
    print(f"\n{Colors.BOLD}🔍 Verificando conexiones...{Colors.ENDC}\n")
    
    servicios_ok = 0
    
    # Verificar Node-RED
    try:
        response = requests.get("http://localhost:1880", timeout=2)
        print(f"{Colors.OKGREEN}  ✓ Node-RED está corriendo en puerto 1880{Colors.ENDC}")
        servicios_ok += 1
    except:
        print(f"{Colors.FAIL}  ✗ Node-RED NO está disponible{Colors.ENDC}")
        print(f"{Colors.WARNING}    Inicia Node-RED con: node-red{Colors.ENDC}")
    
    # Verificar Grafana (opcional)
    try:
        response = requests.get("http://localhost:3000", timeout=2)
        print(f"{Colors.OKGREEN}  ✓ Grafana está corriendo en puerto 3000{Colors.ENDC}")
        servicios_ok += 1
    except:
        print(f"{Colors.WARNING}  ⚠ Grafana no está disponible (opcional){Colors.ENDC}")
    
    print()
    
    if servicios_ok == 0:
        print(f"{Colors.FAIL}❌ No hay servicios disponibles. No se puede continuar.{Colors.ENDC}")
        return False
    
    return True

def guardar_log(datos, exito_nodered, exito_grafana):
    """
    Guarda un log de los envíos
    
    Args:
        datos (dict): Datos enviados
        exito_nodered (bool): Si el envío a Node-RED fue exitoso
        exito_grafana (bool): Si el envío a Grafana fue exitoso
    """
    try:
        with open('logs/json_http.log', 'a') as f:
            f.write(f"{datos['timestamp']} | NodeRED: {exito_nodered} | Grafana: {exito_grafana}\n")
    except:
        pass  # Si no se puede guardar el log, continuar

# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def main():
    """Función principal del programa"""
    
    # Mostrar banner
    imprimir_banner()
    
    # Verificar conexiones
    if not verificar_conexiones():
        sys.exit(1)
    
    print(f"{Colors.OKGREEN}✅ Listo para enviar datos{Colors.ENDC}")
    print(f"{Colors.BOLD}Intervalo de envío: {INTERVALO_ENVIO} segundos{Colors.ENDC}")
    print(f"{Colors.WARNING}Presiona Ctrl+C para detener{Colors.ENDC}\n")
    
    time.sleep(2)
    
    contador = 0
    estadisticas = {
        'enviados': 0,
        'nodered_ok': 0,
        'grafana_ok': 0,
        'errores': 0
    }
    
    try:
        while True:
            contador += 1
            estadisticas['enviados'] += 1
            
            # Generar datos
            datos = generar_datos_json()
            
            # Mostrar datos
            mostrar_datos(datos, contador)
            
            # Enviar a Node-RED
            exito_nodered = enviar_a_nodered(datos)
            if exito_nodered:
                estadisticas['nodered_ok'] += 1
            
            # Enviar a Grafana
            exito_grafana = enviar_a_grafana(datos)
            if exito_grafana:
                estadisticas['grafana_ok'] += 1
            
            # Contar errores
            if not exito_nodered and not exito_grafana:
                estadisticas['errores'] += 1
            
            # Guardar log
            guardar_log(datos, exito_nodered, exito_grafana)
            
            # Mostrar estadísticas
            print(f"\n{Colors.BOLD}📈 Estadísticas:{Colors.ENDC}")
            print(f"   Total enviados: {estadisticas['enviados']}")
            print(f"   Node-RED OK: {estadisticas['nodered_ok']}")
            print(f"   Grafana OK: {estadisticas['grafana_ok']}")
            print(f"   Errores: {estadisticas['errores']}")
            
            # Esperar antes del próximo envío
            print(f"\n⏳ Esperando {INTERVALO_ENVIO} segundos...")
            time.sleep(INTERVALO_ENVIO)
            
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}⏸️  Deteniendo envío de datos...{Colors.ENDC}")
        print(f"\n{Colors.BOLD}📊 Resumen Final:{Colors.ENDC}")
        print(f"   Total enviados: {estadisticas['enviados']}")
        print(f"   Node-RED exitosos: {estadisticas['nodered_ok']}")
        print(f"   Grafana exitosos: {estadisticas['grafana_ok']}")
        print(f"   Errores totales: {estadisticas['errores']}")
        if estadisticas['enviados'] > 0:
            tasa_exito = ((estadisticas['nodered_ok'] + estadisticas['grafana_ok']) / 
                         (estadisticas['enviados'] * 2)) * 100
            print(f"   Tasa de éxito: {tasa_exito:.1f}%")
        print(f"\n{Colors.OKGREEN}✅ Programa finalizado correctamente{Colors.ENDC}\n")
        
    except Exception as e:
        print(f"\n{Colors.FAIL}❌ Error inesperado: {str(e)}{Colors.ENDC}")
        sys.exit(1)

# ============================================================
# PUNTO DE ENTRADA
# ============================================================

if __name__ == "__main__":
    # Crear directorio de logs si no existe
    os.makedirs('logs', exist_ok=True)
    
    # Ejecutar programa principal
    main()
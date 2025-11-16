# Dashboard Ambiental - INFO1128
## Proyecto #3 Interfaces Gráficas

### Descripción
Sistema de monitoreo ambiental en tiempo real con Python, Node-RED, Grafana y MQTT.

### Archivos del Proyecto
- `JSON.py` - HTTP POST a Node-RED y Grafana
- `mqtt_publisher.py` - Publicador MQTT
- `mqtt_subscriber.py` - Suscriptor MQTT

### Instalación
```bash
pip install -r requirements.txt
```

### Ejecución
```bash
# Terminal 1
python mqtt_publisher.py

# Terminal 2
python mqtt_subscriber.py

# Terminal 3
python JSON.py
```

### URLs
- Node-RED: http://localhost:1880
- Grafana: http://localhost:3000

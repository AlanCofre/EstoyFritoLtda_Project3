from flask import Flask, jsonify, request
from flask_cors import CORS
import time
import threading
from datetime import datetime

try:
    from generate_json import generate_sensor_data
except ImportError:
    print("="*50)
    print("ERROR: No se encontró el archivo 'generate_json.py'")
    print("Asegúrate de que esté en la misma carpeta que este script.")
    print("="*50)
    exit()

app = Flask(__name__)
CORS(app)

data_history = []

def generate_data_loop():
    while True:
        current_time = int(time.time() * 1000)
        data_nested = generate_sensor_data()
        data_flat = {
            'te': data_nested['dUMA']['environment']['temperature'],
            'hr': data_nested['dUMA']['environment']['humidity'],
            'pa': data_nested['dUMA']['environment']['air_pressure'],
            
            'p01': data_nested['dUMA']['air_quality']['pm1'],
            'p25': data_nested['dUMA']['air_quality']['pm25'],
            'p10': data_nested['dUMA']['air_quality']['pm10'],
            
            'h03': data_nested['dUMA']['particle_histogram']['h03'],
            'h05': data_nested['dUMA']['particle_histogram']['h05'],
            'h01': data_nested['dUMA']['particle_histogram']['h01'],
            'h25': data_nested['dUMA']['particle_histogram']['h25'],
            'h50': data_nested['dUMA']['particle_histogram']['h50'],
            'h10': data_nested['dUMA']['particle_histogram']['h10']
        }
        
        data_to_append = {'time': current_time}
        data_to_append.update(data_flat)
        data_history.append(data_to_append)
        
        if len(data_history) > 100:
            data_history.pop(0)

        print(f"""
[{datetime.now().strftime('%H:%M:%S')}] --- DATOS ---
    Ambientales:
        Temp: {data_flat['te']:.1f}°C
        Hum:  {data_flat['hr']:.1f}%
        Pres: {data_flat['pa']:.0f} hPa
    Material Particulado (PM):
        PM1.0: {data_flat['p01']:.1f} ug/m3
        PM2.5: {data_flat['p25']:.1f} ug/m3
        PM10:  {data_flat['p10']:.1f} ug/m3
    Histogramas (conteo de partículas):
        h03: {data_flat['h03']:.0f} | h05: {data_flat['h05']:.0f} | h01: {data_flat['h01']:.0f}
        h25: {data_flat['h25']:.0f} | h50: {data_flat['h50']:.0f} | h10: {data_flat['h10']:.0f}
""")
        
        time.sleep(5)

@app.route('/')
def index():
    return jsonify({'status': 'ok', 'message': 'Grafana Server Running', 'data_points': len(data_history)})

@app.route('/search', methods=['POST', 'GET'])
def search():
    """
    Devuelve la lista de métricas que Grafana puede consultar.
    """
    return jsonify([
        'te', 'hr', 'pa', 'p01', 'p25', 'p10', 
        'h03', 'h05', 'h01', 'h25', 'h50', 'h10'
    ])

@app.route('/query', methods=['POST'])
def query():
    req = request.get_json()
    data = []
    
    for target in req.get('targets', []):
      metric = target.get('target', 'te') 
      datapoints = [[int(d['time']), float(d[metric])] for d in data_history if metric in d]
      data.append({'target': metric, 'datapoints': datapoints})
    
    return jsonify(data)

@app.route('/annotations', methods=['POST'])
def annotations():
    return jsonify([])

if __name__ == '__main__':
    print("Servidor Grafana (Versión Proyecto Final) iniciando...")
    thread = threading.Thread(target=generate_data_loop, daemon=True)
    thread.start()
    time.sleep(3)
    app.run(host='0.0.0.0', port=5000, debug=False)
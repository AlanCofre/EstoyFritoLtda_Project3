import numpy as np

def generate_sensor_data():
    """
    Genera datos de sensores ambientales simulados
    Retorna un diccionario con estructura JSON completa
    """
    return {
        'dUMA': {
            'environment': {
                'temperature': round(np.random.normal(20, 2, 1)[0], 2),
                'humidity': round(np.random.normal(70, 2, 1)[0], 2),
                'air_pressure': round(np.random.normal(900, 10, 1)[0], 2)
            },
            'air_quality': {
                'iaq_index': int(np.random.normal(20, 2, 1)[0]),
                'pm1': round(np.random.normal(30, 2, 1)[0], 2),
                'pm25': round(np.random.normal(30, 2, 1)[0], 2),
                'pm10': round(np.random.normal(30, 2, 1)[0], 2)
            },
            'particle_histogram': {
                'h03': int(np.random.normal(1000, 10, 1)[0]),
                'h05': int(np.random.normal(1000, 10, 1)[0]),
                'h01': int(np.random.normal(1000, 10, 1)[0]),
                'h25': int(np.random.normal(1000, 10, 1)[0]),
                'h50': int(np.random.normal(1000, 10, 1)[0]),
                'h10': int(np.random.normal(1000, 10, 1)[0])
            }
        }
    }

if __name__ == '__main__':
    import json
    data = generate_sensor_data()
    print(json.dumps(data, indent=2))

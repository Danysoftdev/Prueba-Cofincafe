from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

def procesarDatos():
    
    archivoPersonal = pd.read_excel('Backend/Data/data1.xlsx')
    archivoFinanciero = pd.read_excel('Backend/Data/data2.xlsx')

    archivoFusionado = pd.merge(archivoPersonal, archivoFinanciero, on='nit')
    
    archivoFusionado['total'] = archivoFusionado['ingresos'] - archivoFusionado['egresos']

    estadisticas = {
        'Total Ingresos': archivoFusionado['ingresos'].sum(),
        'Total Egresos': archivoFusionado['egresos'].sum(),
        'Promedio Ingresos': archivoFusionado['ingresos'].mean(),
        'Promedio Egresos': archivoFusionado['egresos'].mean(),
        'Ingreso Máximo': archivoFusionado['ingresos'].max(),
        'Ingreso Mínimo': archivoFusionado['ingresos'].min(),
        'Egreso Máximo': archivoFusionado['egresos'].max(),
        'Egreso Mínimo': archivoFusionado['egresos'].min()
    }
    
    archivoEstadisticas = pd.DataFrame(list(estadisticas.items()), columns=['Descripcion', 'Valor'])
    
    estadisticas = {k: float(v) for k, v in estadisticas.items()}
    
    archivoFusionado.to_csv('Backend/Data/Results/datos.csv', index=False)
    archivoEstadisticas.to_csv('Backend/Data/Results/estadisticas.csv', index=False)
    
    return archivoFusionado.to_dict('records'), estadisticas

@app.route('/datos', methods=['GET'])
def obtenerInfo():
    datos, estadisticas = procesarDatos()
    return jsonify({'datos': datos, 'estadisticas': estadisticas})

if __name__ == '__main__':
    app.run(port=5000)  


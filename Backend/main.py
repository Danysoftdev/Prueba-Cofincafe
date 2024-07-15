from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import io

app = Flask(__name__)
CORS(app)

def process_data():
    
    archivoPersonal = pd.read_excel('Backend/Data/data1.xlsx')
    archivoFinanciero = pd.read_excel('Backend/Data/data2.xlsx')

    archivoFusionado = pd.merge(archivoPersonal, archivoFinanciero, on='NIT')
    
    archivoFusionado['Nombre Completo'] = archivoFusionado['Nombre'] + ' ' + archivoFusionado['Apellido']
    archivoFusionado['Total'] = archivoFusionado['Ingresos'] - archivoFusionado['Egresos']

    estadisticas = {
        'Total Ingresos': archivoFusionado['Ingresos'].sum(),
        'Total Egresos': archivoFusionado['Egresos'].sum(),
        'Promedio Ingresos': archivoFusionado['Ingresos'].mean(),
        'Promedio Egresos': archivoFusionado['Egresos'].mean(),
        'Ingreso Máximo': archivoFusionado['Ingresos'].max(),
        'Ingreso Mínimo': archivoFusionado['Ingresos'].min(),
        'Egreso Máximo': archivoFusionado['Egresos'].max(),
        'Egreso Mínimo': archivoFusionado['Egresos'].min()
    }
    
    archivoEstadisticas = pd.DataFrame(list(estadisticas.items()), columns=['Descripcion', 'Valor'])
    
    archivoFusionado.to_csv('Backend/Data/Results/base_data.csv', index=False)
    archivoEstadisticas.to_excel('Backend/Data/Results/statistics.csv', index=False)

    return archivoFusionado.to_dict('records'), estadisticas

@app.route('/datos', methods=['GET'])
def get_info():
    datos, estadisticas = process_data()
    return jsonify({'data': datos, 'stats': estadisticas})


import os
import csv
from datetime import datetime
from mrjob.job import MRJob
from mrjob.step import MRStep

class ProcesarArchivoMR(MRJob):

    accion = 'REPSOL'  # Acción a procesar, establecida como atributo de clase

    def mapper(self, _, line):
        row = next(csv.reader([line]))  # Parsear la línea del archivo CSV
        nombre_accion = row[0]
        if nombre_accion == self.accion:
            yield None, {'valor_inicial': float(row[1].replace(',', '.')), 'minimo': float(row[6].replace(',', '.')), 'maximo': float(row[7].replace(',', '.'))}

    def reducer(self, _, valores):
        listado_mensual = {'valor_inicial': 0, 'minimo': float('inf'), 'maximo': float('-inf')}
        for valor in valores:
            listado_mensual['valor_inicial'] += valor['valor_inicial']
            listado_mensual['minimo'] = min(listado_mensual['minimo'], valor['minimo'])
            listado_mensual['maximo'] = max(listado_mensual['maximo'], valor['maximo'])
        yield None, listado_mensual

if __name__ == '__main__':
    accion = 'REPSOL'          # Cambiar a la acción correcta
    fecha_inicio = '01-05-2024'  # Formato día-mes-año
    fecha_fin = '10-05-2024'     # Formato día-mes-año

    archivos_csv = [archivo for archivo in os.listdir() if archivo.endswith('.csv')]
    archivos_input = []
    for archivo in archivos_csv:
        archivos_input.append(archivo)

    mr_job = ProcesarArchivoMR(args=archivos_input)
    mr_job.accion = accion  # Establecer la acción en el objeto mr_job
    with mr_job.make_runner() as runner:
        runner.run()
        for _, resultado in mr_job.parse_output(runner.cat_output()):
            if resultado:
                print("Listado Mensual:", resultado)
                print(f"Valor mínimo de cotización para {accion}: {resultado['minimo']}")
                print(f"Valor máximo de cotización para {accion}: {resultado['maximo']}")
            else:
                print(f"No se encontraron datos para la acción {accion} en el rango de fechas proporcionado.")
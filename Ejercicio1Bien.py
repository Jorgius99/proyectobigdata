import sys
from mrjob.job import MRJob
import csv
import os
from datetime import datetime

class Ejercicio1Bien(MRJob):

    def obtener_semana_actual(self):
        return datetime.now().strftime('%U')

    def obtener_semana_archivo(self, nombre_archivo):
        try:
            fecha_str = nombre_archivo.split('.')[0]  # Obtener la parte del título sin la extensión
            fecha = datetime.strptime(fecha_str, '%d-%m-%Y')
            return fecha.strftime('%U')  # Devolver el número de semana
        except (IndexError, ValueError):
            return None

    def mapper(self, _, line):
        try:
            row = next(csv.reader([line]))  # Parsear la línea CSV
            if len(row) >= 5:  # Verificar si la fila tiene al menos 5 elementos (nombre de acción + 4 valores)
                accion = row[0]
                valor_inicial = float(row[1].replace(',', '.'))  # Reemplazar ',' por '.' para asegurar el formato float
                valor_final = float(row[5].replace(',', '.'))  # El valor final está en la posición 5
                minimo = float(row[6].replace(',', '.'))  # El mínimo está en la posición 6
                maximo = float(row[7].replace(',', '.'))  # El máximo está en la posición 7

                semana_actual = self.obtener_semana_actual()
                nombre_archivo = sys.argv[1]  # Obtener el nombre del archivo CSV directamente de sys.argv
                semana_archivo = self.obtener_semana_archivo(nombre_archivo)  # Obtener el número de semana del archivo actual

                if semana_archivo != semana_actual:
                    yield "Error", f"El archivo {nombre_archivo} no está en la semana actual."
                    return

                yield accion, {'valor_inicial': valor_inicial, 'valor_final': valor_final, 'minimo': minimo, 'maximo': maximo}
        except Exception as e:
            yield "Error", f"Error al procesar la línea: {e}"

    def reducer(self, key, values):
        if key == "Error":
            for value in values:
                yield key, value
        else:
            resultados = {'valor_inicial': 0, 'valor_final': 0, 'minimo': float('inf'), 'maximo': float('-inf')}
            for valor in values:
                resultados['valor_inicial'] += valor['valor_inicial']
                resultados['valor_final'] += valor['valor_final']
                resultados['minimo'] = min(resultados['minimo'], valor['minimo'])
                resultados['maximo'] = max(resultados['maximo'], valor['maximo'])
            yield key, resultados

if __name__ == '__main__':
    Ejercicio1Bien.run()
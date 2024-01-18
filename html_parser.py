""" 
Parseador de contenido HTML dentro de columnas en archivo CSV
dev.nicomartinez@gmail.com
"""

import csv
from bs4 import BeautifulSoup

class CSV_cleaner:
    def __init__(self, csv_path:str) -> None:
        
        self.csv_path = csv_path
        self.new_csv_file = 'curated_' + csv_path.split(' ')[0] + '.csv'

        self.evento_actual = None

    def clean_csv(self) -> None:

        with open(self.csv_path, 'r', encoding='utf-8') as file:
            with open(self.new_csv_file, 'a', encoding='utf-8') as ouput_file:
                reader = csv.reader(file, delimiter='|')

                chunk = []
                # Modificar el tamaño del chunk a gusto y capacidad de memoria
                chunk_size = 100

                #escribo el header
                prev_line = next(reader)

                for line in reader:
                    
                    #si el nro de la linea actual es diferente al de la linea anterior:
                    if line[0] != prev_line[0]:
                        #hago un parsing de los tags HTML de la columna "respuestas"
                        prev_line[-1] = self.parse_html(prev_line[-1])
                        #luego empujo la linea dentro del chunk de lineas
                        chunk.append(prev_line)

                        #transformo la linea previa en la nueva linea vista
                        prev_line = line

                    else:
                        #si ambas lineas contenian el mismo nro de reporte, entonces sumo los valores de las respuestas
                        prev_line[-1] += line[-1]

                    
                    #si el chunk esta lleno:
                    if len(chunk) == chunk_size:

                        for line in chunk:
                            ouput_file.write('|'.join(line) + '\n')
                        chunk = []

                # escribo las ultimas lineas del chunk
                else:
                    for line in chunk:
                            ouput_file.write('|'.join(line) + '\n')

                    ouput_file.flush()


    def parse_html(self, html_text) -> str:

        parsed_A = BeautifulSoup(html_text, 'html.parser').get_text()
        return  parsed_A


if __name__ == '__main__':    
    cleaner = CSV_cleaner('ReporteRedmine556204 - pipes.txt')

    cleaner.clean_csv()


        

            

from zipfile import ZipFile
import pandas as pd
from tqdm import tqdm

archivo_zip = "input/ddjj.zip"

# Especifica la carpeta de destino donde se extraerán los archivos
carpeta_destino = "input/ddjj"

with ZipFile(archivo_zip, 'r') as archivo_zip:
    # Obtiene una lista de los nombres de los archivos en el ZIP
    archivos = archivo_zip.namelist()

    # Utiliza tqdm para crear una barra de progreso
    for archivo in tqdm(archivos, desc="Descomprimiendo"):
        # Extrae el archivo actual en la carpeta de destino
        archivo_zip.extract(archivo, carpeta_destino)

print(f"Archivos descomprimidos en: {carpeta_destino}")


def open_csv_file(csv):
    file = "input/csv/" + csv + ".csv"
    data = pd.read_csv(file, sep=';', decimal=',')
    return pd.DataFrame(data)


def open_txt_file(txt):
    file = "input/ddjj/" + txt + ".txt"
    data = pd.read_csv(file, header=None, sep=';', decimal=',')
    data[8] = data[8].str.lstrip('0').astype(float)
    # column_names = ['Columna1', 'Columna2', 'Columna3']
    #
    # # Asigna los nombres de columna al DataFrame
    # df.columns = column_names


    return pd.DataFrame(data)

from zipfile import ZipFile
import pandas as pd
from tqdm import tqdm

# Especifica la carpeta de destino donde se extraerán los archivos
carpeta_input = "input/"


def unzip_file(name):
    with ZipFile(carpeta_input + name, 'r') as archivo_zip:
        # Obtiene una lista de los nombres de los archivos en el ZIP
        archivos = archivo_zip.namelist()

        # Utiliza tqdm para crear una barra de progreso
        for archivo in tqdm(archivos, desc="Descomprimiendo " + name):
            # Extrae el archivo actual en la carpeta de destino
            archivo_zip.extract(archivo, carpeta_input)

    print(f"Archivos descomprimidos en: {carpeta_input}")


def open_csv_file(name):
    file = carpeta_input + name
    data = pd.read_csv(file, sep=';', decimal=',')
    print(f"Archivo abierto correctamente: -> {file}")
    return pd.DataFrame(data)


def open_txt_file(name):
    file = carpeta_input + name
    data = pd.read_csv(file, header=None, sep=';', decimal=',')
    data[8] = data[8].str.lstrip('0').astype(float)
    print(f"Archivo abierto correctamente: -> {file}")
    return pd.DataFrame(data)

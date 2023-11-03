from zipfile import ZipFile
import pandas as pd
from tqdm import tqdm
from config import path


# Especifica la carpeta de destino donde se extraerán los archivos


def open_csv_file(name):
    file = path + name
    data = pd.read_csv(file, sep=';', decimal=',')
    return pd.DataFrame(data)


def split_detalle_quincena(detalle):
    detalle['Date'] = pd.to_datetime(detalle['Date']).dt.date
    detalle_filtrado = detalle.query('VoidDate.isnull()')

    fecha_inicio = detalle_filtrado['Date'].min()  # Fecha más temprana
    fecha_final = detalle_filtrado['Date'].max()  # Fecha más reciente

    # Calcula la fecha intermedia para dividir en quincenas
    fecha_intermedia = fecha_inicio + pd.DateOffset(days=14)

    # Filtra el DataFrame para la primera quincena
    primera_quincena = detalle_filtrado[detalle_filtrado['Date'] <= fecha_intermedia.date()]
    print(primera_quincena)
    # Filtra el DataFrame para la segunda quincena
    segunda_quincena = detalle_filtrado[detalle_filtrado['Date'] > fecha_intermedia.date()]
    print(segunda_quincena)
    return primera_quincena, segunda_quincena


def open_900_txt_file(name):
    file = path + name
    data = pd.read_csv(file, header=None, sep=';', decimal=',')
    data[8] = data[8].str.lstrip('0').astype(float)
    data.columns = ['CUIT', 'CRC', 'FechaLiq', 'FechaRet', 'NroLiq', 'CantOperaciones', 'Base', 'Alicuota', 'Retencion',
                    'TipoRegistro', 'OpeEx', 'Jurisdiccion']
    return pd.DataFrame(data)


def open_921_txt_file(name):
    file = path + name
    data = pd.read_csv(file, header=None, sep=',', decimal='.')
    data[7] = data[7].astype(float)
    print(f"Archivo abierto correctamente: -> {file}")
    data.columns = ['Renglon', 'TipoComprobante', 'LetraComprobante', 'NroLiq', 'CUIT', 'FechaRet', 'Base', 'Alicuota',
                    'Retencion', 'Regimen', 'Jurisdiccion']
    return pd.DataFrame(data)

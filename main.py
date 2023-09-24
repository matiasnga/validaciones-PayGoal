import zipfile
from zipfile import ZipFile
import pandas as pd
from tqdm import tqdm


def string_to_float(string, i, archivo):
    return round(float(archivo.at[i, string].replace(",", ".")), 2)


def open_csv_file(archivo):
    file = "input/csv/" + archivo + ".csv"
    data = pd.read_csv(file, sep=';')
    return pd.DataFrame(data)


def open_txt_file(archivo):
    file = "input/ddjj/" + archivo + ".txt"
    column_types = {6: float, 7: float, 8: float}  # Especifica los tipos de datos para las columnas 6, 7 y 8

    data = pd.read_csv(file, header=None, sep=';', decimal=',')
    data[8] = data[8].str.lstrip('0').astype(float)

    return pd.DataFrame(data)


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

resumen = open_csv_file("2023-09 1 - resumen")
print("Archivo resumen abierto correctamente")
detalle = open_csv_file("2023-09 1 - detalle")
print("Archivo detalle abierto correctamente")
txt_900 = open_txt_file("900 - 2023-09 1")
print("Archivo ddjj 900 abierto correctamente")

for tax_id in range(7):
    tax = resumen.at[tax_id, 'TaxId']
    total_valor = resumen.at[tax_id, 'Total']

sum_900_resumen = resumen.at[2, 'Total']
sum_900_detalle = 0
sum_900_txt = 0

for tx in range(len(detalle)):
    if pd.isnull(detalle.at[tx, 'VoidDate']):
        sum_900_detalle += string_to_float('TaxCollectionAmount3', tx, detalle)

for ddjj in range(len(txt_900)):
    sum_900_txt += txt_900.at[ddjj, 8]
    sum_900_txt = round(sum_900_txt, 2)

if sum_900_detalle == sum_900_detalle == sum_900_txt:
    print("TaxId: 900 Reporte vs Detalle vs Txt OK ----> $" + "{:,.2f}".format(sum_900_detalle))
else:
    print(sum_900_detalle)
    print(sum_900_resumen)
    print(sum_900_txt)

for linea in tqdm(range(len(txt_900)), desc="Procesando líneas"):
    a2_cuit = txt_900.at[linea, 0]
    x2_dia = txt_900.at[linea, 2][:2]
    c2_date = txt_900.at[linea, 2]
    y2_cert_number = int(txt_900.at[linea, 4][-8:])
    l2_jurisdiccion = txt_900.at[linea, 11]
    i2_retencion = txt_900.at[linea, 8]

    cond1 = (detalle['ShopId'] == a2_cuit)
    cond2 = (pd.isna(detalle['VoidDate']))
    # cond3 = ((x2_dia == 15) & (detalle['Date'] < c2_date + 1)) | ((x2_dia != 15) & (detalle['Date'] >=
    # pd.to_datetime(c2_date).replace(day=16)))
    cond4 = (detalle['TaxCollectionNo3'] == y2_cert_number)
    cond5 = (detalle['TurnoverTax'] == l2_jurisdiccion)

    # Filtrar el DataFrame con las condiciones y crear una copia independiente
    filtrado = detalle[cond1 & cond2 & cond4 & cond5].copy()

    # Reemplazar comas por puntos en la columna 'TaxCollectionAmount3' y convertir a float
    filtrado['TaxCollectionAmount3'] = filtrado['TaxCollectionAmount3'].str.replace(',', '.').astype(float)

    # Calcular la suma de la columna 'TaxCollectionAmount3'
    resultado = filtrado['TaxCollectionAmount3'].sum()

    if round(resultado, 2) != i2_retencion:
        tax_condition = detalle[cond1 & cond2 & cond4 & cond5]['TaxCondition3'].iloc[0]
        shop_id = detalle[cond1 & cond2 & cond4 & cond5]['ShopId'].iloc[0]
        print(str(shop_id))
        print(str(tax_condition))
        to_print = "dif:" + str(round(resultado - i2_retencion, 2)), "cert: " + str(y2_cert_number), "total: " + str(
            round(resultado, 2))
        print(str(a2_cuit) + " - " + str(to_print))
        print('------------------')

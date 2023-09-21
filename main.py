import pandas as pd


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

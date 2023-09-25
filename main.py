import pandas as pd
from tqdm import tqdm
import file_utils
import validation_900

file_utils.unzip_file("csv.zip")
file_utils.unzip_file('ddjj.zip')

resumen = file_utils.open_csv_file("2023-09 1 - resumen.csv")
detalle = file_utils.open_csv_file("2023-09 1 - detalle.csv")
txt_900 = file_utils.open_900_txt_file("900 - 2023-09 1.txt")
txt_921 = file_utils.open_921_txt_file("921 - 2023-09 1 Retención.txt")

sum_900_resumen = resumen.loc[resumen['TaxId'] == 900, 'Total']
sum_900_detalle = detalle[(detalle['VoidDate'].isnull())]['TaxCollectionAmount3'].sum()
sum_900_txt = txt_900['Retencion'].sum()

print("VALIDACION SIRTAC (900): ")

if sum_900_detalle == sum_900_detalle == sum_900_txt:
    print("TaxId: 900 Reporte vs Detalle vs Txt OK ----> $" + "{:,.2f}".format(sum_900_txt))
else:
    print(sum_900_detalle)
    print(sum_900_resumen)
    print(sum_900_txt)

# validation_900.validation_900(txt_900, detalle)
print("------------------------------")

print("VALIDACION SANTA FE (921): ")
sum_921_resumen = round(resumen.loc[resumen['TaxId'] == 921, 'Total'], 2)
sum_921_detalle = round(
    detalle[(detalle['VoidDate'].isnull()) & (detalle['TurnoverTax'] == 921)]['TaxCollectionAmount4'].sum(), 2)
sum_921_txt = round(txt_921['Retencion'].sum(), 2)

if sum_921_detalle == sum_921_detalle == sum_921_txt:
    print("TaxId: 921 Reporte vs Detalle vs Txt OK ----> $" + "{:,.2f}".format(sum_921_txt))
else:
    print(sum_921_detalle)
    print(sum_921_resumen)
    print(sum_921_txt)

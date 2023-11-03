import pandas as pd
import file_utils
import validation_900
from config import cliente, periodo, path

pd.set_option('display.max_colwidth', None)
pd.set_option('display.expand_frame_repr', False)


detalle = file_utils.open_csv_file('2023-10 2 - detalle.csv')
resumen = file_utils.open_csv_file("2023-10 2 - resumen.csv")

# txt_900_1 = file_utils.open_900_txt_file("900 - 2023-10 1.txt")
txt_900_2 = file_utils.open_900_txt_file("900 - 2023-10 2.txt")


primera_quincena, segunda_quincena = file_utils.split_detalle_quincena(detalle)

# # txt_921 = file_utils.open_921_txt_file("921 - 2023-09 1 Retención.txt")
# # #
# # sum_900_resumen = float(resumen.loc[resumen['TaxId'] == 900, 'Total'].iloc[0])
# # sum_900_detalle = round(float(detalle_filtrado['TaxCollectionAmount3'].sum()), 2)
# # sum_900 = float(txt_900_2['Retencion'].sum())
#
# print("VALIDACION SIRTAC (900): ")
# #
# if sum_900_resumen == sum_900_detalle == sum_900:
#     print("TaxId: 900 Reporte vs Detalle vs Txt OK ----> $" + "{:,.2f}".format(sum_900_detalle))
# else:
#     print(sum_900_resumen)
#     print(round(sum_900_detalle, 2))
#     print(sum_900)
# print("------------------------------")
#
validation_900.validation_900(txt_900_2, segunda_quincena)
# print("------------------------------")
#
# print("VALIDACION SANTA FE (921): ")
# sum_921_resumen = round(resumen.loc[resumen['TaxId'] == 921, 'Total'], 2)
# sum_921_detalle = round(
#     detalle[(detalle['VoidDate'].isnull()) & (detalle['TurnoverTax'] == 921)]['TaxCollectionAmount4'].sum(), 2)
# sum_921_txt = round(txt_921['Retencion'].sum(), 2)
#
# if sum_921_detalle == sum_921_detalle == sum_921_txt:
#     print("TaxId: 921 Reporte vs Detalle vs Txt OK ----> $" + "{:,.2f}".format(sum_921_txt))
# else:
#     print(sum_921_detalle)
#     print(sum_921_resumen)
#     print(sum_921_txt)

import file_utils
import validation
from datetime import datetime
from tqdm import tqdm

import pandas as pd

pd.set_option('display.max_colwidth', None)
pd.set_option('display.expand_frame_repr', False)


def calcular_sumifs(row, detalle):
    cuit = row['CUIT']  # Asumiendo que A1326 está en la fila 1326 (índice 1325)
    C1 = row['FechaLiq']
    L1 = row['Jurisdiccion']
    Y1 = int(str(row['NroLiq'])[-8:])
    X1 = C1.day

    cond1 = detalle['ShopId'] == cuit

    if X1 == 15:
        fecha_referencia = datetime(year=C1.year, month=C1.month, day=16)
        cond3 = (detalle['Date'] < C1 + pd.Timedelta(days=1)) & (detalle['Date'] >= fecha_referencia)
    else:
        cond3 = pd.Series([True] * len(detalle))  # Si X1326 no es 15, no aplicar esta condición

    cond4 = detalle['TaxCollectionNo3'] == Y1
    cond5 = detalle['TurnoverTax'] == L1

    resultado = detalle[cond1 & cond3 & cond4 & cond5]['TaxCollectionAmount3'].sum()
    resultado_redondeado = round(resultado, 2)
    print((resultado_redondeado))
    # return resultado_redondeado


def sirtac_900(detalle, resumen, cuit_agente, periodo):
    path = f"input/{cuit_agente}/{periodo}"
    txt_900 = validation.open_900_txt_file(cuit_agente, periodo)
    print(txt_900)

    for index, row in tqdm(txt_900.iterrows(), desc='Validando SIRTAC (900)'):
        calcular_sumifs(row, detalle)
        txt_900.at[index, 'columna_u'] = str(u)

        txt_900.at[index, 'columna_v'] = v
        txt_900.at[index, 'columna_w'] = w
        txt_900.at[index, 'columna_x'] = x
        txt_900.at[index, 'columna_y'] = y

    print(txt_900)
    archivo_reporte = f"{path}/validacion/900_{detalle.iloc[0]['Date']}.xlsx"
    txt_900.to_excel(archivo_reporte, index=False)

#
# def row_validation_file(tax_id, resumen, detalle, txt_921):
#     resumen_fila = resumen[resumen['TaxId'] == tax_id].iloc[0]
#
#     nueva_fila = {
#         'tax_id': tax_id,
#         'tax_collection_type': 'RET',
#         'resumen_1_fortnight': resumen_fila['1stFortnight'],
#         'resumen_2_fortnight': resumen_fila['2stFortnight'],
#         'total_resumen': resumen_fila['Total'],
#         'total_detalle': round(detalle[detalle['TaxId4'] == tax_id]['TaxCollectionAmount4'].sum(), 2),
#         'resumen_vs_detalle': resumen_fila['Total'] - round(
#             detalle[detalle['TaxId4'] == tax_id]['TaxCollectionAmount4'].sum(), 2),
#         '1_fortnight_txt': txt_1_fortnight,
#         '1_txt_vs_detalle': resumen_fila['1stFortnight'] - txt_1_fortnight
#     }
#     return

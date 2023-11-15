import file_utils
import validation
from datetime import datetime
from tqdm import tqdm

import pandas as pd

pd.set_option('display.max_colwidth', None)
pd.set_option('display.expand_frame_repr', False)


def calcular_sumifs(row, detalle_df):
    cuit = row['CUIT']
    fecha_ret = row['FechaRet']
    dia_cert = fecha_ret.day
    cert = int(str(row['NroLiq'])[-8:])
    cond1 = detalle_df['ShopId'] == cuit
    cond2 = detalle_df['TaxId4'] == 921
    type(fecha_ret)
    type(detalle_df['Date'])
    if dia_cert == 15:
        inicio_mes = datetime(fecha_ret.year, fecha_ret.month, 1).date()
        cond3 = (detalle_df['Date'] >= inicio_mes) & (detalle_df['Date'] < fecha_ret + pd.Timedelta(days=1))
        cond4 = detalle_df['TaxCollectionType'] == 'RET'
        suma = detalle_df[cond1 & cond2 & cond3 & cond4]['TaxCollectionAmount4'].sum()
        return round(suma, 2), round(row['Retencion'] - suma, 2), dia_cert, cert


def sf_921(detalle, resumen, cuit_agente, periodo):
    path = f"input/{cuit_agente}/{periodo}"
    txt_921 = validation.open_921_txt_file(cuit_agente, periodo)
    print(txt_921)

    for index, row in tqdm(txt_921.iterrows(), desc='Validando SANTA FE (921)'):
        v, w, x, y = calcular_sumifs(row, detalle)
        txt_921.at[index, 'columna_v'] = v
        txt_921.at[index, 'columna_w'] = w
        txt_921.at[index, 'columna_x'] = x
        txt_921.at[index, 'columna_y'] = y
        txt_921.at[index, 'columna_z'] = 'RET'


    print(txt_921)
    archivo_reporte = f"{path}/validacion/921_{detalle.iloc[0]['Date']}.xlsx"
    txt_921.to_excel(archivo_reporte, index=False)
#
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

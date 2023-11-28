from datetime import datetime
from tqdm import tqdm
import file_utils
import pandas as pd


def calcular_suma_924(row, detalle):
    cuit = int(row['numero_documento'])
    fecha_ret = row['fecha_retencion']
    dia_cert = fecha_ret.day
    cert = int(str(row['numero_certificado'])[-8:])
    cond1 = detalle['ShopId'] == cuit
    cond2 = detalle['TaxId4'] == 924
    if dia_cert == 15:
        inicio_mes = datetime(fecha_ret.year, fecha_ret.month, 1).date()
        cond3 = (detalle['Date'] >= inicio_mes) & (detalle['Date'] < fecha_ret + pd.Timedelta(days=1))
        cond4 = detalle['TaxCollectionType'] == 'RET'
        resultado = detalle[cond1 & cond2 & cond3 & cond4]

        if not resultado.empty:
            tax_condition = resultado['TaxCondition4'].iloc[0]
        else:
            tax_condition = None  # O un valor por defecto apropiado
        suma = round(resultado['TaxCollectionAmount4'].sum(), 2)
        return tax_condition, round(suma, 2), round(row['retencion'] - suma, 2), dia_cert, cert

    if dia_cert != 15:
        inicio_mes = datetime(fecha_ret.year, fecha_ret.month, 16).date()
        cond3 = (detalle['Date'] >= inicio_mes) & (detalle['Date'] < fecha_ret + pd.Timedelta(days=1))
        cond4 = detalle['TaxCollectionType'] == 'RET'

        resultado = detalle[cond1 & cond2 & cond3 & cond4]

        if not resultado.empty:
            tax_condition = resultado['TaxCondition4'].iloc[0]
        else:
            tax_condition = None  # O un valor por defecto apropiado
        suma = round(resultado['TaxCollectionAmount4'].sum(), 2)
        return tax_condition, round(suma, 2), round(row['retencion'] - suma, 2), dia_cert, cert


def tax_924(detalle, cuit_agente, periodo):
    ddjj = file_utils.open_tucuman_txt_file( cuit_agente, periodo)

    ddjj['tax_condition'] = pd.NA
    ddjj['tax_condition'] = ddjj['tax_condition'].astype(str)

    for index, row in tqdm(ddjj.iterrows(), total=ddjj.shape[0],
                           desc=f'Validando TUCUMAN (924) {cuit_agente} {periodo}'):
        u, v, w, x, y = calcular_suma_924(row, detalle)
        ddjj.at[index, 'tax_condition'] = u
        ddjj.at[index, 'suma_reporte'] = v
        ddjj.at[index, 'diferencia'] = w
        ddjj.at[index, 'quincena'] = x
        ddjj.at[index, 'certificado'] = y

    with pd.ExcelWriter(f'validaciones/{cuit_agente} {periodo} reporte.xlsx', mode='a', engine='openpyxl') as writer:
        # Escribir el primer DataFrame en la primera hoja
        ddjj.to_excel(writer, sheet_name='tax_924', index=False)

    ddjj['fecha_retencion'] = pd.to_datetime(ddjj['fecha_retencion'])
    fortnight_1_txt = round(ddjj[ddjj['fecha_retencion'].dt.day == 15]['suma_reporte'].sum(), 2)
    count_1 = ddjj[(ddjj['fecha_retencion'].dt.day == 15) & (ddjj['certificado'] != 0)]['certificado'].count()
    max_1 = ddjj[(ddjj['fecha_retencion'].dt.day == 15) & (ddjj['certificado'] != 0)]['certificado'].max()
    ddjj['fecha_retencion'] = pd.to_datetime(ddjj['fecha_retencion'])
    fortnight_2_txt = round(ddjj[ddjj['fecha_retencion'].dt.day != 15]['suma_reporte'].sum(), 2)
    count_2 = ddjj[(ddjj['fecha_retencion'].dt.day != 15) & (ddjj['certificado'] != 0)]['certificado'].count()
    max_2 = ddjj[(ddjj['fecha_retencion'].dt.day != 15) & (ddjj['certificado'] != 0)]['certificado'].max()
    print(ddjj)
    return fortnight_1_txt, count_1, max_1, fortnight_2_txt, count_2, max_2

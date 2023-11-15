from datetime import datetime
from tqdm import tqdm
import file_utils
import pandas as pd


def calcular_suma_900(row, detalle):
    cuit = row['CUIT']
    fecha_liq = row['FechaLiq']
    jurisdiccion = row['Jurisdiccion']
    cert = int(str(row['NroLiq'])[-8:])
    dia_cert = fecha_liq.day

    cond1 = detalle['ShopId'] == cuit

    if dia_cert == 15:
        inicio_mes = datetime(fecha_liq.year, fecha_liq.month, 1).date()
        cond3 = (detalle['Date'] >= inicio_mes) & (detalle['Date'] < fecha_liq + pd.Timedelta(days=1))
        cond4 = detalle['TaxCollectionType'] == 'RET'

        cond4 = detalle['TaxCollectionNo3'] == cert
        cond5 = detalle['TurnoverTax'] == jurisdiccion

        resultado = detalle[cond1 & cond3 & cond4 & cond5]

        if not resultado.empty:
            tax_condition = resultado['TaxCondition3'].iloc[0]
        else:
            tax_condition = None
        suma = round(resultado['TaxCollectionAmount3'].sum(), 2)

        return tax_condition, round(suma, 2), round(row['Retencion'] - suma, 2), dia_cert, cert


def tax_900(detalle, cuit_agente, periodo):
    ddjj = file_utils.open_900_txt_file(cuit_agente, periodo)

    for index, row in tqdm(ddjj.iterrows(), total=ddjj.shape[0], desc='Validando SIRTAC (900)'):
        u, v, w, x, y = calcular_suma_900(row, detalle)
        ddjj.at[index, ' '] = ' '
        ddjj.at[index, 'condicion_fiscal'] = u
        ddjj.at[index, 'suma_reporte'] = v
        ddjj.at[index, 'diferencia'] = w
        ddjj.at[index, 'quincena'] = x
        ddjj.at[index, 'certificado'] = y
        ddjj.at[index, 'tipo_impuesto'] = 'RET'

    archivo_reporte = f"validaciones/{cuit_agente} {periodo} 900.xlsx"
    ddjj.to_excel(archivo_reporte, index=False)
    fortnight_1_txt = round(ddjj['suma_reporte'].sum(), 2)
    count_1 = ddjj[ddjj['certificado'] != 0]['certificado'].count()
    max_1 = ddjj[ddjj['certificado'] != 0]['certificado'].max()
    return fortnight_1_txt, count_1, max_1


def calcular_suma_921(row, detalle):
    cuit = row['CUIT']
    fecha_ret = row['FechaRet']
    dia_cert = fecha_ret.day
    cert = int(str(row['NroLiq'])[-8:])
    cond1 = detalle['ShopId'] == cuit
    cond2 = detalle['TaxId4'] == 921
    type(fecha_ret)
    type(detalle['Date'])
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
        return tax_condition, round(suma, 2), round(row['Retencion'] - suma, 2), dia_cert, cert


def tax_921(detalle, cuit_agente, periodo):
    ddjj = file_utils.open_921_txt_file(cuit_agente, periodo)

    for index, row in tqdm(ddjj.iterrows(), total=ddjj.shape[0], desc='Validando SANTA FE (921)'):
        u, v, w, x, y = calcular_suma_921(row, detalle)
        ddjj.at[index, ' '] = ' '
        ddjj.at[index, 'tax_condition'] = u
        ddjj.at[index, 'suma_reporte'] = v
        ddjj.at[index, 'diferencia'] = w
        ddjj.at[index, 'quincena'] = x
        ddjj.at[index, 'certificado'] = y
        ddjj.at[index, 'tipo_impuesto'] = 'RET'

    archivo_reporte = f"validaciones/{cuit_agente} {periodo} 921.xlsx"
    ddjj.to_excel(archivo_reporte, index=False)
    fortnight_1_txt = round(ddjj['suma_reporte'].sum(), 2)
    count_1 = ddjj[ddjj['certificado'] != 0]['certificado'].count()
    max_1 = ddjj[ddjj['certificado'] != 0]['certificado'].max()
    return fortnight_1_txt, count_1, max_1

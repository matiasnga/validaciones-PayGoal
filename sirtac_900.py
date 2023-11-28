from datetime import datetime
from tqdm import tqdm
import file_utils
import pandas as pd


def calcular_suma_900(ddjj, row, detalle):
    cuit = row['CUIT']
    fecha_liq = row['FechaLiq']
    jurisdiccion = row['Jurisdiccion']
    cert = int(str(row['NroLiq'])[-8:])
    dia_cert = fecha_liq.day
    cond1 = detalle['ShopId'] == cuit

    if dia_cert == 15:
        inicio_mes = datetime(fecha_liq.year, fecha_liq.month, 16).date()
        cond3 = (detalle['Date'] >= inicio_mes) & (detalle['Date'] < fecha_liq + pd.Timedelta(days=1))

        cond4 = detalle['TaxCollectionNo3'] == cert
        cond5 = detalle['TurnoverTax'] == jurisdiccion
        cond4 = detalle['TaxCollectionType'] == 'RET'

        resultado = detalle[cond1 & cond3 & cond4 & cond5]

        if not resultado.empty:
            tax_condition = resultado['TaxCondition3'].iloc[0]
        else:
            tax_condition = None
        suma = round(resultado['TaxCollectionAmount3'].sum(), 2)

        return tax_condition, round(suma, 2), round(row['Retencion'] - suma, 2), dia_cert, cert

    if dia_cert != 15:
        inicio_mes = datetime(fecha_liq.year, fecha_liq.month, 16).date()
        cond3 = (detalle['Date'] >= inicio_mes) & (detalle['Date'] < fecha_liq + pd.Timedelta(days=1))
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

    ddjj['tax_condition'] = pd.NA
    ddjj['tax_condition'] = ddjj['tax_condition'].astype(str)

    for index, row in tqdm(ddjj.iterrows(), total=ddjj.shape[0],
                           desc=f'Validando SIRTAC (900) {cuit_agente} {periodo}'):
        v, w, x, y, z = calcular_suma_900(ddjj, row, detalle)

        ddjj.at[index, 'tax_condition'] = v
        ddjj.at[index, 'suma_reporte'] = w
        ddjj.at[index, 'diferencia'] = x
        ddjj.at[index, 'quincena'] = y
        ddjj.at[index, 'certificado'] = z
    with pd.ExcelWriter(f'validaciones/{cuit_agente} {periodo} reporte.xlsx', mode='a', engine='openpyxl') as writer:
        # Escribir el primer DataFrame en la primera hoja
        ddjj.to_excel(writer, sheet_name='tax_900', index=False)

    fortnight_1_txt = 0
    count_1 = 0
    max_1 = 0
    fortnight_2_txt = 0
    count_2 = 0
    max_2 = 0

    if periodo[6:7] == '1':
        ddjj['FechaLiq'] = pd.to_datetime(ddjj['FechaLiq'])
        fortnight_1_txt = round(ddjj[ddjj['FechaLiq'].dt.day == 15]['suma_reporte'].sum(), 2)
        count_1 = ddjj[(ddjj['FechaLiq'].dt.day == 15) & (ddjj['certificado'] != 0)]['certificado'].count()
        max_1 = ddjj[(ddjj['FechaLiq'].dt.day == 15) & (ddjj['certificado'] != 0)]['certificado'].max()
    if periodo[6:7] == '2':
        ddjj['FechaLiq'] = pd.to_datetime(ddjj['FechaLiq'])
        fortnight_2_txt = round(ddjj[ddjj['FechaLiq'].dt.day != 15]['suma_reporte'].sum(), 2)
        count_2 = ddjj[(ddjj['FechaLiq'].dt.day != 15) & (ddjj['certificado'] != 0)]['certificado'].count()
        max_2 = ddjj[(ddjj['FechaLiq'].dt.day != 15) & (ddjj['certificado'] != 0)]['certificado'].max()
    print(ddjj)
    return fortnight_1_txt, count_1, max_1, fortnight_2_txt, count_2, max_2

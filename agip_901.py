import pandas as pd
from datetime import datetime
from tqdm import tqdm
import file_utils


def procesar_tax901(detalle, cuit_agente, periodo):
    # Abrir el archivo de datos
    ddjj = file_utils.open_agip_txt_file(cuit_agente, periodo)
    print(ddjj)
    # Procesar cada fila del DataFrame
    for index, row in tqdm(ddjj.iterrows(), total=ddjj.shape[0],
                           desc=f'Validando CABA AGIP (901) {cuit_agente} {periodo}'):
        tax_condition, suma_reporte, diferencia, quincena, certificado = procesar_fila(row, detalle)
        ddjj.at[index, 'tax_condition'] = tax_condition
        ddjj.at[index, 'suma_reporte'] = suma_reporte
        ddjj.at[index, 'diferencia'] = diferencia
        ddjj.at[index, 'quincena'] = quincena
        ddjj.at[index, 'certificado'] = certificado

    # Guardar los resultados en un archivo de Excel
    guardar_en_excel(ddjj, cuit_agente, periodo)
    print(ddjj)
    # Calcular y retornar estadísticas
    return calcular_estadisticas(ddjj)


def procesar_fila(row, detalle):
    cuit = int(row['numero_documento'])
    fecha_ret = row['fecha_retencion']
    dia_cert = fecha_ret.day
    cert = int(str(row['numero_comprobante'][-8:]))
    cond1 = detalle['ShopId'] == cuit
    cond2 = detalle['TaxId5'] == 901
    cond4 = detalle['TaxCollectionType'] == 'RET'

    inicio_mes = datetime(fecha_ret.year, fecha_ret.month, 1 if dia_cert == 15 else 16).date()
    cond3 = (detalle['Date'] >= inicio_mes) & (detalle['Date'] < fecha_ret + pd.Timedelta(days=1))

    resultado = detalle[cond1 & cond2 & cond3 & cond4]
    tax_condition = resultado['TaxCondition5'].iloc[0] if not resultado.empty else None
    suma = round(resultado['TaxCollectionAmount5'].sum(), 2)
    return tax_condition, suma, round(row['retencion'] - suma, 2), dia_cert, cert


def guardar_en_excel(ddjj, cuit_agente, periodo):
    with pd.ExcelWriter(f'validaciones/{cuit_agente} {periodo} reporte.xlsx', mode='a', engine='openpyxl') as writer:
        ddjj.to_excel(writer, sheet_name='tax_901', index=False)


def calcular_estadisticas(ddjj):
    ddjj['fecha_comprobante'] = pd.to_datetime(ddjj['fecha_comprobante'])
    fortnight_1_txt = round(ddjj[ddjj['fecha_comprobante'].dt.day == 15]['suma_reporte'].sum(), 2)
    count_1 = ddjj[(ddjj['fecha_comprobante'].dt.day == 15) & (ddjj['suma_reporte'] != 0)]['certificado'].count()
    max_1 = ddjj[(ddjj['fecha_comprobante'].dt.day == 15) & (ddjj['certificado'] != 0)]['certificado'].max()
    fortnight_2_txt = round(ddjj[ddjj['fecha_comprobante'].dt.day > 15]['suma_reporte'].sum(), 2)
    count_2 = ddjj[(ddjj['fecha_comprobante'].dt.day > 15) & (ddjj['suma_reporte'] != 0)]['certificado'].count()
    max_2 = ddjj[(ddjj['fecha_comprobante'].dt.day > 15)]['certificado'].max()

    return fortnight_1_txt, count_1, max_1, fortnight_2_txt, count_2, max_2

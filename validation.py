from datetime import timedelta
import pandas as pd
from tqdm import tqdm
import report


def validation_900(detalle, resumen, cuit_agente, periodo):
    path = f"input/{cuit_agente}/{periodo}"

    columns = ['ShopId', 'TaxCondition', 'Alicota', 'Diferencia', 'CertTxt', 'CertResumen', 'jurisdiccion', 'Total']
    df_resultados = pd.DataFrame(columns=columns)

    detalle = detalle.query('TaxCollectionAmount3 != 0')

    txt_900 = open_900_txt_file(cuit_agente, periodo)

    txt_900['FechaLiq'] = pd.to_datetime(txt_900['FechaLiq'], format='%d/%m/%Y').dt.date

    txt_sum = 0
    for linea in tqdm(range(len(txt_900)), desc='Validando SIRTAC (900)'):
        cuit = txt_900.at[linea, 'CUIT']
        fecha = txt_900.at[linea, 'FechaLiq']
        dia = int(txt_900.at[linea, 'FechaLiq'].strftime('%d'))
        jurisdiccion = txt_900.at[linea, 'Jurisdiccion']
        retencion = txt_900.at[linea, 'Retencion']
        certificado = int(txt_900.at[linea, 'NroLiq'][-8:])

        cond1 = (detalle['ShopId'] == cuit)
        cond2 = (pd.isna(detalle['VoidDate']))
        cond4 = (detalle['TaxCollectionNo3'] == certificado)
        cond5 = (detalle['TurnoverTax'] == jurisdiccion)
        cond3 = ((dia == 15) & (detalle['Date'] < fecha + timedelta(days=1))) | (
                (dia != 15) & (detalle['Date'] >= fecha.replace(day=16)))

        filtered = detalle[cond1 & cond2 & cond3 & cond4 & cond5]
        suma_detalle = round(filtered['TaxCollectionAmount3'].sum(), 2)
        txt_sum += suma_detalle

        if suma_detalle != retencion:
            alicuota = filtered.iloc[0]['Rate3']
            tax_condition = filtered.iloc[0]['TaxCondition3']
            shop_id = filtered.iloc[0]['ShopId']
            df_resultados.loc[len(df_resultados)] = [shop_id, tax_condition, alicuota, suma_detalle - retencion,
                                                     certificado, filtered.iloc[0]['TaxCollectionNo3'], jurisdiccion,
                                                     suma_detalle]

    df_resultados = df_resultados.sort_values(by='CertTxt')
    report.reporte(900, resumen, detalle, txt_sum)
    archivo_reporte = f"{path}/validacion/900_{detalle.iloc[0]['Date']}.xlsx"
    df_resultados.to_excel(archivo_reporte, index=False)


def open_900_txt_file(cuit_agente, periodo):
    periodo_archivos = periodo[:4] + "-" + periodo[4:6] + " " + periodo[6:]
    file = f"input/{cuit_agente}/{periodo}/900 - {periodo_archivos}.txt"

    data = pd.read_csv(file, header=None, sep=';', decimal=',')
    data[8] = data[8].str.lstrip('0').astype(float)
    data.columns = ['CUIT', 'CRC', 'FechaLiq', 'FechaRet', 'NroLiq', 'CantOperaciones', 'Base', 'Alicuota',
                    'Retencion',
                    'TipoRegistro', 'OpeEx', 'Jurisdiccion']
    return pd.DataFrame(data)

import pandas as pd

import report


def validation_900(txt_900, detalle, resumen):
    print(resumen)

    #

    detalle = detalle.query('TaxCollectionAmount3 != 0')
    report.reporte(900, resumen, detalle, txt_900)

    txt_900['FechaLiq'] = pd.to_datetime(txt_900['FechaLiq'], format='%d/%m/%Y').dt.date

    # column_names = ['ShopId', 'TaxCondition', 'Alicota', 'Diferencia', 'CertTxt', 'CertResumen', 'jurisdiccion',
    #                 'Total']
    # df_resultados = pd.DataFrame(columns=column_names)
    #
    # for linea in tqdm(range(len(txt_900)), desc='Procesando líneas'):
    #     cuit = txt_900.at[linea, 'CUIT']
    #     fecha = txt_900.at[linea, 'FechaLiq']
    #     dia = int(txt_900.at[linea, 'FechaLiq'].strftime('%d'))
    #     jurisdiccion = txt_900.at[linea, 'Jurisdiccion']
    #     retencion = txt_900.at[linea, 'Retencion']
    #     certificado = int(txt_900.at[linea, 'NroLiq'][-8:])
    #
    #     cond1 = (detalle['ShopId'] == cuit)
    #     cond2 = (pd.isna(detalle['VoidDate']))
    #     cond4 = (detalle['TaxCollectionNo3'] == certificado)
    #     cond5 = (detalle['TurnoverTax'] == jurisdiccion)
    #     cond3 = ((dia == 15) & (detalle['Date'] < fecha + timedelta(days=1))) | (
    #             (dia != 15) & (detalle['Date'] >= fecha.replace(day=16)))
    #
    #     filtered = detalle[cond1 & cond2 & cond3 & cond4 & cond5]
    #
    #     suma_detalle = round(filtered['TaxCollectionAmount3'].sum(), 2)
    #
    #     if suma_detalle != retencion:
    #         alicuota = filtered.iloc[0]['Rate3']
    #         tax_condition = filtered.iloc[0]['TaxCondition3']
    #         shop_id = filtered.iloc[0]['ShopId']
    #         df_resultados.loc[len(df_resultados)] = [shop_id, tax_condition, alicuota, suma_detalle - retencion,
    #                                                  certificado, filtered.iloc[0]['TaxCollectionNo3'], jurisdiccion,
    #                                                  suma_detalle]
    #
    # df_resultados = df_resultados.sort_values(by='CertTxt')
    # diferencia = df_resultados['Diferencia'].sum()
    # print(f'Diferencia ---> {diferencia}')
    # archivo_reporte = f"{path}validacion/900_{detalle.iloc[0]['Date']}.xlsx"
    # df_resultados.to_excel(archivo_reporte, index=False)
    # print(df_resultados)

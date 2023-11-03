import pandas as pd

def extract_day(date_string):
    return pd.to_datetime(date_string, format='%d/%m/%Y').day
def reporte(tax_id, resumen, detalle, txt2):

    column_names_validacion = ['tax_id', 'tax_collection_type', 'resumen_1_fortnight', 'resumen_2_fortnight',
                               'total_resumen', 'total_detalle', 'resumen_vs_detalle',
                               '1_fortnight_txt', '1_txt_vs_detalle', '2_fortnight_txt', '1_txt_vs_detalle',
                               '1_fortnight_count', '2_fortnight_count']

    df_validacion = pd.DataFrame(columns=column_names_validacion).reset_index(inplace=True, drop=True)

    nueva_fila = {'tax_id': tax_id, 'tax_collection_type': 'RET'}

    df_validacion = pd.concat([df_validacion, pd.DataFrame([nueva_fila])])
    row = df_validacion[df_validacion['tax_id'] == tax_id].index

    df_validacion.loc[row, 'resumen_1_fortnight'] = resumen.loc[resumen['TaxId'] == tax_id, '1stFortnight'].values[0]
    df_validacion.loc[row, 'resumen_2_fortnight'] = resumen.loc[resumen['TaxId'] == tax_id, '2stFortnight'].values[0]
    df_validacion.loc[row, 'total_resumen'] = resumen.loc[resumen['TaxId'] == tax_id, 'Total'].values[0]
    df_validacion.loc[row, 'total_detalle'] = round(detalle['TaxCollectionAmount3'].sum(), 2)
    df_validacion.loc[row, 'resumen_vs_detalle'] = df_validacion.loc[row, 'total_resumen'].iloc[0] - df_validacion.loc[row, 'total_detalle'].iloc[0]
    txt2['FechaLiq'].apply(extract_day).tolist()

    print(df_validacion)

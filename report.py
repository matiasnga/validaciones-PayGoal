import pandas as pd

pd.set_option('display.max_colwidth', None)
pd.set_option('display.expand_frame_repr', False)


def reporte(tax_id, resumen, detalle, txt_1_fortnight):
    column_names_validacion = ['tax_id', 'tax_collection_type', 'resumen_1_fortnight', 'resumen_2_fortnight',
                               'total_resumen', 'total_detalle', 'resumen_vs_detalle',
                               '1_fortnight_txt', '1_txt_vs_detalle', '2_fortnight_txt', '2_txt_vs_detalle',
                               '1_fortnight_count', '2_fortnight_count']

    resumen_fila = resumen[resumen['TaxId'] == tax_id].iloc[0]

    nueva_fila = {
        'tax_id': tax_id,
        'tax_collection_type': 'RET',
        'resumen_1_fortnight': resumen_fila['1stFortnight'],
        'resumen_2_fortnight': resumen_fila['2stFortnight'],
        'total_resumen': resumen_fila['Total'],
        'total_detalle': round(detalle['TaxCollectionAmount3'].sum(), 2),
        'resumen_vs_detalle': resumen_fila['Total'] - round(detalle['TaxCollectionAmount3'].sum(), 2),
        '1_fortnight_txt': txt_1_fortnight,
        '1_txt_vs_detalle': resumen_fila['1stFortnight'] - txt_1_fortnight,
    }

    df = pd.DataFrame([nueva_fila], columns=column_names_validacion)
    df.to_excel('reporte.xlsx', index=False)
    print(df)

import pandas as pd
import validaciones


def validacion(detalle_ret, detalle_per, resumen, cuit_agente, periodo):
    column_names_validacion = ['tax_id', 'tax_collection_type', 'resumen_1_fortnight', 'resumen_2_fortnight',
                               'total_resumen', 'total_detalle', 'resumen_vs_detalle',
                               '1_fortnight_txt', '1_txt_vs_detalle', '2_fortnight_txt', '2_txt_vs_detalle',
                               '1_fortnight_count', '1_fortnight_max', '2_fortnight_count', '2_fortnight_max']
    df = pd.DataFrame(columns=column_names_validacion)
    for index, row in resumen.iterrows():
        txt_1 = 0
        count_1 = 0
        max_1 = 0
        tax_id = row['TaxId']
        tax_collection_type = row['TaxCollectionType']
        resumen_1_fortnight = row['1stFortnight']
        resumen_2_fortnight = row['2stFortnight']
        total_resumen = row['Total']

        if tax_id == 767:
            id = '1'
        elif tax_id == 217:
            id = '2'
        elif tax_id == 900:
            txt_1, count_1, max_1 = validaciones.tax_900(detalle_ret, cuit_agente, periodo)
            id = '3'
        elif tax_id == 901:
            id = '5'
        elif tax_id == 905:
            id = '4'
        elif tax_id == 921:
            txt_1, count_1, max_1 = validaciones.tax_921(detalle_ret, cuit_agente, periodo)
            id = '4'
        elif tax_id == 924:
            id = '4'

        total_detalle = round(detalle_ret[detalle_ret['TaxId' + id] == row['TaxId']]['TaxCollectionAmount' + id].sum(),
                              2)
        resumen_vs_detalle = total_resumen - total_detalle

        nueva_fila = {
            'tax_id': tax_id,
            'tax_collection_type': tax_collection_type,
            'resumen_1_fortnight': resumen_1_fortnight,
            'resumen_2_fortnight': resumen_2_fortnight,
            'total_resumen': total_resumen,
            'total_detalle': total_detalle,
            'resumen_vs_detalle': resumen_vs_detalle,
            '1_fortnight_txt': txt_1,
            '1_txt_vs_detalle': total_detalle - txt_1,
            '2_fortnight_txt': None,
            '2_txt_vs_detalle': None,
            '1_fortnight_count': count_1,
            '1_fortnight_max': max_1,
            '2_fortnight_count': None,
            '2_fortnight_max': None
        }
        df = pd.concat([df, pd.DataFrame(nueva_fila, index=[0])], ignore_index=True)

    df.to_excel(f'validaciones/{cuit_agente} {periodo} reporte.xlsx', index=False)

import pandas as pd
import validaciones

pd.set_option('display.max_columns', 10)
pd.set_option('display.expand_frame_repr', False)


def calcular_total_detalle(detalle_ret, tax_id, id_mapping):
    id = id_mapping.get(tax_id, '')
    columna_tax = f'TaxId{id}'
    columna_amount = f'TaxCollectionAmount{id}'
    return round(detalle_ret[detalle_ret[columna_tax] == tax_id][columna_amount].sum(), 2)


def obtener_datos_tax(detalle_ret, cuit_agente, periodo, tax_id):
    tax_id_int = int(tax_id)  # Convertir tax_id a entero para manejar correctamente las claves como enteros
    clave_funcion = f'tax_{tax_id_int}'

    # Verificar si la clave existe en el diccionario y si es uno de los IDs específicos que necesitamos
    if clave_funcion in validaciones.__dict__ and tax_id_int in [900, 921]:
        return validaciones.__dict__[clave_funcion](detalle_ret, cuit_agente, periodo)

    return 0, 0, 0


def crear_fila(row, detalle_ret, detalle_per, cuit_agente, periodo, id_mapping):
    tax_id = row['TaxId']
    txt_1, count_1, max_1 = obtener_datos_tax(detalle_ret, cuit_agente, periodo, tax_id)
    if row['TaxCollectionType'] == 'RET':
        total_detalle = calcular_total_detalle(detalle_ret, tax_id, id_mapping)
    else:
        total_detalle = calcular_total_detalle(detalle_per, tax_id, id_mapping)
    return {
        'tax_id': tax_id,
        'tax_collection_type': row['TaxCollectionType'],
        'resumen_1_fortnight': row['1stFortnight'],
        'resumen_2_fortnight': row['2stFortnight'],
        'total_resumen': row['Total'],
        'total_detalle': total_detalle,
        'diff': row['Total'] - total_detalle,
        '1_fortnight_txt': txt_1,
        'diff_1_txt_vs_detalle': total_detalle - txt_1,
        '2_fortnight_txt': 0,
        'diff_2_txt_vs_detalle': 0,
        '1_count': count_1,
        '1_max': max_1,
        '2_count': 0,
        '2_max': 0
    }


def validacion(detalle_ret, detalle_per, resumen, cuit_agente, periodo):
    with pd.ExcelWriter(f'validaciones/{cuit_agente} {periodo} reporte.xlsx') as writer:
        pass

    id_mapping = {
        767: '1',
        217: '2',
        900: '3',
        901: '5',
        905: '4',
        911: '4',
        921: '4',
        924: '4',
    }
    column_names_validacion = ['tax_id', 'tax_collection_type', 'resumen_1_fortnight', 'resumen_2_fortnight',
                               'total_resumen', 'total_detalle', 'diff',
                               '1_fortnight_txt', 'diff_1_txt_vs_detalle', '2_fortnight_txt', 'diff_2_txt_vs_detalle',
                               '1_count', '1_max', '2_count', '2_max']
    filas = [crear_fila(row, detalle_ret, detalle_per, cuit_agente, periodo, id_mapping) for index, row in
             resumen.iterrows()]
    validaciones_result = pd.DataFrame(filas, columns=column_names_validacion)

    with pd.ExcelWriter(f'validaciones/{cuit_agente} {periodo} reporte.xlsx', mode='a', engine='openpyxl') as writer:
        validaciones_result.to_excel(writer, sheet_name='Validaciones', index=False)

        resumen.to_excel(writer, sheet_name='Resumen', index=False)


    print(validaciones_result)

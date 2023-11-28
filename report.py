import pandas as pd
import afip_767
import afip_217
import agip_901
import corrientes_905
import file_utils
import santa_fe_921
import sirtac_900
import tucuman_924

pd.set_option('display.max_columns', 10)
pd.set_option('display.expand_frame_repr', False)


def calcular_total_detalle(detalle_ret, tax_id, id_mapping):
    id = id_mapping.get(tax_id, '')
    columna_tax = f'TaxId{id}'
    columna_amount = f'TaxCollectionAmount{id}'
    return round(detalle_ret[detalle_ret[columna_tax] == tax_id][columna_amount].sum(), 2)


def obtener_datos_tax(detalle_ret, cuit_agente, periodo, tax_id, tax_type):
    tax_id = int(tax_id)  # Convertir tax_id a entero para manejar correctamente las claves como enteros
    if tax_type == 'RET':
        if tax_id == 924:
            return tucuman_924.tax_924(detalle_ret, cuit_agente, periodo)
        if tax_id == 901:
            return agip_901.procesar_tax901(detalle_ret, cuit_agente, periodo)
        if tax_id == 900:
            return sirtac_900.tax_900(detalle_ret, cuit_agente, periodo)
        #
        # if tax_id == 217:
        #     return afip_217.procesar_tax_217(detalle_ret, cuit_agente, periodo)
        if tax_id == 921:
            return santa_fe_921.tax_921(detalle_ret, cuit_agente, periodo)
        if tax_id == 905:
            return corrientes_905.tax_905(detalle_ret, cuit_agente, periodo)
        if tax_id == 767:
            return afip_767.procesar_tax_767(detalle_ret, cuit_agente, periodo)
        else:
            return 0, 0, 0, 0, 0, 0

    else:
        return 0, 0, 0, 0, 0, 0


def crear_fila(row, detalle_ret, detalle_per, cuit_agente, periodo, id_mapping):
    tax_id = row['TaxId']
    txt_1, count_1, max_1, txt_2, count_2, max_2 = obtener_datos_tax(detalle_ret, cuit_agente, periodo, tax_id,
                                                                     row['TaxCollectionType'])

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
        'diff_1_txt_vs_detalle': row['1stFortnight'] - txt_1,
        '2_fortnight_txt': txt_2,
        'diff_2_txt_vs_detalle': row['2stFortnight'] - txt_2,
        '1_count': count_1,
        '1_max': max_1,
        '2_count': count_2,
        '2_max': max_2
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

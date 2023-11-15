import pandas as pd

import test900

pd.set_option('display.max_colwidth', None)
pd.set_option('display.expand_frame_repr', False)


def reporte(detalle, resumen, cuit_agente, periodo):
    column_names_validacion = ['tax_id', 'tax_collection_type', 'resumen_1_fortnight', 'resumen_2_fortnight',
                               'total_resumen', 'total_detalle', 'resumen_vs_detalle',
                               '1_fortnight_txt', '1_txt_vs_detalle', '2_fortnight_txt', '2_txt_vs_detalle',
                               '1_fortnight_count', '1_fortnight_max', '2_fortnight_count', '2_fortnight_max']

    nueva_fila = test900.sirtac_900(detalle, resumen, cuit_agente, periodo)
    # df = pd.DataFrame([nueva_fila], columns=column_names_validacion)
    # df.to_excel('reporte.xlsx', index=False)
    # print(df)

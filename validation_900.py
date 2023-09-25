import pandas as pd
from tqdm import tqdm


def validation_900(txt_900, detalle):
# Define los nombres de las columnas
    column_names = ["ShopId", "TaxCondition", "Diferencia", "Certificado", "Total"]

    # Crea el DataFrame con columnas vacías
    df_resultados = pd.DataFrame(columns=column_names)

    # Define los tipos de datos correspondientes en el mismo orden
    column_types = {'ShopId': int, 'TaxCondition': str, 'Diferencia': float, 'Certificado': int, 'Total': float}

    # Aplica los tipos de datos a las columnas correspondientes
    df_resultados = df_resultados.astype(column_types)

    for linea in tqdm(range(len(txt_900)), desc="Procesando líneas"):
        a2_cuit = txt_900.at[linea, 'CUIT']
        x2_dia = txt_900.at[linea, 'FechaLiq'][:2]
        c2_date = txt_900.at[linea, 'FechaLiq']
        y2_cert_number = int(txt_900.at[linea, 'NroLiq'][-8:])
        l2_jurisdiccion = txt_900.at[linea, 'Jurisdiccion']
        i2_retencion = txt_900.at[linea, 'Retencion']

        cond1 = (detalle['ShopId'] == a2_cuit)
        cond2 = (pd.isna(detalle['VoidDate']))
        # cond3 = ((x2_dia == 15) & (detalle['Date'] < c2_date + 1)) | ((x2_dia != 15) & (detalle['Date'] >=
        # pd.to_datetime(c2_date).replace(day=16)))
        cond4 = (detalle['TaxCollectionNo3'] == y2_cert_number)
        cond5 = (detalle['TurnoverTax'] == l2_jurisdiccion)

        # Filtrar el DataFrame con las condiciones y crear una copia independiente
        filtrado = detalle[cond1 & cond2 & cond4 & cond5].copy()

    # Calcular la suma de la columna 'TaxCollectionAmount3'
        resultado = round(filtrado['TaxCollectionAmount3'].sum(), 2)
        if resultado != i2_retencion:
            tax_condition = detalle[cond1 & cond2 & cond4 & cond5]['TaxCondition3'].iloc[0]
            shop_id = detalle[cond1 & cond2 & cond4 & cond5]['ShopId'].iloc[0]
            # Agregar una fila de datos al DataFrame utilizando loc
            df_resultados.loc[len(df_resultados)] = [shop_id, tax_condition, resultado - i2_retencion, y2_cert_number,
                                                     resultado]

    df_resultados = df_resultados.sort_values(by='Certificado')
    diff = df_resultados['Diferencia'].sum()
    df_resultados.loc[len(df_resultados)] = ["Diferencia Total", "", diff, "", ""]
    print(df_resultados)

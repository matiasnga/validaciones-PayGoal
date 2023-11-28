import pandas as pd


def open_detalle_csv(cuit_agente, periodo, tax_type):
    periodo_archivos = periodo[:4] + "-" + periodo[4:6] + " " + periodo[6:]
    file = f"input/{cuit_agente}/{periodo}/{periodo_archivos} {tax_type} - detalle.csv"
    df = pd.read_csv(file, sep=';', decimal=',', low_memory=False).query('VoidDate.isnull()')
    df['CompanyId'] = df['CompanyId'].astype('Int64')
    df['ShopId'] = df['ShopId'].astype('Int64')
    df['PaymentNo'] = df['PaymentNo'].astype('Int64')

    df['Date'] = pd.to_datetime(df['Date']).dt.date
    if df.iloc[-1].isna().all():
        # Eliminar la última fila
        df = df[:-1]
    print(df)
    return pd.DataFrame(df)


def open_resumen_csv(cuit_agente, periodo):
    periodo_archivos = periodo[:4] + "-" + periodo[4:6] + " " + periodo[6:]
    file = f"input/{cuit_agente}/{periodo}/{periodo_archivos} - resumen.csv"
    df = pd.read_csv(file, sep=';', decimal=',')
    df['TaxId'] = df['TaxId'].astype('Int64')

    if df.iloc[-1].isna().all():
        # Eliminar la última fila
        df = df[:-1]
    print(df)

    return pd.DataFrame(df)


def split_detalle_quincena(detalle):
    detalle['Date'] = pd.to_datetime(detalle['Date']).dt.date
    detalle_filtrado = detalle.query('VoidDate.isnull()')
    fecha_inicio = detalle_filtrado['Date'].min()
    fecha_corte = fecha_inicio + pd.DateOffset(days=14)
    primera_quincena = detalle_filtrado[detalle_filtrado['Date'] <= fecha_corte.date()]
    segunda_quincena = detalle_filtrado[detalle_filtrado['Date'] > fecha_corte.date()]
    return primera_quincena, segunda_quincena


def open_sircar_txt_file(taxid, cuit_agente, periodo):
    if taxid == '921':
        periodo_archivos = periodo[:4] + "-" + periodo[4:6] + " " + periodo[6:]
    else:
        periodo_archivos = periodo[:4] + "-" + periodo[4:6]

    file = f"input/{cuit_agente}/{periodo}/{taxid} - {periodo_archivos} Retención.txt"

    data = pd.read_csv(file, header=None, sep=',', decimal='.')
    data[7] = data[7].astype(float)
    data.columns = ['Renglon', 'TipoComprobante', 'LetraComprobante', 'NroLiq', 'CUIT', 'FechaRet', 'Base', 'Alicuota',
                    'Retencion', 'Regimen', 'Jurisdiccion']
    data['FechaRet'] = pd.to_datetime(data['FechaRet'], format='%d/%m/%Y').dt.date
    return pd.DataFrame(data)


def open_900_txt_file(cuit_agente, periodo):
    periodo_archivos = periodo[:4] + "-" + periodo[4:6] + " " + periodo[6:]
    file = f"input/{cuit_agente}/{periodo}/900 - {periodo_archivos}.txt"

    data = pd.read_csv(file, header=None, sep=';', decimal=',')
    data[8] = data[8].str.lstrip('0').astype(float)
    data.columns = ['CUIT', 'CRC', 'FechaLiq', 'FechaRet', 'NroLiq', 'CantOperaciones', 'Base', 'Alicuota',
                    'Retencion',
                    'TipoRegistro', 'OpeEx', 'Jurisdiccion']

    data['FechaLiq'] = pd.to_datetime(data['FechaLiq'], format='%d/%m/%Y').dt.date
    data['FechaRet'] = pd.to_datetime(data['FechaRet'], format='%d/%m/%Y').dt.date

    return pd.DataFrame(data)


def open_sicore_txt_file(taxid, cuit_agente, periodo):
    datos = []
    periodo_archivos = periodo[:4] + "-" + periodo[4:6]
    file = f"input/{cuit_agente}/{periodo}/{taxid} - {periodo_archivos}.txt"

    with open(file, 'r') as txt:
        # Leer cada línea del archivo
        for line in txt:
            # Extraer los campos usando slicing, ajusta los índices según tus necesidades
            codigo_comprobante = line[0:2].strip()  # .strip() para eliminar espacios en blanco
            fecha_comprobante = line[2:12].strip()
            numero_comprobante = line[12:28].strip()
            importe_comprobante = float(line[28:44].strip().replace(',', '.'))
            codigo_impuesto = line[44:48].strip()
            codigo_regimen = line[48:51].strip()
            codigo_operacion = line[51:52].strip()
            base = float(line[52:66].strip().replace(',', '.'))
            fecha_retencion = line[66:76].strip()
            importe_retencion = float(line[76:93].strip().replace(',', '.'))
            porcentaje_exclusion = float(line[93:99].strip().replace(',', '.'))
            fecha_exclusion = line[99:109].strip()
            tipo_documento = line[109:111]
            cuit = line[111:131]
            numero_certificado_original = line[131:145]

            # Añadir los datos a la lista
            datos.append({'codigo_comprobante': codigo_comprobante, 'fecha_comprobante': fecha_comprobante,
                          'numero_comprobante': numero_comprobante, 'importe_comprobante': importe_comprobante,
                          'codigo_impuesto': codigo_impuesto, 'codigo_regimen': codigo_regimen,
                          'codigo_operacion': codigo_operacion, 'base': base, 'fecha_retencion': fecha_retencion,
                          'importe_retencion': importe_retencion, 'porcentaje_exclusion': porcentaje_exclusion,
                          'fecha_exclusion': fecha_exclusion, 'tipo_documento': tipo_documento, 'cuit': cuit,
                          'numero_certificado_original': numero_certificado_original

                          })
    # Crear un DataFrame con los datos
    data = pd.DataFrame(datos)
    data['fecha_comprobante'] = pd.to_datetime(data['fecha_comprobante'], format='%d/%m/%Y').dt.date
    data['fecha_retencion'] = pd.to_datetime(data['fecha_retencion'], format='%d/%m/%Y').dt.date

    data['fecha_exclusion'] = pd.to_datetime(data['fecha_exclusion'], format='%d/%m/%Y').dt.date
    print(data)
    return data


def open_agip_txt_file(cuit_agente, periodo):
    datos = []
    periodo_archivos = periodo[:4] + "-" + periodo[4:6]
    file = f"input/{cuit_agente}/{periodo}/901 - {periodo_archivos}.txt"

    with open(file, 'r') as txt:
        # Leer cada línea del archivo
        for line in txt:
            # Extraer los campos usando slicing, ajusta los índices según tus necesidades
            tipo_operacion = line[0:1]
            codigo_de_norma = line[1:4]
            fecha_retencion = line[4:14]
            tipo_comprobante = line[14:16]
            letra_comprobante = line[16:17]
            numero_comprobante = line[17:33]
            fecha_comprobante = line[33:43]
            monto_comprobante = float(line[43:59].replace(',', '.'))
            numero_certificado_propio = line[59:75]
            tipo_documento = line[75:76]
            numero_documento = line[76:87]
            situacion_ib = line[87:88]
            numero_inscripcion_ib = line[88:99]
            situacion_iva = line[99:100]
            razon_social = line[100:130]
            importe_otros_conceptos = float(line[130:146].replace(',', '.'))
            importe_iva = float(line[146:162].replace(',', '.'))
            monto_sujeto_a_retencion = float(line[162:178].replace(',', '.'))
            alicuta = float(line[178:183].replace(',', '.'))
            retencion = float(line[183:199].replace(',', '.'))
            monto_total_retenido = float(line[199:215].replace(',', '.'))

            datos.append({'tipo_operacion': tipo_operacion, 'codigo_de_norma': codigo_de_norma,
                          'fecha_retencion': fecha_retencion,
                          'tipo_comprobante': tipo_comprobante, 'letra_comprobante': letra_comprobante,
                          'numero_comprobante': numero_comprobante,
                          'fecha_comprobante': fecha_comprobante, 'monto_comprobante': monto_comprobante,
                          'numero_certificado_propio': numero_certificado_propio,
                          'tipo_documento': tipo_documento, 'numero_documento': numero_documento,
                          'situacion_ib': situacion_ib, 'numero_inscripcion_ib': numero_inscripcion_ib,
                          'situacion_iva': situacion_iva, 'razon_social': razon_social,
                          'importe_otros_conceptos': importe_otros_conceptos, 'importe_iva': importe_iva,
                          'monto_sujeto_a_retencion': monto_sujeto_a_retencion, 'alicuta': alicuta,
                          'retencion': retencion, 'monto_total_retenido': monto_total_retenido

                          })
    # Crear un DataFrame con los datos
    data = pd.DataFrame(datos)
    # data['fecha_comprobante'] = pd.to_datetime(data['fecha_comprobante'], format='%d/%m/%Y').dt.date
    data['fecha_retencion'] = pd.to_datetime(data['fecha_retencion'], format='%d/%m/%Y').dt.date
    data['fecha_comprobante'] = pd.to_datetime(data['fecha_comprobante'], format='%d/%m/%Y').dt.date

    # data['fecha_exclusion'] = pd.to_datetime(data['fecha_exclusion'], format='%d/%m/%Y').dt.date
    print(data)
    return data


def open_tucuman_txt_file(cuit_agente, periodo):
    datos = []
    periodo_archivos = periodo[:4] + "-" + periodo[4:6]
    file = f"input/{cuit_agente}/{periodo}/924 - {periodo_archivos} - datos.txt"

    with open(file, 'r') as txt:
        # Leer cada línea del archivo
        for line in txt:
            # Extraer los campos usando slicing, ajusta los índices según tus necesidades
            fecha_retencion = line[0:8]
            tipo_documento = line[8:10]
            numero_documento = line[10:21]
            a_confirmar_campo = line[21:24]
            numero_certificado = line[24:36]
            base_imponible = float(line[36:52])
            alicuota = float(line[52:57])
            retencion = float(line[57:73])

            #
            # tipo_operacion = line[0:1]
            # monto_comprobante = float(line[43:59].replace(',', '.'))

            datos.append({
                'fecha_retencion': fecha_retencion, 'tipo_documento': tipo_documento, 'numero_documento': numero_documento,
                'a_confirmar_campo': a_confirmar_campo, 'numero_certificado': numero_certificado, 'base_imponible': base_imponible,
                'alicuota': alicuota, 'retencion': retencion

            })
    # Crear un DataFrame con los datos
    data = pd.DataFrame(datos)
    # data['fecha_comprobante'] = pd.to_datetime(data['fecha_comprobante'], format='%d/%m/%Y').dt.date
    data['fecha_retencion'] = pd.to_datetime(data['fecha_retencion'], format='%Y%m%d').dt.date
    # data['fecha_comprobante'] = pd.to_datetime(data['fecha_comprobante'], format='%d/%m/%Y').dt.date

    # data['fecha_exclusion'] = pd.to_datetime(data['fecha_exclusion'], format='%d/%m/%Y').dt.date
    print(data)
    return data

import pandas as pd


class DateExtractor:
    def extract_day(self, date_string):
        return pd.to_datetime(date_string, format='%d/%m/%Y')


def open_detalle_csv(cuit_agente, periodo, tax_type):
    periodo_archivos = periodo[:4] + "-" + periodo[4:6] + " " + periodo[6:]
    file = f"input/{cuit_agente}/{periodo}/{periodo_archivos} {tax_type} - detalle.csv"
    df = pd.read_csv(file, sep=';', decimal=',').query('VoidDate.isnull()')
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    print(df)
    return pd.DataFrame(df)


def open_resumen_csv(cuit_agente, periodo):
    periodo_archivos = periodo[:4] + "-" + periodo[4:6] + " " + periodo[6:]
    file = f"input/{cuit_agente}/{periodo}/{periodo_archivos} - resumen.csv"
    df = pd.read_csv(file, sep=';', decimal=',')
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


def open_921_txt_file(cuit_agente, periodo):
    periodo_archivos = periodo[:4] + "-" + periodo[4:6] + " " + periodo[6:]
    file = f"input/{cuit_agente}/{periodo}/921 - {periodo_archivos} Retención.txt"

    data = pd.read_csv(file, header=None, sep=',', decimal='.')
    data[7] = data[7].astype(float)
    print(f"Archivo abierto correctamente: -> {file}")
    data.columns = ['Renglon', 'TipoComprobante', 'LetraComprobante', 'NroLiq', 'CUIT', 'FechaRet', 'Base', 'Alicuota',
                    'Retencion', 'Regimen', 'Jurisdiccion']
    data['FechaRet'] = pd.to_datetime(data['FechaRet']).dt.date
    return pd.DataFrame(data)


def open_900_txt_file(cuit_agente, periodo):
    periodo_archivos = periodo[:4] + "-" + periodo[4:6] + " " + periodo[6:]
    file = f"input/{cuit_agente}/{periodo}/900 - {periodo_archivos}.txt"

    data = pd.read_csv(file, header=None, sep=';', decimal=',')
    data[8] = data[8].str.lstrip('0').astype(float)
    data.columns = ['CUIT', 'CRC', 'FechaLiq', 'FechaRet', 'NroLiq', 'CantOperaciones', 'Base', 'Alicuota',
                    'Retencion',
                    'TipoRegistro', 'OpeEx', 'Jurisdiccion']

    data['FechaLiq'] = pd.to_datetime(data['FechaLiq']).dt.date
    data['FechaRet'] = pd.to_datetime(data['FechaRet']).dt.date

    return pd.DataFrame(data)

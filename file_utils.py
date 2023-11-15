import pandas as pd


class DateExtractor:
    def extract_day(self, date_string):
        return pd.to_datetime(date_string, format='%d/%m/%Y')


def open_detalle_csv(cuit_agente, periodo):
    periodo_archivos = periodo[:4] + "-" + periodo[4:6] + " " + periodo[6:]
    file = f"input/{cuit_agente}/{periodo}/{periodo_archivos} - detalle.csv"

    df = pd.read_csv(file, sep=';', decimal=',').query('VoidDate.isnull()')
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    print(df['Date'].head())

    # Extraer solo la parte de la fecha
    return pd.DataFrame(df)


def open_resumen_csv(cuit_agente, periodo):
    periodo_archivos = periodo[:4] + "-" + periodo[4:6] + " " + periodo[6:]
    file = f"input/{cuit_agente}/{periodo}/{periodo_archivos} - resumen.csv"
    data = pd.read_csv(file, sep=';', decimal=',')
    print(data)

    return pd.DataFrame(data)


def split_detalle_quincena(detalle):
    detalle['Date'] = pd.to_datetime(detalle['Date']).dt.date
    detalle_filtrado = detalle.query('VoidDate.isnull()')

    fecha_inicio = detalle_filtrado['Date'].min()  # Fecha más temprana
    fecha_final = detalle_filtrado['Date'].max()  # Fecha más reciente

    # Calcula la fecha intermedia para dividir en quincenas
    fecha_intermedia = fecha_inicio + pd.DateOffset(days=14)

    # Filtra el DataFrame para la primera quincena
    primera_quincena = detalle_filtrado[detalle_filtrado['Date'] <= fecha_intermedia.date()]
    # Filtra el DataFrame para la segunda quincena
    segunda_quincena = detalle_filtrado[detalle_filtrado['Date'] > fecha_intermedia.date()]
    return primera_quincena, segunda_quincena



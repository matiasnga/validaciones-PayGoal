import pandas as pd
import file_utils
import validation_900
from config import cliente, periodo, path

pd.set_option('display.max_colwidth', None)
pd.set_option('display.expand_frame_repr', False)


detalle = file_utils.open_csv_file('2023-10 2 - detalle.csv')
detalle = detalle.query('VoidDate.isnull()')

resumen = file_utils.open_csv_file("2023-10 2 - resumen.csv")

# txt_900_1 = file_utils.open_900_txt_file("900 - 2023-10 1.txt")
txt_900_2 = file_utils.open_900_txt_file("900 - 2023-10 2.txt")

primera_quincena, segunda_quincena = file_utils.split_detalle_quincena(detalle)


validation_900.validation_900(txt_900_2, detalle, resumen)

import file_utils
import report
import test921
import validation

# extract_date = file_utils.DateExtractor().extract_day('18/03/2204')
#
# print(extract_date)
periodo = '2023101'
cuit_agente = 'PLAY DIGITAL SA'


detalle = file_utils.open_detalle_csv(cuit_agente, periodo)

resumen = file_utils.open_resumen_csv(cuit_agente, periodo)

primera_quincena, segunda_quincena = file_utils.split_detalle_quincena(detalle)


# validation.sirtac_900(detalle, resumen, cuit_agente, periodo)
report.reporte(detalle, resumen, cuit_agente, periodo)
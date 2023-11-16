import file_utils
import report

periodo = '2023111'
cuit_agente = 'PAYWAY SAU'

detalle_ret = file_utils.open_detalle_csv(cuit_agente, periodo, 'Retenciones')

if cuit_agente == 'PAYWAY SAU':
    detalle_per = file_utils.open_detalle_csv(cuit_agente, periodo, 'Percepciones')
else:
    detalle_per = None

resumen = file_utils.open_resumen_csv(cuit_agente, periodo)

# primera_quincena, segunda_quincena = file_utils.split_detalle_quincena(detalle)

report.validacion(detalle_ret, detalle_per, resumen, cuit_agente, periodo)

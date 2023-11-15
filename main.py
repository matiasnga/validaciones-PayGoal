import file_utils
import report

periodo = '2023101'
cuit_agente = 'PAYWAY SAU'

detalle_ret = file_utils.open_detalle_csv(cuit_agente, periodo, 'Retenciones')
detalle_per = file_utils.open_detalle_csv(cuit_agente, periodo, 'Percepciones')
resumen = file_utils.open_resumen_csv(cuit_agente, periodo)

# primera_quincena, segunda_quincena = file_utils.split_detalle_quincena(detalle)


# validation.sirtac_900(detalle, resumen, cuit_agente, periodo)
report.validacion(detalle_ret, detalle_per, resumen, cuit_agente, periodo)
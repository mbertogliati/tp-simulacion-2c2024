from fitter import Fitter
import pandas as pd
from datetime import datetime, timedelta


datos_intervalo_clicks = "CLICKS_POR_HORA_Y_POR_DIA.csv"
datos_demora_adquisicion = ""
datos_vida_util_dominio = ""

def obtener_parametros_intervalo_clicks():
    df = pd.read_csv(datos_intervalo_clicks)
    sample = df['Clicks']

    # mu = np.mean(weighted_sample)
    # sigma = np.std(weighted_sample)
    # x_range = np.linspace(min(weighted_sample), max(weighted_sample), 1000)

    f = Fitter(sample,distributions=['gamma','rayleigh','uniform', 'laplace', 'norm'])
    f.fit()
    #f.summary(10)


    ## Obtener mejor distribución
    best_dist_name=f.get_best(method='sumsquare_error')
    print(f'BEST DISTRIBUTION: {best_dist_name}')

    #Print the minimum and the maximum
    print(f'MAX: {sample.max()}')
    print(f'MIN: {sample.min()}')

    # loc=best_dist_name['norm']['loc']
    # scale=best_dist_name['norm']['scale']

    def funcion_acumulacion(x):
      return stats.norm.rayleigh(x,loc=284.0784881200463,scale=23.70876879500182)

    def funcion_inversa(x):
      return stats.norm.rayleigh(x,loc=loc,scale=scale)
    #
    # def generar_tiempo_respuesta_incidente():
    #   r=random.random()
    #   return funcion_inversa(r)


    # print("Valor cercano a 0: " + str(funcion_inversa(0.0001)))
    # print("Valor cercano a 1: " + str(funcion_inversa(0.999999999)))
    # print("Valor 0.5: " + str(funcion_inversa(0.5)))

obtener_parametros_intervalo_clicks()

# {'rayleigh': {'loc': -33.39920383559722, 'scale': 143.2873228044864}}
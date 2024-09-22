from fitter import Fitter
import pandas as pd
from datetime import datetime, timedelta

datos = [#'CLICKS_POR_HORA_Y_POR_DIA.csv',
         #'datos_costos_rotacion.csv',
         #'datos_costos_adquisicion.csv',
         #'datos_tiempo_activacion.csv',
         'datos_tiempo_vida.csv'
         ]
datos_demora_adquisicion = ""
datos_vida_util_dominio = ""

def imprimir_distribuciones():
    for file in datos:
        df = pd.read_csv(file)
        sample = df['data']

        f = Fitter(sample, distributions=['lognorm'])
        f.fit(progress=False)

        ## Obtener mejor distribución
        ## best_dist_name = f.summary(Nbest=5,plot=False)
        best_dist_name = f.get_best()

        print(f'FILE: {file}')
        print(f'BEST DISTRIBUTION: {best_dist_name}')

        #Print the minimum and the maximum
        print(f'MAX: {sample.max()}')
        print(f'MIN: {sample.min()}')
        print('\n--------------------------------------------\n')
    
imprimir_distribuciones()
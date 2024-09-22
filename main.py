#DATOS DE LA REALIDAD
from typing import List
from scipy.stats import levy_stable, gamma, lognorm, geninvgauss, exponweib
import random

PC : float = 0 # Porcentaje de compras
HV : int = 10**18
SEGUNDOS_EN_UNA_SEMANA : int = 60*60*24*7

## BEST FIT FOR CLICKS PER DAY{'rayleigh': {'loc': -33.39920383559722, 'scale': 143.2873228044864}}
best_fits = {
    'IC': { # Intervalo entre clicks
        'dist': {
            'name': 'geninvgauss',
            'p': 0.7597113739326666,
            'b': 1.4911571279408409,
            'loc': -13.743531404179322,
            'scale': 79.7246922914876
        },
        'max': 1207,
        'min': 1
    },
    'CA': { # Costo adquisicion
        'dist': {
            'name': 'gamma',
            'a': 1.4730391947214025,
            'loc': 49.19229019699269,
            'scale': 82.49718309481199
        },
        'max': 669.9503172603885,
        'min': 50.11866796937669
    },
    'IA': { # Tiempo activacion
        'dist': {
            'name': 'exponweib',
            'a': 1.0915297707528975,
            'c': 0.9453921404012922,
            'loc': 1.999993712399898,
            'scale': 3.7061185422875864
        },
        'max': 32.72869286435422,
        'min': 2.0000621696849827
    },
    'CR': { # Costo rotacion
        'dist': {
            'name': 'levy_stable',
            'alpha': 2.0,
            'beta': 1.0,
            'loc': 38.74398740006481,
            'scale': 10.382470533203918
        },
        'max': 96.00619072342832,
        'min': 3.1380802068300326
    },
    'IV': {
        'dist': {
            'name': 'lognorm',
            's': 2.592271521409489,
            'loc': 10680.598692429028,
            'scale': 228360.65207097685
        },
        'max': 49273404,
        'min': 10810
    }
}

def fdp_acumulada_inversa_costo_adquisicion(x):
    data = best_fits['CA']['dist']
    return gamma.ppf(x, a=data['a'], loc=data['loc'], scale=data['scale'])
def fdp_acumulada_inversa_tiempo_vida(x):
    data = best_fits['IV']['dist']
    return lognorm.ppf(x, s=data['s'], loc=data['loc'], scale=data['scale'])
def fdp_acumulada_inversa_tiempo_activacion(x):
    data = best_fits['IA']['dist']
    return exponweib.ppf(x, a=data['a'], c=data['c'], loc=data['loc'], scale=data['scale'])*60*60
def fdp_acumulada_inversa_costo_rotacion(x):
    data = best_fits['CR']['dist']
    return levy_stable.ppf(x, alpha=data['alpha'], beta=data['beta'], loc=data['loc'], scale=data['scale'])
def fdp_acumulada_inversa_clicks(x):
    data = best_fits['IC']['dist']
    return geninvgauss.ppf(x, p=data['p'], b=data['b'], loc=data['loc'], scale=data['scale'])/(60*60)

# Eventos posibles
def proximo_evento(TPA, TPR, TPC):
    if TPA <= TPR:
        if TPA < TPC:
            return "ADQUISICION"
        return "CLICK"
    elif TPC <= TPR:
        return "CLICK"
    else:
        "ROTACION"

def generar(valor: str) -> float:

    if valor == 'IC':
        acumulada_inversa = fdp_acumulada_inversa_clicks
    elif valor == 'CA':
        acumulada_inversa = fdp_acumulada_inversa_costo_adquisicion
    elif valor == 'IA':
        acumulada_inversa = fdp_acumulada_inversa_tiempo_activacion
    elif valor == 'CR':
        acumulada_inversa = fdp_acumulada_inversa_costo_rotacion
    elif valor == 'IV':
        acumulada_inversa = fdp_acumulada_inversa_tiempo_vida
    else:
        raise 'INVALID VALUE'

    max = best_fits[valor]['max']
    min = best_fits[valor]['min']

    r = random.random()
    valor = acumulada_inversa(r)
    while valor < min or valor > max:
        r = random.random()
        valor = acumulada_inversa(r)
    return valor

# Logica principal
def iniciar_simulacion(IR, ND, TF):
    global PC, SEGUNDOS_EN_UNA_SEMANA
    # | Condiciones iniciales | #
    T : int = 0  # Tiempo en segundos
    i : int = 0 # Posicion del dominio activo
    TPA = HV # Tiempo de proxima activacion
    TPR = IR # Tiempo de proxima rotacion
    TPC = 0 # Tiempo del proximo click
    SCR : float = 0  # Suma de Costos de Rotación
    SCA : float = 0  # Suma de Costos de Activación
    STO : int = 0  # Suma del Tiempo Ocioso
    DA : int = 0   # Dominio activo
    NCR : int = 0  # Cantidad de clicks rechazados
    NCV : int = 0  # Cantidad de clicks válidos
    IUA : int = 0  # Instante de Última Activación
    TA : List[int] = []  # Tiempo de Activación
    TV : List[int] = []  # Tiempo de vencimiento
    NC : List[int] = []  # Cantidad de clicks validos en el dominio i desde su ultima activacion
    ITO : List[int] = [] # Instante de comienzo de tiempo ocioso

    for i in range(ND):
        TA.append(HV)
        TV.append(generar('IV'))
        NC.append(0)
        ITO.append(0)

    while T < TF:
        evento = proximo_evento(TPA,TPR,TPC)
        if evento == "CLICK":
            T = TPC
            IC = generar('IC')
            TPC = TPC + IC
            if TV[DA] < T or TA[DA] > T:
                NCR += 1
            else:
                NC[DA] += 1
                NCV += 1
                if NC[DA] / (T - IUA) >= 500:
                    TPR = T
        elif evento == "ROTACION":
            T = TPR
            CR = generar('CR')
            SCR = SCR + CR
            TPR = T + IR
            i = DA
            while True:
                i = i + 1
                if i >= ND:
                    i = 0
                    continue
                elif i == DA:
                    TPA = T
                    break
                if TV[i] < T or TA[i] > T:
                    TPA = T
                    continue
                else:
                    IUA = T
                    STO = STO + (T - ITO[i])
                    ITO[DA] = T
                    DA = i
                    break
        elif evento == "ADQUISICION":
            T = TPA
            CA = generar('CA')
            SCA += CA
            for i in range(ND):
                if TV[i] < T:
                    TV[i] = T + generar('IV')
                    TA[i] = T + generar('IA')
                    ITO[i] = TA[i]
    # Calculo
    PTO = 100 * STO / T
    PCNP = 100 * NCR / (NCR+NCV)
    PCDS = (SCA + SCR) / (T / SEGUNDOS_EN_UNA_SEMANA)
    PCP = PCNP * PC
    # Salidas e impresiones
    print(f"PTO: {PTO}")
    print(f"PCNP: {PCNP}")
    print(f"PCDS: {PCDS}")
    print(f"PCP: {PCP}")
    return {'PTO': PTO, 'PCNP': PCNP, 'PCDS': PCDS, 'PCP': PCP}

def calculate_weight(pto, pcnp, pcds):
    peso_pto = 20
    peso_pcnp = 30
    peso_pcds = 50
    return (peso_pto/pto + peso_pcnp/pcnp + peso_pcds/pcds )/ 3.0

def main():
    TF = 60*60*24*30 # 1 MONTH
    IR = 2 * 60 * 60
    ND = 5
    test_fdp()
    # iniciar_simulacion(IR,ND,TF)



def calculate_best(TF):

    ir_min = 1 * 60 * 60  # 1 HORA
    ir_max = 48 * 60 * 60  # 2 DIAS

    nd_min = 2
    nd_max = 20

    current_ir = ir_min
    current_nd = nd_min

    better = None

    while current_ir <= ir_max:
        current_nd = nd_min
        while current_nd <= nd_max:
            results = iniciar_simulacion(current_ir, current_nd, TF)
            weight = calculate_weight(results['PTO'], results['PCNP'], results['PCP'])
            if better is None or better['weight'] < weight:
                better = {
                    'ir': current_ir,
                    'nd': current_nd,
                    'results': results,
                    'weight': weight
                }
            current_nd += 1
        current_ir += 60 * 60  # 1 hora

    print(f'BEST OUTCOME: {better}')


def test_fdp():
    variables_a_generar = ['IC','CA','IA','CR','IV']
    for v in variables_a_generar:
        print(f'## {v} ##:')
        for i in range(10):
            print(generar(v))
        print('\n\n')

if __name__ == "__main__":
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

#DATOS DE LA REALIDAD
from typing import List
from scipy.stats import rayleigh, stats
import random

PC : float = 0 # Porcentaje de compras
HV : int = 10**18
SEGUNDOS_EN_UNA_SEMANA : int = 60*60*24*7

## BEST FIT FOR CLICKS PER DAY{'rayleigh': {'loc': -33.39920383559722, 'scale': 143.2873228044864}}
best_fit = {
    'loc': -33.39920383559722,
    'scale': 143.2873228044864
}
max_clicks_per_hour = 1207
min_click_per_hour = 1

def fdp_acumulada_clicks(x):
    return rayleigh.cdf(x, loc=best_fit['loc'], scale=best_fit['scale'])

def fdp_acumulada_inversa_clicks(x):
    return rayleigh.ppf(x, loc=best_fit['loc'], scale=best_fit['scale'])

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

def generar_IC() -> int:
    valor: int
    r = random.random()
    valor = fdp_acumulada_inversa_clicks(r)
    while valor < min_click_per_hour or valor > max_clicks_per_hour:
        r = random.random()
        valor = fdp_acumulada_inversa_clicks(r)

    return valor

def generar_CR() -> float:
    pass

def generar_CA() ->float:
    pass

def generar_IV() -> int:
    pass

def generar_IA() -> int:
    pass

# Logica principal
def iniciar_simulacion(IR, ND, TF):
    global PC, SEGUNDOS_EN_UNA_SEMANA
    # | Condiciones iniciales | #
    T : int = 0  # Tiempo
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
        TV.append(generar_IV())
        NC.append(0)
        ITO.append(0)

    while T < TF:
        evento = proximo_evento(TPA,TPR,TPC)
        if evento == "CLICK":
            T = TPC
            IC = generar_IC()
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
            CR = generar_CR()
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
            CA = generar_CA()
            SCA += CA
            for i in range(ND):
                if TV[i] < T:
                    TV[i] = T + generar_IV()
                    TA[i] = T + generar_IA()
                    ITO[i] = TA[i]
    # Calculo
    PTO = 100 * STO / T
    PCNP = 100 * NCR / (NCR+NCV)
    PCDS = (SCA + SCR) / (T / SEGUNDOS_EN_UNA_SEMANA)
    PCP = PCNP * PC
    # Salidas e impresiones
    print(f"PTO: {PTO}")
    print(f"PCNP: {(NCR / (NCR + NCV)) * 100}")
    print(f"PCDS: {(SCA + SCR) * 100}")

def main():
    FRD = 0
    ND = 0
    TF = 1000000
    #iniciar_simulacion(FRD,ND,TF)
    print(generar_IC())
    print(generar_IC())
    print(generar_IC())
    print(generar_IC())
    print(generar_IC())

if __name__ == "__main__":
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

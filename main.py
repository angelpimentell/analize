from lxml import etree
import statistics
from datetime import datetime

FILE_PATH = "C:\\Users\\Angel\\Documents\\TRADING\\STRATEGIES\\BUY-SELL-GBPJPY\\BAJISTA\\Statement.htm"

trades = []
duraciones_horas = []

with open(FILE_PATH, "r", encoding="utf-8") as f:
    contenido = f.read()

parser = etree.HTMLParser()
arbol = etree.HTML(contenido, parser)

filas = arbol.xpath("//tr")

for i, fila in enumerate(filas, start=1):
    td14 = fila.xpath("td[14]/text()")

    try:
        float(td14[0])
        pass
    except:
        continue

    celdas = fila.findall('td')
    if len(celdas) >= 9:
        try:
            fecha_inicio = datetime.strptime(celdas[1].text.strip(), "%Y.%m.%d %H:%M:%S")
            fecha_cierre = datetime.strptime(celdas[8].text.strip(), "%Y.%m.%d %H:%M:%S")
            duracion = (fecha_cierre - fecha_inicio).total_seconds() / 3600  # en horas
            duraciones_horas.append(duracion)
        except:
            print(f"Error procesando fila")

    trades.append(float(td14[0]))


def calcular_promedios_rachas(trades):
    rachas_ganadoras = []
    rachas_perdedoras = []
    racha_actual = []
    tipo_actual = None  # 'win' o 'loss'

    for t in trades:
        tipo = 'win' if t > 0 else 'loss'

        if tipo != tipo_actual:
            if tipo_actual == 'win':
                rachas_ganadoras.append(len(racha_actual))
            elif tipo_actual == 'loss':
                rachas_perdedoras.append(len(racha_actual))
            racha_actual = [t]
            tipo_actual = tipo
        else:
            racha_actual.append(t)

    # Añadir la última racha
    if tipo_actual == 'win':
        rachas_ganadoras.append(len(racha_actual))
    elif tipo_actual == 'loss':
        rachas_perdedoras.append(len(racha_actual))

    promedio_ganadoras = sum(rachas_ganadoras) / len(rachas_ganadoras)
    promedio_perdedoras = sum(rachas_perdedoras) / len(rachas_perdedoras)

    return {
        'promedio_ganadoras': promedio_ganadoras,
        'promedio_perdedoras': promedio_perdedoras,
        'racha_ganadora_max': max(rachas_ganadoras),
        'racha_perdedora_max': max(rachas_perdedoras),
    }


# Ejecutar
resultado = calcular_promedios_rachas(trades)
print("Promedio de trades ganadores consecutivos:", resultado['promedio_ganadoras'])
print("Promedio de trades perdedores consecutivos:", resultado['promedio_perdedoras'])

print("")
print("Racha ganadora más larga:", resultado['racha_ganadora_max'])
print("Racha perdedora más larga:", resultado['racha_perdedora_max'])

print("")
if duraciones_horas:
    promedio = statistics.mean(duraciones_horas)
    minimo = min(duraciones_horas)
    maximo = max(duraciones_horas)
    print(f"Duración promedio de los trades: {promedio:.2f} horas")
    print(f"Duración mínima: {minimo:.2f} horas")
    print(f"Duración máxima: {maximo:.2f} horas")
else:
    print("No se encontraron duraciones válidas.")

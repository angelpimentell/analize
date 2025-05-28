from lxml import etree

trades = []

# Carga el archivo .htm
with open("C:\\Users\Angel\Documents\TRADING\STRATEGIES\BUY-SELL-GBPJPY\BAJISTA\Statement.htm", "r",
          encoding="utf-8") as f:
    contenido = f.read()

# Parseamos el contenido HTML
parser = etree.HTMLParser()
arbol = etree.HTML(contenido, parser)

# Seleccionamos todas las filas tr
filas = arbol.xpath("//tr")

# Iteramos cada fila y extraemos el td número 14 (índice XPath empieza en 1)
for i, fila in enumerate(filas, start=1):
    # Extraemos el td[14]
    td14 = fila.xpath("td[14]/text()")

    try:
        float(td14[0])
        pass
    except:
        continue

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
print("Racha ganadora más larga:", resultado['racha_ganadora_max'])
print("Racha perdedora más larga:", resultado['racha_perdedora_max'])

import os
import re


def clear():
    os.system('cls')


def __calcula_bloque(bloque, pesos):
    pesos_temporal = list(pesos)

    # print(bloque)
    if len(bloque) == len(pesos):
        # ASIGA 0 A NA
        for i, item in enumerate(bloque):
            if item == "NA":
                # print("i: {} es NA".format(i))
                pesos_temporal[i] = 0

        # print(f"Pesos: {pesos}")
        # print(f"Pesos temporal: {pesos_temporal}")

        total_temporal = sum(pesos_temporal)

        for i, item in enumerate(pesos_temporal):
            # Calcula el nuevo peso de cada item
            # todo VERIFICAR FORMULA Y OPTIMIZAR
            if total_temporal == 0:
                return sum(pesos)
            elif bloque[i] == "NO":
                pesos_temporal[i] = 0
            else:
                pesos_temporal[i] = item / total_temporal

        # print(pesos_temporal)
        # print(sum(pesos) * sum(pesos_temporal))
        return sum(pesos) * sum(pesos_temporal)
    else:
        raise Exception("Error en bloque")


def calcula_nota(items_base):
    pesos_tec = (1, 2, 2, 2, 1, 5, 4, 10, 4, 4, 22, 0, 0, 0, 0, 0, 0, 0, 7, 2, 15, 3, 3, 3, 2, 2, 3, 3)
    pesos_adm = (1, 2, 2, 2, 1, 3, 4, 10, 3, 2, 3, 2, 2, 14, 0, 0, 0, 2, 2, 2, 2, 5, 2, 15, 3, 3, 3, 2, 2, 3, 3)
    evaluacion = ''.join(str(items_base)).replace("None", "NA")

    evaluacion = re.findall(r"\bSI\b|\bNO\b|\bNA\b", evaluacion)

    if len(evaluacion) == 28:
        bloque1 = evaluacion[0:5]
        bloque2 = evaluacion[5:9]
        bloque3 = evaluacion[9:20]
        bloque4 = evaluacion[20:24]
        bloque5 = evaluacion[24:27]
        bloque6 = evaluacion[27:28]
        bloque1_pesos = pesos_tec[0:5]
        bloque2_pesos = pesos_tec[5:9]
        bloque3_pesos = pesos_tec[9:20]
        bloque4_pesos = pesos_tec[20:24]
        bloque5_pesos = pesos_tec[24:27]
        bloque6_pesos = pesos_tec[27:28]

    elif len(evaluacion) == 31:
        bloque1 = evaluacion[0:5]
        bloque2 = evaluacion[5:9]
        bloque3 = evaluacion[9:23]
        bloque4 = evaluacion[23:27]
        bloque5 = evaluacion[27:30]
        bloque6 = evaluacion[30:31]
        bloque1_pesos = pesos_adm[0:5]
        bloque2_pesos = pesos_adm[5:9]
        bloque3_pesos = pesos_adm[9:23]
        bloque4_pesos = pesos_adm[23:27]
        bloque5_pesos = pesos_adm[27:30]
        bloque6_pesos = pesos_adm[30:31]

    else:
        raise Exception("Erro de cadena")

    b1 = __calcula_bloque(bloque1, bloque1_pesos)
    b2 = __calcula_bloque(bloque2, bloque2_pesos)
    b3 = __calcula_bloque(bloque3, bloque3_pesos)
    b4 = __calcula_bloque(bloque4, bloque4_pesos)
    b5 = __calcula_bloque(bloque5, bloque5_pesos)
    b6 = __calcula_bloque(bloque6, bloque6_pesos)

    # print("######################################")
    # print(f"NOTA FINAL: {b1 + b2 + b3 + b4 + b5 + b6}")
    # print("######################################")

    return round(b1 + b2 + b3 + b4 + b5 + b6, 2)


if __name__ == '__main__':
    # print(calcula_nota(
    #     ('SI', 'SI', 'SI', 'SI', 'NA', 'SI', 'NA', 'SI', 'SI', 'SI', 'SI', 'SI', 'SI', 'SI', 'SI', 'NA', 'NA',
    #      'NA', 'SI', 'SI', 'SI', 'NO', 'SI', 'SI', 'SI', 'SI', 'SI', 'NA')))
    print(calcula_nota(
        ('SI', 'SI', 'SI', 'SI', 'SI', 'NO', 'NO', 'NO', 'SI', 'SI', 'NO', 'SI', 'NO', 'NO', 'SI', 'NO', 'NA',
         'NA', 'NO', 'NO', 'NO', 'NO', 'NO', 'NO', 'SI', 'SI', 'SI', 'NA')))

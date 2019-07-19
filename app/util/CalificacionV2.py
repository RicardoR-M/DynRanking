from app.config import get_pesos_tec, get_pesos_adm


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


def calcula_nota(items_base, skill):
    pesos_tec = get_pesos_tec()
    pesos_adm = get_pesos_adm()
    # evaluacion = ''.join(str(items_base)).replace("None", "NA")

    # items_lista = re.findall(r"\bSI\b|\bNO\b|\bNA\b", items_lista)

    if skill.upper() == 'TEC':
        bloque1 = [valida_item(items_base['SaludaCliente']),
                   valida_item(items_base['SeDirigePorNombre']),
                   valida_item(items_base['InteractuaConCliente']),
                   valida_item(items_base['EvitaUsoTecnicismos']),
                   valida_item(items_base['SeDespideComoIndicaManual'])]

        bloque2 = [valida_item(items_base['ValidaConsultaTransaccion']),
                   valida_item(items_base['RealizaPreguntasPrecision']),
                   valida_item(items_base['ValidaMotivoReal']),
                   valida_item(items_base['ValidaAtencionPrevia'])]

        bloque3 = [valida_item(items_base['ValidaCES']),
                   valida_item(items_base['AtencionPasoAPaso']),
                   valida_item(items_base['SolicitaDNIRUC']),
                   valida_item(items_base['ValidaTRACER']),
                   valida_item(items_base['VerificaWebAverias']),
                   valida_item(items_base['VerificaParametrosServicios']),
                   valida_item(items_base['ProblemasInternetIngresaEMTA']),
                   valida_item(items_base['ProblemasTelefoniaIngresaJANUS']),
                   valida_item(items_base['ProblemasInternetSmarTV']),
                   valida_item(items_base['ExplicacionBrindadaCorresponde']),
                   valida_item(items_base['ValidaConClienteInformacion'])]

        bloque4 = [valida_item(items_base['EjecutaAccionesAplicativos']),
                   valida_item(items_base['SeTipificaSIACSGA']),
                   valida_item(items_base['NotasPlantillaTipificacion']),
                   valida_item(items_base['SeTipificaEnSIAC'])]

        bloque5 = [valida_item(items_base['EvitaComentariosNegativos']),
                   valida_item(items_base['EvitaPalabraSoeces']),
                   valida_item(items_base['EscuchaClienteSinInterrumpirlo'])]

        bloque6 = [valida_item(items_base['MotivoRealNecesidad'])]

        bloque1_pesos = pesos_tec[0:5]
        bloque2_pesos = pesos_tec[5:9]
        bloque3_pesos = pesos_tec[9:20]
        bloque4_pesos = pesos_tec[20:24]
        bloque5_pesos = pesos_tec[24:27]
        bloque6_pesos = pesos_tec[27:28]

    elif skill.upper() == 'ADM':
        bloque1 = items_base[0:5]
        bloque2 = items_base[5:9]
        bloque3 = items_base[9:23]
        bloque4 = items_base[23:27]
        bloque5 = items_base[27:30]
        bloque6 = items_base[30:31]
        bloque1_pesos = pesos_adm[0:5]
        bloque2_pesos = pesos_adm[5:9]
        bloque3_pesos = pesos_adm[9:23]
        bloque4_pesos = pesos_adm[23:27]
        bloque5_pesos = pesos_adm[27:30]
        bloque6_pesos = pesos_adm[30:31]

    else:
        raise Exception("Error de cadena")

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


def valida_item(i):
    if i is None or i == '':
        return 'NA'
    return i


if __name__ == '__main__':
    # print(calcula_nota(
    #     ('SI', 'SI', 'SI', 'SI', 'NA', 'SI', 'NA', 'SI', 'SI', 'SI', 'SI', 'SI', 'SI', 'SI', 'SI', 'NA', 'NA',
    #      'NA', 'SI', 'SI', 'SI', 'NO', 'SI', 'SI', 'SI', 'SI', 'SI', 'NA')))
    print(calcula_nota(
        ('SI', 'SI', 'SI', 'SI', 'SI', 'NO', 'NO', 'NO', 'SI', 'SI', 'NO', 'SI', 'NO', 'NO', 'SI', 'NO', 'NA',
         'NA', 'NO', 'NO', 'NO', 'NO', 'NO', 'NO', 'SI', 'SI', 'SI', 'NA'), 'TEC'))

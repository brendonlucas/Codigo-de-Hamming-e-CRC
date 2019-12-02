def main():
    palavra = '111100101'
    palavra = '101000100111011011'
    palavra = '1100110000111'
    palavra = '000101100111101111011111100'
    g_x = '101101'
    g_x = '10101'
    g_x = '110111'
    g_x = '001111010010011'

    print('-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-')
    print('-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* TRANSMISSOR *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-')
    print('-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-')
    grau = calcular_grau_g_x(g_x)
    palavra_montada = montar_palavra(grau, palavra)
    resto_final_transmissor = calcular_envio(palavra_montada, g_x, grau)
    palavra_transmitida = palavra + resto_final_transmissor

    resto_final_receptor = calcular_envio(palavra_transmitida, g_x, grau)
    print("RESTO DA DIVISAO FEITA PELO TRANSMISSOR:", resto_final_transmissor)
    print("RESTO DA DIVISAO FEITA PELO RECEPTOR:", resto_final_receptor)
    print('Palavra transmitida', palavra_transmitida)

    if resto_final_receptor == '0' * grau:
        print("A palavra chegou corretamente!")
    else:
        print('A palavra não chegou corretamente!')


def calcular_envio(palavra, g_x, grau):
    g_x = remove_0_g_x(g_x)
    n_divisao = palavra[0:len(g_x)]
    r_divisao = dividir(n_divisao, g_x)
    posicao_atual = grau
    while True:
        if posicao_atual >= len(palavra) - 1:
            break
        result = monta_proximo_dividendo(palavra, r_divisao, posicao_atual, grau)
        dividendo = result[1]
        posicao_atual = result[2]

        if result[3] == 1:
            r_divisao = dividir(dividendo, g_x)
        else:
            r_divisao = dividendo

    resto_final = r_divisao[len(r_divisao) - grau:len(r_divisao)]
    return resto_final


def monta_proximo_dividendo(palavra, r_divisao, posicao_atual, grau):
    achou_1 = 0
    zeros_inicio = 0
    n_resto = ''
    posi_atual = posicao_atual
    ainda_divisivel = 1
    for i in range(len(r_divisao)):
        n_1 = r_divisao[i]
        if n_1 == '0' and achou_1 == 0:
            zeros_inicio += 1
        else:
            achou_1 = 1
            n_resto += n_1
    if zeros_inicio > 0:
        if len(palavra[posicao_atual+1:len(palavra)]) >= zeros_inicio:
            for j in range(posi_atual + 1, posi_atual + zeros_inicio + 1):
                n_resto += palavra[j]
                posi_atual += 1
        else:
            n_resto = r_divisao + palavra[posicao_atual + 1:len(palavra)]
            n_resto = n_resto[len(n_resto) - grau - 1:len(n_resto)]
            posi_atual = len(palavra)
            ainda_divisivel = 0
    return [zeros_inicio, n_resto, posi_atual, ainda_divisivel]


def remove_0_g_x(g_x):
    achou_1 = 0
    grau = 0
    novo_g_x = ''
    for i in range(len(g_x)):
        n_1 = g_x[i]
        if n_1 == '0' and achou_1 == 0:
            pass
        else:
            achou_1 = 1
            novo_g_x += n_1
            grau += 1
    return novo_g_x


def calcular_grau_g_x(g_x):
    achou_1 = 0
    grau = 0
    for i in range(len(g_x)):
        n_1 = g_x[i]
        if n_1 == '0' and achou_1 == 0:
            pass
        else:
            achou_1 = 1
            grau += 1
    return grau - 1


def montar_palavra(grau, palavra):
    zeros = '0' * grau
    return palavra + zeros


def dividir(a, g_x):
    resposta = ''
    for i in range(len(a)):
        n_1 = a[i]
        n_2 = g_x[i]
        if n_1 == n_2:
            resposta += '0'
        else:
            resposta += '1'
    return resposta


if __name__ == '__main__':
    main()

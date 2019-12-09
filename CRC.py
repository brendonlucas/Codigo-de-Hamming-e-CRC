def main():
    palavra = str(input("Digite a palvra inicial a ser transmitida, formada por bits 0 e 1. \n >> "))
    while True:
        g_x = str(input("Informe o Polinomio gerador: "))
        if len(g_x) >= 2 and g_x[0] == '1' and g_x[len(g_x)-1] == '1':
            break
        else:
            print("Polinomio gerador Invalido!!")
    print()
    print('-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* TRANSMISSOR *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-')
    grau = calcular_grau_g_x(g_x)
    palavra_montada = montar_palavra(grau, palavra)
    resto_final_transmissor = calcular_envio(palavra_montada, g_x, grau)
    palavra_transmitida = palavra + resto_final_transmissor

    print("RESTO DA DIVISAO FEITA PELO TRANSMISSOR:", resto_final_transmissor)
    print('Palavra a ser transmitida', palavra_transmitida)

    opcao = input("Gerar Erro ? 1-sim / 2-não \n>> ")
    if opcao == '1':
        while True:
            local = int(input("Em qual local da palavra? no maximo: " + str(len(palavra_transmitida)) + " >> "))
            if len(palavra_transmitida) >= local > 0:
                palavra_transmitida = gerar_erro(palavra_transmitida, local)
                break

    palavra_recebida = palavra_transmitida
    print()
    print('-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* Receptor *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-')
    grau = calcular_grau_g_x(g_x)
    resto_final_receptor = calcular_envio(palavra_recebida, g_x, grau)
    print("RESTO DA DIVISAO FEITA PELO RECEPTOR:", resto_final_receptor)

    print()
    print('-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* Saida final *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-')
    print("RESTO DA DIVISAO FEITA PELO TRANSMISSOR:", resto_final_transmissor)
    print("RESTO DA DIVISAO FEITA PELO RECEPTOR:", resto_final_receptor)
    print('Palavra transmitida', palavra_recebida)

    if resto_final_receptor == '0' * grau:
        print("A palavra chegou corretamente!")
    else:
        print('A palavra não chegou corretamente!')


def gerar_erro(palavra_recebida, local):
    nova_palavra_recebida = ''
    for i in range(len(palavra_recebida)):
        if i == local - 1:
            if palavra_recebida[i] == '0':
                nova_palavra_recebida += '1'
            else:
                nova_palavra_recebida += '0'
        else:
            nova_palavra_recebida += palavra_recebida[i]
    return nova_palavra_recebida


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

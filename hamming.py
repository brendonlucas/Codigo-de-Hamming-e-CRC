def main():
    palavra_inicial = input("Digite a palavra inicial formada por bits 0 e 1: \n>>")
    while True:
        paridade = int(input("Digite a paridade: 1-par ou 2-impar"))
        if paridade == 1:
            paridade = 'par'
            break
        elif paridade == 2:
            paridade = 'impar'
            break

    """----------------------------------------TRANSMISSOR------------------------------------------------"""
    palavra_sem_bits_de_verificacao = completar_matriz(palavra_inicial)
    matriz_de_dados = fazer_matriz_de_dados(palavra_sem_bits_de_verificacao)
    bits_de_verificacao = achar_bits_validacao(palavra_sem_bits_de_verificacao)
    matriz_de_paridade = montar_matriz_para_paridade(bits_de_verificacao)
    preencher_matriz_de_paridade(palavra_sem_bits_de_verificacao, matriz_de_paridade, matriz_de_dados)
    paridades = calcula_paridade(matriz_de_paridade, paridade)
    palavra_enviada = montar_palavra_com_paridades(palavra_sem_bits_de_verificacao, paridades)

    opcao = input("Gerar Erro ? 1-sim / 2-não \n>> ")
    if opcao == '1':
        while True:
            local = int(input("Em qual local da palavra? no maximo: " + str(len(palavra_enviada)) + " >> "))
            if len(palavra_enviada) >= local > 0:
                palavra_enviada = gerar_erro(palavra_enviada, local)
                break

    print("""--------------------------------------------RECEPTOR------------------------------------------""")
    palavra_recebida = palavra_enviada
    matriz_de_dados_receptor = fazer_matriz_de_dados(palavra_recebida)
    bits_de_verificacao_receptor = achar_bits_validacao(palavra_recebida)
    matriz_de_paridade_receptor = montar_matriz_para_paridade(bits_de_verificacao_receptor)
    preencher_matriz_de_paridade(palavra_recebida, matriz_de_paridade_receptor, matriz_de_dados_receptor)
    paridades_receptor = calcula_paridade(matriz_de_paridade_receptor, paridade)
    verifica_se_chegou_certo(palavra_recebida, bits_de_verificacao_receptor, paridades_receptor)


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


def verifica_se_chegou_certo(palavra_recebida, bits_de_verificacao_receptor, paridades_receptor):
    paridades_palavra_recebida = ''
    for i in range(len(palavra_recebida)):
        if i + 1 in bits_de_verificacao_receptor:
            paridades_palavra_recebida += palavra_recebida[i]

    soma = 0
    for k in range(len(paridades_palavra_recebida)):
        v_p_recebida = paridades_palavra_recebida[k]
        v_p_receptor = paridades_receptor[k]
        v_bit_verificacao = bits_de_verificacao_receptor[k]
        if v_p_recebida != v_p_receptor:
            soma += v_bit_verificacao

    if soma != 0:
        if soma <= len(palavra_recebida):
            print('Palavra recebida :>>', palavra_recebida)
            print('O bit', soma, 'esta com erro')
        else:
            print('Palavra recebida :>>', palavra_recebida)
            print('o Bit', soma, 'não foi encontrado, possivel ter erro em mais de um bit')
    else:
        print('Palavra recebida :>>', palavra_recebida)
        print('A palavra chegou corretamente')


def montar_palavra_com_paridades(palavra, paridades):
    cont = 0
    nova_palavra = ''
    for i in range(len(palavra)):
        valor_palavra = palavra[i]
        if valor_palavra == '-':
            nova_palavra += paridades[cont]
            cont += 1
        else:
            nova_palavra += valor_palavra

    return nova_palavra


def calcula_paridade(matriz_de_paridade, paridade):
    paridades = ''
    for i in range(len(matriz_de_paridade)):
        valores = matriz_de_paridade[i][2]
        soma_paridade = 0
        for j in range(len(valores)):
            bit_valor = valores[j]
            if bit_valor == 1:
                soma_paridade += 1
        if paridade == 'par':
            if soma_paridade % 2 == 0:
                paridades += '0'
            else:
                paridades += '1'
        elif paridade == 'impar':
            if soma_paridade % 2 == 0:
                paridades += '1'
            else:
                paridades += '0'
    return paridades


def preencher_matriz_de_paridade(palavra, matriz_de_paridade, matriz_de_dados):
    for i in range(len(matriz_de_paridade)):
        valor_bit = matriz_de_paridade[i][0]
        for j in range(len(matriz_de_dados)):
            valores_m_dados = matriz_de_dados[j][1]
            if valor_bit in valores_m_dados:
                matriz_de_paridade[i][1].append(matriz_de_dados[j][0])
                matriz_de_paridade[i][2].append(int(palavra[matriz_de_dados[j][0] - 1]))


def montar_matriz_para_paridade(bits_de_verificacao):
    matriz = []
    for i in range(len(bits_de_verificacao)):
        matriz.append([bits_de_verificacao[i], [], []])
    return matriz


def fazer_matriz_de_dados(palavra):
    bits_validacao = achar_bits_validacao(palavra)
    matriz = []
    for i in range(1, len(palavra) + 1):
        if i not in bits_validacao:
            matriz.append([i, [0] * (len(bits_validacao))])

    for l in range(len(matriz)):
        bits_validacao_para_calculo = bits_validacao[::-1]
        n_maior = matriz[l][0]
        valor_alvo = matriz[l][0]
        soma_total = 0
        proximo_ponto_matrix = 0

        for k in range(len(bits_validacao_para_calculo)):
            bit_corrente = bits_validacao_para_calculo[k]
            if bit_corrente < n_maior:
                soma = bit_corrente + soma_total
                if soma <= valor_alvo:
                    soma_total += bit_corrente
                    matriz[l][1][proximo_ponto_matrix] = bit_corrente
                    n_maior = bit_corrente
                    proximo_ponto_matrix += 1
    return matriz


def completar_matriz(palavra):
    cont = 0
    cont_indice_z_palavra = 1
    n = 1
    z_palavra = ''
    while True:
        if n == cont_indice_z_palavra:
            z_palavra += '-'
            n += n
        else:
            z_palavra += str(palavra[cont])
            cont += 1
        cont_indice_z_palavra += 1
        if cont >= len(palavra):
            break
    return z_palavra


def achar_bits_validacao(palavra):
    n1 = 1
    bits = []
    while True:
        if n1 > len(palavra):
            break
        bits.append(n1)
        n1 += n1
    return bits


if __name__ == '__main__':
    main()

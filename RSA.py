from sympy import mod_inverse, gcd, factorint

# Tabela de pré-codificação
tabela_codificacao = {
    10: "A", 11: "B", 12: "C", 13: "D", 14: "E", 15: "F", 16: "G", 17: "H", 18: "I", 19: "J",
    20: "K", 21: "L", 22: "M", 23: "N", 24: "O", 25: "P", 26: "Q", 27: "R", 28: "S", 29: "T",
    30: "U", 31: "V", 32: "W", 33: "X", 34: "Y", 35: "Z", 99: " "
}

def criptografar_mensagem(mensagem, n, e):
    # Tabela invertida para conversão de letras para números
    tabela_invertida = {v: k for k, v in tabela_codificacao.items()}
    numeros = [tabela_invertida[c.upper()] for c in mensagem if c.upper() in tabela_invertida]
    numeros_criptografados = [pow(m, e, n) for m in numeros]
    return numeros, numeros_criptografados

def interpretar_sequencialmente(valor, tabela, sobra=""):
    resultado = ""
    valor_str = sobra + str(valor)  # Inclui a sobra no início
    print(f"Processando valor decodificado: {valor_str}")
    i = 0
    sobra_atual = ""  # Inicializa a sobra atual para este número
    while i < len(valor_str):
        # Tenta pegar dois dígitos primeiro
        if i + 1 < len(valor_str):
            num = int(valor_str[i:i + 2])
            if num in tabela:
                letra = tabela[num]
                print(f"Par {num} -> {letra}")
                resultado += letra
                i += 2  # Avança dois dígitos
                continue
        # Se não for possível pegar dois dígitos, trata como sobra
        sobra_atual = valor_str[i:]
        print(f"Sobra detectada: {sobra_atual}")
        break
    return resultado, sobra_atual


def decodificar_mensagem(n, e, tabela, valores_codificados):
    # Calcula φ(n) a partir de n (fatoração)
    fatores = factorint(n)
    p, q = list(fatores.keys())
    phi_n = (p - 1) * (q - 1)

    # Verifica se e é coprimo com φ(n)
    if gcd(e, phi_n) != 1:
        raise ValueError(f"e = {e} não é coprimo com φ(n) = {phi_n}. Escolha outro valor para e.")

    # Calcula d
    d = mod_inverse(e, phi_n)

    mensagem_decodificada = ""
    sobra = ""  # Inicialmente, não há sobra

    for valor in valores_codificados:
        c = int(valor)
        # Decodifica o número
        m = pow(c, d, n)
        print(f"\nValor decodificado de {c}: {m}")
        interpretado, sobra = interpretar_sequencialmente(m, tabela, sobra)
        mensagem_decodificada += interpretado

    print("\nMensagem decodificada final:", mensagem_decodificada)


# Solicitar n e e apenas uma vez
print("\nInsira a chave pública inicial (n e):")
n = int(input("n (módulo): "))
e = int(input("e (expoente público): "))

# Loop principal
while True:
    print("\nEscolha uma operação:")
    print("1 - Criptografar mensagem")
    print("2 - Decodificar mensagem")
    print("3 - Encerrar")
    print("4 - Alterar n e e")
    opcao = int(input("Opção: "))

    if opcao == 1:
        # Criptografar mensagem
        mensagem = input("\nInsira a mensagem a ser criptografada: ")
        numeros, criptografados = criptografar_mensagem(mensagem, n, e)
        print("\nMensagem original:", mensagem)
        print("Números correspondentes:", " ".join(map(str, numeros)))
        print("Mensagem criptografada:", " ".join(map(str, criptografados)))
    elif opcao == 2:
        # Decodificar mensagem
        print("\nInsira os valores codificados separados por espaço:")
        valores_codificados = input("Valores: ").strip().split()
        decodificar_mensagem(n, e, tabela_codificacao, valores_codificados)
    elif opcao == 3:
        print("\nEncerrando o programa...")
        break
    elif opcao == 4:
        # Alterar n e e
        print("\nInsira os novos valores para n e e:")
        n = int(input("n (módulo): "))
        e = int(input("e (expoente público): "))
        print("\nChave pública atualizada com sucesso!")
    else:
        print("\nOpção inválida! Tente novamente.")

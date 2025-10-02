menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
[nu] Novo Usuário
[cc] Criar Conta
[lc] Listar Contas

=> """

LIMITE_SAQUES = 3
AGENCIA = "0001"

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
usuarios = []
contas = []
numero_conta = 1


def filtrar_usuarios(cpf, usuarios):
    for usuario in usuarios:
        if cpf == usuario["cpf"]:
            return usuario
    return None


def cadastrar_usuario(cpf):
    usuario = filtrar_usuarios(cpf, usuarios)
    if usuario:
        print("Já existe um usuário com esse CPF!")
        return

    nome_completo = input("Nome completo: ")
    data_nascimento = input("Data de nascimento (dd-mm-aa): ")
    print("\n========== ENDEREÇO ==========")
    logradouro = input("Logradouro (rua, avenida, etc.): ")
    numero = input("Número: ")
    bairro = input("Bairro: ")
    cidade = input("Cidade: ")
    sigla_estado = input("Sigla do estado (ex.: SP): ")

    endereco_formatado = f"{logradouro}, {numero} - {bairro} - {cidade}/{sigla_estado}"

    novo_usuario = {
        "nome": nome_completo,
        "cpf": cpf,
        "data_nascimento": data_nascimento,
        "endereco": endereco_formatado
    }
    usuarios.append(novo_usuario)


def criar_conta(AGENCIA, numero_conta, usuario):
    cpf = input("Informe o CPF: ")
    cpf = cpf.replace(".", "").replace("-", "")
    usuario = filtrar_usuarios(cpf, usuarios)

    if usuario:
        nova_conta = {
            "agencia": AGENCIA,
            "numero_conta": numero_conta,
            "usuario": usuario
        }
        return nova_conta

    else:
        print("\nErro na criação de conta: Usuário não encontrado!")
        return None


def listar_contas(contas):
    if not contas:
        print("\n=> Não há contas cadastradas.")
        return
    print("\n========== LISTA DE CONTAS ==========")

    for i, conta in enumerate(contas):
        print(f"--- Conta {i + 1} ---")
        print(f"Agência: {conta['agencia']}")
        print(f"Número da conta: {conta['numero_conta']}")
        print(f"Titular: {conta['usuario']['nome']}")
        print(f"CPF: {conta['usuario']['cpf']}")
        print("\n =====================================")


def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print(f"Depósito de R$ {valor:.2f} concluído com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, LIMITE_SAQUES):
    if valor > saldo:
        print("Operação falhou! Saldo insuficiente.")
    elif valor > limite:
        print("Operação falhou! O valor desejado excede o limite de saque.")
    elif numero_saques >= LIMITE_SAQUES:
        print("Operação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print("Saque realizado com sucesso!")
    return saldo, numero_saques, extrato


def consultar_extrato(saldo, /, *, extrato):
    print("\n========== EXTRATO ==========")
    print("Não foram realizadas movimentações" if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("===============================")    
    return saldo, extrato


while True:
    opcao = input(menu)

    if opcao == "d":
        valor = float(input("Informe o valor do depósito: "))
        saldo, extrato = depositar(saldo, valor, extrato)

    elif opcao == "s":
        valor = float(input("Informe o valor do saque: "))
        saldo, numero_saques, extrato = sacar(
            saldo=saldo,
            valor=valor,
            extrato=extrato,
            limite=limite,
            numero_saques=numero_saques,
            LIMITE_SAQUES=LIMITE_SAQUES
            )

    elif opcao == "e":
        consultar_extrato(saldo, extrato=extrato)

    elif opcao == "nu":
        cpf = input("Informe seu CPF (apenas números): ")
        cpf = cpf.replace(".", "").replace("-", "")
        cadastrar_usuario(cpf)

    elif opcao == "cc":
        nova_conta = criar_conta(AGENCIA, numero_conta, usuarios)

        if nova_conta:
            contas.append(nova_conta)
            print("Conta corrente criada com sucesso!")
            numero_conta += 1

    elif opcao == "lc":
        listar_contas(contas)

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione a operação novamente.")
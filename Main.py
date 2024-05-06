from datetime import datetime
import textwrap

total_conta = 0
lista_de_depositos = []
lista_de_saques = []

def interface():
    print("""
          
        ###    Welcome To The Bank    ###
          
                Choose an Option:

                [0] - Depositar
                [1] - Sacar
                [2] - Extrato 
                [3] - Criar Usuário
                [4] - Criar Conta
                [5] - Listar Contas

                [6] - Exit          
         
          """) 
    
def fazer_deposito(valor):
    global total_conta
    total_conta += valor
    return total_conta

def fazer_saque(valor):
    global total_conta
    total_conta -= valor
    return total_conta  

def extrato():
    print("\n\n##############################################################################################")
    print("\n#### CONTA DIGITAL ####")
    print()
    print()
    print("R$",total_conta)
    print("\n## Ações Realizadas ##")
    print("\n# Saques #")
    for num in lista_de_saques:
        print("R$",num) 
    print("\n# Depositos #")
    for val in lista_de_depositos:
        print("R$",val)
    print("\n###############################################################################################")
    
def data():
    
    while True:
        data = input("Digite a data de nascimento no formato (DD/MM/AAAA): ")
        try:
            data = datetime.strptime(data, "%d/%m/%Y").date()
            print("Data inserida!")
            break  # Saia do loop se a conversão for bem-sucedida
        except ValueError:
            print()
            print("⚠️ Formato de data inválido. Certifique-se de inserir a data no formato correto (DD/MM/AAAA) ⚠️")
            print()
    return data

def verificar_cpf():
    while True:
        cpf = str(input("Digite seu CPF: ")) 
        if len(cpf) == 11:
                print("CPF inserido!")
                break
        else:
            print()
            print(" ⚠️ Formato de CPF inválido. Certifique-se de inserir o formato correto (7 NÚMEROS) ⚠️")
            print()
                    
    return cpf
         

def criar_usuario(usuarios): 
    cpf = verificar_cpf()   
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n###❗ Já existe usuário com esse CPF ❗ ###")
        return
    
    nome = input("\nDigite seu nome: ").upper()
    data_nascimento = data()
    endereco = input("Digite seu endereço (LOGRADOURO - BAIRRO - CIDADE/SIGLA ESTADO): ").upper()
    
    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("=== Usuário criado com sucesso! ===")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia,numero_conta,usuarios):
    cpf = verificar_cpf()
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    
    print("\n### ❗ Usuário não encontrado, fluxo de criação de conta encerrado ❗ ###")

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))

def main():    
    usuarios = []
    contas = []
    AGENCIA = "0001"

    limite_de_saque = 3       
    while limite_de_saque != 0:
        interface()
        opcao = int(input("\nEscolha uma opção: "))

        match opcao:
            case 0:
                print("### Fazer Deposito ###")
                deposito = float(input("\nValor a depositar: "))
                total_conta = fazer_deposito(deposito)
                lista_de_depositos.append(deposito)
            case 1:
                print("### Fazer Saque ###")
                saque = float(input("\nValor a sacar: "))
                if saque > 500:
                    print("\n🚨 LIMITE EXCEDIDO 🚨")
                    print("# MÁXIMO DE R$500,00 #")
                elif saque > total_conta:
                    print("\n🚨 SALDO INSUFICIENTE 🚨")
                    print(" SALDO ATUAL: ",total_conta)
                else:
                    total_conta = fazer_saque(saque)
                    lista_de_saques.append(saque)
                    limite_de_saque -= 1
            case 2:
                print("### Extrato ###")
                extrato()
            case 3:
                criar_usuario(usuarios)
            
            case 4:
                numero_conta = len(contas) + 1
                conta = criar_conta(AGENCIA, numero_conta, usuarios)

                if conta:
                    contas.append(conta)

            case 5:
                listar_contas(contas)
            case 6:
                print("Exit")
                extrato()
                break

        if limite_de_saque == 0:
            print("\n🚨 LIMITE DE SAQUES ATINGIDO 🚨")
            extrato()

main()

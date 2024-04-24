total_conta = 0
limite_de_saque = 3
lista_de_depositos = []
lista_de_saques = []

def interFace():
    print("""
          
        ###    Welcome To The Bank    ###
          
                Choose an Option:

                [0] - Depositar
                [1] - Sacar
                [2] - Extrato 
                [3] - Exit          
         
          """) 
    
def fazerDeposito(valor):
    global total_conta
    total_conta += valor
    return total_conta

def fazerSaque(valor):
    global total_conta
    total_conta -= valor
    return total_conta  

def extrato():
    print("\n\n##############################################################################################")
    print("\n#### CONTA DIGITAL ####")
    print("R$",total_conta)
    print("\n## Ações Realizadas ##")
    print("\n# Saques #")
    for num in lista_de_saques:
        print("R$",num) 
    print("\n# Depositos #")
    for val in lista_de_depositos:
        print("R$",val)
    print("\n###############################################################################################")
          
while limite_de_saque != 0:
    interFace()
    opcao = int(input("\nEscolha uma opção: "))

    match opcao:
        case 0:
            print("### Fazer Deposito ###")
            deposito = float(input("\nValor a depositar: "))
            total_conta = fazerDeposito(deposito)
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
                total_conta = fazerSaque(saque)
                lista_de_saques.append(saque)
                limite_de_saque -= 1
        case 2:
            print("### Extrato ###")
            extrato()
        case 3:
            print("Exit")
            extrato()
            break
    if limite_de_saque == 0:
        print("\n🚨 LIMITE DE SAQUES ATINGIDO 🚨")
        extrato() 
 
print("\n\n##")



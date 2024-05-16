from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime
import textwrap

class Conta:
    def __init__(self,numero,cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero,cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico
       
    def sacar(self, valor):
        saldo = self.saldo
        
        if valor > saldo:
            print("\n🚨 SALDO INSUFICIENTE 🚨")
        elif valor > 0 :
            self._saldo -= valor
            print("\n=== SAQUE REALIZADO COM SUCESSO! ===")
            return True
        else:
            print("🚨 FALHA NA OPERAÇÃO.VALOR INFORMADO INVÁLIDO 🚨")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== DEPÓSITO REALIZADO COM SUCESSO! ===")
        else:
            print("🚨 FALHA NA OPERAÇÃO.VALOR INFORMADO INVÁLIDO 🚨")
            return False

        return True


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        })


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero,cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou!O valor do saque excede o limite. @@@")

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Cliente:
    def __init__(self, endereço):
        self.endereço = endereço
        self.contas = []
  
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento,endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento


class Transação(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass
    
    @abstractmethod
    def registrar(self,conta):
        pass

class Deposito(Transação):
    def __init__(self,valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Saque(Transação):
    def __init__(self, valor):
        self._valor = valor 

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self) 

def interface():
    print("""
          
        ###    Welcome To The Bank    ###
          
                [0] - Depositar
                [1] - Sacar
                [2] - Extrato          
                [3] - Criar Usuário
                [4] - Criar Conta
                [5] - Listar Contas
          
                [6] - Exit          
         
          """) 

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

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

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n🚨 Cliente não possui conta! 🚨")
        return

    return cliente.contas[0]

def depositar(clientes):
    cpf = verificar_cpf()
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n🚨 Cliente não encontrado! 🚨")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = verificar_cpf()
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n🚨 Cliente não encontrado! 🚨")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = verificar_cpf()
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n🚨 Cliente não encontrado! 🚨")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))


def criar_conta(numero_conta, clientes, contas):
    cpf = verificar_cpf()
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n🚨 Cliente não encontrado, fluxo de criação de conta encerrado! 🚨")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n=== Conta criada com sucesso! ===")

def criar_cliente(clientes):
    cpf = verificar_cpf()
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n🚨 Já existe cliente com esse CPF! 🚨")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")

def main():    
    clientes = []
    contas = []

    while True:
        interface()
        opcao = int(input("\nEscolha uma opção: "))

        match opcao:
            case 0:
                depositar(clientes)

            case 1:
                sacar(clientes)

            case 2:
                 exibir_extrato(clientes)

            case 3:
                criar_cliente(clientes)

            case 4:
                numero_conta = len(contas) + 1
                criar_conta(numero_conta, clientes, contas)

            case 5:
                listar_contas(contas)
            case 6:
                print("\n\t================EXIT================")
                break


main()
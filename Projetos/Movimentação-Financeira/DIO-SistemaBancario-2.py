import textwrap
from datetime import datetime

class Conta:
    def __init__(self, agencia, numero_conta, usuario):
        self.agencia = agencia
        self.numero_conta = numero_conta
        self.usuario = usuario
        self.criado_em = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.saldo = 0
        self.limite = 500
        self.extrato = []
        self.numero_saques = 0
        self.limite_saques = 3

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.extrato.append((datetime.now().strftime('%Y-%m-%d %H:%M:%S'), f"Depósito:\tR$ {valor:.2f}"))
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    def sacar(self, valor):
        excedeu_saldo = valor > self.saldo
        excedeu_limite = valor > self.limite
        excedeu_saques = self.numero_saques >= self.limite_saques

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
        elif excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
        elif valor > 0:
            self.saldo -= valor
            self.extrato.append((datetime.now().strftime('%Y-%m-%d %H:%M:%S'), f"Saque:\t\tR$ {valor:.2f}"))
            self.numero_saques += 1
            print("\n=== Saque realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    def exibir_extrato(self):
        print("\n================ EXTRATO ================")
        print(f"Agência:\t{self.agencia}")
        print(f"C/C:\t\t{self.numero_conta}")
        print(f"Titular:\t{self.usuario['nome']}")
        print(f"CPF:\t\t{self.usuario['cpf']}")
        print("Não foram realizadas movimentações." if not self.extrato else "\n".join(f"{data} {mov}" for data, mov in self.extrato))
        print(f"\nSaldo:\t\tR$ {self.saldo:.2f}")
        print("==========================================")


class Banco:
    def __init__(self, agencia):
        self.agencia = agencia
        self.usuarios = []
        self.contas = []

    def menu(self):
        menu = """\n
        ================ MENU ================
        [d]\tDepositar
        [s]\tSacar
        [e]\tExtrato
        [nc]\tNova conta
        [lc]\tListar contas
        [nu]\tNovo usuário
        [q]\tSair
        => """
        return input(textwrap.dedent(menu))

    def criar_usuario(self):
        cpf = input("Informe o CPF (somente número): ")
        usuario = self.filtrar_usuario(cpf)

        if usuario:
            print("\n@@@ Já existe usuário com esse CPF! @@@")
            return

        nome = input("Informe o nome completo: ")
        data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
        endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

        self.usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco, "criado_em": datetime.now().strftime('%Y-%m-%d %H:%M:%S')})

        print("=== Usuário criado com sucesso! ===")

    def filtrar_usuario(self, cpf):
        usuarios_filtrados = [usuario for usuario in self.usuarios if usuario["cpf"] == cpf]
        return usuarios_filtrados[0] if usuarios_filtrados else None

    def criar_conta(self):
        cpf = input("Informe o CPF do usuário: ")
        usuario = self.filtrar_usuario(cpf)

        if usuario:
            if any(conta for conta in self.contas if conta.usuario["cpf"] == cpf):
                print("\n@@@ Já existe uma conta associada a este CPF. @@@")
                return

            numero_conta = len(self.contas) + 1
            conta = Conta(self.agencia, numero_conta, usuario)
            self.contas.append(conta)
            print("\n=== Conta criada com sucesso! ===")
        else:
            print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")
            print("Criando novo usuário...")
            self.criar_usuario()

    def listar_contas(self):
        for conta in self.contas:
            linha = f"""\
                Agência:\t{conta.agencia}
                C/C:\t\t{conta.numero_conta}
                Titular:\t{conta.usuario['nome']}
                Criado em:\t{conta.criado_em}
            """
            print("=" * 100)
            print(textwrap.dedent(linha))

    def selecionar_conta(self):
        cpf = input("Informe o CPF do titular da conta: ")
        contas_filtradas = [conta for conta in self.contas if conta.usuario["cpf"] == cpf]
        return contas_filtradas[0] if contas_filtradas else None

    def main(self):
        while True:
            opcao = self.menu()

            if opcao in ["d", "s", "e"]:
                conta = self.selecionar_conta()
                if not conta:
                    print("\n@@@ Não há conta associada a este CPF. Por favor, crie um usuário e uma conta. @@@")
                    continue

                if opcao == "d":
                    valor = float(input("Informe o valor do depósito: "))
                    conta.depositar(valor)
                elif opcao == "s":
                    valor = float(input("Informe o valor do saque: "))
                    conta.sacar(valor)
                elif opcao == "e":
                    conta.exibir_extrato()
            elif opcao == "nu":
                self.criar_usuario()
            elif opcao == "nc":
                self.criar_conta()
            elif opcao == "lc":
                self.listar_contas()
            elif opcao == "q":
                break
            else:
                print("Operação inválida, por favor selecione novamente a operação desejada.")

banco = Banco("0001")
banco.main()

import os
import pandas as pd

ARQUIVO_DADOS = 'dados.csv'

# Função para limpar a tela do terminal
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

# Função para carregar dados do arquivo CSV
def carregar_dados():
    if not os.path.exists(ARQUIVO_DADOS):
        # Cria arquivo vazio com colunas padrão se não existir
        df = pd.DataFrame(columns=["id", "nome", "telefone", "segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"])
        df.to_csv(ARQUIVO_DADOS, index=False)
    else:
        df = pd.read_csv(ARQUIVO_DADOS)
    return df

# Função para salvar dados no arquivo CSV
def salvar_dados(df):
    df.to_csv(ARQUIVO_DADOS, index=False)

# Função para exibir a tela de login
def tela_login():
    limpar_tela()
    print("=== SISTEMA DE ACADEMIA ===")
    input("Pressione Enter para continuar...")
    menu_principal()

# Menu principal
def menu_principal():
    limpar_tela()
    print("=== MENU PRINCIPAL ===")
    print("1. Aluna")
    print("2. Professor")
    escolha = input("Escolha uma opção: ")

    if escolha == "1":
        tela_aluna()
    elif escolha == "2":
        senha = input("Digite a senha do professor: ")
        if senha == "academia123":
            tela_professor()
        else:
            print("Senha incorreta.")
            input("Pressione Enter para voltar...")
            menu_principal()
    else:
        print("Opção inválida.")
        input("Pressione Enter para tentar novamente...")
        menu_principal()

# Tela para buscar aluna
def tela_aluna():
    global alunas
    limpar_tela()
    termo = input("Digite o nome da aluna para buscar (pode ser parcial): ").strip().lower()

    resultado = alunas[alunas['nome'].str.lower().str.contains(termo)]

    if resultado.empty:
        print("Nenhuma aluna encontrada.")
    else:
        print(f"\n{len(resultado)} aluna(s) encontrada(s):\n")
        for idx, row in resultado.iterrows():
            print(f"ID: {row['id']}")
            print(f"Nome: {row['nome']}")
            print(f"Telefone: {row['telefone']}")
            print(f"Segunda: {row['segunda']}")
            print(f"Terça: {row['terça']}")
            print(f"Quarta: {row['quarta']}")
            print(f"Quinta: {row['quinta']}")
            print(f"Sexta: {row['sexta']}")
            print(f"Sábado: {row['sábado']}")
            print(f"Domingo: {row['domingo']}")
            print("--------------------")

    input("Pressione Enter para voltar ao menu...")
    menu_principal()

# Tela para professor adicionar nova aluna
def tela_professor():
    global alunas
    limpar_tela()
    print("=== TELA DO PROFESSOR ===")
    print("1. Adicionar nova aluna")
    print("2. Voltar ao menu")
    escolha = input("Escolha uma opção: ")

    if escolha == "1":
        nome = input("Nome da aluna: ")
        telefone = input("Telefone: ")
        segunda = input("Exercício de Segunda: ")
        terca = input("Exercício de Terça: ")
        quarta = input("Exercício de Quarta: ")
        quinta = input("Exercício de Quinta: ")
        sexta = input("Exercício de Sexta: ")
        sabado = input("Exercício de Sábado: ")
        domingo = input("Exercício de Domingo: ")

        novo_id = alunas["id"].max() + 1 if not alunas.empty else 1
        nova_aluna = {
            "id": novo_id,
            "nome": nome,
            "telefone": telefone,
            "segunda": segunda,
            "terça": terca,
            "quarta": quarta,
            "quinta": quinta,
            "sexta": sexta,
            "sábado": sabado,
            "domingo": domingo
        }
        alunas = alunas.append(nova_aluna, ignore_index=True)
        salvar_dados(alunas)
        print("Aluna adicionada com sucesso!")
        input("Pressione Enter para voltar...")
        tela_professor()

    elif escolha == "2":
        menu_principal()
    else:
        print("Opção inválida.")
        input("Pressione Enter para tentar novamente...")
        tela_professor()

# Carrega os dados antes de iniciar o programa
alunas = carregar_dados()

# Inicia o programa
if __name__ == '__main__':
    tela_login()

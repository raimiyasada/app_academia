import pandas as pd
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock

ARQUIVO_DADOS = 'dados.csv'

# Funções para carregar e salvar dados
def carregar_dados():
    try:
        df = pd.read_csv(ARQUIVO_DADOS)
        if "id" not in df.columns:
            df.insert(0, "id", range(1, len(df) + 1))
            salvar_dados(df)
        return df
    except FileNotFoundError:
        df = pd.DataFrame(columns=["id","nome","telefone","segunda","terça","quarta","quinta","sexta","sábado","domingo"])
        salvar_dados(df)
        return df

def salvar_dados(df):
    df = df.sort_values("id").reset_index(drop=True)
    df.to_csv(ARQUIVO_DADOS, index=False)

# Tela inicial (Login)
class TelaLogin(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        layout.add_widget(Label(text="=== SISTEMA DE ACADEMIA ===", font_size=24))
        self.btn_entrar = Button(text="Entrar")
        self.btn_entrar.bind(on_press=self.entrar)
        layout.add_widget(self.btn_entrar)
        self.add_widget(layout)

    def entrar(self, instance):
        self.manager.current = "menu"

# Menu principal (Aluna ou Professor)
class MenuPrincipal(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        layout.add_widget(Label(text="=== MENU PRINCIPAL ===", font_size=24))

        btn_aluna = Button(text="Aluna")
        btn_aluna.bind(on_press=self.ir_aluna)
        layout.add_widget(btn_aluna)

        btn_professor = Button(text="Professor")
        btn_professor.bind(on_press=self.ir_professor_login)
        layout.add_widget(btn_professor)

        self.add_widget(layout)

    def ir_aluna(self, instance):
        self.manager.get_screen('tela_aluna').limpar()
        self.manager.current = "tela_aluna"

    def ir_professor_login(self, instance):
        self.manager.current = "login_professor"

# Tela para login do professor
class LoginProfessor(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        layout.add_widget(Label(text="Senha do professor:", font_size=20))
        self.senha_input = TextInput(password=True, multiline=False)
        layout.add_widget(self.senha_input)

        self.lbl_msg = Label(text="", color=(1,0,0,1))
        layout.add_widget(self.lbl_msg)

        btn_entrar = Button(text="Entrar")
        btn_entrar.bind(on_press=self.tentar_entrar)
        layout.add_widget(btn_entrar)

        btn_voltar = Button(text="Voltar")
        btn_voltar.bind(on_press=self.voltar)
        layout.add_widget(btn_voltar)

        self.add_widget(layout)

    def tentar_entrar(self, instance):
        if self.senha_input.text == "academia123":
            self.senha_input.text = ""
            self.lbl_msg.text = ""
            self.manager.get_screen("tela_professor").limpar()
            self.manager.current = "tela_professor"
        else:
            self.lbl_msg.text = "Senha incorreta!"

    def voltar(self, instance):
        self.senha_input.text = ""
        self.lbl_msg.text = ""
        self.manager.current = "menu"

# Tela da aluna (busca flexível)
class TelaAluna(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout_principal = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        self.label = Label(text="Digite o nome da aluna para buscar (pode ser parcial):", size_hint=(1, 0.1))
        self.layout_principal.add_widget(self.label)
        
        self.input_busca = TextInput(size_hint=(1, 0.1), multiline=False)
        self.layout_principal.add_widget(self.input_busca)

        btn_buscar = Button(text="Buscar", size_hint=(1, 0.1))
        btn_buscar.bind(on_press=self.buscar)
        self.layout_principal.add_widget(btn_buscar)

        self.resultado_scroll = ScrollView(size_hint=(1, 0.6))
        self.layout_principal.add_widget(self.resultado_scroll)

        btn_voltar = Button(text="Voltar", size_hint=(1, 0.1))
        btn_voltar.bind(on_press=self.voltar)
        self.layout_principal.add_widget(btn_voltar)

        self.add_widget(self.layout_principal)

    def limpar(self):
        self.input_busca.text = ""
        self.resultado_scroll.clear_widgets()
        self.label.text = "Digite o nome da aluna para buscar (pode ser parcial):"

    def buscar(self, instance):
        termo = self.input_busca.text.strip().lower()
        df = carregar_dados()
        resultado = df[df['nome'].str.lower().str.contains(termo)]

        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        if resultado.empty:
            layout.add_widget(Label(text="Nenhuma aluna encontrada.", size_hint_y=None, height=40))
        else:
            for _, row in resultado.iterrows():
                texto = f"ID: {row['id']}\nNome: {row['nome']}\nTelefone: {row['telefone']}\n" \
                        f"Segunda: {row['segunda']}\nTerça: {row['terça']}\nQuarta: {row['quarta']}\n" \
                        f"Quinta: {row['quinta']}\nSexta: {row['sexta']}\nSábado: {row['sábado']}\nDomingo: {row['domingo']}\n" \
                        "-------------------------"
                layout.add_widget(Label(text=texto, size_hint_y=None, height=160))

        self.resultado_scroll.clear_widgets()
        self.resultado_scroll.add_widget(layout)

    def voltar(self, instance):
        self.manager.current = "menu"

# Tela do professor para adicionar nova aluna
class TelaProfessor(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout_principal = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.layout_principal.add_widget(Label(text="=== TELA DO PROFESSOR ===", font_size=24))

        self.inputs = {}
        campos = ["nome", "telefone", "segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]
        for campo in campos:
            box = BoxLayout(size_hint=(1, 0.1))
            box.add_widget(Label(text=campo.capitalize()+":", size_hint=(0.3,1)))
            ti = TextInput(multiline=False)
            box.add_widget(ti)
            self.inputs[campo] = ti
            self.layout_principal.add_widget(box)

        btn_adicionar = Button(text="Adicionar nova aluna", size_hint=(1, 0.1))
        btn_adicionar.bind(on_press=self.adicionar_aluna)
        self.layout_principal.add_widget(btn_adicionar)

        btn_voltar = Button(text="Voltar ao menu", size_hint=(1, 0.1))
        btn_voltar.bind(on_press=self.voltar)
        self.layout_principal.add_widget(btn_voltar)

        self.lbl_msg = Label(text="", size_hint=(1, 0.1), color=(1,0,0,1))
        self.layout_principal.add_widget(self.lbl_msg)

        self.add_widget(self.layout_principal)

    def limpar(self):
        for campo in self.inputs:
            self.inputs[campo].text = ""
        self.lbl_msg.text = ""

    def adicionar_aluna(self, instance):
        df = carregar_dados()
        try:
            novo_id = df["id"].max() + 1 if not df.empty else 1
        except:
            novo_id = 1

        nova_aluna = {
            "id": novo_id,
            "nome": self.inputs["nome"].text.strip(),
            "telefone": self.inputs["telefone"].text.strip(),
            "segunda": self.inputs["segunda"].text.strip(),
            "terça": self.inputs["terça"].text.strip(),
            "quarta": self.inputs["quarta"].text.strip(),
            "quinta": self.inputs["quinta"].text.strip(),
            "sexta": self.inputs["sexta"].text.strip(),
            "sábado": self.inputs["sábado"].text.strip(),
            "domingo": self.inputs["domingo"].text.strip(),
        }

        # Verifica se nome está vazio
        if not nova_aluna["nome"]:
            self.lbl_msg.text = "Nome não pode ficar vazio!"
            return

        df = pd.concat([df, pd.DataFrame([nova_aluna])], ignore_index=True)
        salvar_dados(df)

        self.lbl_msg.color = (0, 1, 0, 1)
        self.lbl_msg.text = "Aluna adicionada com sucesso!"
        self.limpar()

    def voltar(self, instance):
        self.manager.current = "menu"

# App principal
class MeuAppVisual(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(TelaLogin(name="login"))
        sm.add_widget(MenuPrincipal(name="menu"))
        sm.add_widget(TelaAluna(name="tela_aluna"))
        sm.add_widget(LoginProfessor(name="login_professor"))
        sm.add_widget(TelaProfessor(name="tela_professor"))
        return sm

if __name__ == "__main__":
    MeuAppVisual().run()

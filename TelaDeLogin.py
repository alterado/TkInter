"""
Conceito de Frame: Frames são subdivisões da tela original do programa. Quando uma instância de Tk() é criada, cria-se uma aplicação com uma tela. A criação de frames é a criação de subdivisões da tela original, que permite uma organização dos Widgets de maneira mais customizada no programa.
O frame pode ser definido simplesmente como uma instância da classe Frame(). Por exemplo:
frame1 = Frame(mestre,*)

Observação importante: Os frames passam a assumir a posição de "mestre" nos argumentos que são dados aos Widgets.
Eles também precisam ser empacotados através do método .pack() para serem exibidos no programa.

Exercício: Criar uma tela de login com divisão de "usuário", "senha" e "entrar/criar" em Frames
obs: otimizei bastante o exercício e desenvolvi uma "base de dados" em formato de arquivo txt
"""
from tkinter import *
m = Tk()
class Login(object):
    def __init__(self, master):
        self.master = master
        m.title("Tela de Login V.2.0")
        m.geometry("300x250")
        # Definição dos Frames:
        #Frame Login
        self.frame1 = Frame(self.master, pady = 5)
        self.frame1.pack()

        #Frame Senha
        self.frame2 = Frame(self.master, pady = 5)
        self.frame2.pack()

        #Frame entrar/criar
        self.frame3 = Frame(self.master, pady = 10)
        self.frame3.pack()


        # Definição dos Widgets
        # Texto de Login
        self.lb1 = Label(self.frame1, text = "Usuário")
        self.lb1.pack()
        # Entrada de texto de Login
        self.ent1 = Entry(self.frame1)
        self.ent1.pack()

        #Texto de Senha
        self.lb2 = Label(self.frame2, text = "Senha")
        self.lb2.pack()
        #Entrada de texto de Senha
        self.ent2 = Entry(self.frame2, show = "*")
        self.ent2.pack()

        #Botão entrar/criar
        self.bt1 = Button(self.frame3, text = "Novo", width = 7, command = self.criaUsuario)
        self.bt1.pack(side=RIGHT)
        self.bt2 = Button(self.frame3, text = "Entrar", width = 7, command = self.entraUsuario)
        self.bt2.pack(side = RIGHT)

    def criaUsuario(self):
        """
        Essa função dá início ao processo de criação de um novo usuário
        """
        #Altera botão de 'Novo'
        self.bt1["text"] = "Criar"
        self.bt1["bg"] = "black"
        self.bt1["fg"] = "white"
        self.bt1["command"] = self.cadastrar

        # Tira o botão "entrar" durante o cadastro
        self.bt2.pack_forget()

        # Altera widget de Login para 'Novo usuário'
        self.lb1["text"] = "Novo usuário"
        self.lb1["fg"] = "green"

        # Altera widget de Senha para 'Nova senha'
        self.lb2["text"] = "Senha"
        self.lb2["fg"] = "green"

        #Texto "confirmar senha"
        self.lb3 = Label(self.frame2, text = "Confirme a senha", fg = "green")
        self.lb3.pack()
        # Entrada de texto confirmação de senha
        self.ent3 = Entry(self.frame2, show = "*")
        self.ent3.pack()
        # Label de status da criação do usuário
        self.lb4 = Label(self.frame2, text = "", wraplength = 170, justify = CENTER)
        self.lb4.pack()


    def cadastrar(self):
        """
        Essa é a função principal de cadastro de novo usuário. Valida o novo usuário e o insere na base de usuários
        """
        #Valida se novo usuário é um usuário válido e adiciona na base:
        if self.validaNovoUsuario(self.ent1.get(), self.ent2.get(), self.ent3.get()) == True:
            user = {}
            with open("BaseDeUsuarios.txt", "a", encoding="utf-8") as arq:
                user[self.ent1.get()] = self.ent2.get()
                arq.write(self.ent1.get() + "," + user[self.ent1.get()]+"\n")
                arq.close()
            # Informa que o usuário foi criado
            self.lb4["text"] = "Usuário cadastrado com sucesso"
            self.lb4["fg"] = "green"
            # Desfaz as alterações da tela de criar
            self.lb1["text"] = "Usuário"
            self.lb1["fg"] = "black"
            self.lb2["text"] = "Senha"
            self.lb2["fg"] = "black"

            self.ent3.pack_forget()
            self.bt2.pack()
            self.bt1.pack_forget()
            self.lb3.pack_forget()
            self.bt2["command"] = self.entraUsuario


    def validaNovoUsuario(self, login, senha, confsenha):
        """
        Essa função valida o novo usuário/senha inputados
        """
        #Verifica login
        if login.isnumeric() == True:
            self.lb4["fg"] = "red"
            self.lb4["text"] = "Utilize apenas caracteres válidos (numeros e letras) com pelo menos 4 caracteres"
        elif login.isalnum() == False:
            self.lb4["fg"] = "red"
            self.lb4["text"] = "Utilize apenas caracteres válidos (numeros e letras) com pelo menos 4 caracteres"
        elif login in self.listaDeUsuarios():
            self.lb4["fg"] = "red"
            self.lb4["text"] = "Usuário já cadastrado"
        elif login.strip() == "" or senha.strip() == "":
            self.lb4["fg"] = "red"
            self.lb4["text"] = "Campos não podem estar vazios"
        elif len(senha) < 4:
            self.lb4["fg"] = 'red'
            self.lb4["text"] = "Sua senha ter 4 ou mais caracteres"
        elif senha != confsenha:
            self.lb4["fg"] = "red"
            self.lb4["text"] = "Campo 'Senha' e 'Confirmação de Senha' devem ser idênticos"
        else:
            return True


    def listaDeUsuarios(self):
        """
        Essa função le um arquivo txt e retorna um dicionário com os usuários existentes no padrão {"usuário":"senha"}
        Se o arquivo txt não existir, retorna um dicionário vazio.
        """
        try:
            arq = open("BaseDeUsuarios.txt", "r", encoding = "UTF-8")
        except FileNotFoundError:
            return {}
        else:
            usuarios = {}
            for linha in arq:
                usuarios[linha.split(",")[0]] = linha.split(",")[1][:(len(linha.split(",")[1])-1)]
            arq.close()
            return usuarios

    def entraUsuario(self):
        """
        Essa função inicia a sessão do usuário, checando se consta na base de dados e, caso positivo, informando ao usuário que o login foi realizado com sucesso
        """
        base = self.listaDeUsuarios()
        user, senha = self.ent1.get(), self.ent2.get()
        if user in base:
            if senha == base[user]:
                self.lb4["fg"] = "black"
                self.lb4["text"] = "Entrando..."
                self.bt2.pack_forget()

            else:
                self.lb4["fg"] = "red"
                self.lb4["text"] = "Senha inválida"

        else:
            self.lb4["fg"] = "red"
            self.lb4["text"] = "Usuário Inválido."
            self.bt1.pack(side = RIGHT)

Login(m)
m.mainloop()
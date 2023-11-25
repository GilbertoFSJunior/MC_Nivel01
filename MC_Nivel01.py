from tkinter import *
from tkinter import ttk
import sqlite3

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image
import webbrowser




root = Tk()

class Relatorios():
    def printSistema(self):
        webbrowser.open("Sistemas.pdf")
    def geraRelatSis(self):
        self.c = canvas.Canvas("Sistemas.pdf")

        self.codigoRel = self.codigo_entry.get()
        self.nome_sistemaRel = self.nome_sistema_entry.get()
        self.versaoRel = self.versao_entry.get()
        self.perfilRel = self.perfil_entry.get()
        self.descricaoRel = self.descricao_entry.get()

        self.c.setFont("Helvetica-Bold", 24)
        self.c.drawString(200, 790, 'Relátorio de Sistemas')

        self.c.setFont("Helvetica-Bold", 18)
        self.c.drawString(50, 700, 'Código: ' )
        self.c.drawString(50, 670, 'Sistema: ' )
        self.c.drawString(50, 640, 'Versão: ' )
        self.c.drawString(50, 610, 'Perfil: ' )
        self.c.drawString(50, 580, 'Descrição: ' )

        self.c.setFont("Helvetica", 18)
        self.c.drawString(150, 700, self.codigoRel)
        self.c.drawString(150, 670, self.nome_sistemaRel)
        self.c.drawString(150, 640, self.versaoRel)
        self.c.drawString(150, 610, self.perfilRel)
        self.c.drawString(150, 580, self.descricaoRel)

        self.c.rect(20,550,550,5, fill=True, stroke=False)

        self.c.showPage()
        self.c.save()
        self.printSistema()




        ###############################################################################################

    
class funcoes():

    #função para limpar a tela
    def limpa_tela(self):
        self.codigo_entry.delete(0, END)
        self.nome_sistema_entry.delete(0, END)
        self.versao_entry.delete(0, END)


    #Função para conectar ao Banco de dados
    def conecta_bd(self):
        self.conn = sqlite3.connect("CadastroGer.bd")
        self.cursor = self.conn.cursor()


    #função para desconectar  banco de dados
    def desconecta_bd(self):
        self.conn.close()


    #Função de montagem da tabela do banco de dados
    def montaTabela(self):
        self.conecta_bd(); print("Conectando ao Banco de Dados")
        #criação da tabela
        self.cursor.execute(""" CREATE TABLE IF NOT EXISTS Cadastros (
                            Codigo INTEGER PRIMARY KEY, sistema CHAR(40) NOT NULL, versao INTEGER(20), 
                            perfil CHAR(60), descricao CHAR(60), cpf INTEGER(40)
                     );
        """)
        self.conn.commit(); print("Banco de dados criado")
        self.desconecta_bd(); print("Banco de dados desconectado")


    #função das variáveis utilizadas
    def variaveis(self):
        self.codigo = self.codigo_entry.get()
        self.nome_sistema = self.nome_sistema_entry.get()
        self.versao = self.versao_entry.get()
        self.perfil = self.perfil_entry.get()
        self.descricao = self.descricao_entry.get()
        self.cpf= self.cpf_entry.get()



    #função de adicionar sitemas
    def add_sistema(self):
        try:
            self.variaveis()
            self.conecta_bd()
 
            self.cursor.execute(""" INSERT INTO Cadastros (sistema, versao, perfil, descricao, cpf)
                            VALUES (?, ?, ?, ?, ?)""", (self.nome_sistema, self.versao, '', '', ''))
            self.conn.commit()
        except Exception as e:
            print(f"Erro ao adicionar Sistema: {e}")
        finally:
            self.desconecta_bd()
            self.select_lista()
            self.limpa_tela()

        self.conecta_bd()
        self.cursor.execute("""INSERT INTO Cadastros (Perfil, Descricao, cpf)
                            VALUES (?, ?, ?)""", (self.perfil, self.descricao, self.cpf))
        self.conn.commit()
        self.desconecta_bd()

        self.select_lista()
        self.limpa_tela()


    #Função de seleção da lista
    def select_lista(self):
        self.listaPrincipal.delete(*self.listaPrincipal.get_children())
        self.conecta_bd()
        lista = self.cursor.execute(""" SELECT codigo, sistema, versao, perfil, descricao, cpf FROM Cadastros
                                     ORDER BY sistema ASC; """)
        for i in lista:
            self.listaPrincipal.insert("", END, values=i)
        self.desconecta_bd()



    #função do duplo click na tabela
    def OndoubleClick(self, event):
        self.limpa_tela()
        for i in self.listaPrincipal.selection():
            values = self.listaPrincipal.item(i, 'values')
            if values:
                col1, col2, col3, col4, col5, col6 = values[:6]
                self.codigo_entry.insert(END, col1)
                self.nome_sistema_entry.insert(END, col2)
                self.versao_entry.insert(END, col3)

                self.perfil_entry.insert(END, col4)
                self.codigo_entryframe_2.insert(END, col1)
                self.descricao_entry.insert(END, col5)
                self.cpf_entry.insert(END, col6)


    #Função para deletar sistema do banco de dados
    def deleta_sistema(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""DELETE FROM Cadastros WHERE codigo = ?""", (self.codigo,))
        self.conn.commit()
        self.desconecta_bd()
        self.limpa_tela()
        self.select_lista()


    #função para alterar sistema cadastrado
    def altera_sistema(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(""" UPDATE Cadastros SET sistema = ?, versao = ? WHERE codigo = ?""",
                            (self.nome_sistema, self.versao, self.codigo,))
        self.conn.commit()
        self.desconecta_bd()
        self.limpa_tela()

    

    #função de adicionar sistemas
    def add_perfil(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(""" INSERT INTO Cadastros (sistema, perfil, descricao, cpf)
                            VALUES (?, ?, ?, ?)""", (self.nome_sistema, self.perfil, self.descricao, self.cpf))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()



       
    
#######################################################################################################

        



class Application(funcoes, Relatorios):
    #Criação e configuração de janela#######################
    def __init__(self):
        self.root = root
        self.tela()
        self.frames_da_tela()
        self.criando_widgets_frame_1()
        self.lista_frame_4()
        self.montaTabela()
        self.select_lista()
        self.Menus()
        self.add_perfil()
        
        root.mainloop()

    def tela(self):
        self.root.title("Sistema de Cadastros")
        self.root.configure(background= '#1e3743')
        self.root.geometry("1366x768")
        self.root.resizable(True, True)
        self.root.maxsize(width = 1366, height= 768)
        self.root.minsize(width= 800, height= 600)
    

    
    #criação dos frames (espaços) da tela###################

    def frames_da_tela(self):
        self.frame_1 = Frame(self.root, bd = 4, bg= '#dfe3ee', highlightbackground='#759fe6',
                             highlightthickness=4 )
        self.frame_1.place(relx= 0.02 , rely= 0.02, relwidth= 0.47, relheight= 0.46 )

        self.frame_2 = Frame(self.root, bd = 4, bg= '#dfe3ee', highlightbackground='#759fe6',
                             highlightthickness=4 )
        self.frame_2.place(relx= 0.51 , rely= 0.02, relwidth= 0.47, relheight= 0.46 )

        self.frame_3 = Frame(self.root, bd = 4, bg= '#dfe3ee', highlightbackground='#759fe6',
                             highlightthickness=4 )
        self.frame_3.place(relx= 0.02 , rely= 0.5, relwidth= 0.47, relheight= 0.46 )

        self.frame_4 = Frame(self.root, bd = 4, bg= '#dfe3ee', highlightbackground='#759fe6',
                             highlightthickness=4 )
        self.frame_4.place(relx= 0.51 , rely= 0.5, relwidth= 0.47, relheight= 0.46 )

    

    #criação dos botões ####################################(FRAME 1)

    def criando_widgets_frame_1(self):
        #botão Limpar frame 1
        self.bt_limpar = Button(self.frame_3, text= "Limpa", bd=3, bg='#107db2', fg='white',
                                font = ('verdana', 8, 'bold'), command= self.limpa_tela)
        self.bt_limpar.place(relx=0.8, rely=0.1, relwidth=0.2, relheight=0.15)

        #botão Buscar frame 1
        self.bt_buscar = Button(self.frame_3, text= "Busca", bd=3, bg='#107db2', fg='white',
                                font = ('verdana', 8, 'bold'))
        self.bt_buscar.place(relx=0.8, rely=0.25, relwidth=0.2, relheight=0.15)

         #botão Novo frame 1
        self.bt_novo = Button(self.frame_3, text= "Novo", bd=3, bg='#107db2', fg='white',
                                font = ('verdana', 8, 'bold'), command= self.add_sistema)
        self.bt_novo.place(relx=0.8, rely=0.4, relwidth=0.2, relheight=0.15)

         #botão Alterar frame 1
        self.bt_alterar = Button(self.frame_3, text= "Alterar", bd=3, bg='#107db2', fg='white',
                                font = ('verdana', 8, 'bold'), command = self.altera_sistema)
        self.bt_alterar.place(relx=0.8, rely=0.55, relwidth=0.2, relheight=0.15)

         #botão Apagar frame 1
        self.bt_apagar = Button(self.frame_3, text= "Apagar", bd=3, bg='#107db2', fg='white',
                                font = ('verdana', 8, 'bold'), command= self.deleta_sistema)
        self.bt_apagar.place(relx=0.8, rely=0.7, relwidth=0.2, relheight=0.15)

        self.lb_cpf = Label(self.frame_3, text="CPF", bg='#dfe3ee')
        self.lb_cpf.place(relx=0.05, rely=0.8)
        self.cpf_entry = Entry(self.frame_1)
        self.cpf_entry.place(relx=0.05, rely=0.90, relwidth=0.13)
        
       

    #Criação das labels e entradas de dados (FRAME 1)

    #código (label)
        self.lb_codigo = Label(self.frame_1, text = "Código", bg= '#dfe3ee')
        self.lb_codigo.place(relx=0.05 , rely=0.05)
    #código (input)
        self.codigo_entry = Entry(self.frame_1, bg='#dfe3ee')
        self.codigo_entry.place(relx=0.05, rely=0.15, relwidth=0.14)

    #Nome do sistema (label)
        self.lb_nome_sistema = Label(self.frame_1, text = "Sistema", bg= '#dfe3ee')
        self.lb_nome_sistema.place(relx=0.05 , rely=0.3)
    #Nome do sistema (input)
        self.nome_sistema_entry = Entry(self.frame_1)
        self.nome_sistema_entry.place(relx=0.05, rely=0.40, relwidth=0.6)

    #Versão do sistema (label)
        self.lb_versao = Label(self.frame_1, text = "Versão", bg= '#dfe3ee')
        self.lb_versao.place(relx=0.05 , rely=0.6)
    #Versão do sistema (input)
        self.versao_entry = Entry(self.frame_1)
        self.versao_entry.place(relx=0.05, rely=0.70, relwidth=0.13) 

    #Cadastro de sistemas (label)
        self.lb_Cadastro_de_Sistemas = Label(self.frame_1, text = "Cadastro de Sistemas",
                                              bg= '#dfe3ee', font = ('verdana', 10, 'bold'))
        self.lb_Cadastro_de_Sistemas.place(relx=0.40 , rely=0.9)

    #Criação das labels e entradas de dados (FRAME 1)



    #Criação das labels e entradas de dados (FRAME 2)


    #codigo do sistema (label)
        self.lb_codigo = Label(self.frame_2, text = "Sistema", bg= '#dfe3ee')
        self.lb_codigo.place(relx=0.05 , rely=0.05)
    #Nome do sistema (input)
        self.codigo_entry = Entry(self.frame_2)
        self.codigo_entry.place(relx=0.05, rely=0.15, relwidth=0.40)

    #Perfil sistema (label)
        self.lb_perfil = Label(self.frame_2, text = "Perfil", bg= '#dfe3ee')
        self.lb_perfil.place(relx=0.05 , rely=0.25)
    #Nome do sistema (input)
        self.perfil_entry = Entry(self.frame_2)
        self.perfil_entry.place(relx=0.05, rely=0.35, relwidth=0.40)    

     #descrição do perfil (label)
        self.lb_descricao = Label(self.frame_2, text = "Descrição", bg= '#dfe3ee')
        self.lb_descricao.place(relx=0.05 , rely=0.45)
    #descrição do perfil (input)
        self.descricao_entry = Entry(self.frame_2)
        self.descricao_entry.place(relx=0.05, rely=0.55, relwidth=0.9, relheight= 0.3) 


    #Cadastro de Perfis (label)
        self.lb_Cadastro_de_Perfis = Label(self.frame_2, text = "Cadastro de Perfis",
                                              bg= '#dfe3ee', font = ('verdana', 10, 'bold'))
        self.lb_Cadastro_de_Perfis.place(relx=0.35 , rely=0.9)   



     #Criação das labels e entradas de dados (FRAME 3)


    #Código do sistema (label)
        self.lb_perfil = Label(self.frame_3, text = "Codigo do sistema", bg= '#dfe3ee')
        self.lb_perfil.place(relx=0.05 , rely=0.05)
    #Nome do sistema (input)
        self.perfil_entry = Entry(self.frame_3)
        self.perfil_entry.place(relx=0.05, rely=0.15, relwidth=0.25)

    #Perfil 1 (label)
        self.lb_codigo = Label(self.frame_3, text = "Perfil 1", bg= '#dfe3ee')
        self.lb_codigo.place(relx=0.05 , rely=0.25)
    #Perfil 1  (input)
        self.codigo_entry = Entry(self.frame_3)
        self.codigo_entry.place(relx=0.05, rely=0.35, relwidth=0.25)

    #Código do sistema (label)
        self.lb_perfil = Label(self.frame_3, text = "Codigo do sistema 2", bg= '#dfe3ee')
        self.lb_perfil.place(relx=0.05 , rely=0.45)
    #Código do sistema (input)
        self.perfil_entry = Entry(self.frame_3)
        self.perfil_entry.place(relx=0.05, rely=0.55, relwidth=0.25)

    #Perfil 2 (label)
        self.lb_codigo = Label(self.frame_3, text = "Perfil 2", bg= '#dfe3ee')
        self.lb_codigo.place(relx=0.05 , rely=0.65)
    #Perfil 2 (input)
        self.codigo_entry = Entry(self.frame_3)
        self.codigo_entry.place(relx=0.05, rely=0.75, relwidth=0.25)

     #CPF (label)
        self.cpf = Label(self.frame_3, text = "CPF USUÁRIO", bg= '#dfe3ee')
        self.lb_cpf.place(relx=0.50 , rely=0.05)
    #CPF (input)
        self.cpf_entry = Entry(self.frame_3)
        self.cpf_entry.place(relx=0.5, rely=0.15, relwidth=0.25)
         

      


    #Matriz SoD
        self.lb_Cadastro_de_Perfis = Label(self.frame_3, text = "Matriz SoD",
                                              bg= '#dfe3ee', font = ('verdana', 10, 'bold'))
        self.lb_Cadastro_de_Perfis.place(relx=0.45 , rely=0.9) 

#################################################################################################

    




    #criação do banco de dados (treeview)
    def lista_frame_4(self):
        self.listaPrincipal = ttk.Treeview(self.frame_4, height= 3, 
                                           column=("col1", "col2", "col3", "col4", "col5", "col6"))
        self.listaPrincipal.heading("#0", text="")
        self.listaPrincipal.heading("#1", text="Código")
        self.listaPrincipal.heading("#2", text="Sistema")
        self.listaPrincipal.heading("#3", text="Versão")
        self.listaPrincipal.heading('#4', text="Perfil")
        self.listaPrincipal.heading("#5", text="Descrição")
        self.listaPrincipal.heading("#6", text="CPF")
        

        self.listaPrincipal.column("#0", width=1)
        self.listaPrincipal.column("#1", width=80)
        self.listaPrincipal.column("#2", width=120)
        self.listaPrincipal.column("#3", width=80)
        self.listaPrincipal.column("#4", width=60)
        self.listaPrincipal.column("#5", width=60)
        self.listaPrincipal.column("#6", width=60)
        

        self.listaPrincipal.place(relx=0.01 , rely=0.1 , relwidth=0.90 , relheight=0.80)

        self.scroolLista = Scrollbar(self.frame_4, orient='vertical')
        self.listaPrincipal.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx=0.92, rely=0.1, relwidth=0.04, relheight=0.80)

        self.scroolLista = Scrollbar(self.frame_4, orient='horizontal')
        self.listaPrincipal.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx=0.01, rely=0.9, relwidth=0.90, relheight=0.1)
        self.listaPrincipal.bind("<Double-1>", self.OndoubleClick)


    #criando barra de menus
    def Menus(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        filemenu = Menu(menubar)
        usermenu2 = Menu(menubar)

        def Quit(): self.root.destroy()

        menubar.add_cascade(label="Opções", menu= filemenu)
        menubar.add_cascade(label="Relatórios", menu= usermenu2)

        filemenu.add_command(label= "Cadastrar Usuário")
        usermenu2.add_command(label='Gerar Relatórios', command= self.geraRelatSis)
        usermenu2.add_command(label="Sair", command= Quit)



        

        


        
        





    

Application()





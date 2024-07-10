import os
import locale

# Arquivo com as funções de resposta
from Functions_UI import Funcs
from ManagerBD import BancoDados

# Biblioteca para a construção da Interface
from ttkbootstrap import Style, DateEntry
from ttkbootstrap.constants import *
import ttkbootstrap as ttk


locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')


class InterfaceBancoDados:

    def __init__(self, janela_principal):
        self.janela_root = janela_principal.root
        self.my_st = janela_principal.my_st
        self.janela = janela_principal
        self.root_db = ttk.Toplevel(self.janela_root)
        self.root_db.title("Banco de Dados")
        self.db = BancoDados()
        self.wid_pes()
        self.inicTree()

    def wid_pes(self):

        self.frames_inputs = ttk.Frame(self.root_db)
        self.frames_inputs.pack(side=TOP, fill=X, padx=10, pady=10)

        self.input_name = ttk.Entry(self.frames_inputs, width=50, font=("Arial", 14))
        self.input_name.pack(side=LEFT)

        self.btn_consulta = ttk.Button(self.frames_inputs, text="Pesquisar", command=self.tree_search)
        self.btn_consulta.pack(side=LEFT, padx=5)

    def tree_search(self):
        
        for row in self.tree.get_children():
            self.tree.delete(row)

        self._lines_add2 = []
        
        for index, i in enumerate(self.db.search(self.input_name.get())):

            if i[0] in self._lines_add2:

                self.tree.insert(self._lines_add2.index(i[0]), ttk.END, text=i[1], values=['', i[1], i[2]])

            else:

                self.tree.insert('', ttk.END, iid=index, text=i[0], values=[i[0], '', ''])
                self.tree.insert(index, ttk.END, text=i[1], values=['', i[1], i[2]])
                self.tree.item(index)

            self._lines_add2.append(i[0])

        del self._lines_add2


    def inicTree(self):

        self.column_names = ["Locadores", "Locatarios", "Contrato"]
        self.tree = ttk.Treeview(self.root_db, columns=self.column_names, height=30, show='headings', style='primary.Treeview')
        self.tree.column("Contrato", width=145, anchor=ttk.CENTER)
        self.tree.column("Locadores", width=200)
        self.tree.column("Locatarios", width=200, anchor=ttk.CENTER)
        
        self.tree.bind('<Return>', self.on_click)

        self.tree.pack(fill=ttk.BOTH, expand=ttk.YES, padx=10, pady=10, side=BOTTOM)
        self.tree.heading("Locadores", text="Locadores", anchor=ttk.CENTER)
        self.tree.heading("Locatarios", text="Locatarios", anchor=ttk.CENTER)
        self.tree.heading("Contrato", text="Contrato", anchor=ttk.CENTER)
        self._lines_add = []
        for index, i in enumerate(self.db.dados_tkinter()):

            if i[0] in self._lines_add:

                self.tree.insert(self._lines_add.index(i[0]), ttk.END, text=i[1], values=['', i[1], i[2]])

            else:

                self.tree.insert('', ttk.END, iid=index, text=i[0], values=[i[0], '', ''])
                self.tree.insert(index, ttk.END, text=i[1], values=['', i[1], i[2]])
                self.tree.item(index)

            self._lines_add.append(i[0])

        del self._lines_add


    def on_click(self, event=None):
        # print(f"\n{self.tree.item(self.tree.index(self.tree.focus()))['text']}\n")
        # print(self.tree.item(self.tree.parent(self.tree.focus()))['text'])
        # print(self.tree.item(self.tree.focus()))
        dic_selec = self.tree.item(self.tree.focus())

        if dic_selec['values'][1] and dic_selec['values'][2]:

            print("Locatario Selecionado")
            print(dic_selec['text'])
            nome_locador = self.tree.item(self.tree.parent(self.tree.focus()))['text']
            lista_dados = self.db.show_line(nome_locador)
            self.insereLocador(lista_dados)
            # print(lista_dados)
            # for dd in lista_dados[2:]:
            #     if dic_selec['text'] in dd[0]:
            #         self.insereLocador(lista_dados[0])

        elif dic_selec['values'][0]:

            print("Somente Locador")
            print("Não Fianalizado JOGADOR de Peteca!!")

        else:
            print("Parece ter ocorrido um erro, Favor jogador de peteca contador o ADM!!!")

        self.root_db.destroy()

    def insereLocador(self, dados):

        locador = dados[0]
        morador = dados[2][0]
        contrato = dados[1][0]

        self.janela.nomeLoca.insert(0, str(locador[1]))
        self.janela.estcivLoca.insert(0, locador[2])
        self.janela.cpfLoca.insert(0, locador[3])
        self.janela.rgLoca.insert(0, locador[4])
        self.janela.org_ex_locador.insert(0, locador[5])
        self.janela.estado_rg_locador.insert(0, locador[6])
        self.janela.cidad_locador.insert(0, locador[7])
        self.janela.est_locador.insert(0, locador[8])
        self.janela.ruaLocador.insert(0, locador[10])
        self.janela.bairroLocador.insert(0, locador[11])
        self.janela.numeroLocador.insert(0, locador[9])
        # self.janela.cepLocador.insert(0, "15130-057")
        self.janela.combLocador.insert(0, "Homem")

        self.janela.nomeMora1.insert(0, morador[1])
        self.janela.estcivMora.insert(0, morador[2])
        self.janela.cpfMora.insert(0, morador[3])
        self.janela.rgMora.insert(0, morador[4])
        self.janela.org_ex_mora.insert(0, morador[5])
        self.janela.estado_rg_mora.insert(0, morador[6])
        self.janela.cidad_mora.insert(0, morador[7])
        self.janela.est_mora.insert(0, morador[6])

        self.janela.endImov.insert(0, contrato[1])
        self.janela.numImov.insert(0, contrato[2])
        self.janela.bairImov.insert(0, contrato[5])
        self.janela.municImov.insert(0, contrato[3])
        self.janela.estImov.insert(0, contrato[4])
        self.janela.vencImov.insert(0, "05 (CINCO)")
        self.janela.fimImov.entry.insert(0, contrato[7])
        self.janela.prazo.insert(0, contrato[8])
        self.janela.valorImov.insert(0, contrato[9])

        

class Interacao(Funcs):

    def __init__(self):
        # self.my_st = Style(theme="vapor")
        self.my_st = Style(theme="litera")
        #self.root = self.my_st.master
        self.root = self.my_st.master
        self.label_font = ttk.font.Font(size=16, weight='bold', underline=True)
        self.configs()
        self.variaveis_images()
        self.menu_config()  
        self.informs_locador()
        self.informs_morador()
        self.informs_imovel()
        self.informs_fiador()
        self.root.mainloop()

    def inicia_db(self):
        InterfaceBancoDados(self)

    def configs(self):
        self.pasta = os.path.dirname(__file__)
        self.root.title("Contratos")
        self.root.geometry("750x550")
        self.root.resizable(True, True)

        #self.my_st.configure('TCheckbutton', font=("Arial", 16))
        self.notbook = ttk.Notebook(self.root)
        #self.notbook.place(x=0, y=0, width=700, height=480, expa)
        self.notbook.pack(fill='both', expand=True)

        # Aba para o Locador (Dono da casa)
        self.frameLocador = ttk.Frame(self.notbook, width=700, height=480)
        self.frameLocador.pack(fill='both', expand=True)
        self.notbook.add(self.frameLocador, text="Locador")
        

        # Aba para o Locatario (Morador)
        self.frameMora = ttk.Frame(self.notbook, width=700, height=480)
        self.frameMora.pack(fill='both', expand=True)
        self.notbook.add(self.frameMora, text="Locatario")

        # Frame para segundo locador se tiver
        self.frameMora1 = ttk.Frame(self.frameMora, width=700, height=480)
        self.frameMora1.pack(fill='both', expand=True)

        # Frame para segundo locador se tiver
        self.frameMora2 = ttk.Frame(self.frameMora, width=700, height=480)
        self.frameMora2.pack(fill='both', expand=True)

        # Frame para o fiador
        self.fiador = ttk.Frame(self.notbook, width=700, height=480)
        self.fiador.pack(fill='both', expand=True)
        self.notbook.add(self.fiador, text="Fiador(ª)")
        self.notbook.hide(2)

        # Dados do contrato
        self.frameContrato = ttk.Frame(self.notbook)
        self.frameContrato.pack(fill='both', expand=True)
        self.notbook.add(self.frameContrato, text="Contrato")
        
    def menu_config(self):
        self.menuBar = ttk.Menu(self.root)
        self.root.config(menu=self.menuBar)

        self.menuConfig = ttk.Menu(self.menuBar, tearoff=0)

        self.temas = ttk.Menu(self.menuConfig, tearoff=0)
        self.temas.add_command(label='DESCONTINUADO!!!')

        self.menuConfig.add_cascade(label="Temas de Fundo", menu=self.temas)
        self.menuBar.add_cascade(label="Configurações", menu=self.menuConfig)

        self.inserMenu = ttk.Menu(self.menuBar, tearoff=0)
        self.inserMenu.add_command(label="Inserir Dados Prontos", command=self.insere_dados)
        self.inserMenu.add_command(label="Banco de Dados", command=self.inicia_db)
        self.menuBar.add_cascade(label="Inserir", menu=self.inserMenu)

    def informs_locador(self):

        self.nameLa = ttk.Label(self.frameLocador, bootstyle=PRIMARY, text='Nome', font=16)
        self.nameLa.grid(sticky=W, padx=10)
        self.nomeLoca = ttk.Entry(self.frameLocador, width=25, font=14)
        #self.nomeLoca.config(bootstyle=PRIMARY)
        self.nomeLoca.grid(sticky=W, padx=10)

        ttk.Label(self.frameLocador, text="Estado Civil", font=16).grid(row=0, column=1, sticky=W, padx=10)
        self.estcivLoca = ttk.Entry(self.frameLocador, width=9, font=14)
        self.estcivLoca.grid(row=1, column=1, sticky=W, padx=10)

        ttk.Label(self.frameLocador, text="CPF", font=16).grid(column=2, row=0, sticky=W, padx=10)
        self.cpfLoca = ttk.Entry(self.frameLocador, width=15, font=14)
        self.cpfLoca.bind("<KeyRelease>", self.format_cpf)
        self.cpfLoca.grid(column=2, row=1, sticky=W, padx=10)

        ttk.Label(self.frameLocador, text="RG", font=16).grid(sticky=W, padx=10)
        self.rgLoca = ttk.Entry(self.frameLocador, width=20, font=14)
        # self.rgLoca.bind("<KeyRelease>", self.format_rg)
        self.rgLoca.grid(sticky=W, padx=10)

        ttk.Label(self.frameLocador, text="Orgão Expeditor", font=16).grid(row=2, column=1, sticky=W, padx=10)
        self.org_ex_locador = ttk.Entry(self.frameLocador, width=9, font=14)
        self.org_ex_locador.grid(row=3, column=1, sticky=W, padx=10)

        ttk.Label(self.frameLocador, text="Estado", font=16).grid(row=2, column=2, sticky=W, padx=10)
        self.estado_rg_locador = ttk.Entry(self.frameLocador, width=9, font=14)
        self.estado_rg_locador.grid(row=3, column=2, sticky=W, padx=10)

        ttk.Label(self.frameLocador, text='Cidade', font=16).grid(sticky=W, padx=10)
        self.cidad_locador = ttk.Entry(self.frameLocador, font=14, width=20)
        self.cidad_locador.grid(sticky=W, padx=10)

        ttk.Label(self.frameLocador, text="Estado", font=16).grid(row=4, column=1, sticky=W, padx=10)
        self.est_locador = ttk.Entry(self.frameLocador, font=14, width=9)
        self.est_locador.grid(column=1, row=5, sticky=W, padx=10)

        ttk.Label(self.frameLocador, text="Rua/Avenida", font=16).grid(sticky=W, padx=10)
        self.ruaLocador = ttk.Entry(self.frameLocador, width=25, font=14)
        self.ruaLocador.grid(sticky=W, padx=10)

        ttk.Label(self.frameLocador, text="Numero", font=16).grid(row=4, column=2, sticky=W, padx=10)
        self.numeroLocador = ttk.Entry(self.frameLocador, font=14, width=5)
        self.numeroLocador.grid(row=5, column=2, sticky=W, padx=10)

        ttk.Label(self.frameLocador, text="Bairro", font=16).grid(row=6, column=1, sticky=W, padx=10)
        self.bairroLocador = ttk.Entry(self.frameLocador, font=14, width=10)
        self.bairroLocador.grid(row=7, column=1, sticky=W, padx=10)

        ttk.Label(self.frameLocador, text="Complemento", font=16).grid(row=6, column=2, sticky=W, padx=10)
        self.complLocador = ttk.Entry(self.frameLocador, font=14, width=13)
        self.complLocador.grid(row=7, column=2, sticky=W, padx=10)

        ttk.Label(self.frameLocador, text="CEP", font=16).grid(sticky=W, padx=10)
        self.cepLocador = ttk.Entry(self.frameLocador, width=15, font=14)
        self.cepLocador.grid(sticky=W, padx=10)
        
        rosa = "#ff0039"

        self.combStr = ttk.StringVar()
        self.combLocador = ttk.Combobox(self.frameLocador, textvariable=self.combStr, width=13, state='readonly')
        self.combLocador['values'] = ('Homem', 'Mulher')
        self.combLocador.bind("<<ComboboxSelected>>", self.alte_img)
        self.combLocador.grid(row=1, column=3, padx=10)
        self.img_locador = ttk.Label(self.frameLocador, image=self.h_on_image)
        self.img_locador.grid(row=3, rowspan=3, column=3)

        self._fundo_im = ttk.Label(self.frameLocador, image=self.fundo)
        self._fundo_im.grid(columnspan=4, sticky=N)

    def informs_morador(self):
        ttk.Label(self.frameMora1, text='Nome', font=16).grid(sticky=W, padx=10)
        self.nomeMora1 = ttk.Entry(self.frameMora1, width=25, font=14)
        self.nomeMora1.grid(sticky=W, padx=10)

        ttk.Label(self.frameMora1, text="Estado Civil", font=16).grid(row=0, column=1, sticky=W, padx=10)
        self.estcivMora = ttk.Entry(self.frameMora1, width=9, font=14)
        self.estcivMora.grid(row=1, column=1, sticky=W, padx=10, pady=5)

        ttk.Label(self.frameMora1, text="CPF", font=16).grid(column=2, row=0, sticky=W, padx=10)
        # validate="key", validatecommand=(self.vcmd2, "%P")
        self.cpfMora = ttk.Entry(self.frameMora1, width=15, font=14)
        self.cpfMora.bind("<KeyRelease>", self.format_cpf)
        self.cpfMora.grid(column=2, row=1, sticky=W, padx=10)

        ttk.Label(self.frameMora1, text="RG", font=16).grid(sticky=W, padx=10)
        # , validate="key", validatecommand=(self.vcmd, "%P")
        self.rgMora = ttk.Entry(self.frameMora1, width=20, font=14)
        # self.rgMora.bind("<KeyRelease>", self.format_rg)
        self.rgMora.grid(sticky=W, padx=10)

        ttk.Label(self.frameMora1, text="Orgão Expeditor", font=16).grid(row=2, column=1, sticky=W, padx=10)
        self.org_ex_mora = ttk.Entry(self.frameMora1, width=9, font=14)
        self.org_ex_mora.grid(row=3, column=1, sticky=W, padx=10)

        ttk.Label(self.frameMora1, text="Estado", font=16).grid(row=2, column=2, sticky=W, padx=10)
        self.estado_rg_mora = ttk.Entry(self.frameMora1, width=9, font=14)
        self.estado_rg_mora.grid(row=3, column=2, sticky=W, padx=10)

        ttk.Label(self.frameMora1, text='Cidade', font=16).grid(sticky=W, padx=10)
        self.cidad_mora = ttk.Entry(self.frameMora1, font=14, width=20)
        self.cidad_mora.grid(sticky=W, padx=10)

        ttk.Label(self.frameMora1, text="Estado", font=16).grid(row=4, column=1, sticky=W, padx=10)
        self.est_mora = ttk.Entry(self.frameMora1, font=14, width=9)
        self.est_mora.grid(column=1, row=5, sticky=W, padx=10)

        self.combMoraStr = ttk.StringVar()
        self.combMorador1 = ttk.Combobox(self.frameMora1, textvariable=self.combMoraStr, width=13, state='readonly')
        self.combMorador1['values'] = ('Homem', 'Mulher')
        self.combMorador1.bind("<<ComboboxSelected>>", self.alte_img)
        self.combMorador1.grid(row=1, column=3, padx=10)
        self.img_mora = ttk.Label(self.frameMora1, image=self.h_on_image)
        self.img_mora.grid(row=3, rowspan=3, column=3)
        
        self.quantidadeLocatarios = ttk.IntVar()
        self.quantidadeLocatarios.set(1)
        self.add_seg_morador = ttk.Checkbutton(self.frameMora1, image=self.add_locatarios_img , text='Dois Locatarios', variable=self.quantidadeLocatarios, onvalue=2, offvalue=1, command=lambda: self.ativa_locatarios(1))
        self.add_seg_morador.grid(sticky=W, padx=10, pady=15)

        self.varfiad = ttk.IntVar()
        self.varfiad.set(0)

        self.my_st.configure('custom.TCheckbutton', font=('Arial', 16, 'bold'))
        
        self.add_fiad = ttk.Checkbutton(self.frameMora1, text='Fiador', style='custom.TCheckbutton', variable=self.varfiad, onvalue=1, offvalue=0, command=self.add_fiador)
        self.add_fiad.grid(row=6, columnspan=1)

        # --------------------------------------------------------------------------------------------------------------------------

        
        ttk.Label(self.frameMora2, text='Nome', font=16).grid(sticky=W, padx=10)
        self.nomeMora2 = ttk.Entry(self.frameMora2, width=25, font=14)
        self.nomeMora2.grid(sticky=W, padx=10)

        ttk.Label(self.frameMora2, text="Estado Civil", font=16).grid(row=0, column=1, sticky=W, padx=10)
        self.estcivMora2 = ttk.Entry(self.frameMora2, width=9, font=14)
        self.estcivMora2.grid(row=1, column=1, sticky=W, padx=10)

        ttk.Label(self.frameMora2, text="CPF", font=16).grid(column=2, row=0, sticky=W, padx=10)
        # validate="key", validatecommand=(self.vcmd2, "%P")
        self.cpfMora2 = ttk.Entry(self.frameMora2, width=15, font=14)
        self.cpfMora2.bind("<KeyRelease>", self.format_cpf)
        self.cpfMora2.grid(column=2, row=1, sticky=W, padx=10)

        ttk.Label(self.frameMora2, text="RG", font=16).grid(sticky=W, padx=10)
        # , validate="key", validatecommand=(self.vcmd, "%P")
        self.rgMora2 = ttk.Entry(self.frameMora2, width=20, font=14)
        # self.rgMora2.bind("<KeyRelease>", self.format_rg)
        self.rgMora2.grid(sticky=W, padx=10)

        ttk.Label(self.frameMora2, text="Orgão Expeditor", font=16).grid(row=2, column=1, sticky=W, padx=10)
        self.org_ex_mora2 = ttk.Entry(self.frameMora2, width=9, font=14)
        self.org_ex_mora2.grid(row=3, column=1, sticky=W, padx=10)

        ttk.Label(self.frameMora2, text="Estado", font=16).grid(row=2, column=2, sticky=W, padx=10)
        self.estado_rg_mora2 = ttk.Entry(self.frameMora2, width=9, font=14)
        self.estado_rg_mora2.grid(row=3, column=2, sticky=W, padx=10)

        ttk.Label(self.frameMora2, text='Cidade', font=16).grid(sticky=W, padx=10)
        self.cidad_mora2 = ttk.Entry(self.frameMora2, font=14, width=20)
        self.cidad_mora2.grid(sticky=W, padx=10)

        ttk.Label(self.frameMora2, text="Estado", font=16).grid(row=4, column=1, sticky=W, padx=10)
        self.est_mora2 = ttk.Entry(self.frameMora2, font=14, width=9)
        self.est_mora2.grid(column=1, row=5, sticky=W, padx=10)

        self.canvas = ttk.Canvas(self.frameMora2, width=135, height=53, bg='white')
        self.canvas.place(rely=1.0, relx=1.0, anchor=SE)
        self.canvas.create_image(
            (70, 30),
            image=self.fund_pq
        )

        self.combMora2Str = ttk.StringVar()
        self.combMora2 = ttk.Combobox(self.frameMora2, textvariable=self.combMora2Str, width=13, state='readonly')
        self.combMora2['values'] = ('Homem', 'Mulher')
        self.combMora2.bind("<<ComboboxSelected>>", self.alte_img)
        self.combMora2.grid(row=1, column=3, padx=10)
        self.img_mora2 = ttk.Label(self.frameMora2, image=self.f_on_image)
        self.img_mora2.grid(row=3, rowspan=3, column=3)

        if self.quantidadeLocatarios.get() == 1:
            for child in self.frameMora2.winfo_children():
                child.configure(state='disable')
    
    def informs_imovel(self):

        ttk.Label(self.frameContrato, text="Endereço Imovel", font=self.label_font).grid(sticky=W, padx=10)
        ttk.Label(self.frameContrato, image=self.imgCasa).grid(row=0, column=0, columnspan=2)
        ttk.Label(self.frameContrato, text="Rua/Avenida", font="16").grid(sticky=W, padx=10)
        self.endImov = ttk.Entry(self.frameContrato, font="14", width=25)
        self.endImov.grid(sticky=W, padx=10)

        ttk.Label(self.frameContrato, text="Numero", font='16').grid(row=1, column=1, sticky=W, padx=10)
        self.numImov = ttk.Entry(self.frameContrato, width=9, font='14')
        self.numImov.grid(row=2, column=1, sticky=W, padx=10)

        ttk.Label(self.frameContrato, text="Complemento", font='16').grid(row=1, column=2, sticky=W, padx=10)
        self.complImov = ttk.Entry(self.frameContrato, width=15, font='14')
        self.complImov.grid(row=2, column=2, sticky=W, padx=10)

        self.finalidadeVar = ttk.IntVar()
        self.residencial = ttk.Checkbutton(self.frameContrato, text="Residencial", onvalue=0, offvalue=1, variable=self.finalidadeVar, style="TCheckbutton")
        self.residencial.grid(row=1, column=3, sticky=W, padx=15)
        self.comercial = ttk.Checkbutton(self.frameContrato, text="Comercio", onvalue=1, offvalue=0, variable=self.finalidadeVar, style='teste.TCheckbutton')
        self.comercial.grid(row=2, column=3, sticky=W, padx=15)

        self.iptuVar = ttk.IntVar()
        ttk.Label(self.frameContrato, text='Pagamento IPTU', font=15).grid(row=3, column=3, sticky=W)
        self.iptuLoca = ttk.Checkbutton(self.frameContrato, text='Locador(ª)', onvalue=1, offvalue=0, variable=self.iptuVar, style='teste.TCheckbutton')
        self.iptuLoca.grid(row=4, column=3, sticky=W, padx=10)
        self.iptuMora = ttk.Checkbutton(self.frameContrato, text='Locatario(ª)', onvalue=0, offvalue=1, variable=self.iptuVar, style='teste.TCheckbutton')
        self.iptuMora.grid(row=5, column=3, sticky=W, padx=10)

        ttk.Label(self.frameContrato, text="Bairro", font='16').grid(row=3, column=0, sticky=W, padx=10)
        self.bairImov = ttk.Entry(self.frameContrato, width=20, font='14')
        self.bairImov.grid(row=4, column=0, sticky=EW, padx=10)

        ttk.Label(self.frameContrato, text="Municipio", font='16').grid(row=3, column=1, sticky=W, padx=10)
        self.municImov = ttk.Entry(self.frameContrato, width=9, font='14')
        self.municImov.grid(row=4, column=1, sticky=W, padx=10)

        ttk.Label(self.frameContrato, text="Estado", font='16').grid(row=3, column=2, sticky=W, padx=10)
        self.estImov = ttk.Entry(self.frameContrato, width=5, font='14')
        self.estImov.grid(row=4, column=2, sticky=W, padx=10)

        ttk.Label(self.frameContrato, text="Vencimento Aluguel", font='16').grid(row=5, column=0, sticky=EW, padx=10)
        self.vencImov = ttk.Entry(self.frameContrato, width=9, font='14')
        self.vencImov.grid(row=6, column=0, padx=10, sticky=EW)

        ttk.Label(self.frameContrato, text="Inicio", font='16').grid(row=5, column=1,sticky=W, padx=10)
        self.inicioImov = DateEntry(self.frameContrato)
        self.inicioImov.grid(row=6, column=1, sticky=W, padx=10)
        self.inicioImov.entry['font'] = 14
        self.inicioImov.entry['width'] = 9

        ttk.Label(self.frameContrato, text="Fim", font='16').grid(row=5, column=2, sticky=W, padx=10)
        self.fimImov = DateEntry(self.frameContrato)
        self.fimImov.grid(row=6, column=2, sticky=W, padx=10)
        self.fimImov.entry['font'] = 14
        self.fimImov.entry['width'] = 9

        ttk.Label(self.frameContrato, text='Prazo da Locação', font='16').grid(sticky=W, padx=10)
        self.prazo = ttk.Entry(self.frameContrato, font='14', width=11)
        self.prazo.grid(sticky=W, padx=10)

        ttk.Label(self.frameContrato, text="Valor", font='16').grid(sticky=W, padx=10, columnspan=3)
        self.valorImov = ttk.Entry(self.frameContrato, font='14')
        self.valorImov.grid(sticky=EW, padx=10, columnspan=3)

        self.txtCaucao = ttk.Label(self.frameContrato, text='Valor Caução', font='16')
        self.caucao = ttk.Entry(self.frameContrato, font='14')
        self.txtCaucao.grid(row=7, column=1, sticky=W, padx=10)
        self.caucao.grid(row=8, column=1, sticky=EW, padx=10, columnspan=2)

        self.txtCaucao.grid_forget()
        self.caucao.grid_forget()

        self.caucaoVar = ttk.IntVar()
        self.comCaucao = ttk.Checkbutton(self.frameContrato, text='Com Caucão', onvalue=1, offvalue=0, variable=self.caucaoVar, command=self.ativa_caucao, style='teste.TCheckbutton')
        self.comCaucao.grid(row=6, column=3, sticky=W, padx=10)
        self.semCaucao = ttk.Checkbutton(self.frameContrato, text='Sem Caucão', onvalue=0, offvalue=1, variable=self.caucaoVar, command=self.ativa_caucao, style='teste.TCheckbutton')
        self.semCaucao.grid(row=7, column=3, sticky=W, padx=10)

        ttk.Label(self.frameContrato, text='Forma de Pagamento', font=16).grid(sticky=W, padx=10)
        self.formPG = ttk.Entry(self.frameContrato, font=14)
        self.formPG.grid(sticky=EW, padx=10, columnspan=3)

        self.salve = ttk.Button(self.frameContrato, text="Salvar", width=15, style="<danger>", command=self.salvar_word)
        self.salve.grid(column=3)

        self.delBtn = ttk.Button(self.frameContrato, image=self.lixeira, command=lambda: self.limp_tela(ttk))
        self.delBtn.grid(row=0, column=4)

        self._fundo_im_c = ttk.Label(self.frameContrato, image=self.fund_pq)
        #self._fundo_im.grid(columnspan=4, sticky=N)
        self._fundo_im_c.place(rely=1.0, relx=1.0, anchor=SE)

    def informs_fiador(self):

        self.lb_fram_f1 = ttk.LabelFrame(self.fiador, text="Dados Fiador", style=PRIMARY, relief='solid')
        self.lb_fram_f1.grid(sticky=NW, ipady=5, padx=10)

        self.lb_fram_f2 = ttk.LabelFrame(self.fiador, text="Dados Fiador", style=PRIMARY, relief='solid')
        self.lb_fram_f2.grid(sticky=NW, ipady=5, padx=10)

        self.lb_fram_end = ttk.LabelFrame(self.fiador, text="Endereço", style=PRIMARY, relief='solid')
        self.lb_fram_end.grid(sticky=NW, ipady=5, padx=10)

        # --------------------------------------------------------------------------------------------------

        ttk.Label(self.lb_fram_f1, text='Nome', font=16).grid(sticky=W, padx=10)
        self.nomeFiador = ttk.Entry(self.lb_fram_f1, width=25, font=14)
        self.nomeFiador.grid(sticky=W, padx=10)

        ttk.Label(self.lb_fram_f1, text="Estado Civil", font=16).grid(row=0, column=1, sticky=W, padx=10)
        self.estcivFiador = ttk.Entry(self.lb_fram_f1, width=9, font=14)
        self.estcivFiador.grid(row=1, column=1, sticky=W, padx=10)

        ttk.Label(self.lb_fram_f1, text="CPF", font=16).grid(column=2, row=0, sticky=W, padx=10)
        # validate="key", validatecommand=(self.vcmd2, "%P")
        self.cpfFiador = ttk.Entry(self.lb_fram_f1, width=15, font=14)
        self.cpfFiador.bind("<KeyRelease>", self.format_cpf)
        self.cpfFiador.grid(column=2, row=1, sticky=W, padx=10)

        ttk.Label(self.lb_fram_f1, text="RG", font=16).grid(sticky=W, padx=10)
        # , validate="key", validatecommand=(self.vcmd, "%P")
        self.rgFiador = ttk.Entry(self.lb_fram_f1, width=20, font=14)
        # self.rgFiador.bind("<KeyRelease>", self.format_rg)
        self.rgFiador.grid(sticky=W, padx=10)

        ttk.Label(self.lb_fram_f1, text="Orgão Expeditor", font=16).grid(row=2, column=1, sticky=W, padx=10)
        self.org_ex_fiador = ttk.Entry(self.lb_fram_f1, width=9, font=14)
        self.org_ex_fiador.grid(row=3, column=1, sticky=W, padx=10)

        ttk.Label(self.lb_fram_f1, text="Estado", font=16).grid(row=2, column=2, sticky=W, padx=10)
        self.estado_rg_fiador = ttk.Entry(self.lb_fram_f1, width=9, font=14)
        self.estado_rg_fiador.grid(row=3, column=2, sticky=W, padx=10)

        # -----------------------------------------------------------------------------

        ttk.Label(self.lb_fram_f2, text='Nome', font=16).grid(sticky=W, padx=10)
        self.nomeFiador2 = ttk.Entry(self.lb_fram_f2, width=25, font=14)
        self.nomeFiador2.grid(sticky=W, padx=10)

        ttk.Label(self.lb_fram_f2, text="Estado Civil", font=16).grid(row=0, column=1, sticky=W, padx=10)
        self.estcivFiador2 = ttk.Entry(self.lb_fram_f2, width=9, font=14)
        self.estcivFiador2.grid(row=1, column=1, sticky=W, padx=10)

        ttk.Label(self.lb_fram_f2, text="CPF", font=16).grid(column=2, row=1, sticky=W, padx=10)
        # validate="key", validatecommand=(self.vcmd2, "%P")
        self.cpfFiador2 = ttk.Entry(self.lb_fram_f2, width=15, font=14)
        self.cpfFiador2.bind("<KeyRelease>", self.format_cpf)
        self.cpfFiador2.grid(column=2, row=1, sticky=W, padx=10)

        ttk.Label(self.lb_fram_f2, text="RG", font=16).grid(sticky=W, padx=10)
        # , validate="key", validatecommand=(self.vcmd, "%P")
        self.rgFiador2 = ttk.Entry(self.lb_fram_f2, width=20, font=14)
        # self.rgFiador2.bind("<KeyRelease>", self.format_rg)
        self.rgFiador2.grid(sticky=W, padx=10)

        ttk.Label(self.lb_fram_f2, text="Orgão Expeditor", font=16).grid(row=2, column=1, sticky=W, padx=10)
        self.org_ex_fiador2 = ttk.Entry(self.lb_fram_f2, width=9, font=14)
        self.org_ex_fiador2.grid(row=3, column=1, sticky=W, padx=10)

        ttk.Label(self.lb_fram_f2, text="Estado", font=16).grid(row=2, column=2, sticky=W, padx=10)
        self.estado_rg_fiador2 = ttk.Entry(self.lb_fram_f2, width=9, font=14)
        self.estado_rg_fiador2.grid(row=3, column=2, sticky=W, padx=10)


        # -----------------------------------------------------------------------------
        # Endereço

        ttk.Label(self.lb_fram_end, text="Rua/Avenida", font=16).grid(sticky=W, padx=10)
        self.ruaFiador = ttk.Entry(self.lb_fram_end, width=25, font=14)
        self.ruaFiador.grid(sticky=W, padx=10)

        ttk.Label(self.lb_fram_end, text="Numero", font=16).grid(row=0, column=2, sticky=W, padx=10)
        self.numeroFiador = ttk.Entry(self.lb_fram_end, font=14, width=5)
        self.numeroFiador.grid(row=1, column=2, sticky=W, padx=10)

        ttk.Label(self.lb_fram_end, text="Bairro", font=16).grid(row=0, column=1, sticky=W, padx=10)
        self.bairroFiador = ttk.Entry(self.lb_fram_end, font=14, width=10)
        self.bairroFiador.grid(row=1, column=1, sticky=W, padx=10)

        ttk.Label(self.lb_fram_end, text='Cidade', font=16).grid(sticky=W, padx=10)
        self.cidad_fiador = ttk.Entry(self.lb_fram_end, font=14, width=20)
        self.cidad_fiador.grid(sticky=W, padx=10)

        ttk.Label(self.lb_fram_end, text="Estado", font=16).grid(row=2, column=1, sticky=W, padx=10)
        self.est_fiador = ttk.Entry(self.lb_fram_end, font=14, width=9)
        self.est_fiador.grid(column=1, row=3, sticky=W, padx=10)

        ttk.Label(self.lb_fram_end, text="Complemento", font=16).grid(row=2, column=2, sticky=W, padx=10)
        self.complFiador = ttk.Entry(self.lb_fram_end, font=14, width=13)
        self.complFiador.grid(row=3, column=2, sticky=W, padx=10)

        ttk.Label(self.lb_fram_end, text="CEP", font=16).grid(sticky=W, padx=10)
        self.cepFiador = ttk.Entry(self.lb_fram_end, width=15, font=14)
        self.cepFiador.grid(sticky=W, padx=10)

        # Habilitar segundo fiador

        self.var2fiador = ttk.IntVar()
        self.var2fiador.set(0)

        self.hab_fiador = ttk.Checkbutton(self.fiador, text='2ª Fiador', style='custom.TCheckbutton', variable=self.var2fiador, onvalue=1, offvalue=0, command=lambda: self.ativa_locatarios(2))
        self.hab_fiador.grid(row=2, columnspan=1, sticky=E)        

        # ------------------------------------------------------------------------
        # Imagens Feminino/Masculino
        self.combFiadorStr = ttk.StringVar()
        self.combFiador = ttk.Combobox(self.lb_fram_f1, textvariable=self.combFiadorStr, width=13, state='readonly')
        self.combFiador['values'] = ('Homem', 'Mulher')
        self.combFiador.bind("<<ComboboxSelected>>", self.alte_img)
        self.combFiador.grid(row=1, column=3, padx=10)
        self.img_fiador = ttk.Label(self.lb_fram_f1, image=self.h_on_image)
        self.img_fiador.grid(row=2, rowspan=3, column=3)

        # --------------------------------------------------------

        self.combFiadorStr2 = ttk.StringVar()
        self.combFiador2 = ttk.Combobox(self.lb_fram_f2, textvariable=self.combFiadorStr2, width=13, state='readonly')
        self.combFiador2['values'] = ('Homem', 'Mulher')
        self.combFiador2.bind("<<ComboboxSelected>>", self.alte_img)
        self.combFiador2.grid(row=1, column=3, padx=10)
        self.img_fiador2 = ttk.Label(self.lb_fram_f2, image=self.h_on_image)
        self.img_fiador2.grid(row=2, rowspan=3, column=3)

        if self.var2fiador.get() == 0:
            for child in self.lb_fram_f2.winfo_children():
                child.configure(state='disable')

        #  self._fundo_im = ttk.Label(self.fiador, image=self.fund_pq)
        #self._fundo_im.grid(columnspan=4, sticky=N)
        #  self._fundo_im.place(rely=1.0, relx=1.0, anchor=SE)


Interacao()

import tkinter as tk
from tkinter import messagebox, ttk
import random
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict
import locale
import platform
from PIL import Image, ImageTk

THEME = {
    'BG': '#141414',
    'CARD_BG': '#1F1F1F',
    'PAPER': '#222222',
    'TEXT': '#F5F5F5',
    'ACCENT_PRIMARY': '#1976D2', 
    'ACCENT_SECOND': '#9C27B0',   
    'ACCENT_THIRD': '#FF9800',     
    'ACCENT_SUCCESS': '#43A047', 
    'DANGER': '#E53935'
}
FONT = ("Segoe UI", 11)
FONT_BOLD = ("Segoe UI", 12, "bold")

vendas_historico = []
logo_image_tk = None

def gerar_vendas_aleatorias():
    global vendas_historico
    if vendas_historico:
        return
    produtos = ["Pizza", "Refrigerante", "Hambúrguer", "Cerveja"]
    precos = [75, 5.00, 20.00, 8.00]
    formas_pagamento = ["Dinheiro", "Cartão", "Pix"]
    hoje = datetime.now()

    for _ in range(random.randint(5, 15)):
        produto = random.choice(produtos)
        vendas_historico.append({
            "data": hoje.strftime("%Y-%m-%d"),
            "produto": produto,
            "preco": precos[produtos.index(produto)],
            "quantidade": random.randint(1, 3),
            "forma_pagamento": random.choice(formas_pagamento)
        })

    for i in range(1, 91):
        data_passada = hoje - timedelta(days=i)
        for _ in range(random.randint(1, 10)):
            produto = random.choice(produtos)
            vendas_historico.append({
                "data": data_passada.strftime("%Y-%m-%d"),
                "produto": produto,
                "preco": precos[produtos.index(produto)],
                "quantidade": random.randint(1, 2),
                "forma_pagamento": random.choice(formas_pagamento)
            })

gerar_vendas_aleatorias()

produtos_estoque = [
    {"nome": "Pizza", "preço": 75.00, "quantidade": 55, "validade": "31/12/2025"},
    {"nome": "Hambúrguer", "preço": 20.00, "quantidade": 68, "validade": "15/09/2025"},
    {"nome": "Salgadinho de Queijo", "preço": 5.50, "quantidade": 150, "validade": "10/10/2025"},
    {"nome": "Batata Frita", "preço": 15.00, "quantidade": 85, "validade": "25/11/2025"},
    {"nome": "Coxinha", "preço": 7.00, "quantidade": 120, "validade": "05/11/2025"},
    {"nome": "Refrigerante", "preço": 5.00, "quantidade": 112, "validade": "20/11/2026"},
    {"nome": "Cerveja", "preço": 8.00, "quantidade": 95, "validade": "10/05/2027"},
    {"nome": "Vinho Tinto", "preço": 45.00, "quantidade": 30, "validade": "Indeterminada"},
    {"nome": "Suco de Laranja", "preço": 6.50, "quantidade": 75, "validade": "01/10/2025"},
    {"nome": "Água Mineral", "preço": 3.00, "quantidade": 200, "validade": "20/08/2027"},
    {"nome": "Bolo de Chocolate", "preço": 12.00, "quantidade": 40, "validade": "22/09/2025"},
    {"nome": "Sorvete", "preço": 10.00, "quantidade": 60, "validade": "30/06/2026"},
    {"nome": "Mousse de Maracujá", "preço": 8.50, "quantidade": 50, "validade": "18/09/2025"}
]

mesas = [{"nome": f"Mesa {i+1}", "status": "Ocupada" if i % 2 == 0 else "Disponível", "comanda": [], "reserva_nome": "", "reserva_tel": ""} for i in range(10)]
vendas = []

def style_label(lbl):
    lbl.config(bg=THEME['CARD_BG'], fg=THEME['TEXT'], font=FONT)

def style_button(btn, bg_color=None, fg_color=None, bold=False):
    if bg_color is None:
        bg_color = THEME['ACCENT_PRIMARY']
    if fg_color is None:
        fg_color = THEME['TEXT']
    f = ("Segoe UI", 11, "bold") if bold else FONT
    btn.config(bg=bg_color, fg=fg_color, font=f, relief="flat")

def show_success_dialog(logo_tk):
    success_window = tk.Toplevel(login_window)
    success_window.title("Login Bem-Sucedido")
    success_window.config(bg=THEME['BG'])
    success_window.geometry("300x300")
    success_window.transient(login_window)
    success_window.grab_set()

    login_window.update_idletasks()
    x = login_window.winfo_x() + login_window.winfo_width() // 2 - success_window.winfo_width() // 2
    y = login_window.winfo_y() + login_window.winfo_height() // 2 - success_window.winfo_height() // 2
    success_window.geometry(f'+{x}+{y}')

    lbl_logo = tk.Label(success_window, image=logo_tk, bg=THEME['BG'])
    lbl_logo.image = logo_tk
    lbl_logo.pack(pady=10, padx=10)

    lbl_msg = tk.Label(success_window, text="Login bem-sucedido!", font=FONT_BOLD, fg=THEME['TEXT'], bg=THEME['BG'])
    lbl_msg.pack(pady=5)
    
    success_window.after(1500, lambda: [success_window.destroy(), login_window.destroy(), abrir_tela_principal()])


def login():
    global logo_image_tk
    username = entry_username.get()
    password = entry_password.get()
    if username == "admin" and password == "1234":
        show_success_dialog(logo_image_tk)
    else:
        messagebox.showerror("Erro", "Credenciais inválidas!")


def abrir_tela_principal():
    global main_window
    main_window = tk.Tk()
    main_window.title("Sistema PDV Cobra Demandas")
    main_window.geometry("900x650")
    main_window.config(bg=THEME['BG'])

    header = tk.Frame(main_window, bg=THEME['BG'])
    header.pack(fill=tk.X, padx=20, pady=(20, 10))

    lbl_title = tk.Label(header, text="Sistema PDV Cobra Demandas", font=("Segoe UI", 20, "bold"), fg=THEME['TEXT'], bg=THEME['BG'])
    lbl_title.pack(side=tk.LEFT)

    lbl_sub = tk.Label(header, text=datetime.now().strftime("%d/%m/%Y"), font=FONT, fg=THEME['TEXT'], bg=THEME['BG'])
    lbl_sub.pack(side=tk.RIGHT)

    frame_menu = tk.Frame(main_window, bg=THEME['BG'])
    frame_menu.pack(pady=20)

    botoes = [
        ("Estoque de Produtos", abrir_estoque, THEME['ACCENT_PRIMARY']),
        ("Mesas", abrir_mesas, THEME['ACCENT_SECOND']),
        ("Reservar Mesa", abrir_reserva, THEME['ACCENT_THIRD']),
        ("Demandas", abrir_comandas, THEME['ACCENT_PRIMARY']), 
        ("Caixa", abrir_caixa, THEME['ACCENT_SUCCESS']),
        ("Relatórios de Vendas", abrir_relatorios, THEME['ACCENT_SECOND']),
        ("Relatório de Pagamentos", abrir_relatorios_pagamentos, THEME['DANGER'])
    ]

    for i, (texto, comando, cor) in enumerate(botoes):
        btn = tk.Button(frame_menu, text=texto, width=24, height=3,
                        font=("Segoe UI", 11, "bold"), bg=cor, fg=THEME['TEXT'], relief="flat",
                        command=comando)
        btn.grid(row=i // 3, column=i % 3, padx=16, pady=16)

    btn_sair = tk.Button(main_window, text="Sair", width=20, height=2, font=FONT_BOLD,
                         bg=THEME['DANGER'], fg=THEME['TEXT'], relief="flat", command=main_window.destroy)
    btn_sair.pack(pady=20)

    main_window.mainloop()

def salvar_alteracoes_estoque(produto, quantidade_entry, validade_entry, tela_estoque):
    try:
        nova_quantidade = int(quantidade_entry.get())
        nova_validade = validade_entry.get()
        if nova_quantidade >= 0:
            for item in produtos_estoque:
                if item['nome'] == produto['nome']:
                    item['quantidade'] = nova_quantidade
                    item['validade'] = nova_validade
                    break
            messagebox.showinfo("Sucesso", f"Estoque de {produto['nome']} atualizado.")
            tela_estoque.destroy()
            abrir_estoque()
        else:
            messagebox.showerror("Erro", "A quantidade deve ser um número positivo.")
    except ValueError:
        messagebox.showerror("Erro", "A quantidade deve ser um número válido.")


def abrir_estoque():
    tela_estoque = tk.Toplevel(main_window)
    tela_estoque.title("Estoque de Produtos")
    tela_estoque.geometry("760x600")
    tela_estoque.config(bg=THEME['BG'])

    canvas = tk.Canvas(tela_estoque, bg=THEME['BG'], highlightthickness=0)
    scrollbar = tk.Scrollbar(tela_estoque, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=THEME['CARD_BG'])

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True, padx=(10,0), pady=10)
    scrollbar.pack(side="right", fill="y", padx=(0,10), pady=10)

    header_frame = tk.Frame(scrollable_frame, bg=THEME['CARD_BG'])
    header_frame.pack(fill=tk.X, pady=(10,5))

    tk.Label(header_frame, text="Produto", font=FONT_BOLD, fg=THEME['TEXT'], bg=THEME['CARD_BG'], width=22, anchor='w').grid(row=0, column=0, padx=5)
    tk.Label(header_frame, text="Preço", font=FONT_BOLD, fg=THEME['TEXT'], bg=THEME['CARD_BG'], width=10, anchor='w').grid(row=0, column=1, padx=5)
    tk.Label(header_frame, text="Quantidade", font=FONT_BOLD, fg=THEME['TEXT'], bg=THEME['CARD_BG'], width=14, anchor='w').grid(row=0, column=2, padx=5)
    tk.Label(header_frame, text="Validade", font=FONT_BOLD, fg=THEME['TEXT'], bg=THEME['CARD_BG'], width=12, anchor='w').grid(row=0, column=3, padx=5)
    tk.Label(header_frame, text="", font=FONT_BOLD, fg=THEME['TEXT'], bg=THEME['CARD_BG'], width=12).grid(row=0, column=4, padx=5)

    for i, produto in enumerate(produtos_estoque):
        preco_formatado = f"R${produto['preço']:.2f}".replace('.', ',')
        row_frame = tk.Frame(scrollable_frame, bg=THEME['CARD_BG'])
        row_frame.pack(fill=tk.X, padx=8, pady=6)

        tk.Label(row_frame, text=produto['nome'], font=FONT, fg=THEME['TEXT'], bg=THEME['CARD_BG'], width=22, anchor='w').grid(row=0, column=0, padx=5)
        tk.Label(row_frame, text=preco_formatado, font=FONT, fg=THEME['TEXT'], bg=THEME['CARD_BG'], width=10, anchor='w').grid(row=0, column=1, padx=5)

        quantidade_entry = tk.Entry(row_frame, font=FONT, bg=THEME['PAPER'], fg=THEME['TEXT'], width=12, relief="flat")
        quantidade_entry.insert(0, str(produto['quantidade']))
        quantidade_entry.grid(row=0, column=2, padx=5)

        validade_entry = tk.Entry(row_frame, font=FONT, bg=THEME['PAPER'], fg=THEME['TEXT'], width=14, relief="flat")
        validade_entry.insert(0, produto['validade'])
        validade_entry.grid(row=0, column=3, padx=5)

        btn_salvar = tk.Button(row_frame, text="Salvar", font=("Segoe UI", 10, "bold"), bg=THEME['ACCENT_SUCCESS'], fg=THEME['TEXT'], relief="flat", command=lambda p=produto, q=quantidade_entry, v=validade_entry, t=tela_estoque: salvar_alteracoes_estoque(p, q, v, t))
        btn_salvar.grid(row=0, column=4, padx=10)

    btn_voltar = tk.Button(tela_estoque, text="Voltar", width=18, height=2, font=FONT_BOLD, bg=THEME['DANGER'], fg=THEME['TEXT'], relief="flat", command=tela_estoque.destroy)
    btn_voltar.pack(pady=12)

def abrir_relatorios():
    tela_relatorios = tk.Toplevel(main_window)
    tela_relatorios.title("Relatórios de Vendas")
    tela_relatorios.geometry("900x650")
    tela_relatorios.config(bg=THEME['BG'])

    lbl_titulo = tk.Label(tela_relatorios, text="Relatórios de Vendas", font=("Segoe UI", 16, "bold"), fg=THEME['TEXT'], bg=THEME['BG'])
    lbl_titulo.pack(pady=12)

    frame_grafico = tk.Frame(tela_relatorios, bg=THEME['BG'])
    frame_grafico.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    opcoes_periodo = ["Diário", "Semanal", "Mensal", "Trimestral"]
    periodo_selecionado = tk.StringVar()
    periodo_selecionado.set("Semanal")

    combobox_periodo = ttk.Combobox(tela_relatorios, textvariable=periodo_selecionado, values=opcoes_periodo, font=FONT)
    combobox_periodo.pack(pady=6)

    def gerar_dados_grafico(periodo):
        dados = defaultdict(float)
        hoje = datetime.now().date()

        if periodo == "Diário":
            dias_passados = 1
            data_inicio = hoje
        elif periodo == "Semanal":
            dias_passados = 7
            data_inicio = hoje - timedelta(days=dias_passados)
        elif periodo == "Mensal":
            dias_passados = 30
            data_inicio = hoje - timedelta(days=dias_passados)
        elif periodo == "Trimestral":
            dias_passados = 90
            data_inicio = hoje - timedelta(days=dias_passados)
        else:
            return [], []

        vendas_periodo = [v for v in vendas_historico if datetime.strptime(v['data'], "%Y-%m-%d").date() >= data_inicio]

        for venda in vendas_periodo:
            data_venda = datetime.strptime(venda['data'], "%Y-%m-%d").date()
            total = venda['preco'] * venda['quantidade']
            if periodo == "Diário":
                dados[data_venda.strftime("%d/%m")] += total
            elif periodo == "Semanal":
                dados[data_venda.strftime("%A, %d/%m")] += total
            elif periodo == "Mensal":
                mes_ano = data_venda.strftime("%B, %Y")
                dados[mes_ano] += total
            elif periodo == "Trimestral":
                mes_ano = data_venda.strftime("%B, %Y")
                dados[mes_ano] += total

        labels = list(dados.keys())
        valores = list(dados.values())
        return labels, valores

    def criar_e_exibir_grafico(frame_grafico, periodo):
        for widget in frame_grafico.winfo_children():
            widget.destroy()

        labels, valores = gerar_dados_grafico(periodo)

        if not labels:
            tk.Label(frame_grafico, text="Nenhum dado de venda para o período.", bg=THEME['BG'], fg=THEME['TEXT'], font=FONT).pack(pady=20)
            return

        fig = plt.figure(figsize=(7, 4), dpi=100, facecolor=THEME['BG'])
        ax = fig.add_subplot(111)

        ax.bar(labels, valores, color=THEME['ACCENT_PRIMARY'])
        ax.set_title(f"Vendas - {periodo}", color=THEME['TEXT'])
        ax.set_ylabel("Receita (R$)", color=THEME['TEXT'])
        ax.set_xlabel("Período", color=THEME['TEXT'])
        ax.tick_params(axis='x', rotation=45, colors=THEME['TEXT'])
        ax.tick_params(axis='y', colors=THEME['TEXT'])
        ax.set_facecolor(THEME['CARD_BG'])
        fig.patch.set_facecolor(THEME['BG'])
        ax.spines['bottom'].set_color(THEME['TEXT'])
        ax.spines['left'].set_color(THEME['TEXT'])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)

    def on_combobox_change(event):
        periodo = periodo_selecionado.get()
        criar_e_exibir_grafico(frame_grafico, periodo)

    combobox_periodo.bind("<<ComboboxSelected>>", on_combobox_change)

    criar_e_exibir_grafico(frame_grafico, periodo_selecionado.get())

    btn_voltar = tk.Button(tela_relatorios, text="Voltar", width=18, height=2, font=FONT_BOLD, bg=THEME['DANGER'], fg=THEME['TEXT'], relief="flat", command=tela_relatorios.destroy)
    btn_voltar.pack(pady=12)

def abrir_relatorios_pagamentos():
    tela_relatorios_pagamentos = tk.Toplevel(main_window)
    tela_relatorios_pagamentos.title("Relatório de Pagamentos")
    tela_relatorios_pagamentos.geometry("520x420")
    tela_relatorios_pagamentos.config(bg=THEME['BG'])

    lbl_titulo = tk.Label(tela_relatorios_pagamentos, text="Relatório por Forma de Pagamento", font=("Segoe UI", 16, "bold"), fg=THEME['TEXT'], bg=THEME['BG'])
    lbl_titulo.pack(pady=12)

    dados_pagamentos = defaultdict(lambda: {"quantidade_vendas": 0, "valor_total": 0.0})

    for venda in vendas_historico:
        forma = venda['forma_pagamento']
        total = venda['preco'] * venda['quantidade']
        dados_pagamentos[forma]['quantidade_vendas'] += 1
        dados_pagamentos[forma]['valor_total'] += total

    for forma, dados in dados_pagamentos.items():
        info_str = f"{forma}: {dados['quantidade_vendas']} vendas (Total: R${dados['valor_total']:.2f})".replace('.', ',')
        tk.Label(tela_relatorios_pagamentos, text=info_str, font=FONT, fg=THEME['TEXT'], bg=THEME['BG']).pack(pady=6)

    btn_voltar = tk.Button(tela_relatorios_pagamentos, text="Voltar", width=18, height=2, font=FONT_BOLD, bg=THEME['DANGER'], fg=THEME['TEXT'], relief="flat", command=tela_relatorios_pagamentos.destroy)
    btn_voltar.pack(pady=20)

def alternar_status_mesa(mesa_nome, tela):
    for mesa in mesas:
        if mesa['nome'] == mesa_nome:
            if mesa['status'] == "Ocupada":
                mesa['status'] = "Disponível"
                messagebox.showinfo("Mesa Liberada", f"{mesa_nome} foi liberada com sucesso!")
            elif mesa['status'] == "Reservada":
                mesa['status'] = "Disponível"
                mesa['reserva_nome'] = ""
                mesa['reserva_tel'] = ""
                messagebox.showinfo("Reserva Cancelada", f"A reserva de {mesa_nome} foi cancelada.")
            else:
                mesa['status'] = "Ocupada"
                messagebox.showinfo("Mesa Ocupada", f"{mesa_nome} foi ocupada com sucesso!")
            tela.destroy()
            abrir_mesas()
            return


def abrir_mesas():
    tela_mesas = tk.Toplevel(main_window)
    tela_mesas.title("Mesas")
    tela_mesas.geometry("700x520")
    tela_mesas.config(bg=THEME['BG'])

    frame_grid_mesas = tk.Frame(tela_mesas, bg=THEME['BG'])
    frame_grid_mesas.pack(pady=20, padx=20)

    def on_click(mesa):
        if mesa['comanda']:
            abrir_comanda_mesa(mesa)
        else:
            alternar_status_mesa(mesa['nome'], tela_mesas)

    for i, mesa in enumerate(mesas):
        if mesa['status'] == "Ocupada":
            cor_status = THEME['ACCENT_THIRD']
            texto_status = "Ocupada"
        elif mesa['status'] == "Disponível":
            cor_status = THEME['ACCENT_SUCCESS']
            texto_status = "Disponível"
        elif mesa['status'] == "Reservada":
            cor_status = THEME['ACCENT_PRIMARY']
            texto_status = "Reservada"

        mesa_card = tk.Frame(frame_grid_mesas, bg=THEME['CARD_BG'], relief="flat", bd=2)
        mesa_card.grid(row=i // 3, column=i % 3, padx=12, pady=12, ipadx=8, ipady=8)

        tk.Label(mesa_card, text=mesa['nome'], font=("Segoe UI", 14, "bold"), fg=THEME['TEXT'], bg=THEME['CARD_BG']).pack(pady=6, padx=12)
        tk.Label(mesa_card, text=texto_status, font=FONT, fg=cor_status, bg=THEME['CARD_BG']).pack(pady=4, padx=12)

        mesa_card.bind("<Button-1>", lambda event, m=mesa: on_click(m))
        for child in mesa_card.winfo_children():
            child.bind("<Button-1>", lambda event, m=mesa: on_click(m))

    btn_voltar = tk.Button(tela_mesas, text="Voltar", width=18, height=2, font=FONT_BOLD, bg=THEME['DANGER'], fg=THEME['TEXT'], relief="flat", command=tela_mesas.destroy)
    btn_voltar.pack(pady=16)

def abrir_reserva():
    tela_reserva = tk.Toplevel(main_window)
    tela_reserva.title("Reservar Mesa")
    tela_reserva.geometry("420x420")
    tela_reserva.config(bg=THEME['BG'])

    lbl_titulo = tk.Label(tela_reserva, text="Fazer uma Reserva", font=("Segoe UI", 16, "bold"), fg=THEME['TEXT'], bg=THEME['BG'])
    lbl_titulo.pack(pady=10)

    frame_reserva = tk.Frame(tela_reserva, bg=THEME['CARD_BG'], padx=12, pady=12)
    frame_reserva.pack(padx=16, pady=12, fill=tk.BOTH, expand=True)

    lbl_mesa = tk.Label(frame_reserva, text="Selecione a Mesa:", font=FONT, fg=THEME['TEXT'], bg=THEME['CARD_BG'])
    lbl_mesa.grid(row=0, column=0, pady=8, sticky='w')

    mesas_disponiveis = [m['nome'] for m in mesas if m['status'] == 'Disponível']
    if not mesas_disponiveis:
        tk.Label(frame_reserva, text="Nenhuma mesa disponível para reserva.", font=FONT, fg=THEME['TEXT'], bg=THEME['CARD_BG']).grid(row=1, column=0, columnspan=2, pady=10)
        combo_mesas = ttk.Combobox(frame_reserva, values=[], state='disabled', font=FONT)
    else:
        combo_mesas = ttk.Combobox(frame_reserva, values=mesas_disponiveis, state='readonly', font=FONT)
        combo_mesas.set(mesas_disponiveis[0])

    combo_mesas.grid(row=0, column=1, pady=8, padx=6)

    lbl_nome = tk.Label(frame_reserva, text="Nome do Cliente:", font=FONT, fg=THEME['TEXT'], bg=THEME['CARD_BG'])
    lbl_nome.grid(row=1, column=0, pady=8, sticky='w')
    entry_nome = tk.Entry(frame_reserva, font=FONT, bg=THEME['PAPER'], fg=THEME['TEXT'], relief="flat")
    entry_nome.grid(row=1, column=1, pady=8, padx=6)

    lbl_telefone = tk.Label(frame_reserva, text="Telefone:", font=FONT, fg=THEME['TEXT'], bg=THEME['CARD_BG'])
    lbl_telefone.grid(row=2, column=0, pady=8, sticky='w')
    entry_telefone = tk.Entry(frame_reserva, font=FONT, bg=THEME['PAPER'], fg=THEME['TEXT'], relief="flat")
    entry_telefone.grid(row=2, column=1, pady=8, padx=6)

    def fazer_reserva():
        mesa_selecionada = combo_mesas.get()
        nome_cliente = entry_nome.get()
        telefone_cliente = entry_telefone.get()

        if not mesa_selecionada or not nome_cliente or not telefone_cliente:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return

        for mesa in mesas:
            if mesa['nome'] == mesa_selecionada:
                if mesa['status'] == "Disponível":
                    mesa['status'] = "Reservada"
                    mesa['reserva_nome'] = nome_cliente
                    mesa['reserva_tel'] = telefone_cliente
                    messagebox.showinfo("Sucesso", f"Mesa {mesa_selecionada} reservada para {nome_cliente}.")
                    tela_reserva.destroy()
                    abrir_mesas()
                else:
                    messagebox.showerror("Erro", f"A mesa {mesa_selecionada} não está disponível para reserva.")
                return

    btn_reservar = tk.Button(tela_reserva, text="Confirmar Reserva", width=20, height=2, font=FONT_BOLD, bg=THEME['ACCENT_SUCCESS'], fg=THEME['TEXT'], relief="flat", command=fazer_reserva)
    btn_reservar.pack(pady=12)

    btn_voltar = tk.Button(tela_reserva, text="Voltar", width=18, height=2, font=FONT_BOLD, bg=THEME['DANGER'], fg=THEME['TEXT'], relief="flat", command=tela_reserva.destroy)
    btn_voltar.pack(pady=6)

def abrir_comanda_mesa(mesa):
    tela_comanda = tk.Toplevel(main_window)
    tela_comanda.title(f"Demanda - {mesa['nome']}")
    tela_comanda.geometry("640x720")
    tela_comanda.config(bg=THEME['BG'])

    frame_comanda = tk.Frame(tela_comanda, bg=THEME['BG'])
    frame_comanda.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    lbl_comanda = tk.Label(frame_comanda, text=f"Demanda da {mesa['nome']}", font=("Segoe UI", 16, "bold"), fg=THEME['TEXT'], bg=THEME['BG'])
    lbl_comanda.pack(pady=10)

    frame_pedidos = tk.LabelFrame(frame_comanda, text="Pedidos", font=("Segoe UI", 12, "bold"), fg=THEME['TEXT'], bg=THEME['CARD_BG'], bd=2, relief=tk.GROOVE)
    frame_pedidos.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    canvas_pedidos = tk.Canvas(frame_pedidos, bg=THEME['CARD_BG'], highlightthickness=0)
    scrollbar_pedidos = tk.Scrollbar(frame_pedidos, orient="vertical", command=canvas_pedidos.yview)
    scrollable_pedidos_frame = tk.Frame(canvas_pedidos, bg=THEME['CARD_BG'])

    scrollable_pedidos_frame.bind(
        "<Configure>",
        lambda e: canvas_pedidos.configure(
            scrollregion=canvas_pedidos.bbox("all")
        )
    )

    canvas_pedidos.create_window((0, 0), window=scrollable_pedidos_frame, anchor="nw")
    canvas_pedidos.configure(yscrollcommand=scrollbar_pedidos.set)

    canvas_pedidos.pack(side="left", fill="both", expand=True)
    scrollbar_pedidos.pack(side="right", fill="y")

    total_comanda = 0.0

    def atualizar_lista_pedidos():
        nonlocal total_comanda
        for widget in scrollable_pedidos_frame.winfo_children():
            widget.destroy()

        total_comanda = 0.0
        if not mesa['comanda']:
            tk.Label(scrollable_pedidos_frame, text="Nenhum pedido adicionado.", font=FONT, fg=THEME['TEXT'], bg=THEME['CARD_BG']).pack(pady=8)
        else:
            for i, pedido in enumerate(mesa['comanda']):
                preco_total_pedido = pedido['preço'] * pedido['quantidade']
                total_comanda += preco_total_pedido
                pedido_info = f"{pedido['quantidade']}x {pedido['nome']} - R${pedido['preço']:.2f} (Total: R${preco_total_pedido:.2f})".replace('.', ',')
                tk.Label(scrollable_pedidos_frame, text=pedido_info, font=FONT, fg=THEME['TEXT'], bg=THEME['CARD_BG'], anchor='w').pack(fill=tk.X, padx=6, pady=4)

        lbl_total.config(text=f"Total da Demanda: R${total_comanda:.2f}".replace('.', ','))

    def adicionar_pedido():
        produto_selecionado = combo_produtos.get()
        quantidade_str = entry_quantidade.get()

        if not produto_selecionado or not quantidade_str:
            messagebox.showerror("Erro", "Selecione um produto e informe a quantidade.")
            return

        try:
            quantidade = int(quantidade_str)
            if quantidade <= 0:
                messagebox.showerror("Erro", "A quantidade deve ser um número positivo.")
                return
        except ValueError:
            messagebox.showerror("Erro", "A quantidade deve ser um número válido.")
            return

        produto_encontrado = None
        for p in produtos_estoque:
            if p['nome'] == produto_selecionado:
                produto_encontrado = p
                break

        if produto_encontrado:
            if produto_encontrado['quantidade'] >= quantidade:
                novo_pedido = {
                    "nome": produto_encontrado['nome'],
                    "preço": produto_encontrado['preço'],
                    "quantidade": quantidade
                }
                mesa['comanda'].append(novo_pedido)
                produto_encontrado['quantidade'] -= quantidade
                atualizar_lista_pedidos()
                messagebox.showinfo("Sucesso", f"{quantidade}x {produto_encontrado['nome']} adicionado à demanda.")
                entry_quantidade.delete(0, tk.END)
                combo_produtos.set('')
            else:
                messagebox.showerror("Erro", f"Estoque insuficiente para {produto_encontrado['nome']}. Disponível: {produto_encontrado['quantidade']}.")
        else:
            messagebox.showerror("Erro", "Produto não encontrado.")

    def finalizar_comanda():
        if not mesa['comanda']:
            messagebox.showwarning("Aviso", "A demanda está vazia. Adicione pedidos antes de finalizar.")
            return

        def registrar_pagamento(forma_pagamento):
            hoje = datetime.now().strftime("%Y-%m-%d")
            total_venda = 0.0

            for pedido in mesa['comanda']:
                total_venda += pedido['preço'] * pedido['quantidade']
                vendas_historico.append({
                    "data": hoje,
                    "produto": pedido['nome'],
                    "preco": pedido['preço'],
                    "quantidade": pedido['quantidade'],
                    "forma_pagamento": forma_pagamento
                })

            mesa['comanda'] = []
            mesa['status'] = "Disponível"

            messagebox.showinfo("Sucesso", f"Demanda de {mesa['nome']} finalizada. Total: R${total_venda:.2f} pagos com {forma_pagamento}.".replace('.', ','))
            tela_comanda.destroy()
            abrir_comandas()

        tela_pagamento = tk.Toplevel(tela_comanda)
        tela_pagamento.title("Finalizar Pagamento")
        tela_pagamento.geometry("320x260")
        tela_pagamento.config(bg=THEME['BG'])

        lbl_total_final = tk.Label(tela_pagamento, text=f"Total a pagar: R${total_comanda:.2f}".replace('.', ','), font=("Segoe UI", 14, "bold"), fg=THEME['TEXT'], bg=THEME['BG'])
        lbl_total_final.pack(pady=12)

        lbl_pagamento = tk.Label(tela_pagamento, text="Selecione a forma de pagamento:", font=FONT, fg=THEME['TEXT'], bg=THEME['BG'])
        lbl_pagamento.pack(pady=8)

        btn_dinheiro = tk.Button(tela_pagamento, text="Dinheiro", font=FONT, bg=THEME['CARD_BG'], fg=THEME['TEXT'], relief="flat", command=lambda: registrar_pagamento("Dinheiro"))
        btn_dinheiro.pack(pady=6, ipadx=10)

        btn_cartao = tk.Button(tela_pagamento, text="Cartão", font=FONT, bg=THEME['CARD_BG'], fg=THEME['TEXT'], relief="flat", command=lambda: registrar_pagamento("Cartão"))
        btn_cartao.pack(pady=6, ipadx=10)

        btn_pix = tk.Button(tela_pagamento, text="Pix", font=FONT, bg=THEME['CARD_BG'], fg=THEME['TEXT'], relief="flat", command=lambda: registrar_pagamento("Pix"))
        btn_pix.pack(pady=6, ipadx=10)

    frame_add_pedido = tk.LabelFrame(frame_comanda, text="Adicionar Pedido", font=("Segoe UI", 12, "bold"), fg=THEME['TEXT'], bg=THEME['CARD_BG'], bd=2, relief=tk.GROOVE)
    frame_add_pedido.pack(fill=tk.X, padx=10, pady=8)

    lbl_produto = tk.Label(frame_add_pedido, text="Produto:", font=FONT, fg=THEME['TEXT'], bg=THEME['CARD_BG'])
    lbl_produto.grid(row=0, column=0, padx=6, pady=6)

    produtos_nomes = [p['nome'] for p in produtos_estoque]
    combo_produtos = ttk.Combobox(frame_add_pedido, values=produtos_nomes, font=FONT, state='readonly')
    combo_produtos.grid(row=0, column=1, padx=6, pady=6)

    lbl_quantidade = tk.Label(frame_add_pedido, text="Quantidade:", font=FONT, fg=THEME['TEXT'], bg=THEME['CARD_BG'])
    lbl_quantidade.grid(row=1, column=0, padx=6, pady=6)

    entry_quantidade = tk.Entry(frame_add_pedido, font=FONT, bg=THEME['PAPER'], fg=THEME['TEXT'], relief="flat")
    entry_quantidade.grid(row=1, column=1, padx=6, pady=6)

    btn_adicionar = tk.Button(frame_add_pedido, text="Adicionar", font=("Segoe UI", 10, "bold"), bg=THEME['ACCENT_SUCCESS'], fg=THEME['TEXT'], relief="flat", command=adicionar_pedido)
    btn_adicionar.grid(row=2, column=0, columnspan=2, pady=8)

    lbl_total = tk.Label(frame_comanda, text="Total da Demanda: R$0,00", font=("Segoe UI", 14, "bold"), fg=THEME['TEXT'], bg=THEME['BG'])
    lbl_total.pack(pady=10)

    frame_botoes_comanda = tk.Frame(tela_comanda, bg=THEME['BG'])
    frame_botoes_comanda.pack(pady=8, padx=10, fill=tk.X)

    btn_finalizar = tk.Button(frame_botoes_comanda, text="Finalizar Demanda", width=18, height=2, font=FONT_BOLD, bg=THEME['ACCENT_SUCCESS'], fg=THEME['TEXT'], relief="flat", command=finalizar_comanda)
    btn_finalizar.pack(side=tk.LEFT, padx=10, expand=True)

    btn_voltar = tk.Button(frame_botoes_comanda, text="Voltar", width=18, height=2, font=FONT_BOLD, bg=THEME['DANGER'], fg=THEME['TEXT'], relief="flat", command=tela_comanda.destroy)
    btn_voltar.pack(side=tk.RIGHT, padx=10, expand=True)

    atualizar_lista_pedidos()

def abrir_comandas():
    tela_comandas = tk.Toplevel(main_window)
    tela_comandas.title("Demandas")
    tela_comandas.geometry("480x520")
    tela_comandas.config(bg=THEME['BG'])

    lbl_comandas = tk.Label(tela_comandas, text="Demandas por Mesa", font=("Segoe UI", 14, "bold"), fg=THEME['TEXT'], bg=THEME['BG'])
    lbl_comandas.pack(pady=12)

    for mesa in mesas:
        status = "Aberta" if mesa['comanda'] else "Disponível"
        cor = "#FFC107" if status == "Aberta" else THEME['ACCENT_SUCCESS']
        btn_comanda = tk.Button(tela_comandas, text=f"{mesa['nome']} - Status: {status} (Ver Demanda)", width=36, height=2, font=FONT, bg=THEME['CARD_BG'], fg=cor, relief="flat",
                                 command=lambda m=mesa: abrir_comanda_mesa(m))
        btn_comanda.pack(pady=6)

    btn_voltar = tk.Button(tela_comandas, text="Voltar", width=18, height=2, font=FONT_BOLD, bg=THEME['DANGER'], fg=THEME['TEXT'], relief="flat", command=tela_comandas.destroy)
    btn_voltar.pack(pady=12)

def abrir_caixa():
    tela_caixa = tk.Toplevel(main_window)
    tela_caixa.title("Caixa")
    tela_caixa.geometry("520x420")
    tela_caixa.config(bg=THEME['BG'])

    lbl_caixa = tk.Label(tela_caixa, text="Status das Vendas por Mesa", font=("Segoe UI", 14, "bold"), fg=THEME['TEXT'], bg=THEME['BG'])
    lbl_caixa.pack(pady=12)

    vendas_caixa = [
        {"mesa": "Mesa 1", "status": "Confirmada"},
        {"mesa": "Mesa 2", "status": "Pendente"},
        {"mesa": "Mesa 3", "status": "Confirmada"},
        {"mesa": "Mesa 4", "status": "Pendente"},
        {"mesa": "Mesa 5", "status": "Confirmada"},
        {"mesa": "Mesa 6", "status": "Pendente"},
    ]

    status_cores_caixa = {"Confirmada": THEME['ACCENT_SUCCESS'], "Pendente": "#FFC107"}

    for venda in vendas_caixa:
        cor = status_cores_caixa[venda["status"]]
        venda_info = f"{venda['mesa']} - Venda: {venda['status']}"
        tk.Label(tela_caixa, text=venda_info, font=FONT, fg=cor, bg=THEME['BG']).pack(pady=6)

    btn_voltar = tk.Button(tela_caixa, text="Voltar", width=18, height=2, font=FONT_BOLD, bg=THEME['DANGER'], fg=THEME['TEXT'], relief="flat", command=tela_caixa.destroy)
    btn_voltar.pack(pady=16)

def iniciar_app():
    global login_window, entry_username, entry_password, logo_image_tk
    
    try:
        img_raw = Image.open("logo.png")
        img_resized = img_raw.resize((150, 150), Image.LANCZOS)
        logo_image_tk = ImageTk.PhotoImage(img_resized)
    except FileNotFoundError:
        messagebox.showerror("Erro de Arquivo", "Arquivo 'logo.jpg' não encontrado. Certifique-se de que ele está na mesma pasta que o script.")
        return
    except ImportError:
        messagebox.showerror("Erro de Biblioteca", "A biblioteca 'Pillow' (PIL) não está instalada. Instale com 'pip install Pillow'.")
        return
    except Exception as e:
        messagebox.showerror("Erro de Imagem", f"Não foi possível carregar a imagem: {e}")
        return

    login_window = tk.Tk()
    login_window.title("Login Cobra Demandas")
    login_window.geometry("420x520")
    login_window.config(bg=THEME['BG'])

    lbl_logo = tk.Label(login_window, image=logo_image_tk, bg=THEME['BG'])
    lbl_logo.pack(pady=10)

    lbl_title_login = tk.Label(login_window, text="COBRA DEMANDAS", font=("Segoe UI", 18, "bold"), fg=THEME['TEXT'], bg=THEME['BG'])
    lbl_title_login.pack(pady=5)
    
    frame_login_card = tk.Frame(login_window, bg=THEME['CARD_BG'], padx=20, pady=20, relief="flat")
    frame_login_card.pack(pady=10)

    lbl_username = tk.Label(frame_login_card, text="Usuário:", font=FONT_BOLD, fg=THEME['TEXT'], bg=THEME['CARD_BG'])
    lbl_username.pack(pady=6, anchor='w')
    entry_username = tk.Entry(frame_login_card, font=FONT, bg=THEME['PAPER'], fg=THEME['TEXT'], relief="flat", width=30)
    entry_username.pack(pady=6)

    lbl_password = tk.Label(frame_login_card, text="Senha:", font=FONT_BOLD, fg=THEME['TEXT'], bg=THEME['CARD_BG'])
    lbl_password.pack(pady=6, anchor='w')
    entry_password = tk.Entry(frame_login_card, show="*", font=FONT, bg=THEME['PAPER'], fg=THEME['TEXT'], relief="flat", width=30)
    entry_password.pack(pady=6)

    entry_username.bind("<Return>", lambda event: login())
    entry_password.bind("<Return>", lambda event: login())

    btn_login = tk.Button(login_window, text="Entrar", width=18, height=2, font=FONT_BOLD, bg=THEME['ACCENT_SUCCESS'], fg=THEME['TEXT'], relief="flat", command=login)
    btn_login.pack(pady=10)

    btn_sair = tk.Button(login_window, text="Sair", width=18, height=2, font=FONT_BOLD, bg=THEME['DANGER'], fg=THEME['TEXT'], relief="flat", command=login_window.destroy)
    btn_sair.pack(pady=4)

    login_window.mainloop()

if __name__ == "__main__":
    iniciar_app()
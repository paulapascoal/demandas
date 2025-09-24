import tkinter as tk
from tkinter import messagebox, ttk
import random
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict
import locale
import platform

try:
    if platform.system() == 'Windows':
        locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil')
    else:
        locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
except locale.Error:
    messagebox.showwarning("Aviso de Localização", "Não foi possível definir o local para português. Nomes de dias e meses podem aparecer em inglês.")

vendas_historico = []

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

    for i in range(1, 8):
        data_passada = hoje - timedelta(days=i)
        for _ in range(random.randint(3, 10)):
            produto = random.choice(produtos)
            vendas_historico.append({
                "data": data_passada.strftime("%Y-%m-%d"),
                "produto": produto,
                "preco": precos[produtos.index(produto)],
                "quantidade": random.randint(1, 2),
                "forma_pagamento": random.choice(formas_pagamento)
            })

    for i in range(8, 31):
        data_passada = hoje - timedelta(days=i)
        for _ in range(random.randint(2, 8)):
            produto = random.choice(produtos)
            vendas_historico.append({
                "data": data_passada.strftime("%Y-%m-%d"),
                "produto": produto,
                "preco": precos[produtos.index(produto)],
                "quantidade": random.randint(1, 2),
                "forma_pagamento": random.choice(formas_pagamento)
            })

    for i in range(31, 91):
        data_passada = hoje - timedelta(days=i)
        for _ in range(random.randint(1, 5)):
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

def login():
    username = entry_username.get()
    password = entry_password.get()
    if username == "admin" and password == "1234":
        messagebox.showinfo("Login", "Login bem-sucedido!")
        login_window.destroy()
        abrir_tela_principal()
    else:
        messagebox.showerror("Erro", "Credenciais inválidas!")

def abrir_tela_principal():
    global main_window
    main_window = tk.Tk()
    main_window.title("Sistema PDV Restaurante")
    main_window.geometry("800x600")
    main_window.config(bg="#1E1E1E")
    
    frame_menu = tk.Frame(main_window, bg="#1E1E1E")
    frame_menu.pack(pady=50)

    btn_estoque = tk.Button(frame_menu, text="Estoque de Produtos", width=20, height=4,
                             font=("Segoe UI", 12), bg="#2D2D30", fg="#F0F0F0", relief="flat", command=abrir_estoque)
    btn_estoque.grid(row=0, column=0, padx=10, pady=10)
    btn_mesas = tk.Button(frame_menu, text="Mesas", width=20, height=4, font=("Segoe UI",
                                                                                 12), bg="#2D2D30", fg="#F0F0F0", relief="flat", command=abrir_mesas)
    btn_mesas.grid(row=0, column=1, padx=10, pady=10)
    btn_reservar_mesa = tk.Button(frame_menu, text="Reservar Mesa", width=20, height=4, font=(
        "Segoe UI", 12), bg="#2D2D30", fg="#F0F0F0", relief="flat", command=abrir_reserva)
    btn_reservar_mesa.grid(row=0, column=2, padx=10, pady=10)
    btn_comandas = tk.Button(frame_menu, text="Comandas", width=20, height=4, font=(
        "Segoe UI", 12), bg="#2D2D30", fg="#F0F0F0", relief="flat", command=abrir_comandas)
    btn_comandas.grid(row=1, column=0, padx=10, pady=10)
    btn_caixa = tk.Button(frame_menu, text="Caixa", width=20, height=4, font=("Segoe UI",
                                                                                 12), bg="#2D2D30", fg="#F0F0F0", relief="flat", command=abrir_caixa)
    btn_caixa.grid(row=1, column=1, padx=10, pady=10)
    btn_relatorios = tk.Button(frame_menu, text="Relatórios de Vendas", width=20, height=4, font=(
        "Segoe UI", 12), bg="#2D2D30", fg="#F0F0F0", relief="flat", command=abrir_relatorios)
    btn_relatorios.grid(row=1, column=2, padx=10, pady=10)
    btn_relatorios_pagamentos = tk.Button(frame_menu, text="Relatório de Pagamentos", width=20, height=4, font=(
        "Segoe UI", 12), bg="#2D2D30", fg="#F0F0F0", relief="flat", command=abrir_relatorios_pagamentos)
    btn_relatorios_pagamentos.grid(row=2, column=1, padx=10, pady=10)

    btn_sair = tk.Button(main_window, text="Sair", width=25, height=2, font=("Segoe UI", 12),
                          bg="#E53935", fg="#FFFFFF", relief="flat", command=main_window.destroy)
    btn_sair.pack(pady=30)
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
    tela_estoque.geometry("650x550")
    tela_estoque.config(bg="#1E1E1E")
    
    canvas = tk.Canvas(tela_estoque, bg="#1E1E1E")
    scrollbar = tk.Scrollbar(tela_estoque, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#1E1E1E")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    tk.Label(scrollable_frame, text="Produto", font=("Segoe UI", 12, "bold"), fg="#F0F0F0", bg="#1E1E1E", width=20, anchor='w').grid(row=0, column=0, padx=5)
    tk.Label(scrollable_frame, text="Preço", font=("Segoe UI", 12, "bold"), fg="#F0F0F0", bg="#1E1E1E", width=8, anchor='w').grid(row=0, column=1, padx=5)
    tk.Label(scrollable_frame, text="Quantidade", font=("Segoe UI", 12, "bold"), fg="#F0F0F0", bg="#1E1E1E", width=12, anchor='w').grid(row=0, column=2, padx=5)
    tk.Label(scrollable_frame, text="Validade", font=("Segoe UI", 12, "bold"), fg="#F0F0F0", bg="#1E1E1E", width=12, anchor='w').grid(row=0, column=3, padx=5)
    tk.Label(scrollable_frame, text="", font=("Segoe UI", 12, "bold"), fg="#F0F0F0", bg="#1E1E1E", width=10).grid(row=0, column=4, padx=5)

    for i, produto in enumerate(produtos_estoque):
        preco_formatado = f"R${produto['preço']:.2f}".replace('.', ',')
        
        tk.Label(scrollable_frame, text=produto['nome'], font=("Segoe UI", 12), fg="#F0F0F0", bg="#1E1E1E", width=20, anchor='w').grid(row=i+1, column=0, pady=5, padx=5)
        tk.Label(scrollable_frame, text=preco_formatado, font=("Segoe UI", 12), fg="#F0F0F0", bg="#1E1E1E", width=8, anchor='w').grid(row=i+1, column=1, pady=5, padx=5)

        quantidade_entry = tk.Entry(scrollable_frame, font=("Segoe UI", 12), bg="#2D2D30", fg="#F0F0F0", width=10, relief="flat")
        quantidade_entry.insert(0, str(produto['quantidade']))
        quantidade_entry.grid(row=i+1, column=2, pady=5, padx=5)
        
        validade_entry = tk.Entry(scrollable_frame, font=("Segoe UI", 12), bg="#2D2D30", fg="#F0F0F0", width=12, relief="flat")
        validade_entry.insert(0, produto['validade'])
        validade_entry.grid(row=i+1, column=3, pady=5, padx=5)

        btn_salvar = tk.Button(scrollable_frame, text="Salvar", font=("Segoe UI", 10), bg="#4CAF50", fg="#FFFFFF", relief="flat", command=lambda p=produto, q=quantidade_entry, v=validade_entry, t=tela_estoque: salvar_alteracoes_estoque(p, q, v, t))
        btn_salvar.grid(row=i+1, column=4, pady=5, padx=5)

    btn_voltar = tk.Button(tela_estoque, text="Voltar", width=20, height=2, font=("Segoe UI", 12), bg="#E53935", fg="#FFFFFF", relief="flat", command=tela_estoque.destroy)
    btn_voltar.pack(pady=20)


def abrir_relatorios():
    tela_relatorios = tk.Toplevel(main_window)
    tela_relatorios.title("Relatórios de Vendas")
    tela_relatorios.geometry("800x600")
    tela_relatorios.config(bg="#1E1E1E")

    lbl_titulo = tk.Label(tela_relatorios, text="Relatórios de Vendas", font=("Segoe UI", 16, "bold"), fg="#F0F0F0", bg="#1E1E1E")
    lbl_titulo.pack(pady=10)

    frame_grafico = tk.Frame(tela_relatorios, bg="#1E1E1E")
    frame_grafico.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    opcoes_periodo = ["Diário", "Semanal", "Mensal", "Trimestral"]
    periodo_selecionado = tk.StringVar()
    periodo_selecionado.set("Semanal")

    combobox_periodo = ttk.Combobox(tela_relatorios, textvariable=periodo_selecionado, values=opcoes_periodo, font=("Segoe UI", 12))
    combobox_periodo.pack(pady=10)

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
            return {}, "", ""

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
        return labels, valores, periodo

    def criar_e_exibir_grafico(frame_grafico, periodo):
        for widget in frame_grafico.winfo_children():
            widget.destroy()
        
        labels, valores, titulo = gerar_dados_grafico(periodo)
        
        if not labels:
            tk.Label(frame_grafico, text="Nenhum dado de venda para o período.", bg="#1E1E1E", fg="#F0F0F0").pack(pady=20)
            return

        fig = plt.figure(figsize=(5, 4), dpi=100, facecolor='#1E1E1E')
        ax = fig.add_subplot(111)
        
        ax.bar(labels, valores, color='#007ACC')
        ax.set_title(f"Vendas - Período {titulo}", color="#F0F0F0")
        ax.set_ylabel("Receita (R$)", color="#F0F0F0")
        ax.set_xlabel("Período", color="#F0F0F0")
        ax.tick_params(axis='x', rotation=45, colors="#F0F0F0")
        ax.tick_params(axis='y', colors="#F0F0F0")
        ax.set_facecolor("#2D2D30")
        fig.patch.set_facecolor('#1E1E1E')
        ax.spines['bottom'].set_color('#F0F0F0')
        ax.spines['left'].set_color('#F0F0F0')
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
    
    btn_voltar = tk.Button(tela_relatorios, text="Voltar", width=20, height=2, font=("Segoe UI", 12), bg="#E53935", fg="#FFFFFF", relief="flat", command=tela_relatorios.destroy)
    btn_voltar.pack(pady=20)

def abrir_relatorios_pagamentos():
    tela_relatorios_pagamentos = tk.Toplevel(main_window)
    tela_relatorios_pagamentos.title("Relatório de Pagamentos")
    tela_relatorios_pagamentos.geometry("500x400")
    tela_relatorios_pagamentos.config(bg="#1E1E1E")

    lbl_titulo = tk.Label(tela_relatorios_pagamentos, text="Relatório por Forma de Pagamento", font=("Segoe UI", 16, "bold"), fg="#F0F0F0", bg="#1E1E1E")
    lbl_titulo.pack(pady=20)
    
    dados_pagamentos = defaultdict(lambda: {"quantidade_vendas": 0, "valor_total": 0.0})

    for venda in vendas_historico:
        forma = venda['forma_pagamento']
        total = venda['preco'] * venda['quantidade']
        dados_pagamentos[forma]['quantidade_vendas'] += 1
        dados_pagamentos[forma]['valor_total'] += total

    for forma, dados in dados_pagamentos.items():
        info_str = f"{forma}: {dados['quantidade_vendas']} vendas (Total: R${dados['valor_total']:.2f})".replace('.', ',')
        tk.Label(tela_relatorios_pagamentos, text=info_str, font=("Segoe UI", 14), fg="#F0F0F0", bg="#1E1E1E").pack(pady=5)
    
    btn_voltar = tk.Button(tela_relatorios_pagamentos, text="Voltar", width=20, height=2, font=("Segoe UI", 12), bg="#E53935", fg="#FFFFFF", relief="flat", command=tela_relatorios_pagamentos.destroy)
    btn_voltar.pack(pady=40)

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
    tela_mesas.geometry("600x400")
    tela_mesas.config(bg="#1E1E1E")

    frame_grid_mesas = tk.Frame(tela_mesas, bg="#1E1E1E")
    frame_grid_mesas.pack(pady=20, padx=20)
    
    def on_click(mesa):
        if mesa['comanda']:
            abrir_comanda_mesa(mesa)
        else:
            alternar_status_mesa(mesa['nome'], tela_mesas)

    for i, mesa in enumerate(mesas):
        if mesa['status'] == "Ocupada":
            cor_status = "#FF5722"
            texto_status = "Ocupada"
        elif mesa['status'] == "Disponível":
            cor_status = "#4CAF50"
            texto_status = "Disponível"
        elif mesa['status'] == "Reservada":
            cor_status = "#2196F3"
            texto_status = "Reservada"

        mesa_card = tk.Frame(frame_grid_mesas, bg="#2D2D30", relief="flat", bd=2)
        mesa_card.grid(row=i // 3, column=i % 3, padx=10, pady=10)

        tk.Label(mesa_card, text=mesa['nome'], font=("Segoe UI", 14, "bold"), fg="#F0F0F0", bg="#2D2D30").pack(pady=5, padx=10)
        tk.Label(mesa_card, text=texto_status, font=("Segoe UI", 12), fg=cor_status, bg="#2D2D30").pack(pady=5, padx=10)
        
        mesa_card.bind("<Button-1>", lambda event, m=mesa: on_click(m))
        for child in mesa_card.winfo_children():
            child.bind("<Button-1>", lambda event, m=mesa: on_click(m))

    btn_voltar = tk.Button(tela_mesas, text="Voltar", width=20, height=2, font=("Segoe UI", 12), bg="#E53935", fg="#FFFFFF", relief="flat", command=tela_mesas.destroy)
    btn_voltar.pack(pady=20)

def abrir_reserva():
    tela_reserva = tk.Toplevel(main_window)
    tela_reserva.title("Reservar Mesa")
    tela_reserva.geometry("400x400")
    tela_reserva.config(bg="#1E1E1E")

    lbl_titulo = tk.Label(tela_reserva, text="Fazer uma Reserva", font=("Segoe UI", 16, "bold"), fg="#F0F0F0", bg="#1E1E1E")
    lbl_titulo.pack(pady=10)

    frame_reserva = tk.Frame(tela_reserva, bg="#1E1E1E")
    frame_reserva.pack(padx=20, pady=20)

    lbl_mesa = tk.Label(frame_reserva, text="Selecione a Mesa:", font=("Segoe UI", 12), fg="#F0F0F0", bg="#1E1E1E")
    lbl_mesa.grid(row=0, column=0, pady=5, sticky='w')

    mesas_disponiveis = [m['nome'] for m in mesas if m['status'] == 'Disponível']
    if not mesas_disponiveis:
        tk.Label(frame_reserva, text="Nenhuma mesa disponível para reserva.", font=("Segoe UI", 12), fg="#F0F0F0", bg="#1E1E1E").grid(row=1, column=0, columnspan=2, pady=10)
        combo_mesas = ttk.Combobox(frame_reserva, values=[], state='disabled', font=("Segoe UI", 12))
    else:
        combo_mesas = ttk.Combobox(frame_reserva, values=mesas_disponiveis, state='readonly', font=("Segoe UI", 12))
        combo_mesas.set(mesas_disponiveis[0])
    
    combo_mesas.grid(row=0, column=1, pady=5)

    lbl_nome = tk.Label(frame_reserva, text="Nome do Cliente:", font=("Segoe UI", 12), fg="#F0F0F0", bg="#1E1E1E")
    lbl_nome.grid(row=1, column=0, pady=5, sticky='w')
    entry_nome = tk.Entry(frame_reserva, font=("Segoe UI", 12), bg="#2D2D30", fg="#F0F0F0", relief="flat")
    entry_nome.grid(row=1, column=1, pady=5)

    lbl_telefone = tk.Label(frame_reserva, text="Telefone:", font=("Segoe UI", 12), fg="#F0F0F0", bg="#1E1E1E")
    lbl_telefone.grid(row=2, column=0, pady=5, sticky='w')
    entry_telefone = tk.Entry(frame_reserva, font=("Segoe UI", 12), bg="#2D2D30", fg="#F0F0F0", relief="flat")
    entry_telefone.grid(row=2, column=1, pady=5)
    
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

    btn_reservar = tk.Button(tela_reserva, text="Confirmar Reserva", width=20, height=2, font=(
        "Segoe UI", 12), bg="#4CAF50", fg="#FFFFFF", relief="flat", command=fazer_reserva)
    btn_reservar.pack(pady=20)
    
    btn_voltar = tk.Button(tela_reserva, text="Voltar", width=20, height=2, font=(
        "Segoe UI", 12), bg="#E53935", fg="#FFFFFF", relief="flat", command=tela_reserva.destroy)
    btn_voltar.pack(pady=10)
    
def abrir_comanda_mesa(mesa):
    tela_comanda = tk.Toplevel(main_window)
    tela_comanda.title(f"Comanda - {mesa['nome']}")
    tela_comanda.geometry("600x600")
    tela_comanda.config(bg="#1E1E1E")
    
    frame_comanda = tk.Frame(tela_comanda, bg="#1E1E1E")
    frame_comanda.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    lbl_comanda = tk.Label(frame_comanda, text=f"Comanda da {mesa['nome']}", font=("Segoe UI", 16, "bold"), fg="#F0F0F0", bg="#1E1E1E")
    lbl_comanda.pack(pady=10)

    frame_pedidos = tk.LabelFrame(frame_comanda, text="Pedidos", font=("Segoe UI", 12, "bold"), fg="#F0F0F0", bg="#2D2D30", bd=2, relief=tk.GROOVE)
    frame_pedidos.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    canvas_pedidos = tk.Canvas(frame_pedidos, bg="#2D2D30")
    scrollbar_pedidos = tk.Scrollbar(frame_pedidos, orient="vertical", command=canvas_pedidos.yview)
    scrollable_pedidos_frame = tk.Frame(canvas_pedidos, bg="#2D2D30")
    
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
            tk.Label(scrollable_pedidos_frame, text="Nenhum pedido adicionado.", font=("Segoe UI", 12), fg="#F0F0F0", bg="#2D2D30").pack(pady=5)
        else:
            for i, pedido in enumerate(mesa['comanda']):
                preco_total_pedido = pedido['preço'] * pedido['quantidade']
                total_comanda += preco_total_pedido
                pedido_info = f"{pedido['quantidade']}x {pedido['nome']} - R${pedido['preço']:.2f} (Total: R${preco_total_pedido:.2f})".replace('.', ',')
                tk.Label(scrollable_pedidos_frame, text=pedido_info, font=("Segoe UI", 12), fg="#F0F0F0", bg="#2D2D30", anchor='w').pack(fill=tk.X, padx=5, pady=2)
        
        lbl_total.config(text=f"Total da Comanda: R${total_comanda:.2f}".replace('.', ','))
        
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
                messagebox.showinfo("Sucesso", f"{quantidade}x {produto_encontrado['nome']} adicionado à comanda.")
                entry_quantidade.delete(0, tk.END)
                combo_produtos.set('')
            else:
                messagebox.showerror("Erro", f"Estoque insuficiente para {produto_encontrado['nome']}. Disponível: {produto_encontrado['quantidade']}.")
        else:
            messagebox.showerror("Erro", "Produto não encontrado.")
    
    def finalizar_comanda():
        if not mesa['comanda']:
            messagebox.showwarning("Aviso", "A comanda está vazia. Adicione pedidos antes de finalizar.")
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
            
            messagebox.showinfo("Sucesso", f"Comanda de {mesa['nome']} finalizada. Total: R${total_venda:.2f} pagos com {forma_pagamento}.".replace('.', ','))
            tela_comanda.destroy()
            abrir_comandas()
        
        tela_pagamento = tk.Toplevel(tela_comanda)
        tela_pagamento.title("Finalizar Pagamento")
        tela_pagamento.geometry("300x250")
        tela_pagamento.config(bg="#1E1E1E")
        
        lbl_total_final = tk.Label(tela_pagamento, text=f"Total a pagar: R${total_comanda:.2f}".replace('.', ','), font=("Segoe UI", 14, "bold"), fg="#F0F0F0", bg="#1E1E1E")
        lbl_total_final.pack(pady=10)
        
        lbl_pagamento = tk.Label(tela_pagamento, text="Selecione a forma de pagamento:", font=("Segoe UI", 12), fg="#F0F0F0", bg="#1E1E1E")
        lbl_pagamento.pack(pady=10)
        
        btn_dinheiro = tk.Button(tela_pagamento, text="Dinheiro", font=("Segoe UI", 12), bg="#2D2D30", fg="#FFFFFF", relief="flat", command=lambda: registrar_pagamento("Dinheiro"))
        btn_dinheiro.pack(pady=5)
        
        btn_cartao = tk.Button(tela_pagamento, text="Cartão", font=("Segoe UI", 12), bg="#2D2D30", fg="#FFFFFF", relief="flat", command=lambda: registrar_pagamento("Cartão"))
        btn_cartao.pack(pady=5)
        
        btn_pix = tk.Button(tela_pagamento, text="Pix", font=("Segoe UI", 12), bg="#2D2D30", fg="#FFFFFF", relief="flat", command=lambda: registrar_pagamento("Pix"))
        btn_pix.pack(pady=5)
        
    frame_add_pedido = tk.LabelFrame(frame_comanda, text="Adicionar Pedido", font=("Segoe UI", 12, "bold"), fg="#F0F0F0", bg="#2D2D30", bd=2, relief=tk.GROOVE)
    frame_add_pedido.pack(fill=tk.X, padx=10, pady=10)
    
    lbl_produto = tk.Label(frame_add_pedido, text="Produto:", font=("Segoe UI", 12), fg="#F0F0F0", bg="#2D2D30")
    lbl_produto.grid(row=0, column=0, padx=5, pady=5)
    
    produtos_nomes = [p['nome'] for p in produtos_estoque]
    combo_produtos = ttk.Combobox(frame_add_pedido, values=produtos_nomes, font=("Segoe UI", 12), state='readonly')
    combo_produtos.grid(row=0, column=1, padx=5, pady=5)

    lbl_quantidade = tk.Label(frame_add_pedido, text="Quantidade:", font=("Segoe UI", 12), fg="#F0F0F0", bg="#2D2D30")
    lbl_quantidade.grid(row=1, column=0, padx=5, pady=5)
    
    entry_quantidade = tk.Entry(frame_add_pedido, font=("Segoe UI", 12), bg="#1E1E1E", fg="#F0F0F0", relief="flat")
    entry_quantidade.grid(row=1, column=1, padx=5, pady=5)
    
    btn_adicionar = tk.Button(frame_add_pedido, text="Adicionar", font=("Segoe UI", 10), bg="#4CAF50", fg="#FFFFFF", relief="flat", command=adicionar_pedido)
    btn_adicionar.grid(row=2, column=0, columnspan=2, pady=10)

    lbl_total = tk.Label(frame_comanda, text="Total da Comanda: R$0,00", font=("Segoe UI", 14, "bold"), fg="#F0F0F0", bg="#1E1E1E")
    lbl_total.pack(pady=10)

    frame_botoes_comanda = tk.Frame(tela_comanda, bg="#1E1E1E")
    frame_botoes_comanda.pack(pady=10, padx=10, fill=tk.X)
    
    btn_finalizar = tk.Button(frame_botoes_comanda, text="Finalizar Comanda", width=20, height=2, font=("Segoe UI", 12), bg="#4CAF50", fg="#FFFFFF", relief="flat", command=finalizar_comanda)
    btn_finalizar.pack(side=tk.LEFT, padx=10, expand=True)

    btn_voltar = tk.Button(frame_botoes_comanda, text="Voltar", width=20, height=2, font=("Segoe UI", 12), bg="#E53935", fg="#FFFFFF", relief="flat", command=tela_comanda.destroy)
    btn_voltar.pack(side=tk.RIGHT, padx=10, expand=True)

    atualizar_lista_pedidos()

def abrir_comandas():
    tela_comandas = tk.Toplevel(main_window)
    tela_comandas.title("Comandas")
    tela_comandas.geometry("400x400")
    tela_comandas.config(bg="#1E1E1E")
    lbl_comandas = tk.Label(tela_comandas, text="Comandas por Mesa", font=("Segoe UI", 14),
                             fg="#F0F0F0", bg="#1E1E1E")
    lbl_comandas.pack(pady=10)

    for mesa in mesas:
        status = "Aberta" if mesa['comanda'] else "Disponível"
        cor = "#FFC107" if status == "Aberta" else "#4CAF50"
        btn_comanda = tk.Button(tela_comandas, text=f"{mesa['nome']} - Status: {status}", width=30, height=2,
                                 font=("Segoe UI", 12), bg="#2D2D30", fg=cor, relief="flat",
                                 command=lambda m=mesa: abrir_comanda_mesa(m))
        btn_comanda.pack(pady=5)
        
    btn_voltar = tk.Button(tela_comandas, text="Voltar", width=20, height=2, font=(
        "Segoe UI", 12), bg="#E53935", fg="#FFFFFF", relief="flat", command=tela_comandas.destroy)
    btn_voltar.pack(pady=20)


def abrir_caixa():
    tela_caixa = tk.Toplevel(main_window)
    tela_caixa.title("Caixa")
    tela_caixa.geometry("400x400")
    tela_caixa.config(bg="#1E1E1E")
    lbl_caixa = tk.Label(tela_caixa, text="Status das Vendas por Mesa", font=("Segoe UI", 14),
                          fg="#F0F0F0", bg="#1E1E1E")
    lbl_caixa.pack(pady=10)

    vendas_caixa = [
        {"mesa": "Mesa 1", "status": "Confirmada"},
        {"mesa": "Mesa 2", "status": "Pendente"},
        {"mesa": "Mesa 3", "status": "Confirmada"},
        {"mesa": "Mesa 4", "status": "Pendente"},
        {"mesa": "Mesa 5", "status": "Confirmada"},
        {"mesa": "Mesa 6", "status": "Pendente"},
    ]

    status_cores_caixa = {"Confirmada": "#4CAF50", "Pendente": "#FFC107"}
    
    for venda in vendas_caixa:
        cor = status_cores_caixa[venda["status"]]
        venda_info = f"{venda['mesa']} - Venda: {venda['status']}"
        tk.Label(tela_caixa, text=venda_info, font=("Segoe UI", 12),
                  fg=cor, bg="#1E1E1E").pack(pady=5)

    btn_voltar = tk.Button(tela_caixa, text="Voltar", width=20, height=2, font=("Segoe UI", 12), bg="#E53935", fg="#FFFFFF", relief="flat", command=tela_caixa.destroy)
    btn_voltar.pack(pady=20)

def iniciar_app():
    global login_window, entry_username, entry_password
    login_window = tk.Tk()
    login_window.title("Login Sistema PDV")
    login_window.geometry("400x350")
    login_window.config(bg="#1E1E1E")
    
    frame_login_card = tk.Frame(login_window, bg="#2D2D30", padx=20, pady=20, relief="flat")
    frame_login_card.pack(pady=30)

    lbl_username = tk.Label(frame_login_card, text="Usuário:", font=("Segoe UI", 12), fg="#F0F0F0", bg="#2D2D30")
    lbl_username.pack(pady=5)
    entry_username = tk.Entry(frame_login_card, font=("Segoe UI", 12), bg="#3A3A3C", fg="#FFFFFF", relief="flat")
    entry_username.pack(pady=5)

    lbl_password = tk.Label(frame_login_card, text="Senha:", font=("Segoe UI", 12), fg="#F0F0F0", bg="#2D2D30")
    lbl_password.pack(pady=5)
    entry_password = tk.Entry(frame_login_card, show="*", font=("Segoe UI", 12), bg="#3A3A3C", fg="#FFFFFF", relief="flat")
    entry_password.pack(pady=5)
    
    entry_username.bind("<Return>", lambda event: login())
    entry_password.bind("<Return>", lambda event: login())
    
    btn_login = tk.Button(login_window, text="Entrar", width=15, height=2, font=("Segoe UI", 12), bg="#4CAF50", fg="#FFFFFF", relief="flat", command=login)
    btn_login.pack(pady=10)

    btn_sair = tk.Button(login_window, text="Sair", width=15, height=2, font=("Segoe UI", 12), bg="#E53935", fg="#FFFFFF", relief="flat", command=login_window.destroy)
    btn_sair.pack(pady=5)
    
    login_window.mainloop()

if __name__ == "__main__":
    iniciar_app()
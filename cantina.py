import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
import random

class ModernCantinaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cantina Escolar Moderna")
        self.root.geometry("1000x700")
        self.root.resizable(False, False)

        
        # Banco de dados simulado
        self.products = {
            "Lanche": {
                "Sanduíche": {"price": 5.00, "image": None},
                "Hot Dog": {"price": 4.50, "image": None},
                "Pizza": {"price": 6.00, "image": None}
            },
            "Bebidas": {
                "Suco": {"price": 3.50, "image": None},
                "Refri": {"price": 4.00, "image": None},
                "Água": {"price": 2.50, "image": None}
            },
            "Doces": {
                "Bolo": {"price": 3.00, "image": None},
                "Brigadeiro": {"price": 1.50, "image": None},
                "Sorvete": {"price": 4.50, "image": None}
            }
        }
        
        self.students = {
            "12345": {"name": "João Silva", "balance": 50.00},
            "54321": {"name": "Maria Souza", "balance": 30.00}
        }
        
        self.current_user = None
        self.cart = {}
        
        # Estrutura principal
        self.main_frame = tb.Frame(self.root)
        self.main_frame.pack(fill=tb.BOTH, expand=True)
        
        # Carregar imagens (substitua por imagens reais)
        self.load_placeholders()
        
        # Iniciar com a tela de login
        self.create_login_screen()

    def load_placeholders(self):
        """Cria placeholders para imagens dos produtos"""
        for category in self.products:
            for product in self.products[category]:
                self.products[category][product]["image"] = self.create_color_block(200, 150, "#" + "%06x" % random.randint(0, 0xFFFFFF), product)

    def create_color_block(self, width, height, color, text):
        """Cria uma imagem de placeholder colorida com texto"""
        from PIL import Image, ImageDraw, ImageFont
        try:
            image = Image.new("RGB", (width, height), color)
            draw = ImageDraw.Draw(image)
            font = ImageFont.load_default()
            textwidth, textheight = draw.textsize(text, font)
            draw.text(((width - textwidth)/2, (height - textheight)/2), text, fill="black", font=font)
            return ImageTk.PhotoImage(image)
        except:
            return None

    def clear_screen(self):
        """Limpa todos os widgets do frame principal"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def create_login_screen(self):
        """Cria a tela de login"""
        self.clear_screen()
        
        # Frame do cabeçalho
        header_frame = tb.Frame(self.main_frame, style="TFrame")
        header_frame.pack(fill=tk.X, padx=20, pady=20)
        
        title = tb.Label(header_frame, text="Cantina Escola Feliz", style="Title.TLabel")
        title.pack(fill=tk.X, ipady=20)
        
        # Frame do conteúdo
        content_frame = tb.Frame(self.main_frame, style="TFrame")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Imagem de boas-vindas
        img_frame = tb.Frame(content_frame)
        img_frame.pack(pady=20)
        
        welcome_img = self.create_color_block(500, 200, "#a1d6f4", "Bem-vindo à Cantina!")
        img_label = tb.Label(img_frame, image=welcome_img)
        img_label.image = welcome_img
        img_label.pack()
        
        # Formulário de login
        login_frame = tb.Frame(content_frame)
        login_frame.pack(pady=20)
        
        tb.Label(login_frame, text="Digite sua matrícula:", font=("Arial", 12)).pack()
        
        self.matricula_entry = tb.Entry(login_frame, font=("Arial", 14), width=20)
        self.matricula_entry.pack(pady=10)
        
        login_btn = tb.Button(login_frame, text="Entrar", bootstyle="primary", command=self.validate_login)
        login_btn.pack(pady=10)

    def validate_login(self):
        """Valida o login do aluno"""
        matricula = self.matricula_entry.get()
        
        if matricula in self.students:
            self.current_user = self.students[matricula]
            self.current_user["matricula"] = matricula
            self.create_main_menu()
        else:
            messagebox.showerror("Erro", "Matrícula não encontrada. Tente novamente.")

    def create_main_menu(self):
        """Cria o menu principal após login"""
        self.clear_screen()
        
        # Header com informações do aluno
        header_frame = tb.Frame(self.main_frame, style="TFrame")
        header_frame.pack(fill=tk.X, padx=20, pady=10)
        
        user_info = tb.Label(
            header_frame, 
            text=f"Bem-vindo, {self.current_user['name']} | Saldo: R${self.current_user['balance']:.2f}",
            font=("Arial", 12, "bold"),
            foreground="#3a7ff6"
        )
        user_info.pack(side=tk.LEFT)

        logout_btn = tb.Button(
            header_frame,
            text="Sair",
            bootstyle="danger",
            command=lambda: [setattr(self, 'current_user', None), self.create_login_screen()]
        )
        logout_btn.pack(side=tk.RIGHT)
        
        # Abas para navegação
        notebook = tb.Notebook(self.main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Tab de produtos
        products_tab = tb.Frame(notebook)
        notebook.add(products_tab, text="Produtos")
        self.create_products_tab(products_tab)
        
        # Tab de carrinho
        cart_tab = tb.Frame(notebook)
        notebook.add(cart_tab, text="Carrinho")
        self.create_cart_tab(cart_tab)
        
        # Tab de recarga
        recharge_tab = tb.Frame(notebook)
        notebook.add(recharge_tab, text="Recarregar")
        self.create_recharge_tab(recharge_tab)

    def create_products_tab(self, parent):
        """Cria a aba de seleção de produtos"""
        notebook = tb.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        for category in self.products:
            category_frame = tb.Frame(notebook)
            notebook.add(category_frame, text=category)
            
            row, col = 0, 0
            for product, details in self.products[category].items():
                product_frame = tb.Frame(category_frame)
                product_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
                
                # Imagem do produto
                img_label = tb.Label(product_frame, image=details["image"])
                img_label.image = details["image"]
                img_label.pack()
                
                # Nome e preço
                tb.Label(
                    product_frame, 
                    text=f"{product}\nR${details['price']:.2f}", 
                    font=("Arial", 10, "bold"),
                    justify="center"
                ).pack()
                
                # Botão para adicionar
                tb.Button(
                    product_frame,
                    text="Adicionar",
                    bootstyle="success",
                    command=lambda p=product, pr=details["price"]: self.add_to_cart(p, pr)
                ).pack(pady=5)
                
                col += 1
                if col > 2:
                    col = 0
                    row += 1
            
            for i in range(3):
                category_frame.columnconfigure(i, weight=1)

    def add_to_cart(self, product, price):
        """Adiciona produto ao carrinho"""
        if product in self.cart:
            self.cart[product]["quantity"] += 1
        else:
            self.cart[product] = {"price": price, "quantity": 1}

        messagebox.showinfo("Sucesso", f"{product} adicionado ao carrinho!")

        # 🔧 ATUALIZA A EXIBIÇÃO DO CARRINHO SE ELE JÁ FOI CRIADO
        if hasattr(self, 'cart_tree'):
            self.update_cart_display()

    def create_cart_tab(self, parent):
        """Cria a aba do carrinho de compras"""
        # Frame para listagem
        cart_frame = tb.Frame(parent)
        cart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        tb.Label(
            cart_frame, 
            text="Seu Carrinho", 
            font=("Arial", 14, "bold")
        ).pack(pady=10)
        
        # Árvore de itens
        columns = ("Produto", "Preço Unitário", "Quantidade", "Subtotal")
        self.cart_tree = tb.Treeview(
            cart_frame, 
            columns=columns, 
            show="headings",
            height=10
        )
        
        for col in columns:
            self.cart_tree.heading(col, text=col)
            self.cart_tree.column(col, width=150, anchor="center")
        
        self.cart_tree.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Frame do total
        total_frame = tb.Frame(cart_frame)
        total_frame.pack(fill=tk.X, pady=10)
        
        self.total_label = tb.Label(
            total_frame,
            text="Total: R$0.00",
            font=("Arial", 12, "bold"),
            foreground="#3a7ff6"
        )
        self.total_label.pack(side=tk.RIGHT)
        
        # Botões
        btn_frame = tb.Frame(cart_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        tb.Button(btn_frame, text="Remover Item", bootstyle="danger-outline", command=self.remove_item).pack(side=LEFT, padx=5)
        tb.Button(btn_frame, text="Limpar Carrinho", bootstyle="warning-outline", command=self.clear_cart).pack(side=LEFT, padx=5)
        
        tb.Button(btn_frame, text="Finalizar Compra", bootstyle="success", command=self.checkout).pack(side=RIGHT)
        
        self.update_cart_display()

    def update_cart_display(self):
        """Atualiza a exibição do carrinho"""
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)

        total = 0
        for product, details in self.cart.items():
            subtotal = details["price"] * details["quantity"]
            total += subtotal
            self.cart_tree.insert("", "end", values=(
                product,
                f"R${details['price']:.2f}",
                details["quantity"],
                f"R${subtotal:.2f}"
            ))

        self.total_label.config(text=f"Total: R${total:.2f}")

    def remove_item(self):
        """Remove item selecionado do carrinho"""
        selected = self.cart_tree.selection()
        if selected:
            product = self.cart_tree.item(selected)["values"][0]
            del self.cart[product]
            self.update_cart_display()
            messagebox.showinfo("Sucesso", f"{product} removido do carrinho")

    def clear_cart(self):
        """Limpa todo o carrinho"""
        self.cart = {}
        self.update_cart_display()
        messagebox.showinfo("Sucesso", "Carrinho limpo")

    def checkout(self):
        """Finaliza a compra"""
        if not self.cart:
            messagebox.showerror("Erro", "Carrinho vazio!")
            return
        
        total = sum(details["price"] * details["quantity"] for details in self.cart.values())
        if total > self.current_user["balance"]:
            messagebox.showerror("Erro", "Saldo insuficiente!")
            self.create_recharge_tab()
            return
        
        # Processa o pagamento
        self.current_user["balance"] -= total
        self.cart = {}
        self.update_cart_display()
        messagebox.showinfo("Sucesso", "Compra realizada com sucesso!")
        self.create_main_menu()  # Atualiza o saldo na tela

    def create_recharge_tab(self, parent):
        """Cria a aba de recarga de saldo"""
        frame = tb.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        tb.Label(
            frame, 
            text="Recarregar Saldo", 
            font=("Arial", 14, "bold")
        ).pack(pady=10)
        
        # Saldo atual
        tb.Label(
            frame,
            text=f"Saldo Atual: R${self.current_user['balance']:.2f}",
            font=("Arial", 12),
            foreground="#3a7ff6"
        ).pack()
        
        # Valor da recarga
        tb.Label(
            frame,
            text="Valor da Recarga:",
            font=("Arial", 12)
        ).pack(pady=10)
        
        self.recharge_entry = tb.Entry(
            frame,
            font=("Arial", 12),
            width=10
        )
        self.recharge_entry.pack()
        
        # Botões de valores rápidos
        quick_frame = tb.Frame(frame)
        quick_frame.pack(pady=10)

        for value in [10, 20, 50]:
            tb.Button(
                quick_frame,
                text=f"R${value:.2f}",
                bootstyle="info",
                command=lambda v=value: [self.recharge_entry.delete(0, "end"), self.recharge_entry.insert(0, str(v))]
            ).pack(side=LEFT, padx=5)
        
        # Botão de confirmação
        tb.Button(
            frame,
            text="Confirmar Recarga",
            bootstyle="primary",
            command=self.process_recharge
        ).pack(pady=10)

    def process_recharge(self):
        """Processa a recarga do cartão"""
        try:
            value = float(self.recharge_entry.get())
            if value <= 0:
                raise ValueError
                
            self.current_user["balance"] += value
            messagebox.showinfo("Sucesso", f"Saldo recarregado com sucesso! Novo saldo: R${self.current_user['balance']:.2f}")
            self.create_main_menu()
        except:
            messagebox.showerror("Erro", "Valor inválido! Digite um número positivo.")

if __name__ == "__main__":
    root = tb.Window(themename="flatly")  # ou "cosmo", "superhero", "morph", etc.
    app = ModernCantinaApp(root)
    root.mainloop()

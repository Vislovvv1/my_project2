import tkinter as tk
from tkinter import messagebox, simpledialog, ttk


class Client:
    def __init__(self, name, phone, email):
        self.name = name
        self.phone = phone
        self.email = email
        self.orders = []

    def add_order(self, order):
        self.orders.append(order)

    def __str__(self):
        return f"{self.name} | Телефон: {self.phone} | Email: {self.email} | Заказов: {len(self.orders)}"

    def get_orders_info(self):
        """Возвращает информацию о заказах клиента"""
        if not self.orders:
            return "У этого клиента пока нет заказов."
        return "\n".join(str(order) for order in self.orders)


class Order:
    def __init__(self, order_id, date_created=None):
        self.order_id = order_id
        self.products = []
        self.date_created = date_created or "Сегодня"  # В реальном приложении используйте datetime

    def add_product(self, product, price, qty):
        self.products.append({"product": product, "price": price, "qty": qty})

    def total(self):
        return sum(p["price"] * p["qty"] for p in self.products)

    def __str__(self):
        items = ", ".join([f'{p["product"]} x{p["qty"]}' for p in self.products])
        return f"Заказ {self.order_id}: {items} | Сумма: {self.total()} руб."


class StoreManager:
    def __init__(self):
        self.clients = []
        self.orders = []
        self.next_order_id = 1

    def add_client(self, name, phone, email):
        # Проверка на дубликаты
        if any(client.name.lower() == name.lower() for client in self.clients):
            raise ValueError("Клиент с таким именем уже существует")

        client = Client(name, phone, email)
        self.clients.append(client)
        return client

    def add_order(self, client):
        order = Order(self.next_order_id)
        self.next_order_id += 1
        client.add_order(order)
        self.orders.append(order)
        return order

    def list_clients(self):
        return "\n".join(str(c) for c in self.clients)

    def list_orders(self):
        return "\n".join(str(o) for o in self.orders)

    def find_client(self, name):
        return [c for c in self.clients if name.lower() in c.name.lower()]

    def get_client_by_name(self, name):
        """Получить клиента по точному имени"""
        for client in self.clients:
            if client.name.lower() == name.lower():
                return client
        return None


class SimpleStoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Система управления магазином")
        self.root.geometry("400x250")

        # Центрирование окна
        self.center_window(400, 250)

        self.manager = StoreManager()

        # Создаем основной фрейм
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Заголовок
        title_label = ttk.Label(main_frame, text="Управление клиентами и заказами",
                                font=("Arial", 12, "bold"))
        title_label.pack(pady=10)

        # Поисковая строка
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=5)

        ttk.Label(search_frame, text="Поиск клиента:").pack(side=tk.LEFT, padx=(0, 5))

        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.search_entry.bind("<Return>", lambda e: self.search_client())

        # Кнопки
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=15)

        self.search_btn = ttk.Button(btn_frame, text="Поиск клиента",
                                     command=self.search_client, width=18)
        self.search_btn.grid(row=0, column=0, padx=5, pady=5)

        self.view_btn = ttk.Button(btn_frame, text="Просмотр клиентов",
                                   command=self.view_clients, width=18)
        self.view_btn.grid(row=0, column=1, padx=5, pady=5)

        self.add_btn = ttk.Button(btn_frame, text="Добавить клиента",
                                  command=self.add_client_dialog, width=18)
        self.add_btn.grid(row=1, column=0, padx=5, pady=5)

        self.orders_btn = ttk.Button(btn_frame, text="Все заказы",
                                     command=self.view_all_orders, width=18)
        self.orders_btn.grid(row=1, column=1, padx=5, pady=5)

    def center_window(self, width, height):
        """Центрирует окно на экране"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def search_client(self):
        name = self.search_entry.get().strip()
        if not name:
            messagebox.showwarning("Внимание", "Введите имя для поиска")
            return

        found = self.manager.find_client(name)
        if found:
            result = "Найдены клиенты:\n\n" + "\n".join(str(c) for c in found)
            messagebox.showinfo("Результат поиска", result)
        else:
            if messagebox.askyesno("Клиент не найден",
                                   f"Клиент '{name}' не найден.\nХотите добавить нового клиента?"):
                self.add_client_dialog(name)

    def add_client_dialog(self, prefill_name=""):
        name = prefill_name or simpledialog.askstring("Добавить клиента", "Введите имя:")
        if not name:
            return

        phone = simpledialog.askstring("Добавить клиента", "Введите телефон:")
        if not phone:
            return

        email = simpledialog.askstring("Добавить клиента", "Введите email:")
        if not email:
            return

        try:
            self.manager.add_client(name, phone, email)
            messagebox.showinfo("Успех", f"Клиент '{name}' успешно добавлен!")

            if messagebox.askyesno("Добавить заказ", "Хотите добавить заказ для этого клиента?"):
                self.add_order(name)

        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    def add_order(self, client_name):
        client = self.manager.get_client_by_name(client_name)
        if not client:
            messagebox.showerror("Ошибка", "Клиент не найден")
            return

        order = self.manager.add_order(client)

        while True:
            product = simpledialog.askstring("Добавить товар",
                                             "Название товара (отмена - закончить):")
            if not product:
                if not order.products:
                    messagebox.showwarning("Внимание", "Заказ без товаров был отменен")
                    client.orders.remove(order)
                    self.manager.orders.remove(order)
                break

            try:
                price = float(simpledialog.askstring("Добавить товар", "Цена:"))
                qty = int(simpledialog.askstring("Добавить товар", "Количество:"))

                if price <= 0 or qty <= 0:
                    messagebox.showerror("Ошибка", "Цена и количество должны быть положительными числами")
                    continue

            except (ValueError, TypeError):
                messagebox.showerror("Ошибка", "Неверный формат числа")
                continue

            order.add_product(product, price, qty)

        if order.products:
            messagebox.showinfo("Успех", f"Заказ #{order.order_id} на сумму {order.total()} руб. добавлен!")

    def view_clients(self):
        if not self.manager.clients:
            messagebox.showinfo("Клиенты", "Клиентов пока нет.")
            return

        win = tk.Toplevel(self.root)
        win.title("Список клиентов")
        win.geometry("600x400")
        self.center_child_window(win, 600, 400)

        # Фрейм для списка
        list_frame = ttk.Frame(win)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Label(list_frame, text="Список клиентов (двойной клик для просмотра заказов):",
                  font=("Arial", 10, "bold")).pack(anchor=tk.W)

        # Создаем Treeview для лучшего отображения
        columns = ("#", "Имя", "Телефон", "Email", "Заказов")
        tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)

        # Настраиваем колонки
        tree.heading("#", text="#")
        tree.heading("Имя", text="Имя")
        tree.heading("Телефон", text="Телефон")
        tree.heading("Email", text="Email")
        tree.heading("Заказов", text="Заказов")

        tree.column("#", width=40)
        tree.column("Имя", width=120)
        tree.column("Телефон", width=100)
        tree.column("Email", width=150)
        tree.column("Заказов", width=60)

        # Добавляем данные
        for idx, client in enumerate(self.manager.clients, start=1):
            tree.insert("", tk.END, values=(
                idx, client.name, client.phone, client.email, len(client.orders)
            ), tags=(client.name,))

        tree.pack(fill=tk.BOTH, expand=True, pady=5)

        # Привязываем двойной клик
        tree.bind("<Double-1>", lambda e: self.show_client_orders(tree))

    def show_client_orders(self, tree):
        selection = tree.selection()
        if selection:
            item = tree.item(selection[0])
            client_name = item['tags'][0]
            client = self.manager.get_client_by_name(client_name)

            if client:
                orders_text = client.get_orders_info()
                messagebox.showinfo(f"Заказы клиента: {client.name}", orders_text)

    def view_all_orders(self):
        if not self.manager.orders:
            messagebox.showinfo("Заказы", "Заказов пока нет.")
            return

        win = tk.Toplevel(self.root)
        win.title("Все заказы")
        win.geometry("700x400")
        self.center_child_window(win, 700, 400)

        text_widget = tk.Text(win, wrap=tk.WORD, padx=10, pady=10)
        scrollbar = ttk.Scrollbar(win, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)

        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        total_revenue = sum(order.total() for order in self.manager.orders)

        orders_text = f"Всего заказов: {len(self.manager.orders)}\n"
        orders_text += f"Общая выручка: {total_revenue} руб.\n\n"
        orders_text += "\n\n".join(str(order) for order in self.manager.orders)

        text_widget.insert(tk.END, orders_text)
        text_widget.config(state=tk.DISABLED)

    def center_child_window(self, window, width, height):
        """Центрирует дочернее окно относительно главного"""
        self.root.update()
        x = self.root.winfo_x() + (self.root.winfo_width() - width) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleStoreApp(root)
    root.mainloop()
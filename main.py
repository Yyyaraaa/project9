#ипортируем все нужное
import tkinter as tk
from tkinter import ttk
import sqlite3

class Main(tk.Frame):#создаем класс для хранения функций
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self): #добавление контакта
        toolbar = tk.Frame(bg="#d7d8e0", bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        self.add_img = tk.PhotoImage(file="./img/add.png")
        btn_open_dialog = tk.Button(
            toolbar, bg="#d7d8e0", bd=0, image=self.add_img, command=self.open_dialog
        )
        btn_open_dialog.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(
            self, columns=("ID", "name", "tel", "email"), height=45, show="headings"
        )

        #создание таблицы данных
        #разметка таблицы
        self.tree.column("ID", width=30, anchor=tk.CENTER)
        self.tree.column("name", width=300, anchor=tk.CENTER)
        self.tree.column("tel", width=150, anchor=tk.CENTER)
        self.tree.column("email", width=150, anchor=tk.CENTER)

        #названия строк
        self.tree.heading("ID", text="ID")
        self.tree.heading("name", text="ФИО")
        self.tree.heading("tel", text="Телефон")
        self.tree.heading("email", text="E-mail")

        self.tree.pack(side=tk.LEFT) #размещение кнопки

        #создание кнопки изменения контакта
        self.update_img = tk.PhotoImage(file="./img/update.png")
        btn_edit_dialog = tk.Button(
            toolbar,
            bg="#d7d8e0",
            bd=0,
            image=self.update_img,
            command=self.open_update_dialog,
        )
        btn_edit_dialog.pack(side=tk.LEFT)#расположение

        #создание кнопки удаления контакта
        self.delete_img = tk.PhotoImage(file="./img/delete.png")
        btn_delete = tk.Button(
            toolbar,
            bg="#d7d8e0",
            bd=0,
            image=self.delete_img,
            command=self.delete_records,
        )
        btn_delete.pack(side=tk.LEFT)#расположение

        #создание кнопки поиска контакта
        self.search_img = tk.PhotoImage(file="./img/search.png")
        btn_search = tk.Button(
            toolbar,
            bg="#d7d8e0",
            bd=0,
            image=self.search_img,
            command=self.open_search_dialog,
        )
        btn_search.pack(side=tk.LEFT)#расположение

        #создание кнопки обновления
        self.refresh_img = tk.PhotoImage(file="./img/refresh.png")
        btn_refresh = tk.Button(
            toolbar,
            bg="#d7d8e0",
            bd=0,
            image=self.refresh_img,
            command=self.open_search_dialog,
        )
        btn_refresh.pack(side=tk.LEFT)#расположение

    #подключение класса
    def open_dialog(self):
        Child()

    #сохранение данных в бд
    def records(self, name, tel, email):
        self.db.insert_data(name, tel, email)
        self.view_records()

    #обновление данных
    def view_records(self):
        self.db.cursor.execute("SELECT * FROM db")
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert("", "end", values=row) for row in self.db.cursor.fetchall()]

    #подключение класса
    def open_update_dialog(self):
        Update()

    #изменение данных
    def update_records(self, name, tel, email):
        self.db.cursor.execute(
            """UPDATE db SET name=?, tel=?, email=? WHERE id=?""",
            (name, tel, email, self.tree.set(self.tree.selection()[0], "#1")),
        )
        self.db.conn.commit()
        self.view_records()

    #удаление данных
    def delete_records(self):
        for selection_items in self.tree.selection():
            self.db.cursor.execute(
                "DELETE FROM db WHERE id=?", (self.tree.set(selection_items, "#1"))
            )
        self.db.conn.commit()
        self.view_records()

    #подключаем класс
    def open_search_dialog(self):
        Search()

    #поиск контакта
    def search_records(self, name):
        name = "%" + name + "%"
        self.db.cursor.execute("SELECT * FROM db WHERE name LIKE ?", (name,)) #сюда передаем кортеж (name), а не просто name

        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert("", "end", values=row) for row in self.db.cursor.fetchall()]

class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    #создаем таблицу для добавления данных
    def init_child(self):
        self.title("Добавить")
        self.geometry("400x220")
        self.resizable(False, False)

        self.grab_set()
        self.focus_set()

        #названия и размещение строк
        label_name = tk.Label(self, text="ФИО:")
        label_name.place(x=50, y=50)
        label_select = tk.Label(self, text="Телефон:")
        label_select.place(x=50, y=80)
        label_sum = tk.Label(self, text="E-mail:")
        label_sum.place(x=50, y=110)

    #размеры строк
        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=80)
        self.entry_tel = ttk.Entry(self)
        self.entry_tel.place(x=200, y=110)

        #добавляем кнопку закрыть
        self.btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)
        self.btn_cancel.place(x=220, y=170)

        #добавляем кнопку добавить
        self.btn_ok = ttk.Button(self, text="Добавить")
        self.btn_ok.place(x=300, y=170)

        self.btn_ok.bind(
            "<Button-1>",
            lambda event: self.view.records(
                self.entry_name.get(), self.entry_email.get(), self.entry_tel.get()
            ),
        )

class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    #создем функцию редактирования контакта
    def init_edit(self):
        self.title("Редактирование контакта")#название
        btn_edit = ttk.Button(self, text="Редактировать")#кнопка
        btn_edit.place(x=205, y=170)
        btn_edit.bind(
            "<Button-1>",
            lambda event: self.view.update_records(
                self.entry_name.get(), self.entry_email.get(), self.entry_tel.get()
            ),
        )
        btn_edit.bind("<Button-1>", lambda event: self.destroy(), add="+")
        self.btn_ok.destroy()

    #изменяем данные определенного id
    def default_data(self):
        self.db.cursor.execute(
            "SELECT * FROM db WHERE id=?",
            self.view.tree.set(self.view.tree.selection()[0], "#1"),
        )
        row = self.db.cursor.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_email.insert(0, row[2])
        self.entry_tel.insert(0, row[3])

class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    #функция поиска контакта
    def init_search(self):
        self.title("Поиск контакта")
        self.geometry("300x100")
        self.resizable(False, False)

        #название строки, размещение
        label_search = tk.Label(self, text="Имя:")
        label_search.place(x=50, y=20)

        #длинна строки
        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=100, y=20, width=150)

        #добавление кнопки закрыть
        btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy) #тут не должно быть скобок у self.destroy
        btn_cancel.place(x=185, y=50)

        #добавление кнопки найти
        search_btn = ttk.Button(self, text="Найти")
        search_btn.place(x=105, y=50)
        search_btn.bind(
            "<Button-1>",
            lambda event: self.view.search_records(self.entry_search.get()),
        )
        search_btn.bind("<Button-1>", lambda event: self.destroy(), add="+")

#создание бд
class DB:
    def __init__(self):
        self.conn = sqlite3.connect("db.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS db (
                id INTEGER PRIMARY KEY,
                name TEXT,
                tel TEXT,
                email TEXT
            )"""
        )
        self.conn.commit()

    #функция по добавлению данны в бд
    def insert_data(self, name, tel, email):
        self.cursor.execute(
            """INSERT INTO db(name, tel, email) VALUES(?, ?, ?)""", (name, tel, email)
        )
        self.conn.commit()

if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Телефонная книга")
    root.geometry("665x450")
    root.resizable(False, False)
    root.mainloop()#запуск
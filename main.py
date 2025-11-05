import customtkinter as ctk
from tkinter import messagebox
import sys
import os

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')

class StickyArea(ctk.CTkFrame):
    """Область отображения стикеров"""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(fg_color='#2b2b2b')

        self.hint_label = ctk.CTkLabel(
            self,
            text='Область для стикеров',
            text_color='#a0a0a0',
            font=('Arial', 16),
        )
        self.hint_label.place(relx=0.5, rely=0.5, anchor='center')

class TabPanel(ctk.CTkFrame):
    """Панель вкладок"""
    def __init__(self, master, on_tab_changed, **kwargs):
        super().__init__(master, **kwargs)

        self.on_tab_changed = on_tab_changed
        self._current_tab = 'Основаная'
        self.tab_buttons = {}

        self.configure(fg_color='#e9ecef', width=200)
        self.pack_propagate(False)

        self.title_label = ctk.CTkLabel(
            self,
            text='ВКЛАДКИ',
            text_color='#495057',
            font=('Arial', 18, 'bold')
        )
        self.title_label.pack(pady=(20, 15))

        self.separator = ctk.CTkFrame(self, height=2, fg_color='#dee2e6')
        self.separator.pack(fill='x', padx=10, pady=(0, 15))

        self.tabs_container = ctk.CTkScrollableFrame(self, fg_color='transparent')
        self.tabs_container.pack(fill='both', expand=True, padx=10, pady=5)

        self.initialize_tabs()

    def initialize_tabs(self):
        """Создание начального набора вкладок"""
        initial_labs = ['Основаная','Работа','Личное']
        for tab_name in initial_labs:
            self.add_tab(tab_name)

    def add_tab(self, name):
        """Добавление новой вкладки"""
        tab_button = ctk.CTkButton(
            self.tabs_container,
            text=name,
            font=('Arial', 14),
            anchor='w',
            fg_color='#007bff' if name == self._current_tab else 'transparent',
            text_color='white' if name == self._current_tab else '#495057',
            hover_color='#0056b3' if name == self._current_tab else '#f8f9fa',
            corner_radius=8,
            height=40,
            command=lambda tab=name: self.select_tab(tab)
        )
        tab_button.pack(fill='x', pady=2)
        self.tab_buttons[name] = tab_button

    def select_tab(self, tab_name):
        """Выбор вкладки"""
        if tab_name in self.tab_buttons:
            if self._current_tab in self.tab_buttons:
                old_btn = self.tab_buttons[self.current_tab]
                old_btn.configure(
                    fg_color='transparent',
                    text_color='#495057',
                    hover_color='#f8f9fa'
                )

            new_btn = self.tab_buttons[tab_name]
            new_btn.configure(
                fg_color='#007bff',
                text_color='white',
                hover_color='#0056b3'
            )

            self.current_tab = tab_name
            self.on_tab_changed(tab_name)

class TrashIcon(ctk.CTkButton):
    """Иконка корзины"""
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            text='🗑️',
            font=('Arial', 18),
            width=40,
            height=40,
            fg_color='#dc3545',
            hover_color='#c82333',
            corner_radius=20,
            **kwargs
        )

class MainWindow(ctk.CTk):
    """Главное окно"""
    def __init__(self):
        super().__init__()

        self.title('Доска со стикерами')
        self.geometry('1200x800')
        self.minsize(1000, 600)

        self.create_interface()

        self.bind_events()

    def create_interface(self):
        """Основной интерфейс"""
        self.main_container = ctk.CTkFrame(self, fg_color='transparent')
        self.main_container.pack(fill='both', expand=True, padx=10, pady=10)

        self.tab_panel = TabPanel(
            self.main_container,
            on_tab_changed=self.on_tab_changed,
            width=200
        )
        self.tab_panel.pack(side='left', fill='y', padx=(0, 10))

        self.sticky_area = StickyArea(self.main_container)
        self.sticky_area.pack(side='left', fill='both', expand=True)

        self.trash_icon = TrashIcon(
            self.sticky_area,
            command = self.open_trash
        )
        self.trash_icon.place(relx=0.95, rely=0.95, anchor='se')

    def bind_events(self):
        """Привязка обработчиков событий"""
        self.sticky_area.bind("<Button-3>", self.show_context_menu)
        self.sticky_area.bind("<Button-3>", self.show_tabs_context_menu)

    def on_tab_changed(self, tab_name):
        """Обработчик смены вкладок"""
        pass

    def open_trash(self):
        """Открытие корзины"""
        pass

    def show_context_menu(self, event):
        """Контекстное меню для области стикеров"""
        context_menu = ctk.CTkMenu(
            self,
            values=['Создать заметку', "Уполядочить стикеры"],
            command=self.handle_context_menu
        )
        context_menu.show(event.x_root, event.y_root)

    def show_tabs_context_menu(self, event):
        """Показ контекстного меню для панели вкладом"""
        context_menu = ctk.CTkMenu(
            self,
            values=['Создать вкладку', 'Переименовать', "Удалить"],
            camman=self.handle_tabs_context_menu
        )
        context_menu.show(event.x_root, event.y_root)

    def handle_context_menu(self, option):
        """Обработчик контекстного меню области стикеров"""
        if option == 'Создать заметку':
            self.create_new_note()
        elif option == 'Упорядочить стикеры':
            self.arrange_notes()

    def handle_tabs_context_menu(self, option):
        """Обработчик контекстного меню панели вкладок"""
        if option == 'Создать вкладку':
            self.create_new_tab()
        elif option == 'Переименовать':
            self.rename_tab()
        elif option == 'Удалить':
            self.delete_tab()

    def create_new_note(self):
        """Создание новой заметки"""
        pass

    def arrange_notes(self):
        """Упорядочевание стикеров"""
        pass

    def create_new_tab(self):
        """Создание новой вкладки"""
        pass

    def rename_tab(self):
        """Переименование вкладки"""
        pass

    def delete_tab(self):
        """Удаление вкладки"""
        pass

def main():
    """Основная функция приложения"""
    app = MainWindow()
    app.mainloop()


if __name__ == '__main__':
    main()
import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageDraw
import sys
import os
import json


ctk.set_appearance_mode('Dark')
ctk.set_default_color_theme('blue')


class StickyNotesApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title('Планировщик задач')
        self.geometry('900x700')
        self.minsize(700, 500)

        self.tray_icon = None
        self.tray_icon_running = False

        self.create_tray_icon()

        self.protocol('WM_DELETE_WINDOW', self.hide_to_tray)
        self.bind('<Unmap>', self.check_minimize)

        self.create_ui()

        self.deiconify()
        self.lift()
        self.focus_force()

    def check_minimize(self, event):
        """Проверка, когда окно минимизируется"""
        if self.state() == 'iconic':
            self.hide_to_tray()

    def create_ui(self):
        """Создает базовый интерфейс приложения"""
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        self.tabview = ctk.CTkTabview(main_frame)
        self.tabview.grid(row=0, column=0, sticky='nsew')

        self.main_tab = self.tabview.add('Мои задачи')
        self.trash_tab = self.tabview.add('Корзина')

        for tab_name in ['Мои задачи', 'Корзина']:
            tab = self.tabview.tab(tab_name)
            tab.grid_rowconfigure(0, weight=1)
            tab.grid_columnconfigure(0, weight=1)

        self.setup_main_tab()
        self.setup_trash_tab()
        self.setup_control_panel(main_frame)

    def setup_main_tab(self):
        """Настраиваем вклудку с задачами"""
        content_frame = ctk.CTkFrame(self.main_tab, fg_color='transparent')
        content_frame.grid(row=0, column=0, sticky='nsew')
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)

        instruction_text = (
            'Добро пожаловать в ваш стикер-пранировщик! \n\n'
            'На следующих этапах здесь появятся:\n'
            '• Создание стикеров-задач\n'
            '• Перемещение стикеров\n'
            '• Вкладки с разными тематиками\n'
            '• Приоритеты в цветах и дедлайны\n\n'
            'Сейчас приложение работает в трее - проверьте иконку рядом с часами!'
        )
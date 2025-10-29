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

        instruction_label = ctk.CTkLabel(
            content_frame,
            text=instruction_text,
            font=ctk.CTkFont(size=14),
            text_color='#bdc3c7',
            justify='left'
        )
        instruction_label.grid(row=0, column=0, padx=20, pady=20)

    def setup_trash_tab(self):
        'Настройка корзины'
        content_frame = ctk.CTkFrame(self.trash_tab, fg_color='transparent')
        content_frame.grid(row=0, column=0, sticky='nsew')
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)

        trash_text = (
            '🗑️ Корзина\n\n'
            'Здесь будут появляться выполненные задачи\n'
            'Вы сможете:\n'
            '• Восстанавливать задачи\n'
            '• Очищать корзину полностью\n'
            '• Видеть историю авполненных задач'
        )

        trash_label = ctk.CTkLabel(
            content_frame,
            text=trash_text,
            font=ctk.CTkFont(size=14),
            text_color='#7f8c8d',
            justify='center'
        )
        trash_label.grid(row=0, column=0, padx=20, pady=20)

    def setup_control_panel(self, parent):
        """Панель управления внизу окна"""
        control_frame = ctk.CTkFrame(parent)
        control_frame.grid(row=1, column=0, padx=0, pady=(10, 0), sticky='ew')

        left_frame = ctk.CTkFrame(control_frame, fg_color='transparent')
        left_frame.pack(side='left', padx=10, pady=10)

        self.tray_btn = ctk.CTkButton(
            left_frame,
            text='📌 Свернуть в трей',
            command=self.hide_to_tray,
            width=120,
            fg_color='#2c3e50',
            hover='#34495e'
        )
        self.tray_btn.pack(side='left', padx=(0, 10))

        right_frame = ctk.CTkFrame(control_frame, fg_color='transparent')
        right_frame.pack(side='right', padx=10, pady=10)

        self.tray_status = ctk.CTkLabel(
            right_frame,
            text='Приложение работает в трее',
            text_color='#27ae60',
            font=ctk.CTkFont(size=12)
        )
        self.tray_status.pack(side='right')

    def create_tray_icon(self):
        """Создает иконку в системном трее"""
        try:
            import pystray
            from pystray import MenuItem as item

            def create_image():
                width = 64
                height = 64
                image = Image.new('RGB', (width, height), '#1a1a1a')
                dc = ImageDraw.Draw(image)
                dc.rectangle([10, 10, width-10, height-10], fill='#f1c40f', outline='#f39c12', width=2)

                for i in range(15, height-15, 8):
                    dc.line([15, i, width-15, i], fill='#d35400', width=1)
                
                return image
            
            menu = pystray.Menu(
                item('Открыть планировщик', self.show_from_tray),
                item('Веход', self.quit_app)
            )

            self.tray_icon =  pystray.Icon(
                'sticky_notes_planner',
                create_image(),
                'Мой стикер-планировщик',
                menu
            )

            import threading
            def run_tray_icon():
                self.tray_icon_running = True
                self.tray_icon.run()

            thread = threading.Thread(target=run_tray_icon, daemon=True)
            thread.start()

        except ImportError as e:
            print(f'Библиотека pystray не установлена: {e}')
            self.show_pystray_error()
        except Exception as e:
            print(f'Ошибка создания иконки трея: {e}')

    def show_pystray_error(self):
        """Сообщение об ошибке"""
        error_label = ctk.CTkLabel(
            self,
            text='Для работы работы с треем установите: pip install pystray',
            text_color="#e74c3c",
            font=ctk.CTkFont(size=12)
        )
        error_label.grid(row=2, column=0, pady=10)
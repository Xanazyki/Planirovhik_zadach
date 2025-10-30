import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageDraw
import sys
import os
import json
import winreg as reg


ctk.set_appearance_mode('Dark')
ctk.set_default_color_theme('blue')


class StickyNotesApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title('Планировщик задач')
        self.geometry('1000x800')
        self.minsize(800, 600)

        self.tray_icon = None
        self.tray_icon_running = False

        self.create_ui()

        self.create_tray_icon()

        self.protocol('WM_DELETE_WINDOW', self.hide_to_tray)

    def create_ui(self):
        """Создает базовый интерфейс приложения"""
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        self.tabview = ctk.CTkTabview(main_frame, segmented_button_font=ctk.CTkFont(size=16, weight='bold'))
        self.tabview.grid(row=0, column=0, sticky='nsew')

        self.main_tab = self.tabview.add('Мои задачи')

        self.main_tab.grid_rowconfigure(0, weight=1)
        self.main_tab.grid_columnconfigure(0, weight=1)

        self.setup_canvas()
        self.setup_control_panel(main_frame)

    def setup_trash_icon(self):
        'Иконка корзины'
        self.trash_icon = ctk.CTkButton(
            self.main_tab,
            text='🗑️'
            width=60,
            height=60,
            font=ctk.CTkFont(size=24),
            fg_color='#e74c3c',
            hover_color='#c0392b',
            corner_radius=30,
            state='disabled',
            command=self.open_trash
        )

        self.trash_icon.place(relx=1.0, rely=1.0, x=-20, y=-20, anchor='se')

    def setup_canvas(self):
        "Свободное размещение задач"
        self.canvas = tk.Canvas(
            self.main_tab,
            bg='#2b2b2b',
            highlightthickness=0
        )

        self.canvas.grid(row=0, column=0, sticky='nsew')

        self.canvas.bind('<Button-1>', self.on_canvas_click)
        self.canvas.bind('<B1-Motion>', self.on_canvas_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_canvas_release)

    def create_temp_sticker(self, text, x, y):
        sticker_width = 250
        sticker_height = 180

        sticker_bg = self.canvas.create_rectangle(
            x, y, x + sticker_width, y + sticker_height,
            fill="#ca9911",
            outline='#f39c12'
            width=2,
            tags='temp_sticker'
        )

        sticker_text = self.canvas.create_text(
            x + sticker_width // 2, y + sticker_height // 2,
            text=text,
            width=sticker_width - 20,
            font=('Arial', 11),
            fill='#2c3e50'
            justify='center',
            tags='temp_sticker'
        )

    def open_trash(self):
        """Открытие корзины"""
        pass

    def on_canvas_click(self, event):
        """Обработчик клика на холсте"""
        print(f'Клик на холсте: {event.x}, {event.y}')

    def on_canvas_drag(self, event):
        """Перемещение по холсту"""
        pass

    def on_canvas_release(self, event):
        """Отпускание мыши"""

        pass

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
                
                dc.rectangle([12, 12, width-12, height-12], fill='#f1c40f', outline='#f39c12', width=3)
                dc.polygon([width=25, 12, width-12, 12, width-12, 25], fill='#d35400')

                for i in range(20, height-20, 10):
                    dc.line([20, i, width-20, i], fill='#d35400', width=2)
                
                return image
            
            menu = pystray.Menu(
                item('📋 Открыть планировщик', self.show_from_tray),
                item('❌ Веход', self.quit_app)
            )

            self.tray_icon =  pystray.Icon(
                'sticky_notes_planner',
                create_image(),
                'Мой стикер-планировщик',
                menu
            )

            def on_left_click(icon, item):
                self.show_from_tray()

            self.tray_icon._handler = on_left_click

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

    def hide_to_tray(self):
        "Скрывает окно в трее"
        self.withdraw()
        self.update_tray_status('Свернуто в трей')

    def show_from_tray(self, icon=None, item=None):
        """Показывает окно из трея"""
        self.deiconify()
        self.lift()
        self.focus_force()
        self.state('normal')
        self.update_tray_status('Окно открыто')

    def quit_app(self, icon=None, item=None):
        """Полностью закрывает приложение"""
        if self.tray_icon:
            self.tray_icon.stop()
        self.destroy()
        sys.exit()

def setup_autostart():
    """Автозапуск на Windows"""

if __name__ == "__main__":
    setup_autostart()
    
    app = StickyNotesApp()
    app.mainloop()
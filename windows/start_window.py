import tkinter as tk
from .add_document_window import AddDocWindow


class StartWindow(tk.Tk):

    def __init__(
            self,
            width: int = 900,
            height: int = 600,
            program_name: str = 'Программа для учета документов'
    ):
        super().__init__()
        self.geometry(f'{width}x{height}')
        self.resizable(width=False, height=False)
        self.config(bg='green')
        self.title(program_name)
        self.iconbitmap(default='icon.ico')

        self._buttons_width: int = 30
        self._buttons_height: int = 5
        self._buttons_font: int = 16

        self._create_buttons()

    def run(self):
        self.mainloop()

    def _create_buttons(self):
        self._create_add_doc_button()
        self._create_find_doc_button()

    def _create_add_doc_button(self):
        button_name: str = 'Добавить документ'
        self._incoming_btn = tk.Button(
            text=button_name,
            width=self._buttons_width,
            height=self._buttons_height,
            font=self._buttons_font,
            command=self._call_add_doc_window,
        )
        self._incoming_btn.pack(side=tk.LEFT, padx=40)

    def _create_find_doc_button(self):
        button_name: str = 'Найти документ'
        self._outgoing_button = tk.Button(
            text=button_name,
            width=self._buttons_width,
            height=self._buttons_height,
            font=self._buttons_font,
        )
        self._outgoing_button.pack(side=tk.RIGHT, padx=40)

    def _call_add_doc_window(self):
        window = AddDocWindow()
        self.destroy()
        window.deiconify()

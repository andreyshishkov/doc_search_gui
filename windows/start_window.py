import tkinter as tk
from .add_document_window import AddDocWindow
from .find_document_window import FindDocWindow


class StartWindow(tk.Tk):

    def __init__(
            self,
            width: int = 750,
            height: int = 600,
            program_name: str = 'Программа для учета документов'
    ):
        super().__init__()
        self.geometry(f'{width}x{height}')
        self.resizable(width=False, height=False)
        #self.config(bg='green')
        self.title(program_name)
        self.iconbitmap(default='icon.ico')

        self._buttons_width: int = 30
        self._buttons_height: int = 5
        self._buttons_font: int = 16

        self._create_background()
        self._create_buttons()

    def run(self):
        self.mainloop()

    def _create_background(self):
        background_image = tk.PhotoImage(file='background.png')
        background_label = tk.Label(self, image=background_image)
        background_label.image = background_image
        background_label.place(x=0, y=0, relheight=1, relwidth=1)

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
            command=self._call_find_doc_window,
        )
        self._outgoing_button.pack(side=tk.RIGHT, padx=40)

    def _call_add_doc_window(self):
        window = AddDocWindow(self)
        self.withdraw()
        window.deiconify()

    def _call_find_doc_window(self):
        window = FindDocWindow(self)
        self.withdraw()
        window.deiconify()

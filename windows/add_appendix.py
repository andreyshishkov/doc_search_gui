import tkinter as tk
import tkinter.filedialog as fd


class AddAppendixWindow(tk.Toplevel):

    def __init__(self,
                 parent=None,
                 doc_id: str = '',
                 width: int = 550,
                 height: int = 100,
                 window_name: str = 'Добавить приложение к документу',
                 ):
        super().__init__()
        self.geometry(f'{width}x{height}')
        self.resizable(width=False, height=False)
        self.title(window_name)

        self._doc_id = doc_id
        self._appendix_name = None
        self.default_appendix_name = None
        self.file_path = None

        self._create_widgets()

    def run(self):
        self.mainloop()

    def _create_widgets(self):
        self._create_label_input_appendix_name()
        self.create_choose_file_button()
        self.create_add_button()

    def _create_label_input_appendix_name(self):

        self._appendix_name = tk.Entry(
            self,
            width=47,
            font='TimesNewRoman 15',
        )
        self.default_appendix_name = True

        def handle_focus_in(_):
            if self.default_appendix_name:
                self._appendix_name.delete(0, tk.END)
                self._appendix_name.config(fg='black')
                self.default_appendix_name = False

        self._appendix_name.insert(0, 'Введите название приложения')
        self._appendix_name.config(fg='grey')

        self._appendix_name.bind("<FocusIn>", handle_focus_in)
        self._appendix_name.grid(row=0, column=0, padx=10, pady=15, columnspan=2)

    def choose_file(self):
        file_types = (
            ('Любой', '*'),
            ('Документ Word', '*.docx *.doc'),
            ('Текстовый файл', '*.txt'),
            ('PDF-документ', '*.pdf'),
            ('Изображение', '*.png *.jpg'),
        )
        filename = fd.askopenfilename(title='Выбрать файл', filetypes=file_types)
        self.file_path = filename

    def create_choose_file_button(self):
        button = tk.Button(
            self,
            text='Выбрать файл',
            width=20,
            font='TimesNewRoman 12',
            command=self.choose_file
        )
        button.grid(row=1, column=0)

    def create_add_button(self):
        button = tk.Button(
            self,
            text='Прикрепить к документу',
            bg='blue',
            fg='white',
            font='TimesNewRoman 12',
        )
        button.grid(row=1, column=1)

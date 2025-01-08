import os
import tkinter as tk
import tkinter.filedialog as fd
import shutil
from tkinter import messagebox as msgbox

from db.db_manager import DBManager


class AddDocWindow(tk.Tk):

    def __init__(self,
                 width: int = 600,
                 height: int = 300,
                 window_name: str = 'Добавить документ',
                 ):
        super().__init__()
        self.geometry(f'{width}x{height}')
        self.resizable(width=False, height=False)
        self.config(bg='gray')
        self.title(window_name)

        self.option_add('*Label*Font', 'Arial 15')
        self.option_add('*Button*Font', 'Arial 15')
        self.option_add('*Radiobutton*Font', 'Arial 15')

        self._label_filename = None
        self._input_filename = None
        self.is_income = None
        self.file_path = None
        self.default_text = True
        self.frame = tk.Frame(self)

        self.create_widgets()

    def run(self):
        self.mainloop()

    def grab_focus(self):
        self.grab_set()
        self.focus_set()
        self.wait_window()

    def create_widgets(self):
        self.create_label_input_filename()
        self.create_document_type_radiobuttons()
        self.create_choose_file_button()
        self.create_add_button()
        self.create_back_button()

    def create_label_input_filename(self):

        self._input_filename = tk.Entry(
            self,
            width=47,
            font='Arial 15',
        )
        self.default_text = True

        def handle_focus_in(_):
            if self.default_text:
                self._input_filename.delete(0, tk.END)
                self._input_filename.config(fg='black')
                self.default_text = False

        def handle_focus_out(_):
            # self._input_filename.delete(0, tk.END)
            # self._input_filename.config(fg='grey')
            # self._input_filename.insert(0, 'Введите название документа')
            self._input_filename.insert(0, self._input_filename.get())

        self._input_filename.insert(0, 'Введите название документа')
        self._input_filename.config(fg='grey')

        self._input_filename.bind("<FocusIn>", handle_focus_in)
        #self._input_filename.bind("<FocusOut>", handle_focus_out)
        #self._input_filename.bind("<Return>", handle_enter)
        self._input_filename.pack(anchor='n', pady=15)

    def create_document_type_radiobuttons(self):
        self.is_income = tk.BooleanVar()
        self.is_income.set(True)

        income_button = tk.Radiobutton(
            self.frame,
            text='Входящие',
            variable=self.is_income,
            value=True,
            width=21,
        )
        outcome_button = tk.Radiobutton(
            self.frame,
            text='Исходящие',
            variable=self.is_income,
            value=False,
            width=21,
        )

        income_button.grid(row=1, column=1)
        outcome_button.grid(row=1, column=2)

        self.frame.pack(pady=20)

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
            command=self.choose_file
        )
        button.pack()

    def create_add_button(self):
        button = tk.Button(
            self,
            text='Добавить',
            width=30,
            command=self.add_document_to_db
        )
        button.pack(pady=30)

    def add_document_to_db(self):
        if not self.file_path:
            msgbox.showwarning(
                'Не выбран документ для сохранения',
                'Выберите документ, который хотите сохранить',
            )
            return

        document_name = self._input_filename.get()
        if self.default_text:
            msgbox.showwarning(
                'Не введено имя файла',
                'Введите имя имя для файла, чтобы добавить его в базу данных'
            )
            return

        db_manager = DBManager()


        target_path_to_save = self.get_target_filename(document_name)
        self.copy_file(document_name)
        db_manager.add_document(
            name=document_name,
            path=target_path_to_save,
            is_income=self.is_income.get(),
        )
        msgbox.showinfo(
            'Операция завершена успешно',
            'Документ успешно добавлен в базу данных'
        )

    def copy_file(self, document_name: str) -> None:
        cur_path = os.getcwd()
        documents_path = os.path.join(cur_path, 'documents')

        if not os.path.exists(documents_path):
            os.makedirs('documents/income')
            os.makedirs('documents/outcome')

        target_path_to_save = self.get_target_filename(document_name)
        shutil.copyfile(self.file_path, target_path_to_save)

    def get_target_filename(self, document_name: str) -> str:
        cur_path = os.getcwd()
        documents_path = os.path.join(cur_path, 'documents')
        doc_type_dir = 'income' if self.is_income else 'outcome'
        target_path_to_save = os.path.join(documents_path, doc_type_dir)

        file_ext = self.file_path.split('.')[-1]
        file_name = document_name + '.' + file_ext

        target_path_to_save = os.path.join(target_path_to_save, file_name)
        return target_path_to_save

    def create_back_button(self):
        button = tk.Button(
            self,
            text='Назад',
            command=self.come_back_to_start_window,
        )
        button.pack()

    def come_back_to_start_window(self):
        from .start_window import StartWindow
        window = StartWindow()
        self.destroy()
        window.run()

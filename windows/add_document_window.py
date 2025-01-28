import os
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import tkinter.filedialog as fd
import shutil
from tkinter import messagebox as msgbox

from db.db_manager import DBManager


class AddDocWindow(tk.Toplevel):

    def __init__(self,
                 parent,
                 width: int = 600,
                 height: int = 400,
                 window_name: str = 'Добавить документ',
                 ):
        super().__init__()
        self.parent = parent
        self.geometry(f'{width}x{height}')
        self.resizable(width=False, height=False)
        self.title(window_name)

        self.option_add('*Label*Font', 'TimesNewRoman 15')
        self.option_add('*Button*Font', 'TimesNewRoman 15')
        self.option_add('*Radiobutton*Font', 'TimesNewRoman 15')

        self._label_filename = None
        self._input_filename = None
        self.is_income = None
        self.file_path = None
        self.default_text = True
        self.frame = tk.Frame(self)
        self._date_entry = None
        self._sender = None
        self._own_number = None
        self.style = ttk.Style(self)

        self.create_widgets()

    def run(self):
        self.mainloop()

    def grab_focus(self):
        self.grab_set()
        self.focus_set()
        self.wait_window()

    def create_widgets(self):
        self.create_label_input_filename()
        self.create_date_field()
        self.create_sender_field()
        self.create_own_number_doc_field()
        self.create_document_type_radiobuttons()
        self.create_choose_file_button()
        self.create_add_button()
        self.create_back_button()

    def create_label_input_filename(self):

        self._input_filename = tk.Entry(
            self,
            width=47,
            font='TimesNewRoman 15',
        )
        self.default_text = True

        def handle_focus_in(_):
            if self.default_text:
                self._input_filename.delete(0, tk.END)
                self._input_filename.config(fg='black')
                self.default_text = False

        self._input_filename.insert(0, 'Введите название документа')
        self._input_filename.config(fg='grey')

        self._input_filename.bind("<FocusIn>", handle_focus_in)
        self._input_filename.pack(anchor='n', pady=15)

    def create_date_field(self):
        frame = tk.Frame(self, width=47)
        label = tk.Label(
            frame,
            width=33,
            text='Дата документа:\t',
            anchor='w'
        )
        label.grid(row=0, column=0)
        self._date_entry = DateEntry(
            frame,
            date_pattern='yyyy-MM-dd',
            selectmode='day',
            font='Arial 15'
        )
        self._date_entry.grid(row=0, column=1)

        frame.pack()

    def create_sender_field(self):
        frame = tk.Frame(self, width=47)

        label = tk.Label(
            frame,
            anchor='w',
            width=27,
            text='От кого документ:\t'
        )
        label.grid(row=0, column=0)
        self._sender = tk.Entry(
            frame,
            width=20,
            font='TimesNewRoman 15'
        )
        self._sender.grid(row=0, column=1)

        frame.pack(pady=6)

    def create_own_number_doc_field(self):
        frame = tk.Frame(self, width=47)

        label = tk.Label(
            frame,
            anchor='w',
            width=27,
            text='За каким номером учтен:\t'
        )
        label.grid(row=0, column=0)
        self._own_number = tk.Entry(
            frame,
            width=20,
            font='TimesNewRoman 15'
        )
        self._own_number.grid(row=0, column=1)

        frame.pack()

    def create_document_type_radiobuttons(self):
        self.is_income = tk.BooleanVar()
        self.is_income.set(True)
        self.style.configure('TRadiobutton', font=(15,))

        income_button = ttk.Radiobutton(
            self.frame,
            text='Входящие',
            variable=self.is_income,
            value=True,
            width=10,
        )
        outcome_button = ttk.Radiobutton(
            self.frame,
            text='Исходящие',
            variable=self.is_income,
            value=False,
            width=10,
        )

        income_button.grid(row=1, column=1, padx=40)
        outcome_button.grid(row=1, column=2, padx=40)

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
        sender = self._sender.get()
        date = self._date_entry.get_date()
        own_number = self._own_number.get()
        self.copy_file(document_name)
        db_manager.add_document(
            name=document_name,
            path=target_path_to_save,
            is_income=self.is_income.get(),
            date=date,
            sender=sender,
            own_number=own_number,
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
        self.destroy()
        self.parent.deiconify()

import os
import tkinter as tk
from tkinter import ttk

from tkcalendar import DateEntry
import tkinter.filedialog as fd
import shutil
from tkinter import messagebox as msgbox
import uuid

from windows.add_appendix import AddAppendixWindow
from db.db_manager import DBManager


class AddDocWindow(tk.Toplevel):

    def __init__(self,
                 parent,
                 width: int = 600,
                 height: int = 500,
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
        self._signature_number = None
        self.style = ttk.Style(self)
        self.db_manager = DBManager()
        self.appendixes = []
        self.doc_id = self.generate_doc_id()

        self.create_widgets()

        self.bind('<Destroy>', self._kill_parent)

    def run(self):
        self.mainloop()

    def _kill_parent(self, event=None):
        if event.widget == self and self.parent.winfo_exists():
            self.parent.destroy()

    def grab_focus(self):
        self.grab_set()
        self.focus_set()
        self.wait_window()

    def create_widgets(self):
        self.create_label_input_filename()
        self.create_date_field()
        self.create_sender_field()
        self.create_own_number_doc_field()
        self.create_signature_number_field()
        self.create_document_type_radiobuttons()
        self.create_choose_file_and_add_appendix_buttons()
        self.create_add_button()
        self.create_back_button()

    @staticmethod
    def generate_doc_id() -> str:
        return str(uuid.uuid4())

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

    def create_signature_number_field(self):
        frame = tk.Frame(self)

        label = tk.Label(
            frame,
            anchor='w',
            width=27,
            text='Подписной номер:\t'
        )
        label.grid(row=0, column=0)
        self._signature_number = tk.Entry(
            frame,
            width=20,
            font='TimesNewRoman 15'
        )
        self._signature_number.grid(row=0, column=1)

        frame.pack(pady=6)

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

    def create_choose_file_and_add_appendix_buttons(self):
        frame = tk.Frame(self)
        self.create_choose_file_button(frame)
        self.create_add_appendix_button(frame)
        frame.pack()

    def create_choose_file_button(self, frame):
        button = tk.Button(
            frame,
            text='Выбрать документ',
            width=20,
            command=self.choose_file
        )
        button.grid(row=0, column=0, padx=10)

    def create_add_appendix_button(self, frame):
        button = tk.Button(
            frame,
            text='Добавить приложение',
            width=20,
            command=self._call_add_appendix_window,
        )
        button.grid(row=0, column=1, padx=10)

    def _call_add_appendix_window(self):
        appendix_window = AddAppendixWindow(self)
        appendix_window.focus()
        appendix_window.grab_set()

    def create_add_button(self):
        button = tk.Button(
            self,
            text='Добавить',
            width=30,
            bg='blue',
            fg='white',
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

        target_path_to_save = self.get_target_filename(document_name)
        sender = self._sender.get()
        date = self._date_entry.get_date()
        own_number = self._own_number.get()
        signature_number = self._signature_number.get()
        self.copy_file(target_path_to_save)
        self.db_manager.add_document(
            doc_id=self.doc_id,
            name=document_name.lower(),
            path=target_path_to_save,
            is_income=self.is_income.get(),
            date=date,
            sender=sender.lower(),
            doc_number=own_number.lower(),
            signature_number=signature_number.lower(),
        )

        for appendix in self.appendixes:
            self.add_appendix(self.doc_id, appendix.name, appendix.file_path)

        self.file_path = None
        self.appendixes = []
        self.doc_id = self.generate_doc_id()
        msgbox.showinfo(
            'Операция завершена успешно',
            'Документ успешно добавлен в базу данных'
        )

    def add_appendix(self, doc_id: str, appendix_name: str, source_path: str) -> None:
        target_path_to_save = self._get_target_path_to_save_appendix(appendix_name, source_path)
        shutil.copyfile(source_path, target_path_to_save)
        self.db_manager.add_appendix(
            doc_id=doc_id,
            name=appendix_name,
            file_path=target_path_to_save,
        )

    @staticmethod
    def _get_target_path_to_save_appendix(appendix_name: str, source_path: str) -> str:
        cur_dir = os.getcwd()
        target_dir = os.path.join(cur_dir, 'documents', 'appendixes')
        file_ext = source_path.split('.')[-1]
        random_element = uuid.uuid4().hex[:4]
        filename = appendix_name + '_' + random_element + '.' + file_ext
        target_path_to_save = os.path.join(target_dir, filename)
        return target_path_to_save

    def copy_file(self, target_path_to_save) -> None:
        cur_path = os.getcwd()
        documents_path = os.path.join(cur_path, 'documents')

        if not os.path.exists(documents_path):
            os.makedirs(os.path.join(documents_path, 'income'))
            os.makedirs(os.path.join(documents_path, 'outcome'))
            os.makedirs(os.path.join(documents_path, 'appendixes'))

        shutil.copyfile(self.file_path, target_path_to_save)

    def get_target_filename(self, document_name: str) -> str:
        cur_path = os.getcwd()
        documents_path = os.path.join(cur_path, 'documents')
        doc_type_dir = 'income' if self.is_income else 'outcome'
        target_path_to_save = os.path.join(documents_path, doc_type_dir)

        random_element = uuid.uuid4().hex[:4]
        file_ext = self.file_path.split('.')[-1]
        file_name = document_name + '_' +  random_element + '.' + file_ext

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
        from .start_window import StartWindow
        window = StartWindow()
        window.run()

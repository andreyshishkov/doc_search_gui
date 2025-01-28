import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msgbox
from enum import Enum
from db.db_manager import DBManager
from datetime import datetime
import pathlib
import os
import platform
import subprocess
from .exceptions import WrongDateFormatError


class Criteria(Enum):
    DOC_NUM = 'За каким номер пришел документ'
    INNER_NUM = 'Внутренний номер документа'
    OWNER = 'От кого пришел документ'
    DATE = 'Дата (день.месяц.год)'



class FindDocWindow(tk.Toplevel):

    def __init__(self,
                 parent,
                 width: int = 800,
                 height: int = 600,
                 window_name: str = 'Найти документ',
                 ):
        super().__init__()
        self.geometry(f'{width}x{height}')
        self.title(window_name)

        self.option_add('*Label*Font', 'Arial 15')
        self.option_add('*Button*Font', 'Arial 15')
        self.option_add('*Radiobutton*Font', 'Arial 15')

        self.parent = parent
        self.criteria = None
        self.result_tree = None

        self.create_widgets()

        self.bind('<Destroy>', self._kill_parent)

    def run(self):
        self.mainloop()

    def _kill_parent(self, event=None):
        if event.widget == self and self.parent.winfo_exists():
            self.parent.destroy()

    def create_widgets(self):
        self.create_params_frame()
        self.create_search_results_frame()
        self._create_back_button()

    def create_params_frame(self):
        params_frame = ttk.LabelFrame(self, text="Выберите критерий поиска и введите значение", padding=20)

        self._create_criteria_field(params_frame)
        self._create_input_criteria(params_frame)
        self._create_doc_type_field(params_frame)
        self._create_search_button(params_frame)

        params_frame.columnconfigure(1, weight=1)
        params_frame.pack(side=tk.TOP, fill='x', pady=15)

    def _create_back_button(self):
        button = ttk.Button(
            self,
            text='Назад в главное меню',
            command=self.come_back_to_start_window,
        )
        button.pack()

    def come_back_to_start_window(self):
        self.destroy()
        self.parent.deiconify()

    def _create_doc_type_field(self, frame):

        self.is_income = tk.BooleanVar()
        self.is_income.set(False)

        income_button = ttk.Radiobutton(frame, text='Входящие', variable=self.is_income, value=True)
        outcome_button = ttk.Radiobutton(frame, text='Исходящие', variable=self.is_income, value=False)

        income_button.grid(row=2, column=0, pady=10)
        outcome_button.grid(row=2, column=1, pady=10)

    def _create_criteria_field(self, frame):
        criteria_label = ttk.Label(frame, text='Критерий:\t')
        criteria_label.grid(row=0, column=0)

        criteria_list = [
            Criteria.DOC_NUM.value,
            Criteria.INNER_NUM.value,
            Criteria.DATE.value,
            Criteria.OWNER.value,
        ]
        self.criteria = tk.StringVar(value=criteria_list[0])
        combobox = ttk.Combobox(frame, state='readonly', values=criteria_list, textvariable=self.criteria)
        combobox.grid(row=0, column=1, sticky=tk.EW, padx=10)

    def _create_input_criteria(self, frame):
        criteria_input_label = ttk.Label(frame, text='Значение поиска')
        self.search_value = tk.StringVar()
        criteria_input = ttk.Entry(frame, textvariable=self.search_value)

        criteria_input_label.grid(row=1, column=0, pady=15)
        criteria_input.grid(row=1, column=1, sticky=tk.EW, padx=10)

    def _create_search_button(self, frame):
        button = ttk.Button(frame, text='Поиск', command=self._show_search_results)
        button.grid(row=2, column=2)

    def create_search_results_frame(self):
        results_frame = ttk.LabelFrame(self, text='Результаты поиска', padding=20)
        self.result_tree = ttk.Treeview(
            results_frame,
            columns=(1, 2, 3, 4, 5),
            show='headings',
            height=10,
            selectmode='browse'
        )
        self.result_tree.heading(1, text='Номер док-та (нач.)')
        self.result_tree.heading(2, text='Дата')
        self.result_tree.heading(3, text='Внутренний номер')
        self.result_tree.heading(4, text='Отправитель')
        self.result_tree.heading(5, text='Путь к файлу')

        self.result_tree.column(1, width=120, anchor='center')
        self.result_tree.column(2, width=120, anchor='center')
        self.result_tree.column(3, width=120, anchor='center')
        self.result_tree.column(4, width=120, anchor='center')

        self.result_tree.bind('<Double-1>', self.doubleclick_record)

        self.result_tree.pack(side=tk.TOP, expand='yes', fill='both')
        results_frame.pack(expand='yes', fill='both')

    def _show_search_results(self):
        self.result_tree.delete(*self.result_tree.get_children())

        try:
            documents = self.__get_search_results()
        except WrongDateFormatError:
            msgbox.showwarning(
                'Неверный формат ввода даты',
                'Введено некорректное значение даты, введите корректное значение. Пример: 01.01.2020'
            )
            return
        if not documents:
            msgbox.showinfo(
                'Ничего не найдено',
                'По вашему запросу ничего не найдено. Проверьте корректность введенных данных'
            )
            return

        for document in documents:
            doc_time = document.date.strftime('%d.%m.%Y')
            doc_record = (document.name, doc_time, document.own_number, document.sender, document.path)
            self.result_tree.insert('', 'end', values=doc_record)

    def __get_search_results(self):
        db_manager = DBManager()

        is_income = self.is_income.get()
        search_value = self.search_value.get()
        criteria = self.criteria.get()
        if criteria == Criteria.DOC_NUM.value:
            results = db_manager.get_doc_by_name(search_value, is_income)
        elif criteria == Criteria.OWNER.value:
            results = db_manager.get_doc_by_sender(search_value, is_income)
        elif criteria == Criteria.DATE.value:
            try:
                search_value = datetime.strptime(search_value, '%d.%m.%Y').date()
            except ValueError:
                raise WrongDateFormatError
            results = db_manager.get_doc_by_date(search_value, is_income)
        elif criteria == Criteria.INNER_NUM.value:
            results = db_manager.get_doc_by_inner_num(search_value, is_income)
        else:
            raise ValueError
        return results

    def doubleclick_record(self, event=None):
        id_ = self.result_tree.selection()
        if id_:
            self._show_selected_result(id_)

    def _show_selected_result(self, id_item):
        record = self.result_tree.item(id_item, 'values')
        path = pathlib.Path(record[-1]).absolute()
        if platform.system() == 'Windows':
            os.startfile(path)
        else:
            subprocess.call(['xdg-open', path])

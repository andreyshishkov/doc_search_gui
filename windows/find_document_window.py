import tkinter as tk
from tkinter import ttk
from enum import Enum


class Criteria(Enum):
    DOC_NUM = 'За каким номер пришел документ'
    INNER_NUM = 'Внутренний номер документа'
    OWNER = 'От кого пришел документ'
    DATE = 'Дата (день.месяц.год)'



class FindDocWindow(tk.Tk):

    def __init__(self,
                 width: int = 800,
                 height: int = 400,
                 window_name: str = 'Найти документ',
                 ):
        super().__init__()
        self.geometry(f'{width}x{height}')
        self.title(window_name)

        self.option_add('*Label*Font', 'Arial 15')
        self.option_add('*Button*Font', 'Arial 15')
        self.option_add('*Radiobutton*Font', 'Arial 15')

        self.criteria = None

        self.create_widgets()

    def run(self):
        self.mainloop()

    def create_widgets(self):
        self.create_params_frame()
        self.create_search_results_frame()

    def create_params_frame(self):
        label_frame = ttk.LabelFrame(self, text="Выберите критерий поиска и введите значение", padding=20)

        self._create_criteria_field(label_frame)
        self._create_input_criteria(label_frame)
        self._create_doc_type_field(label_frame)
        self._create_search_button(label_frame)

        label_frame.columnconfigure(1, weight=1)
        label_frame.pack(side=tk.TOP, fill='x', pady=15)

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
        combobox = ttk.Combobox(frame, values=criteria_list, textvariable=self.criteria)
        combobox.grid(row=0, column=1, sticky=tk.EW, padx=10)

    def _create_input_criteria(self, frame):
        criteria_input_label = ttk.Label(frame, text='Значение поиска')
        self.search_value = tk.StringVar()
        criteria_input = ttk.Entry(frame, textvariable=self.search_value)

        criteria_input_label.grid(row=1, column=0, pady=15)
        criteria_input.grid(row=1, column=1, sticky=tk.EW, padx=10)

    def _create_search_button(self, frame):
        button = ttk.Button(frame, text='Поиск')
        button.grid(row=2, column=2)

    def create_search_results_frame(self):
        results_frame = ttk.LabelFrame(self, text='Результаты поиска', padding=20)
        result_tree = ttk.Treeview(
            results_frame,
            columns=(1, 2, 3, 4, 5),
            show='headings',
            height=10,
            selectmode='browse'
        )
        result_tree.heading(1, text='Номер документа')
        result_tree.heading(2, text='Дата')
        result_tree.heading(3, text='Внутренний номер\nдокумента')
        result_tree.heading(4, text='Отправитель')
        result_tree.heading(5, text='Путь к файлу')

        result_tree.column(1, width=120, anchor='center')
        result_tree.column(2, width=120, anchor='center')
        result_tree.column(3, width=120, anchor='center')
        result_tree.column(4, width=120, anchor='center')

        result_tree.pack(side=tk.TOP, expand='yes', fill='both')
        results_frame.pack(expand='yes', fill='both')

if __name__ == '__main__':
    window = FindDocWindow()
    window.run()

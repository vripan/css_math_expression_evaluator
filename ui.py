from ast import Expression
import tkinter as tk
from tkinter import messagebox as tk_messagebox
from tkinter import filedialog as tk_filedialog
from types import SimpleNamespace
from data_validator import DataValidator
from ui_strings import Strings
from ui_config import Config
from simple_xml import SimpleXML

import os

def command(func, *args, **kwargs): # pragma: no cover
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as exc:
            args = exc.args[1:]
            args = args[::-1]
            msg = "When " + "\n  then ".join(args) + "\nexception occured:\n  " + str(exc.args[0])

            tk_messagebox.showerror("Runtime error", msg)

            raise

    inner.__undecorated__ = func
    return inner

class ExceptionContext:
    def __init__(self, *args):
        self.args = args

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
       if type is not None:
          value.args += self.args
          return False
        

class MathExpressionEvaluatorUi(tk.Frame):
    def __init__(self, master, backend, open_file_callback=tk_filedialog.askopenfile, save_file_as_callback=tk_filedialog.asksaveasfilename, ):
        super().__init__(master)
        
        self.backend = backend
        self.open_file_callback = open_file_callback
        self.save_file_as_callback = save_file_as_callback

        self.master.title(Strings.APP_TITLE)
        self.master.geometry(self.__build_geometry_str())
        self.master.resizable(Config.RESIZEABLE_HEIGHT, Config.RESIZEABLE_WIDTH)
        self.master.config(menu=self.__build_menu_bar())

        self.__build_exponent_widget()
        self.__build_expression_widget()
        self.__build_vars_widget()
        self.__build_result_widget()
        self.__build_steps_widget()
        self.__build_compute_widget()

        self.pack()

        self.exponent_value(self.backend.exponent())

    def __build_geometry_str(self):
        coord_x = (self.master.winfo_screenwidth() - Config.WIDTH) // 2
        coord_y = (self.master.winfo_screenheight() - Config.HEIGHT) // 2
        return f"{Config.WIDTH}x{Config.HEIGHT}+{coord_x}+{coord_y}"
        
    def __build_menu_bar(self):
        bar = tk.Menu(self.master)

        file = tk.Menu(bar, tearoff=0)
        file.add_command(label=Strings.OPEN_XML_COMMAND, command=self.__command_open_xml_file)
        file.add_command(label=Strings.SAVE_XML_COMMAND, command=self.__command_save_xml_file)
        file.add_command(label=Strings.RUN_XML_COMMAND, command=self.__command_run_xml_file)
        file.add_separator()
        file.add_command(label=Strings.EXIT_COMMAND, command=self.__command_exit)
        bar.add_cascade(label=Strings.FILE_CASCADE_MENU, menu=file)

        return bar    

    def __build_exponent_widget(self):
        self.exponent = SimpleNamespace()
        
        self.exponent.frame = tk.LabelFrame(self.master, text=Strings.WIDGET_EXPONENT_TITLE, width=480)
        self.exponent.label = tk.Label(self.exponent.frame, text=Strings.WIDGET_EXPONENT_DESCRIPTION, state=tk.DISABLED).pack(anchor=tk.W)
        self.exponent.box = tk.Entry(self.exponent.frame)
        
        self.exponent.box.pack(side=tk.TOP, fill=tk.X, padx=5, pady=(0,5), expand=False)
        self.exponent.frame.pack(fill=tk.X, padx=10) 

    def __build_expression_widget(self):
        self.expression = SimpleNamespace()
        
        self.expression.frame = tk.LabelFrame(self.master, text=Strings.WIDGET_EXPRESSION_TITLE, width=480)
        self.expression.label = tk.Label(self.expression.frame, text=Strings.WIDGET_EXPRESSION_DESCRIPTION, state=tk.DISABLED)
        self.expression.box = tk.Entry(self.expression.frame)
        
        self.expression.label.pack(anchor=tk.W)
        self.expression.box.pack(side=tk.TOP, fill=tk.X, padx=5, pady=(0,5), expand=False)
        self.expression.frame.pack(fill=tk.X, padx=10) 

    def __build_vars_widget(self):
        self.vars = SimpleNamespace()
        self.vars.frame = tk.LabelFrame(self.master, text=Strings.WIDGET_VARIABLES_TITLE, width=200)

        self.vars.header_frame = tk.Frame(self.vars.frame)
        tk.Label(self.vars.header_frame, text=Strings.WIDGET_VARIABLES_DESCRIPTION, state=tk.DISABLED).pack(anchor=tk.W, side=tk.LEFT)
        tk.Button(self.vars.header_frame, text="+", command=self.__add_var_fields, height=1, borderwidth=0).pack(anchor=tk.E, side=tk.RIGHT)
        self.vars.header_frame.pack(side=tk.TOP, fill=tk.X)
        
        p_frame = tk.Frame(self.vars.frame)
        self.vars.canvas = tk.Canvas(p_frame, borderwidth=0, background=Config.UI_BACKGROUND_COLOR, highlightthickness=0, height=73)
        self.vars.canvas_frame = tk.Frame(self.vars.canvas, background=Config.UI_BACKGROUND_COLOR)
        vsb = tk.Scrollbar(p_frame, orient=tk.VERTICAL, command=self.vars.canvas.yview)
        self.vars.canvas.configure(yscrollcommand=vsb.set)

        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.vars.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.vars.canvas.create_window((0,0), window=self.vars.canvas_frame, anchor=tk.NW)
        self.vars.canvas_frame.bind("<Configure>", lambda _: self.vars.canvas.configure(scrollregion=self.vars.canvas.bbox("all")))
        
        self.vars.fields = []
        self.__add_var_fields()

        p_frame.pack(side=tk.TOP, fill=tk.X)
        self.vars.frame.pack(fill=tk.X, padx=10) 

    def __add_var_fields(self):
        ff = tk.Frame(self.vars.canvas_frame)
        vars_box_name = tk.Entry(ff, width=15)
        vars_box_name.pack(padx=5, pady=(0,5), fill=tk.BOTH, side=tk.LEFT)
        vars_box_value = tk.Entry(ff, width=57)
        vars_box_value.pack(padx=(5,7), pady=(0,5), expand=True, fill=tk.BOTH, side=tk.RIGHT)
        ff.pack(expand=True, fill=tk.X)
        
        self.vars.fields.append((vars_box_name, vars_box_value))

    def __build_result_widget(self):
        self.result = SimpleNamespace()
        self.result.frame = tk.LabelFrame(self.master, text=Strings.WIDGET_RESULT_TITLE, width=480)
        self.result.box = tk.Entry(self.result.frame)
          
        self.result.box.bind("<Button-1>", lambda e: "break")
        self.result.box.bind("<Key>", lambda e: "break")
        
        self.result.box.pack(side=tk.TOP, fill=tk.X, padx=5, pady=(5,5), expand=False)
        self.result.frame.pack(fill=tk.X, padx=10) 

    def __build_steps_widget(self):
        self.steps = SimpleNamespace()
        self.steps.frame = tk.LabelFrame(self.master, text=Strings.WIDGET_STEPS_TITLE, width=480)
        self.steps.box = tk.Text(self.steps.frame)
        
        self.steps.box.pack(side=tk.TOP, fill=tk.X, padx=5, pady=(5, 5), expand=False)
        self.steps.frame.pack(fill=tk.X, padx=10) 

    def __build_compute_widget(self):
        self.compute = SimpleNamespace()
        self.compute.button = tk.Button(self.master, text=Strings.WIDGET_COMPUTE_TITLE, command=self.__command_compute)

        self.compute.button.pack(side=tk.TOP, fill=tk.X, padx=10, pady=15)

    @command
    def __command_open_xml_file(self):
        with ExceptionContext("opening xml file"):
            filename = self.open_file_callback(title=Strings.FILE_DIALOG_TITLE, filetypes=Config.FILE_DIALOG_FILETYPES)
            
            if filename is None:
                return

            with ExceptionContext("loading xml file"):
                expression, variables = SimpleXML.load(filename.name)

            with ExceptionContext("setting GUI from xml"):
                self.expression_value(expression)
                self.variables_value(variables)

            return filename.name

    @command
    def __command_save_xml_file(self):
        with ExceptionContext("saving xml file"):
            filename = self.save_file_as_callback()
            self.__save_to(filename)

    def __save_to(self, filename):
        with ExceptionContext("reading GUI fields"):
            expression = self.expression_value()
            variables = self.variables_value()
            result = self.result_value()
            steps = self.steps_value()

        with ExceptionContext("writting to file"):
            SimpleXML.save(filename, expression, variables, result, steps)

        return True

    @command
    def __command_run_xml_file(self): # pragma: no cover 
        with ExceptionContext("running xml file"):
            filename = self.__command_open_xml_file.__undecorated__(self)
            
            name, ext = os.path.splitext(filename)
            out_filename = name + "_out" + ext

            self.__command_compute.__undecorated__(self)
            self.__save_to(out_filename)

    @command
    def __command_exit(self): # pragma: no cover
        self.master.destroy()
    
    @command
    def __command_compute(self):
        with ExceptionContext("loading data from GUI"):
            expression = self.expression_value()
            variables = self.variables_value()
            exponent = self.exponent_value()

        with ExceptionContext("computing math expression"):
            result, steps = self.backend.compute_data(expression, list(variables.items()), int(exponent))

        with ExceptionContext("display results in GUI"):
            self.result_value(result)
            self.steps_value(steps)

    def exponent_value(self, value=None):
        """Set or get exponent field"""

        with ExceptionContext("reading exponent field"):
            if value is None:
                value = self.exponent.box.get()
                DataValidator.is_unsigned_integer(value)
                DataValidator.is_not_zero(value)
                return value
        
        with ExceptionContext("setting exponent field"):
            DataValidator.is_unsigned_integer(value)
            DataValidator.is_not_zero(value)
            self.exponent.box.delete(0, tk.END)
            self.exponent.box.insert(0, value)

    def expression_value(self, value=None):
        """Set or get expression field"""

        with ExceptionContext("reading math expression field"):
            if value is None:
                value = self.expression.box.get()
                DataValidator.is_math_expression(value)
                DataValidator.is_not_empty(value)
                return value

        with ExceptionContext("setting math expression field"):
            DataValidator.is_math_expression(value)
            DataValidator.is_not_empty(value)
            self.expression.box.delete(0, tk.END)
            self.expression.box.insert(0, value)

    def variables_value(self, var_list=None):
        """Set or get expression variables fields"""

        with ExceptionContext("reading variables fields"):
            if var_list is None:
                vars = {}
                for var_box, value_box in self.vars.fields:
                    name = var_box.get()
                    value = value_box.get()

                    if len(name) == 0:
                        continue

                    DataValidator.is_expression_variable(name)
                    DataValidator.is_unsigned_integer(value)

                    if name in vars:
                        raise Exception("variables not unique")

                    vars[name] = value
                return vars

        with ExceptionContext("setting variables fields"):
            while len(self.vars.fields) < len(var_list):
                self.__add_var_fields()

            for var_box, value_box in self.vars.fields:
                var_box.delete(0, tk.END)
                value_box.delete(0, tk.END)

            for idx, var  in enumerate(var_list.items()):
                name, value = var
                var_box, value_box = self.vars.fields[idx]

                DataValidator.is_expression_variable(name)
                DataValidator.is_unsigned_integer(value)

                var_box.delete(0, tk.END)
                var_box.insert(0, name)

                value_box.delete(0, tk.END)
                value_box.insert(0, value)

    def steps_value(self, value=None):
        """Set or get steps field"""

        with ExceptionContext("reading steps text area"):
            if value is None:
                value = self.steps.box.get(1.0, tk.END)
                value = value.strip('\n')
                return value
        
        with ExceptionContext("setting steps text area"):
            self.steps.box.delete(1.0, tk.END)
            self.steps.box.insert(1.0, value)

    def result_value(self, value=None):
        """Set or get result field"""

        with ExceptionContext("reading result field"):
            if value is None:
                value = self.result.box.get()
                DataValidator.is_unsigned_integer(value)
                return value
        
        with ExceptionContext("setting result field"):
            DataValidator.is_unsigned_integer(value)
            self.result.box.delete(0, tk.END)
            self.result.box.insert(0, value)

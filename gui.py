from calendar import c
from email.policy import default
from tkinter.ttk import Scrollbar, Treeview
from typing import List
from algorithm import ComputerGenerator
from models import Computer,  UserPreferences
from tkinter import BOTH, END, EXTENDED, LEFT, MULTIPLE, SINGLE, VERTICAL, W, Y, Label, Listbox, Entry, Button, messagebox
import matplotlib.pyplot as plt
import numpy as np

class ComputerGeneratorGUI:

    def __init__(self, master):
        self.master = master
        self.setup_gui()

    def setup_gui(self):
        self.master.title("Generador  de computadoras")
        self.master.geometry("1000x800")
        self.master.configure(background='white')


        def usage_option_changed(event):
            if listbox.curselection(): #Precios minimo-Max
                usage_selected = computer_usages[listbox.curselection()[0]]
                match(usage_selected):
                    case 'ofimática':
                        price_start_range.delete(0, END)
                        price_start_range.insert(0, "8000")
                    case 'juegos':
                        price_start_range.delete(0, END)
                        price_start_range.insert(0, "10000")
                    case 'diseño gráfico':
                        price_start_range.delete(0, END)
                        price_start_range.insert(0, "15000")
                    case 'edición de video':
                        price_start_range.delete(0, END)
                        price_start_range.insert(0, "18000")
                    case 'navegación web':
                        price_start_range.delete(0, END)
                        price_start_range.insert(0, "5000")
                    case 'educación':
                        price_start_range.delete(0, END)
                        price_start_range.insert(0, "8000")
                    case 'arquitectura':
                        price_start_range.delete(0, END)
                        price_start_range.insert(0, "20000")
                    case _:
                        print('Debe seleccionar un uso de la computadora')


        def execute_algorithm():
            price_range: tuple = (int(price_start_range.get()),
                             int(price_end_range.get()))
            
            is_option_selected = listbox.curselection()
            usage_selected = ""
            if(is_option_selected):
                usage_selected = computer_usages[is_option_selected[0]]

            population_size = int(population_size_entry.get())
            cross_over_rate = float(cross_over_rate_entry.get())
            mutation_rate = float(mutation_rate_entry.get())
            generations = int(generations_entry.get())

            if price_range[1] < price_range[0]:
                messagebox.showerror('Error', 'El rango de precio no es valido')
                return

            if usage_selected:
                generator = ComputerGenerator(population_size, cross_over_rate, mutation_rate, generations, UserPreferences(min_price=price_range[0], max_price=price_range[1], usage=usage_selected))

                best_computer = generator.run()#EJECUTO
                self.display_computer(best_computer)
                self.graph(generator)
            else:
                messagebox.showerror('Error', 'Debe seleccionar un uso de la computadora')

        price_range_label = Label(self.master, text="Rango de precio:")
        price_range_label.grid(row=0, column=0, padx=10, pady=10)
        price_start_range = Entry(self.master)
        price_start_range.insert("end", "10000")
        price_start_range.grid(row=1, column=0, padx=10, pady=10)
        price_end_range = Entry(self.master)
        price_end_range.insert("end", "15000")
        price_end_range.grid(row=1, column=1, padx=10, pady=10)

        population_size_label = Label(self.master, text="Tamaño de la población:")
        population_size_label.grid(row=0, column=2, padx=10, pady=10)
        population_size_entry = Entry(self.master)
        population_size_entry.insert("end", "4")
        population_size_entry.grid(row=1, column=2, padx=10, pady=10)

        cross_over_rate_label = Label(self.master, text="Probabilidad de cruce:")
        cross_over_rate_label.grid(row=2, column=2, padx=10, pady=10)
        cross_over_rate_entry = Entry(self.master)
        cross_over_rate_entry.insert("end", "0.5")
        cross_over_rate_entry.grid(row=3, column=2, padx=10, pady=10)

        mutation_rate_label = Label(self.master, text="Probabilidad de mutación:")
        mutation_rate_label.grid(row=0, column=3, padx=10, pady=10)
        mutation_rate_entry = Entry(self.master)
        mutation_rate_entry.insert("end", "0.01")
        mutation_rate_entry.grid(row=1, column=3, padx=10, pady=10)
        
        generations_label = Label(self.master, text="Número de generaciones:")
        generations_label.grid(row=2, column=3, padx=10, pady=10)
        generations_entry = Entry(self.master)
        generations_entry.insert("end", "100")
        generations_entry.grid(row=3, column=3, padx=10, pady=10)

        computer_usages = ['ofimática', 'juegos', 'diseño gráfico', 'edición de video', 'navegación web', 'educación', 'arquitectura']

        listbox = Listbox(self.master, selectmode=SINGLE)
        for usage in computer_usages:
            listbox.insert(END, usage)
        listbox.grid(row=2, column=0, padx=10, pady=10)
        listbox.bind("<<ListboxSelect>>", usage_option_changed)

        get_all_data_button = Button(
            self.master, text="Generar computadora", command=execute_algorithm)
        get_all_data_button.grid(row=3, column=0, columnspan=2, pady=10)




    def run(self):
        self.master.resizable(False, False)
        self.master.mainloop()


    
    def graph(self, ga: ComputerGenerator):
        best_cases = []
        worst_cases = []
        avg_cases = []
        
        for i in range(ga.generations):
            best_cases.append(ga.best_cases[i].fitness)
            worst_cases.append(ga.worst_cases[i].fitness)
            avg_cases.append(ga.avg_cases[i])
            
        plt.plot(np.arange(0, ga.generations), best_cases, label="Mejores aptitud")
        plt.plot(np.arange(0, ga.generations), worst_cases, label="Peores aptitud")
        plt.plot(np.arange(0, ga.generations), avg_cases, label="Aptitud promedio")
        plt.legend()
        plt.title("Evolución de la población")
        plt.xlabel("Generaciones/Iteraciones")
        plt.ylabel("Valor de aptitud")
        plt.show()
        
    def display_computer(self, computer:Computer):
        tree = Treeview(self.master, columns=('Modelo',))
        tree.heading('#0', text='Componentes')
        tree.heading('#1', text='Modelo')

        tree.column('#1', width=600) 
        # Insertar datos en el Treeview
        tree.insert('', 'end', text='CPU', values=(str(computer.cpu),))
        tree.insert('', 'end', text='GPU', values=(str(computer.gpu),))
        tree.insert('', 'end', text='RAM', values=(str(computer.ram),))
        tree.insert('', 'end', text='Almacenamiento', values=(str(computer.storage),))
        tree.insert('', 'end', text='Motherboard', values=(str(computer.motherboard),))
        tree.insert('', 'end', text='PSU', values=(str(computer.psu),))

        tree.grid(row=4, column=0, columnspan=10)
        total_price_label = Label(self.master, text=f"Total: {computer.price:.2f}")
        total_price_label.grid(row=5, column=0, padx=10, pady=10)

import tkinter as tk

class Application(tk.Frame):

	def __init__(self, master):
		tk.Frame.__init__(self, master)

		self.input_text = tk.Text(self, wrap="word", height=50)
		self.input_text.grid(row=0, column=0)
		
		self.output_text = tk.Text(self, wrap="word", height=50)
		self.output_text.grid(row=0, column=1)
		
		self.button_holder = tk.Frame(self)
		self.button_holder.grid(row=1, column=0, sticky="W")

		self.create_clean_button = tk.Button(self.button_holder, 
																text="Create Clean",
																padx=10,
																pady=5,
																command=self._generate_class)
		self.create_clean_button.grid(row=0, column=0, padx=10, pady=5)

		self.create_dirty_button = tk.Button(self.button_holder, 
																text="Create Dirty",
																padx=10,
																pady=5,
																command=self._generate_class)
		self.create_dirty_button.grid(row=0, column=1, padx=10, pady=5)
		
	def _generate_class(self):
		self.output_text.delete(1.0, tk.END)
		self.output_text.insert(1.0, self.input_text.get(1.0, tk.END))
		print("Im trying")
		
		
root = tk.Tk()
app = Application(root).pack(side="top", fill="both", expand=True)

root.mainloop()
#!/user/bin/python
"""Credit to David Monts, circa 2017

The JSON Class Designer!!!
"""

import json
import tkinter as tk
from jcu import Jcu

class Application(tk.Frame):
    """Provides a wrapper interface to the JSON Class utility.
    """

    class Input_types:
        """Either the JSON input should be in the form of the currently
        supported JSON schema which we call "clean", or it should be
        as written which we call "dirty".
        """

        DIRTY = "dirty"
        CLEAN = "clean"

    def __init__(self, master):
        """Create the necessary Graphical elements
        """

        self.jcutil = Jcu()
        self.file_array = []

        tk.Frame.__init__(self, master)

        self.input_text = tk.Text(self, wrap="word")
        self.input_text.grid(row=0, column=0)

        self.output_text = tk.Text(self, wrap="word")
        self.output_text.grid(row=0, column=1)

        self.button_holder = tk.Frame(self)
        self.button_holder.grid(row=1, column=0, sticky="W")

        self.create_clean_button = tk.Button(self.button_holder,
                                             text="Create Clean",
                                             padx=10,
                                             pady=5,
                                             command=self._generate_class_clean)
        self.create_clean_button.grid(row=0, column=0, padx=10, pady=5)

        self.create_dirty_button = tk.Button(self.button_holder,
                                             text="Create Dirty",
                                             padx=10,
                                             pady=5,
                                             command=self._generate_class_dirty)
        self.create_dirty_button.grid(row=0, column=1, padx=10, pady=5)

        # Create the picker for the desired programming language
        self.language_opt = tk.StringVar(self.button_holder)
        self.language_opt.set("python")

        self.language_OptionMenu = tk.OptionMenu(self.button_holder,
                                                 self.language_opt,
                                                 "python",
                                                 "csharp",
                                                 "cpp")
        self.language_OptionMenu.grid(row=0, column=2, padx=10, pady=5)

        self.selection_holder = tk.Frame(self)
        self.selection_holder.grid(row=1, column=1, sticky="W")

        self.files = tk.StringVar(self.selection_holder)
        self.files.set("")

        self.files_OptionMenu = tk.OptionMenu(self.selection_holder, self.files, "")
        self.files_OptionMenu.grid(row=0, column=1, padx=10, pady=5)

        self.show_files = tk.Button(self.selection_holder,
                                    text="Show class",
                                    padx=10,
                                    pady=5,
                                    command=self._show_file_contents)
        self.show_files.grid(row=0, column=0, padx=10, pady=5)

    def _show_file_contents(self):
        """Find the selected file and show the contents of that file in the output window.
        """
        self.output_text.delete(1.0, tk.END)
        for file in self.file_array:
            next_file = self.files.get()
            if file.file_name == next_file:
                self.output_text.insert(1.0, file.file_contents)
                break

    def _generate_class_dirty(self):
        """Generate classes assuming the input json is in the dirty form
        """
        self._generate_class(self.Input_types.DIRTY)

    def _generate_class_clean(self):
        """Generate classes assuming the input json is in the clean form
        """
        self._generate_class(self.Input_types.CLEAN)

    def _generate_class(self, input_type):
        """Generate classes for the JSON and load the first class into the output screen.
        Also fill in the option menu for the output screen.

        Args:
            input_type (Input_types) - Either clean or dirty.
        """

        try:
            json_info = json.loads(self.input_text.get(1.0, tk.END))
            self.file_array = []
            if input_type == self.Input_types.CLEAN:
                self.file_array.extend(self.jcutil.create_classes_clean(json_info,
                                                                        self.language_opt.get()))
            else:
                self.file_array.extend(self.jcutil.create_classes_dirty(json_info,
                                                                        "todo",
                                                                        self.language_opt.get()))
            if self.file_array:
                print(self.language_opt.get())
                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(1.0, self.file_array[0].file_contents)

                file_names_list = [get[0] for get in self.file_array]
                print(file_names_list)

                menu_options = self.files_OptionMenu.children["menu"]
                menu_options.delete(0, 'end')
                self.files.set('')
                for files in file_names_list:
                    menu_options.add_command(label=files, command=tk._setit(self.files, files))
                self.files.set(file_names_list[0])
            else:
                self.output_text.insert(tk.END, "Got here with nothing")
        except json.JSONDecodeError as json_decode_error:
            self.output_text.delete(1.0,
                                    tk.END)
            self.output_text.insert(1.0,
                                    "Invalid JSON file at line " + str(json_decode_error.lineno))


if __name__ == '__main__':
    ROOT = tk.Tk()
    APP = Application(ROOT).pack(side="top", fill="both", expand=True)
    ROOT.mainloop()

import gtts
import os

from slugify import slugify
import tkinter as tk

from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showerror
from playsound import playsound


ACC_AUSTRALIA = "com.au"
ACC_UK = "co.uk"
ACC_USA = "com"
ACC_CANADIAN = "ca"
ACC_INDIAN = "co.in"
ACC_IRISH = "ie"
ACC_AFRICAN = "co.za"
ACC_FR_CANADA = "ca"
ACC_FRENCH = "fr"


class MainWindow(tk.Tk):
    """
    Our Tkinter Window wrapper class
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.elements = { }
        self.configure_gui()


    def configure_gui(self):
        """
        Build our GUI
        """


        """
        Add Top-Left Label & Combobox for selecting Language
        """
        self.elements["labelLanguage"] = ttk.Label(self, text = "Select the Language :", 
                font = ("Times New Roman", 10)).grid(column = 0, 
                row = 0, padx = 10, pady = 10)

        self.elements["variableLanguage"] = language_variable = tk.StringVar()
        self.elements["comboLanguage"] = ttk.Combobox(self, width = 27, textvariable=language_variable)
        self.elements["comboLanguage"].grid(column = 1, 
                row = 0, padx = 10, pady = 10)
        self.elements["comboLanguage"]['values'] = list(gtts.lang.tts_langs().keys())
        self.elements["comboLanguage"].current(self.elements["comboLanguage"]['values'].index('en'))


        """
        Add Top-Right Label & Combobox for selecting Accent
        """
        self.elements["labelAccent"] = ttk.Label(self, text = "Select the Accent :", 
                font = ("Times New Roman", 10)).grid(column = 2, 
                row = 0, padx = 10, pady = 10)

        self.elements["variableAccent"] = accent_variable = tk.StringVar()
        self.elements["comboAccent"] = ttk.Combobox(self, width = 27, textvariable=accent_variable)
        self.elements["comboAccent"].grid(column = 3, 
                row = 0, padx = 10, pady = 10)

        self.elements["comboAccent"]['values'] = [ACC_AUSTRALIA, ACC_UK, ACC_USA, ACC_CANADIAN, ACC_INDIAN, ACC_IRISH, ACC_AFRICAN, ACC_FRENCH]
        self.elements["comboAccent"].current(3)


        """
        Add Main Text Box
        """
        self.elements["textBoxInput"] = tk.Text()
        self.elements["textBoxInput"].insert("1.0", "Insert Text Here")
        self.elements["textBoxInput"].grid(column = 0, 
                row = 2, padx = 10, pady = 10, columnspan = 4)


        """
        Add Play Button
        """
        self.elements["buttonPlay"] = tk.Button(
            font = ("Times New Roman", 10),
            text="Play",
            width=25,
            height=1,
            bg="black",
            fg="white",
            command=self.play_file
        )
        self.elements["buttonPlay"].grid(column = 0, 
                row = 3, padx = 10, pady = (0, 10), columnspan = 2)


        """
        Add Save Button
        """
        self.elements["buttonSave"] = tk.Button(
            font = ("Times New Roman", 10),
            text="Save to Disk",
            width=25,
            height=1,
            bg="black",
            fg="white",
            command=self.select_file
        )
        self.elements["buttonSave"].grid(column = 2, 
                row = 3, padx = 10, pady = (0, 10), columnspan = 2)


    def select_file(self):
        text = self.elements["textBoxInput"].get("1.0", tk.END).strip()

        if not text:
            showerror('Uh oh!', "Gonna need to write some text in the window before saving.")
            return False

        text_name = slugify(text[:20])
        file_name = self._get_unique_filename(text_name=text_name)

        files = [('MP3 Files', '*.mp3')]
        file = fd.asksaveasfilename(filetypes = files, defaultextension = files, initialfile=file_name)

        if not file:
            return

        self._generate_and_save(file, text)

        return True
    

    def play_file(self):
        text = self.elements["textBoxInput"].get("1.0", tk.END).strip()

        if not text:
            showerror('Uh oh!', "Gonna need to write some text in the window before playing.")
            return False

        self._generate_and_save('.temp.mp3', text)
        playsound('.temp.mp3')
        os.remove(".temp.mp3")

        return True

    def _get_unique_filename(self, text_name):
        iteration = 0
        while os.path.exists(f'{text_name}.mp3' if not iteration else f'{text_name} ({iteration}).mp3') is True:
            iteration += 1

        return f'{text_name}.mp3' if not iteration else f'{text_name} ({iteration}).mp3'


    def _generate_and_save(self, filename, text):
        tts = gtts.gTTS(text, lang=self.elements["comboLanguage"].get(), tld=self.elements["comboAccent"].get())

        if os.path.exists(filename):
            os.remove(filename)
        try:
            tts.save(filename)
        except PermissionError:
            print ('Permission denied. Is there already a file with that name?')


if __name__ == "__main__":
    window = MainWindow()
    window.title('MP3 Text to Speech Generator')
    window.mainloop()


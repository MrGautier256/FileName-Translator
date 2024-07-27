import os
from tkinter import Tk, Label, Button, Entry, StringVar, OptionMenu, filedialog, BooleanVar, Checkbutton
from deep_translator import GoogleTranslator


def rename_files_in_directory(directory, src_lang, dest_lang, include_subfolders):
    translator = GoogleTranslator(source=src_lang, target=dest_lang)

    for root, _, files in os.walk(directory):
        for filename in files:
            try:
                # Extracting file extension
                file_name, file_extension = os.path.splitext(filename)

                # Translating each word in the file name
                translated_name_parts = []
                for word in file_name.split():
                    translated_word = translator.translate(word)
                    if translated_word is None:
                        translated_word = word  # fallback to the original word if translation fails
                    translated_name_parts.append(translated_word)
                translated_name = ' '.join(translated_name_parts)

                # Constructing new file name
                new_filename = f"{translated_name}{file_extension}"

                # Renaming the file
                os.rename(
                    os.path.join(root, filename),
                    os.path.join(root, new_filename)
                )
                print(f'Renamed "{filename}" to "{new_filename}"')
            except Exception as e:
                print(f'Error renaming "{filename}": {e}')

        # If not including subfolders, break after the first iteration
        if not include_subfolders:
            break

# Function to open a file dialog to select a directory


def browse_directory():
    directory_path.set(filedialog.askdirectory())

# Function to start the renaming process


def start_renaming():
    directory = directory_path.get()
    src_lang = src_lang_var.get()
    dest_lang = dest_lang_var.get()
    include_subfolders = include_subfolders_var.get()
    rename_files_in_directory(
        directory, src_lang, dest_lang, include_subfolders)


# Create the main window
root = Tk()
root.title("File Name Translator")

# Variables to store user inputs
directory_path = StringVar()
src_lang_var = StringVar(value='en')
dest_lang_var = StringVar(value='fr')
include_subfolders_var = BooleanVar()

# List of languages
languages = ['en', 'fr', 'es', 'de', 'it', 'pt', 'nl', 'ru', 'ja', 'zh-cn']

# Create and place widgets
Label(root, text="Source Language:").grid(row=0, column=0, padx=10, pady=10)
OptionMenu(root, src_lang_var, *languages).grid(row=0,
                                                column=1, padx=10, pady=10)

Label(root, text="Destination Language:").grid(
    row=1, column=0, padx=10, pady=10)
OptionMenu(root, dest_lang_var, *languages).grid(row=1,
                                                 column=1, padx=10, pady=10)

Label(root, text="Directory:").grid(row=2, column=0, padx=10, pady=10)
Entry(root, textvariable=directory_path, width=50).grid(
    row=2, column=1, padx=10, pady=10)
Button(root, text="Browse", command=browse_directory).grid(
    row=2, column=2, padx=10, pady=10)

Checkbutton(root, text="Include Subfolders", variable=include_subfolders_var).grid(
    row=3, column=0, columnspan=3, pady=10)

Button(root, text="Start Renaming", command=start_renaming).grid(
    row=4, column=0, columnspan=3, pady=20)

# Start the GUI event loop
root.mainloop()

import os
import threading
from tkinter import Tk, Label, Entry, StringVar, OptionMenu, filedialog, BooleanVar, Checkbutton, messagebox, ttk
from ttkthemes import ThemedTk
from deep_translator import GoogleTranslator

# Global variables to control the renaming process
stop_renaming = False
renaming_in_progress = False


def rename_files_in_directory(directory, src_lang, dest_lang, include_subfolders):
    global stop_renaming, renaming_in_progress
    stop_renaming = False
    renaming_in_progress = True
    translator = GoogleTranslator(source=src_lang, target=dest_lang)

    # Count total files
    total_files = sum([len(files) for r, d, files in os.walk(
        directory) if include_subfolders or r == directory])

    # Update progress bar
    progress_bar['maximum'] = total_files
    progress_value = 0

    for root, _, files in os.walk(directory):
        for filename in files:
            if stop_renaming:
                break

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

            # Update the progress bar
            progress_value += 1
            progress_bar['value'] = progress_value
            progress_label_var.set(
                f"{int((progress_value / total_files) * 100)}%")
            root_window.update_idletasks()

        if stop_renaming:
            break

    renaming_in_progress = False

    # Show completion message if not stopped
    if not stop_renaming:
        messagebox.showinfo("Done", "File renaming is complete!")

    # Reset progress bar and percentage
    progress_bar['value'] = 0
    progress_label_var.set("0%")

# Function to open a file dialog to select a directory


def browse_directory():
    directory_path.set(filedialog.askdirectory())

# Function to start the renaming process in a new thread


def start_renaming():
    rename_thread = threading.Thread(target=rename_files_in_directory, args=(
        directory_path.get(), src_lang_var.get(), dest_lang_var.get(), include_subfolders_var.get()))
    rename_thread.start()

# Function to stop the renaming process


def stop_renaming_process():
    global stop_renaming
    stop_renaming = True
    if renaming_in_progress:
        messagebox.showinfo("Stopped", "File renaming has been stopped.")
    # Reset progress bar and percentage
    progress_bar['value'] = 0
    progress_label_var.set("0%")

# Function to handle closing the application


def on_closing():
    if renaming_in_progress:
        stop_renaming_process()
    root_window.destroy()


# Create the main window with a theme
root_window = ThemedTk(theme="radiance")
root_window.title("File Name Translator")
root_window.geometry("700x350")
root_window.protocol("WM_DELETE_WINDOW", on_closing)

# Variables to store user inputs
directory_path = StringVar()
src_lang_var = StringVar(value='en')
dest_lang_var = StringVar(value='fr')
include_subfolders_var = BooleanVar()
progress_label_var = StringVar(value="0%")

# List of languages
languages = ['en', 'fr', 'es', 'de', 'it', 'pt', 'nl', 'ru', 'ja', 'zh-cn']

# Create and place widgets with ttk style
ttk.Label(root_window, text="Source Language:", font=('Helvetica', 12,
          'bold')).grid(row=0, column=0, padx=10, pady=10, sticky='w')
OptionMenu(root_window, src_lang_var, *languages).grid(row=0,
                                                       column=1, padx=10, pady=10, sticky='ew')

ttk.Label(root_window, text="Destination Language:", font=(
    'Helvetica', 12, 'bold')).grid(row=1, column=0, padx=10, pady=10, sticky='w')
OptionMenu(root_window, dest_lang_var, *languages).grid(row=1,
                                                        column=1, padx=10, pady=10, sticky='ew')

ttk.Label(root_window, text="Directory:", font=('Helvetica', 12, 'bold')).grid(
    row=2, column=0, padx=10, pady=10, sticky='w')
ttk.Entry(root_window, textvariable=directory_path, width=40).grid(
    row=2, column=1, padx=10, pady=10, sticky='ew')
ttk.Button(root_window, text="Browse", command=browse_directory).grid(
    row=2, column=2, padx=10, pady=10, sticky='ew')

Checkbutton(root_window, text="Include Subfolders", variable=include_subfolders_var,
            font=('Helvetica', 12)).grid(row=3, column=0, columnspan=3, pady=10)

ttk.Button(root_window, text="Start Renaming", command=start_renaming).grid(
    row=4, column=0, padx=10, pady=10, sticky='ew')
ttk.Button(root_window, text="Stop Renaming", command=stop_renaming_process).grid(
    row=4, column=1, padx=10, pady=10, sticky='ew')

# Add progress bar and label
progress_bar = ttk.Progressbar(
    root_window, orient="horizontal", length=400, mode="determinate")
progress_bar.grid(row=5, column=0, columnspan=2, pady=20, sticky='ew')

ttk.Label(root_window, textvariable=progress_label_var, font=(
    'Helvetica', 12, 'bold')).grid(row=5, column=2, padx=10, pady=20, sticky='w')

# Start the GUI event loop
root_window.mainloop()

# File Name Translator

File Name Translator is a Python application that renames files in a specified directory by translating their names from one language to another using the `deep_translator` library. The application provides a graphical user interface (GUI) for easy interaction, allowing users to select the source and destination languages, the directory containing the files, and whether to include subfolders in the renaming process.

## Features

- Translate file names from one language to another.
- Support for multiple languages.
- Include or exclude subfolders.
- Progress bar to show the translation progress.
- Start and stop the renaming process.

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/FileName-Translator.git
    cd FileName-Translator
    ```

2. Install the required dependencies:

    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the application:

   ```sh
    python src/main.py
    ```

2. In the GUI:
   - Select the source language from the dropdown menu.
   - Select the destination language from the dropdown menu.
   - Browse and select the directory containing the files you want to rename.
   - Check the "Include Subfolders" option if you want to rename files in subfolders as well.
   - Click the "Start Renaming" button to begin the renaming process.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


## Acknowledgements

- This project uses the [deep_translator](https://pypi.org/project/deep-translator/) library for language translation.
- The GUI is built using the [tkinter](https://docs.python.org/3/library/tkinter.html) library.

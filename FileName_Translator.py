import os
from deep_translator import GoogleTranslator


def rename_files_in_directory(directory):
    translator = GoogleTranslator(source='en', target='fr')

    for filename in os.listdir(directory):
        if not os.path.isfile(os.path.join(directory, filename)):
            continue

        # Extracting file extension
        file_name, file_extension = os.path.splitext(filename)

        # Translating file name
        translated_name = translator.translate(file_name)

        # Constructing new file name
        new_filename = f"{translated_name}{file_extension}"

        # Renaming the file
        os.rename(
            os.path.join(directory, filename),
            os.path.join(directory, new_filename)
        )
        print(f'Renamed "{filename}" to "{new_filename}"')


# Example usage
directory_path = r''
rename_files_in_directory(directory_path)

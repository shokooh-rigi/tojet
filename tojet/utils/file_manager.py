import base64
import os
import random
import logging

logger = logging.getLogger(__name__)


def store_file(file) -> str:
    """
    Store a file in the 'media' directory with a unique name if necessary.

    :param file: The file object to be stored.
    :return: The file path of the stored file.
    """
    try:
        directory = "media"
        os.makedirs(directory, exist_ok=True)

        file_path = os.path.join(directory, file.filename)
        if os.path.exists(file_path):
            file_name, file_extension = os.path.splitext(file.filename)
            while os.path.exists(file_path):
                new_file_name = f"{file_name}_{random.randint(0, 9999)}{file_extension}"
                file_path = os.path.join(directory, new_file_name)

        with open(file_path, "wb") as stored_file:
            stored_file.write(file.read())

        logger.info(f"File stored successfully at: {file_path}")
        return file_path

    except Exception as e:
        logger.error(f"Failed to store file. Exception: {str(e)}")
        raise e


def is_file_extensions_valid(file, allowed_extensions: tuple) -> bool:
    """
    Check if the file's extension is in the allowed extensions.

    :param file: The file object.
    :param allowed_extensions: A tuple of allowed file extensions.
    :return: True if valid, False otherwise.
    """
    return file.filename.lower().endswith(allowed_extensions)


def set_file_name_by_extension(file_name: str, file) -> str:
    """
    Generate a file name with the correct extension from the file object.

    :param file_name: The base file name.
    :param file: The file object.
    :return: The file name with its extension.
    """
    file_extension = os.path.splitext(file.filename)[1]
    return f"{file_name}{file_extension}"


def store_file_in_local(file_name: str, file_path: str, file) -> str:
    """
    Store a file at the specified path with the given name.

    :param file_name: The desired file name.
    :param file_path: The directory path where the file will be stored.
    :param file: The file object to store.
    :return: The full path of the stored file.
    """
    try:
        local_file_path = os.path.join(file_path, file_name)

        # Remove existing file if it exists
        if os.path.exists(local_file_path):
            os.remove(local_file_path)

        # Create directories if they don't exist
        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)

        # Write the file
        with open(local_file_path, 'wb') as stored_file:
            stored_file.write(file.read())

        logger.info(f"File stored locally at: {local_file_path}")
        return local_file_path

    except Exception as e:
        logger.error(f"Failed to store file locally. Exception: {str(e)}")
        raise e


def get_file_extension(directory_path: str, filename: str) -> str:
    """
    Retrieve the file extension for a file in the specified directory.

    :param directory_path: The directory path to search in.
    :param filename: The base name of the file to search for.
    :return: The file extension if found, otherwise None.
    """
    try:
        files = os.listdir(directory_path)
        for file in files:
            if file.startswith(filename):
                _, file_extension = os.path.splitext(file)
                logger.info(f"File extension found: {file_extension}")
                return file_extension

        logger.warning(f"File {filename} not found in {directory_path}")
        return None

    except Exception as e:
        logger.error(f"Failed to retrieve file extension. Exception: {str(e)}")
        raise e


def read_base64_file_content(file_path: str) -> str:
    """
    Read the content of a file and return it as a Base64-encoded string.

    :param file_path: The full path of the file.
    :return: The Base64-encoded content of the file.
    """
    try:
        with open(file_path, "rb") as file:
            file_content = file.read()
            base64_file_content = base64.b64encode(file_content).decode("utf-8")

        logger.info(f"File read and encoded successfully: {file_path}")
        return base64_file_content

    except Exception as e:
        logger.error(f"Failed to read file as Base64. Exception: {str(e)}")
        raise e

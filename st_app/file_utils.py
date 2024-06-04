from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve().parent
DATA_PATH = Path(__file__).resolve().parent
UPLOAD_FOLDER = DATA_PATH / "uploads" 
OUTPUT_FOLDER = DATA_PATH / "outputs"
ALLOWED_DATAFILE_EXTENSIONS = {".csv"}
ALLOWED_CONFIGFILE_EXTENSIONS = {".json"}
ERROR_MESSAGE_REJECT_EXTENSION = (
    "{} has wrong extension {}, it will be ignored. See list of allowed formats: {}"
)
upload_folder = SCRIPT_PATH / UPLOAD_FOLDER
output_folder = SCRIPT_PATH / OUTPUT_FOLDER


class InvalidFileExtension(Exception):
    """Raised when uploaded file is rejected due to invalid format."""


def upload_file_or_reject(uploaded_file, upload_folder) -> None:
    name = uploaded_file.name
    if (ext := Path(name).suffix) in ALLOWED_DATAFILE_EXTENSIONS:
        with open(upload_folder / name, "wb") as f:
            f.write(uploaded_file.read())
    else:
        raise InvalidFileExtension(
            ERROR_MESSAGE_REJECT_EXTENSION.format(name, ext, ALLOWED_DATAFILE_EXTENSIONS)
        )
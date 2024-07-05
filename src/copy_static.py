import shutil
import os
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)


def remove_directory_safely(directory: Path) -> None:
    logging.info(f"Removing directory safely: {directory}")

    # First, look for any existing `._`(virtual copies on macos) files and safely remove them first
    for root, _, files in os.walk(directory):
        for file in files:
            if file.startswith("._"):
                file_path = Path(root) / file
                try:
                    logging.info(f"Removing resource fork file: {file_path}")
                    file_path.unlink()
                except Exception as e:
                    logging.warning(
                        f"Unable to remove virtual copy file {file_path}: {str(e)}"
                    )

    try:
        if directory.exists() and directory.is_dir():
            shutil.rmtree(directory)
        logging.info(f"Directory removed safely: {directory}")
    except Exception as e:
        logging.error(f"Error removing directory {directory}: {str(e)}")
        raise


def copy_static(src: str, dest: str) -> None:
    logging.info(f"Copying static files from {src} to {dest}")
    src_path = Path(src).absolute()
    dest_path = Path(dest).absolute()

    if not src_path.exists() or not src_path.is_dir():
        raise ValueError(
            f"Source directory {src_path} does not exist or is not directory"
        )

    if dest_path.exists():
        remove_directory_safely(dest_path)

    os.mkdir(dest)

    try:
        shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
    except Exception as e:
        logging.error(f"Error copying from {src_path} to {dest_path}: {str(e)}")
        raise

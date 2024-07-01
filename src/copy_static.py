import shutil
import os


def remove_directory_safely(directory: str) -> None:
    print("Removing directory safely")
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file.startswith("._"):
                os.unlink(file_path)
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            remove_directory_safely(dir_path)

    if os.path.exists(directory):
        shutil.rmtree(directory)


def copy_static(src: str, dest: str) -> None:
    print("Copying static files")
    cwd = os.getcwd()
    src = os.path.join(cwd, src)
    dest = os.path.join(cwd, dest)
    if not os.path.exists(src):
        raise ValueError(f"Source directory {src} does not exist")

    if os.path.exists(dest):
        remove_directory_safely(dest)

    os.mkdir(dest)

    for file in os.listdir(src):
        src_file = os.path.join(src, file)
        dest_file = os.path.join(dest, file)
        if os.path.isfile(src_file):
            shutil.copy(src_file, dest_file)
        else:
            os.mkdir(dest_file)
            copy_static(src_file, dest_file)

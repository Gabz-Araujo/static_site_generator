from gen_content import generate_pages_recursively
from copy_static import copy_static


def main():
    copy_static("static", "public")
    generate_pages_recursively("./content", "./template.html", "./public")


if __name__ == "__main__":
    main()

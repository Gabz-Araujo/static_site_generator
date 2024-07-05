import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from gen_content import generate_pages_recursively
from copy_static import copy_static


def main():

    static_src = "static"
    public_dest = "public"
    content_src = "content"
    template_file = "template.html"

    copy_static(static_src, public_dest)
    generate_pages_recursively(
        Path(content_src), Path(template_file), Path(public_dest)
    )


if __name__ == "__main__":
    main()

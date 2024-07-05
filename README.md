# Static Site Generator

This project is a static site generator designed to convert a set of Markdown files into a complete static website using HTML templates. It handles various content features like images, links, and nested blocks while allowing users to customize their pages using a predefined template. The script also manages static assets by copying them into the deployed directory.

## Table of Contents

- [Features](#features)
- [Directory Structure](#directory-structure)
- [Setup](#setup)
- [Usage](#usage)
- [License](#license)

## Features

- **Markdown to HTML Conversion**: Converts Markdown files into HTML documents using a customizable HTML template.
- **Static Asset Management**: Copies static files (such as CSS, images) to the deployment directory.
- **Recursive File Handling**: Processes files within directories recursively.
- **Modern Python Practices**: Utilizes `pathlib`, `shutil`, and `logging` for Pythonic code.

## Directory Structure

```
Project Root
├── content                    # Directory for markdown content files
│   ├── index.md
│   └── majesty
│       └── index.md
├── main.sh                    # Shell script to run the main.py
├── public                     # Output directory for generated HTML files
│   ├── images
│       └── rivendell.png
│   └── ...
├── README.md                  # README file
├── requirements.txt           # List of required Python packages
├── server.py                  # Script to start a local server
├── src                        # Source files for the project
│   ├── block_markdown/
│   ├── copy_static.py
│   ├── gen_content.py
│   ├── inline_markdown/
│   ├── main.py                # Main script
│   └── text_node.py
├── static                     # Directory to store static assets
│   ├── images
│       └── rivendell.png
│   └── index.css
├── template.html              # HTML template file
└── test                       # Directory with test cases
    ├── test_block_markdown.py
    └── ...
```

## Setup

### Prerequisites

- Python 3.6+ (specific features require Python 3.8+)
- `pip` - Python package installer

### Installation

1. Clone the repository:

   ```sh
   git clone <repository-url>
   cd static_site_generator
   ```

2. (Optional) Create and activate a virtual environment:

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the project dependencies:

   ```sh
   pip install -r requirements.txt
   ```

4. Ensure scripts have execution permissions:

   ```sh
   chmod +x main.sh
   chmod +x test.sh
   ```

## Usage

### Run the Main Script

The `main.py` script generates the static site by copying static files and converting markdown files to HTML.

Execute the script using:

```sh
./main.sh
```

Alternatively, run it directly with Python:

```sh
python src/main.py
```

### Run Tests

The `test.sh` script runs all unit tests to ensure code functionality.

Run tests using:

```sh
./test.sh
```

Or directly with Python:

```sh
python -m unittest discover -s test
```

### Start a Local Server

To serve the generated pages locally, you can use the `server.py` script. Navigate to the `public` directory and start a simple HTTP server:

```sh
cd public
python -m http.server 8888
```

Visit `http://localhost:8888` in your browser to see the generated site.

## License

Distributed under the MIT License. See `LICENSE` for more information.


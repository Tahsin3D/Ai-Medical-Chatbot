import os;
from pathlib import Path;
import logging;

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

list_of_files = [
    "src/__init__.py",
    "src/helper.py",
    ".env",
    "requirments.txt",
    "setup.py",
    "app.py",
    "research/trials.ipynb",
]

for path in list_of_files:
    path = Path(path)
    filedir, filename = os.path.split(path)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Created directory: {filedir}")

    if not os.path.exists(path) or os.path.getsize(path) == 0:
        with open(path, "w") as file:
            pass
            logging.info(f"Created file: {path}")

    else:
        logging.info(f"File already exists: {path}")
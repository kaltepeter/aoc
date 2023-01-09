#!/usr/bin/env python3

import datetime
from os import chmod, mkdir, path
from pathlib import Path
from shutil import copyfile
from markdownify import MarkdownConverter
import requests
from datetime import date
from bs4 import BeautifulSoup


def md(soup, **options):
    return MarkdownConverter(**options).convert_soup(soup)


today = datetime.datetime(2022, 12, 16)

day_dir = path.join("py_src", f"y{today.year}", f"day_{today.day}")
template_dir = path.join("py_src", "template")
if not path.exists(day_dir):
    mkdir(day_dir)


def create_empty_files(filename: str) -> None:
    if not path.exists(path.join(day_dir, filename)):
        Path(path.join(day_dir, filename)).touch()


def copy_template_files() -> None:
    if not path.exists(path.join(day_dir, "day.py")):
        copyfile(path.join(template_dir, "day.py"), path.join(day_dir, "day.py"))
    if not path.exists(path.join(day_dir, "day_test.py")):
        copyfile(
            path.join(template_dir, "day_test.py"), path.join(day_dir, "day_test.py")
        )


create_empty_files("input.txt")
create_empty_files("example.txt")
create_empty_files("__init__.py")
copy_template_files()

url = f"https://adventofcode.com/{today.year}/day/{today.day}"

page = requests.get(url)
soup = BeautifulSoup(page.text, "html.parser")
articles = soup.find_all("article")

with open(path.join(day_dir, "puzzle.md"), "w") as file:
    file.write("# Puzzle\n\n")
    md_text = md(
        articles[0],
        heading_style="atx",
        newline_style="BACKSLASH",
        code_language="text",
        strong_em_symbol="__",
    )
    md_text = md_text.replace("\n\n\n", "\n\n").replace("\n\n```", "\n```")
    file.write(md_text.strip())
    file.write("\n")

#!/usr/bin/env python3

import datetime
from os import chmod, mkdir, path
from pathlib import Path
from markdownify import MarkdownConverter
import requests
from datetime import date
from bs4 import BeautifulSoup


def md(soup, **options):
    return MarkdownConverter(**options).convert_soup(soup)


today = datetime.datetime(2022, 12, 11)

day_dir = path.join("python", f"{today.year}", f"day_{today.day}")
if not path.exists(day_dir):
    mkdir(day_dir)


def create_empty_files(filename: str) -> None:
    if not path.exists(path.join(day_dir, filename)):
        Path(path.join(day_dir, filename)).touch()


create_empty_files("input.txt")
create_empty_files("example.txt")
create_empty_files("__init__.py")
create_empty_files("day.py")
create_empty_files("day_test.py")

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

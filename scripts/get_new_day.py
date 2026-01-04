#!/usr/bin/env python3

import datetime
from os import makedirs, path
from pathlib import Path
from shutil import copyfile
from typing import Literal, TypedDict, Union
from markdownify import MarkdownConverter
import requests
from bs4 import BeautifulSoup
import sys


def md(soup, **options):
    return MarkdownConverter(**options).convert_soup(soup)


def print_usage():
    help_text = """
    Usage: python scripts/get_new_day.py YEAR DAY LANGUAGE_DIR

    YEAR: The year of the day
    DAY: The day of the year
    LANGUAGE_DIR: The directory of the language to scaffold

    Examples:
    python scripts/get_new_day.py 2025 1 dotnet
    python scripts/get_new_day.py 2024 1 py_src
    """
    print(help_text)
    exit(1)


def create_empty_files(day_dir: str, filename: str) -> None:
    if not path.exists(path.join(day_dir, filename)):
        Path(path.join(day_dir, filename)).touch()


def copy_template_files(day_dir: str, template_dir: str) -> None:
    if not path.exists(path.join(day_dir, "day.py")):
        copyfile(path.join(template_dir, "day.py"), path.join(day_dir, "day.py"))
    if not path.exists(path.join(day_dir, "day_test.py")):
        copyfile(
            path.join(template_dir, "day_test.py"), path.join(day_dir, "day_test.py")
        )


def process_template(template_path: str, replacements: dict) -> str:
    """Read a template file and replace placeholders with actual values."""
    with open(template_path, "r") as f:
        content = f.read()
    for placeholder, value in replacements.items():
        content = content.replace(placeholder, str(value))
    return content


def scaffold_python_day(day_dir: str, template_dir: str) -> None:
    create_empty_files(day_dir, "input.txt")
    create_empty_files(day_dir, "example.txt")
    create_empty_files(day_dir, "__init__.py")
    copy_template_files(day_dir, template_dir)


def scaffold_dotnet_day(day_dir: str, template_dir: str, year: int, day: int) -> None:
    dotnet_test_dir = path.join("dotnet", f"y{year}.unit", f"day_{day}")
    dotnet_template_dir = path.join("dotnet", "template")

    makedirs(dotnet_test_dir, exist_ok=True)

    create_empty_files(day_dir, "input.txt")
    create_empty_files(dotnet_test_dir, "example.txt")

    # Template replacements
    replacements = {
        "{YEAR}": year,
        "{DAY}": day,
    }

    # Process and write Day.cs
    day_template_path = path.join(dotnet_template_dir, "Day.cs.template")
    if path.exists(day_template_path):
        day_content = process_template(day_template_path, replacements)
        day_output_path = path.join(day_dir, "Day.cs")
        if not path.exists(day_output_path):
            with open(day_output_path, "w") as f:
                f.write(day_content)
            print(f"  Created {day_output_path}")
    else:
        print(f"  Warning: Template not found at {day_template_path}")

    # Process and write DayTest.cs
    test_template_path = path.join(
        dotnet_template_dir, "DayTest.cs.template"
    )
    if path.exists(test_template_path):
        test_content = process_template(test_template_path, replacements)
        test_output_path = path.join(dotnet_test_dir, "Day.cs")
        if not path.exists(test_output_path):
            with open(test_output_path, "w") as f:
                f.write(test_content)
            print(f"  Created {test_output_path}")
    else:
        print(f"  Warning: Template not found at {test_template_path}")


args = sys.argv[1:]

if len(args) < 3:
    print_usage()


target_year = int(args[0])
target_day = int(args[1])
target_language = args[2]

if target_language == "python":
    target_language_dir = path.join("py_src")
elif target_language == "dotnet":
    target_language_dir = path.join("dotnet")
else:
    print(f"Invalid language: {target_language}")
    exit(1)

if not target_year or not target_day:
    print_usage()

today = datetime.datetime(target_year, 12, target_day)

print(f"Creating day {today.day} for year {today.year} in {target_language}")

day_dir = path.join(target_language_dir, f"y{today.year}", f"day_{today.day}")
template_dir = path.join(target_language_dir, "template")
makedirs(day_dir, exist_ok=True)

if target_language == "python":
    scaffold_python_day(day_dir, template_dir)
elif target_language == "dotnet":
    scaffold_dotnet_day(day_dir, template_dir, today.year, today.day)
else:
    print(f"Invalid language: {target_language}")
    exit(1)


# Fetch puzzle description
url = f"https://adventofcode.com/{today.year}/day/{today.day}"

print("Fetching puzzle description...")
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

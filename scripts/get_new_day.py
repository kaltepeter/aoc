#!/usr/bin/env python3

import datetime
from os import mkdir, path
from pathlib import Path
from shutil import copyfile
from markdownify import MarkdownConverter
import requests
from bs4 import BeautifulSoup
import sys


def md(soup, **options):
    return MarkdownConverter(**options).convert_soup(soup)


def print_usage():
    print("Usage: python create_day.py YEAR DAY")
    exit(1)


def process_template(template_path: str, replacements: dict) -> str:
    """Read a template file and replace placeholders with actual values."""
    with open(template_path, "r") as f:
        content = f.read()
    for placeholder, value in replacements.items():
        content = content.replace(placeholder, str(value))
    return content


def scaffold_dotnet_day(year: int, day: int) -> None:
    """Scaffold dotnet day structure with template replacements."""
    dotnet_day_dir = path.join("dotnet", f"y{year}", f"day_{day}")
    dotnet_test_dir = path.join("dotnet", f"y{year}.unit", f"day_{day}")
    dotnet_template_dir = path.join("dotnet", "templates")

    # Create directories
    if not path.exists(dotnet_day_dir):
        mkdir(dotnet_day_dir)
    if not path.exists(dotnet_test_dir):
        mkdir(dotnet_test_dir)

    # Template replacements
    replacements = {
        "{YEAR}": year,
        "{DAY}": day,
    }

    # Process and write Day.cs
    day_template_path = path.join(dotnet_template_dir, "Day.cs.template")
    if path.exists(day_template_path):
        day_content = process_template(day_template_path, replacements)
        day_output_path = path.join(dotnet_day_dir, "Day.cs")
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

    # Create empty input files
    input_file = path.join(dotnet_day_dir, "input.txt")
    if not path.exists(input_file):
        Path(input_file).touch()
        print(f"  Created {input_file}")

    example_file = path.join(dotnet_test_dir, "example.txt")
    if not path.exists(example_file):
        Path(example_file).touch()
        print(f"  Created {example_file}")


args = sys.argv[1:]

if len(args) < 2:
    print_usage()

target_year = int(args[0])
target_day = int(args[1])

if not target_year or not target_day:
    print_usage()

today = datetime.datetime(target_year, 12, target_day)

print(f"Creating day {today.day} for year {today.year}")

# Python scaffolding
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


print("Scaffolding Python day...")
create_empty_files("input.txt")
create_empty_files("example.txt")
create_empty_files("__init__.py")
copy_template_files()

print("Scaffolding .NET day...")
scaffold_dotnet_day(today.year, today.day)

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

# Write puzzle.md for .NET
dotnet_day_dir = path.join("dotnet", f"y{today.year}", f"day_{today.day}")
dotnet_puzzle_path = path.join(dotnet_day_dir, "puzzle.md")
if not path.exists(dotnet_puzzle_path):
    with open(dotnet_puzzle_path, "w") as file:
        file.write("# Puzzle\n\n")
        md_text = md(
            articles[0],
            heading_style="atx",
            newline_style="BACKSLASH",
            code_language="text",
            strong_em_symbol="__",
        )
        md_text = md_text.replace("\n\n\n", "\n\n")
        md_text = md_text.replace("\n\n```", "\n```")
        file.write(md_text.strip())
        file.write("\n")
    print(f"  Created {dotnet_puzzle_path}")

print("Done!")

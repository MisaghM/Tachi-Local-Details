
# Tachi-Local Details

[![license](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](https://github.com/MisaghM/Tachi-Local-Details/blob/main/LICENSE "Repository License")

- [Tachi-Local Details](#tachi-local-details)
  - [About](#about)
  - [Usage](#usage)
  - [Options](#options)
  - [Installation](#installation)
    - [pip](#pip)
    - [Manual pip](#manual-pip)
    - [PyInstaller](#pyinstaller)
    - [Zipapp](#zipapp)
    - [Manual run](#manual-run)
  - [Makefile](#makefile)

## About

[**Tachiyomi**](https://tachiyomi.org/) local manga [details.json](https://tachiyomi.org/help/guides/local-manga/#editing-local-manga-details) creator.  
Using [Baka-Updates Manga](https://www.mangaupdates.com).
  
*Requires Python >= 3.7*

## Usage

You can either directly use a Mangaupdates series link/id, or search using the script.  
The script will scrape the website and generate the `details.json` for you.

```text
tachi-local <id>
tachi-local https://www.mangaupdates.com/series/<id>
tachi-local -s <title>
```

## Options

You can see all the options in --help.

```text
Main commands:
  using a link or id
  using -s or --search

Search options:
  -a/--auto-first-result: automatically select the first search result
  -m/--max-search-results: maximum search results to show

Options:
  -h/--help and --version
  -k/--keep-status-values: keep the "_status values" entry in the json
  -o/--output: output filename
```

## Installation

You can use any of the following methods:

### pip

This is the easiest way.  
Run the following command:

**`pip install tachi-local`**

Now `tachi-local` should be in a location in your PATH and available in your command-line.  
So you can just run it: `tachi-local --help`

It can be uninstalled with this command: `pip uninstall tachi-local`  
And updated with: `pip install -U tachi-local`

*(This method downloads the program from **[PyPI](https://pypi.org/project/tachi-local/))***

### Manual pip

You can download the source and run this command in the project's root directory:

`pip install .`

Then `tachi-local` will be available in your command-line.

### PyInstaller

You can download an .exe file created using **[PyInstaller](https://pyinstaller.readthedocs.io/en/stable/index.html)** from the **[releases](https://github.com/MisaghM/Tachi-Local-Details/releases)** section.  
You can place the .exe in a location in your environment PATH so you can run it from anywhere.

### Zipapp

You can get a python zipped executable file from the **[releases](https://github.com/MisaghM/Tachi-Local-Details/releases)** section. (file named *tachi-local*)  
You can run it like a normal executable:

`./tachi-local`

You can use this on Windows as well, but it cannot be executed like an exe.  
You can run it like this:

`python tachi-local`

### Manual run

You can download the source and run the code:

`python tachi_local`

## Makefile

The makefile is used to automate some tasks.  
The targets are:

- `make all` creates the zipapp.
- `make get-version` prints the program's version.
- `make dist` creates s-dist and b-dist (pure python wheel).
- `make upload` uploads to PyPI.
- `make pyi-spec` creates the .spec file for PyInstaller. (needed once)
- `make pyi-exe` creates a one-file executable using the .spec file.
- `make clean` cleans up pycache and the build. (there are separate more specific targets for cleaning as well)

`pyi_create_version_info.py` is ran with `make pyi-exe` and creates `pyi_win_version_info.py` from `pyi_win_version_info.template` which is used by PyInstaller to make the Windows executable's metadata.

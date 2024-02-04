# `AVglue`

## Purpose
Streamline your computer-based workflow (and other equipment) with DIY microcontroller consoles and custom GUIs.

## Table of Contents
1. [Overall Architecture](docs/Architecture.md)
1. [Installation](#Installation)

## Installation
To run `AVglue`, you first need to install Python 3.x.

To make the `AVglue` library to be available to your own application, you must add it to your `PYTHONPATH` somehow:
- Windows `CMD` shell:<br>
  `set PYTHONPATH=C:\path\to\AVglue\libpython`
- `bash` shell:<br>
  `export PYTHONPATH=/path/to/AVglue/libpython`
- ...

Usage examples are available in the [samples](samples/) subdirectory.

## Compatibility
Tested with the following configurations
- Windows 10 / Python 3.12.1
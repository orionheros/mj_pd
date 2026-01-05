# PD UI Manager
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

[🇺🇸 English] | [🇵🇱 Polski](readme.pl.md)

A desktop tool for calculating average shim thicknesses in **1.9 and 2.0 TDI (Pumpe Düse)** unit injectors. Designed for mechanics and diesel enthusiasts.

Detailed instructions will be available soon within the application.

## Features
* **Precise Calculations:** Accurate shim thickness estimation for injector kits.
* **Modern UI:** Built with **PyQt6** for a native look and feel.
* **High Performance:** Real-time data visualization using **pyqtgraph**.

## Installation

### REQUIREMENTS:

- **Python 3.10+**

- **Git**

1. Clone the repository:
   ```bash
   git clone https://github.com/orionheros/mj_pd.git
   cd mj_pd
   ```

2. Prepare .venv and install requirements:

   Windows:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

   Linux:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements_linux.txt
   ```

3. Start program:

   ```bash
   python -m pd
   ```

## Project Origins

The idea for this application was born from the need to speed up and streamline the process of setting the opening pressure in unit injectors (PD - Pumpe Duse). The goal is to verify the hypothesis that there are averaged, repeatable thicknesses of adjustment shims (and their total sum together with the spring) within the injector components. This program is an analytical tool—its core is the database built by the user within the data directory.

Measurement results obtained during the pressure adjustment process are entered into the database. Based on this data, the application—developed using the PyQt6 framework—calculates average values and other parameters (with more features coming in future updates).

## About the Autor

I have been interested in programming since the summer of 2025. Although I am a hobbyist learning for my own satisfaction and pleasure, I aim to create free, open-source software that might help others in their professional work.

I am very grateful for any help, feedback, support, or words of encouragement.
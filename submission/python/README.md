
# spidercam_simulator

## Setup

### Using `conda`
Prerequisites:
- `conda` (https://docs.conda.io/en/latest/miniconda.html)

Navigate to the project root directory `/python`

Create a `conda` environment from the `environment.yml` file:
```
    conda env create -f environment.yml
```

Contents of `environment.yml` (installs dependencies using `pip`):
```
    name: spidercam_simulator
    dependencies:
    - python>=3.10
    - pip
    - pip:
        - -r requirements.txt
```

Activate the environment:
```
    conda activate spidercam_simulator
```

Install local `python` package in edit-mode
- Using `pip` (uses `setup.py`):
```
    pip install -e .
```

### Using `pip`
Alternatively, you can use `pip` on its own to install the package:

Navigate to the project root directory `/python`

Install dependencies: 
```
    pip install -r requirements.txt
    pip install -e .
```

### Running the module
To run the module, use the following command:
```
    python -m spidercam_simulator
```

## Arguments

| Argument | Description | Default |
|----|---|---|
| `--input`, `-i` | Path to input file or dir | `/input` |
| `--output`, `-o` | Path to output dir | `/output` |
| `--no-plot`, `-np` | Disable plotting | `False` |
| `--debug`, `-d` | Enable debug mode | `False` |

## Scripts

The scripts are located at `/python/scripts` and should be run from the project root directory `/python`.

Please have the module installed (see above).

| Script | Description 
|----|---|
| `run.py` | Run the module |

## Generate API-Docs and Diagrams
### API-Docs
Prerequisites:
- `pdoc` (https://pdoc.dev/)

```
    pdoc spidercam_simulator -o docs --docformat 'google' --math
```

It can also be executed using the `scripts/generate_docs.sh` script.	

Please ensure that you execute the script from the project root directory `/python`.

### Diagrams
Prerequisites:
- `pyreverse` (https://www.logilab.org/blogentry/6882) (part of `pylint`)
- `graphviz` (https://graphviz.org/) (proper package and not using the python package found using `pip`)

All classes and packages in one diagram:
```
    pyreverse -o pdf spidercam_simulator && mv *.pdf uml
```

Every class in its own diagram:
```
    for f in spidercam_simulator/*.py; do pyreverse -o pdf $f && mv classes.pdf uml/$(basename $f .py).pdf; done
```

Both can be executed using the `scripts/generate_diagrams.sh` script.

Please ensure that you execute the script from the project root directory `/python`.
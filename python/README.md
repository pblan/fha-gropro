
# IHK GroPro-Template (Python)

## Generate API-Docs and Diagrams
### API-Docs
Prerequisites:
- `pdoc` (https://pdoc.dev/)

```
    pdoc spidercam_simulator -o docs --docformat 'google' 
```

### Diagrams
Prerequisites:
- `pyreverse` (https://www.logilab.org/blogentry/6882) (part of `pylint`)
- `graphviz` (https://graphviz.org/) (proper package and not using the python package found using `pip`)

```
    pyreverse -o pdf spidercam_simulator && mv *.pdf uml
```


## Development Setup

Prerequisites:
- `conda` (https://docs.conda.io/en/latest/miniconda.html)

1. Create a `conda` environment from the `environment.yml` file:
    ```
        conda env create -f environment.yml
    ```

    `environment.yml` (installs dependencies using `pip`):
    ```
        name: spidercam_simulator
        dependencies:
        - python>=3.10
        - pip
        - pip:
            - -r requirements.txt
    ```

2. Activate the environment:
    ```
        conda activate spidercam_simulator
    ```

3. Install local `python` package in edit-mode
    - Using `pip` (uses `setup.py`):
    ```
        pip install -e .
    ```

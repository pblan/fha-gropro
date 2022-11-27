
# IHK GroPro-Template (Python)

## Generate API-Docs
Prerequisites:
- `pdoc` (https://pdoc.dev/)

```
    pdoc project_name -o docs --docformat 'google' 
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
        name: project_name
        dependencies:
        - python>=3.10
        - pip
        - pip:
            - -r requirements.txt
    ```

2. Activate the environment:
    ```
        conda activate project_name
    ```

3. Install local `python` package in edit-mode
    - Using `pip` (uses `setup.py`):
    ```
        pip install -e .
    ```

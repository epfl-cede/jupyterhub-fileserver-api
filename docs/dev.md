__most commands should be launched in the project root__

# Environment management

- Create env (_venv_ folder) : ``` python3 -m venv venv ```
- Activate env : ``` source venv/bin/activate ```
- Deactivate env : ``` deactivate ```

# Package management

- Save package list : ``` pip freeze > requirements.txt ```
- Install packages from list : ``` pip install -r requirements.txt ```
- Upgrade packages : ``` pip install --upgrade -r requirements.txt ```

## Install noto lib
```cp -rv /usr/local/lib/python3.6/dist-packages/cedelogger venv/lib/python3.6/site-packages```
```cp -rv /usr/local/lib/python3.6/dist-packages/notouser venv/lib/python3.6/site-packages```

# Run
- ```sudo ./venv/bin/flask run --port 8080 --host 0.0.0.0```

# Pre commit
`pre-commit` tests for clean Python code, consistent formatting,
security issues and more. If installed it will run before commits
(hence its name) and refuse to commit upon failure. Run manually
fix some issues and reformat code.

- Install (in venv): ```pip install pre-commit```
- Init: ```pre-commit init```
- Run manually: ```pre-commit run --all-files```

# Tests
Install modules from `tests/requirements.txt` to your venv first.

Run tests with `python -m pytest` to have the current directory in `sys.path`.

Generate test coverage reports with `coverage run -m pytest` and `coverage report`
or `coverage html`.

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

# Python env (if not installed by [dev](dev.md))
- Install needed packages (see [packages.md](packages.md))
- Create env (_venv_ folder) : ``` python3 -m venv --system-site-packages venv ```
- Activate env : ``` source venv/bin/activate ```
- Install packages : ``` pip install -r requirements.txt ```

# Test
- ```flask run``` should finish with ```* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit) ```
- ``` gunicorn app:app  ``` should start

# Install service

- Install service file :  ```sudo cp systemd/notoapi.service /etc/systemd/system```
- Load service daemon ```sudo systemctl daemon-reload```
- Start api ```sudo systemctl start notoapi```
- Start api during boot ```sudo systemctl enable notoapi```

# Other commands

- api Status : ```sudo systemctl status notoapi```
- Stop api : ```sudo systemctl stop notoapi```

__Configuration is done in ```config.json``` file, and may be
overwritten with environment variables.__

# ```config.json``` file
## Example of ```config.json```

```
{
  "auth":
          [
            {
              "user": "Szt7TQpqbCQHpCg0",
              "key": "pHV2QrraLMVPb6Ns"
            }
          ],
  "ttl": 10,
  "root": "/Users/antoine/Documents/epfl-cede/noto-api/test-data",
  "chmod": false
}
```

## auth
Table of user and key for accessing API

## ttl
TimeToLive : time validity of the request (in seconds)

Env variable: `TTL`

## root
Path to the root of user directories.

Env variable: `HOMEROOT`


# Changing the production port

Edit ```systemd/notoapi.service``` and change the port in the ```gunicorn``` command.

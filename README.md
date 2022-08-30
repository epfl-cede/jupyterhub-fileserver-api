# JupyterHub Fileserver API

## Background
This software is intended to work with plugins for the
[Moodle learning management system](https://moodle.org). Please visit the following
repositories for further information about the Moodle plugins
 - [Jupyter assignment submission plugin](https://github.com/epfl-cede/moodle-mod-assign-submission-noto)
 - [Jupyter assignment feedback plugin](https://github.com/epfl-cede/moodle-mod-assign-feedback-noto)

It runs as a service in an environment which has access to the file storage used by
JupyterHub users as workspaces. It accepts requests from Moodle to copy files from a
teacher workspace to student workspaces, and vice versa.

## Execution Environments
The API service is in production use in two different environments, with JupyterHub and API running:
 - on "conventional" servers
 - in a Kubernetes cluster

While the Kubernetes environment is very generic and needs little to no extension, a conventional
server requires the API to get access to authentication and authorization services.

## Usage
### Configuration
Configuration may be done by a configuration file names `config.json` located in the root directory
of the installation. Some settings are configurable by environment variables. For a Kubernetes environment,
all applicable settings are covered by environment variables. See the supplied `config.json.example` for
information about the JSON structure of the configuration file.

 - `auth`: key/secret pair shared with the Moodle plugin configuration
 - `ttl`: time until the authentication secret built from `auth` expires
 - `root`: path in the execution environment to the user workspaces
 - `dynamic_root`: TBD
 - `chmod`: adjust file permissions after transfer

Corresponding environment variables:
 - `AUTH_USER`, `AUTH_KEY`
 - `TTL`
 - `HOMEROOT`

The other options are not applicable in Kubernetes and available in the configuration file only.

### On a File Server
Installation instructions and some low level documentation can be found in the [docs folder](docs).

### Kubernetes
The directory `deployment` contains an [example for a deployment](deployment/README.md) in Kubernetes.
It makes use of the highly versatile `kustomize` tool included in `kubectl`. The `base`directory may be
used by multiple installations and is referenced by the detailed
configuration in the `example` directory. Don't copy the example as is, but adopt it to your environment.

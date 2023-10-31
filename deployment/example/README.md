# Kustomization Example Specific for a Single JupyterHub Instance
We run one JupyterHub per Moodle course. This allows for easy individualisation of
courses and an uncomplicated lifecycle management, but comes at higher costs in respect to
memory and CPU consumption.

## kustomization.yml
The main file collects resources like the base, additional files and patches for existing objects.

## ingress.yml
Since an ingress object is highly specific to a Kubernetes application, it is not part of the base
and simply added per JupyterHub instance.

## env-vars.yml
The base deployment object has no environment variables defined. We patch the deployment with this
file and add the missing variables.

## volume.yml
The patch adds a reference to the PV created for the JupyterHub and mounts the volume to the same
mount point used in the environment variables patch. By adding the username to the mount point,
the API is able to access all user directories and copy files from and to the home directories.

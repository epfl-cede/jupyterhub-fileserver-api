# Kubernetes Deployment
This directory contains files to deploy the file server API in Kubernetes. It uses
`kustomize` to generate Kubernetes objects from templates. It is part of `kubectl` or
can be used as a standalone program. Find [more information at the website](https://kustomize.io/).

The configuration can be built with `kubectl` by changing to a directory and issuing

```shell
kubectl kustomize .
```

or
```shell
kustomize build .
```


## Directory `base`
`kustomize` works template-free, but the base directory can be treated as a kind of template. It defines
Kubernetes objects and attributes which are shared across different installations.

## Directory `example`
This directory provides all objects and attributes which complete the base to form a fully working API server
deployment. It adds deployment specific objects like an ingress or patches objects provided by the base.

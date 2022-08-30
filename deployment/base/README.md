# Base kustomize configuration
This directory may be used as a base resource for `kustomize` tool. API deployments share most
of the configuration items, keeping them in a common place makes it easier for updates.

## Kustomization
Attributes specific to individual API deployments will be overwritten later:

 - the image tag `latest` should be replaced by a stable version.
 - the PVC used to access the user homes is unique to each deployment

See the [example](../example) for details about the kustomization.

# Deployment

## Run Locally

To ease development, there is a `docker-compose.sh` helper script.

This runs docker compose to build and deploy containers to a local docker daemon.

```bash
./docker-compose.sh build <version>
./docker-compose.sh up <version>

# Application running on port 8000...
# Type Ctrl+C to quit.

./docker-compose.sh down <version>
```

## Deployment (Helm Charts)

To package the project, there is a helm chart called `qrcode-generator`. The version of this chart corresponds to the project version (>=0.7.0). To show an example deployment, I have used helmfile. This enables the user to deploy kafka and redis alongside the main chart.

To deploy using helmfile, follow these steps:

1. Set kubectl access to your cluster
2. Create a namespace (if applicable)
3. Change directories to `./helm` and run `helmfile apply`
4. Run `kubectl get services | grep public-api` to find the service port (using NodePort by default)

To cleanup the environment, run `helmfile destroy`.

Note: If using helmfile, note that some Persistent Volumes and Persistent Volume Claims may be left. To cleanup these, run `./cleanup.sh`.

---

[Back to README.md](../README.md)

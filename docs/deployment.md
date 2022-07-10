# Deployment

## Running Locally (Docker Compose)

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

Coming Soon!

---

[Back to README.md](../README.md)

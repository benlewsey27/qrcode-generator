# Testing

Note: All testing currently requires a live environment.

## Smoke Tests
A postman collection can be used to run a smoke test. The smoke tests include a basic happy flow to ensure an environment is working as expected.

To run these tests, install newman and run the following command.

``` bash
cd tests/smoke
newman run --env-var entrypoint-url='XXX' qrcode-generator-smoke-tests.postman_collection.json
```

## End To End Tests
A postman collection can be used to run a full end-to-end test. The e2e tests include a full list of flows to ensure an all valid requests are working as expected.

To run these tests, install newman and run the following command.

``` bash
cd tests/e2e
newman run --env-var public-api-url='XXX' qrcode-generator-e2e-tests.postman_collection.json
```

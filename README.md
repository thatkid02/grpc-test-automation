# grpc-test-automation

This project aims to automate grpc sanity tests just by providing the grpc host.

### Project Structure
```
├── docker
│   ├── Dockerfile.karate
│   └── Dockerfile.nestgrpc
├── docker-compose.yaml
├── grpc-python
│   ├── HelloService.feature
│   └── sanity.py
├── hello-world-demo
│   ├── hello.proto
│   ├── nest-cli.json
│   ├── package.json
│   ├── package-lock.json
│   ├── README.md
│   ├── src
│   │   ├── app.controller.spec.ts
│   │   ├── app.controller.ts
│   │   ├── app.module.ts
│   │   ├── app.service.ts
│   │   ├── grpc-client.options.ts
│   │   ├── hello
│   │   │   ├── hello.module.ts
│   │   │   ├── hello.service.spec.ts
│   │   │   └── hello.service.ts
│   │   └── main.ts
│   ├── test
│   │   ├── app.e2e-spec.ts
│   │   └── jest-e2e.json
│   ├── tsconfig.build.json
│   └── tsconfig.json
└── README.md
```

### Guide

- `hello-world-demo` project is a NestJS microservice exposing 
    - rest API : 0.0.0.0:3000
    - GRPC API : 0.0.0.0:5000
- `hello.proto` serves necessary schema
- `grpc-python` provides a simple script to list the collection of methods exposed by the service
- You can create .feature files using the script for the server you specified
- Thanks to [pecker-io](https://github.com/pecker-io), a neat demo of how to run the karate files for grpc is shown in [this repository](https://github.com/pecker-io/karate-grpc)

### Usage

#### Generate proto

```
python sanity.py 
```

```
docker compose up
``` 
The above command builds and runs the project
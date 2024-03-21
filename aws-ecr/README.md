# AWS ECR Dagger Module

## Usage

### Functions

If pulling module from Github:

* `dagger -m github.com/mjb141/daggerverse/aws-ecr functions`

If running module locally:

* `dagger functions`

### Help

* `dagger call with-credentials --help`
* `dagger call push --help`

### Examples

#### Shell

Push `alpine:latest` to an ECR repository named `test` in AWS account ID `123456789012` with it's existing tag (`latest`):

`dagger call with-credentials --access-key env:AWS_ACCESS_KEY_ID --secret-key env:AWS_SECRET_ACCESS_KEY --session-token env:AWS_SESSION_TOKEN push --ctr alpine:latest --account-id 123456789012 --repository test`

Push `alpine:latest` to an ECR repository named `test` in AWS account ID `123456789012` with a single new tag:

`dagger call with-credentials --access-key env:AWS_ACCESS_KEY_ID --secret-key env:AWS_SECRET_ACCESS_KEY --session-token env:AWS_SESSION_TOKEN push --ctr alpine:latest --account-id 123456789012 --repository test --tags new`

Push `alpine:latest` to an ECR repository named `test` in AWS account ID `123456789012` with multiple tags:

`dagger call with-credentials --access-key env:AWS_ACCESS_KEY_ID --secret-key env:AWS_SECRET_ACCESS_KEY --session-token env:AWS_SESSION_TOKEN push --ctr alpine:latest --account-id 123456789012 --repository test --tags new,latest,testing,1`

#### Module

Push `alpine:latest` to an ECR repository named `test` in AWS account ID `123456789012` with multiple tags:

```py
image = dag.container().from_("alpine:latest")

dag.aws_ecr().with_credentials(
    access_key = os.getenv("AWS_ACCESS_KEY_ID"),
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY"),
    session_token = os.getenv("AWS_SESSION_TOKEN")
).push(
    image,
    "123456789012",
    "test",
    tags = ["new", "latest", "1"]
)
```

Push a built image to an ECR repository named `test` in AWS account ID `123456789012` with a `latest` tag:

```py
image = dag.directory(".").docker_build()

dag.aws_ecr().with_credentials(
    access_key = os.getenv("AWS_ACCESS_KEY_ID"),
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY"),
    session_token = os.getenv("AWS_SESSION_TOKEN")
).push(
    image,
    "123456789012",
    "test",
    tags = ["latest"]
)
```

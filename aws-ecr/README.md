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

* Installation: See module installed as a dependency in [test/dagger.json](./test/dagger.json).
* Usage: See usage as a dependency in [test/dagger/src/main.py](./test/dagger/src/main.py)
* Run tests: See running these module as dependency tests in [test/README.md](./test/README.md)

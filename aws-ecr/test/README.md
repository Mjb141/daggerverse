To test:

Image built: `dagger call test-build --dir . --ak env:AWS_ACCESS_KEY_ID --sk env:AWS_SECRET_ACCESS_KEY --st env:AWS_SESSION_TOKEN --aid $AWS_ACCOUNT_ID --repo $AWS_ECR_NAME`

Image from another repository: `dagger call test-image --ak env:AWS_ACCESS_KEY_ID --sk env:AWS_SECRET_ACCESS_KEY --st env:AWS_SESSION_TOKEN --aid $AWS_ACCOUNT_ID --repo $AWS_ECR_NAME`

Tagging: `dagger call test-tagging --ak env:AWS_ACCESS_KEY_ID --sk env:AWS_SECRET_ACCESS_KEY --st env:AWS_SESSION_TOKEN --aid $AWS_ACCOUNT_ID --repo $AWS_ECR_NAME --tags hello,goodbye`

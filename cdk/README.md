## To test this module:

First assume a role that has permissions to deploy CDK stacks

`dagger -m "github.com/mjb141/daggerverse/cdk@main" call with-credentials --access-key $AWS_ACCESS_KEY_ID --secret-key $AWS_SECRET_ACCESS_KEY --ses-token $AWS_SESSION_TOKEN with-config --region <REGION> --account <ACCOUNT_ID> with-env-var --key MISC_VALUE --value daggerdeployment with-source --source . deploy`

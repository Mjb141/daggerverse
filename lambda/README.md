# Sample Poetry Lambda app

* Authenticate with AWS in your terminal

**Note**: The handler for the function must be set to `lambda_py.handler.handle`
This is formed of: 
* `lambda_py` (the package name)
* `handler` (the file name that contains the entry function)
* `handle` (the function name for the entry point)

### To use from Dagger:

#### Building:
* `dagger call with-sdk --sdk python with-source --source . build`

#### Interactive shell:
* `dagger call with-sdk --sdk python with-source --source test/lambda-py build terminal`

#### Export the zip for Lambda:
* `dagger download with-sdk --sdk python with-source --source . export`

#### Publish the zip to S3:
* `dagger call with-credentials --access-key env:AWS_ACCESS_KEY_ID --secret-key env:AWS_SECRET_ACCESS_KEY --ses-token env:AWS_SESSION_TOKEN with-sdk --sdk python with-source --source . publish --bucket_name $BUCKET_NAME --object-key $OBJECT_NAME`

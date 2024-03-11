# Sample Poetry Lambda app

* Authenticate with AWS in your terminal

**Note**: The handler for the function must be set to `lambda_py.handler.handle`
This is formed of: 
* `lambda_py` (the package name)
* `handler` (the file name that contains the entry function)
* `handle` (the function name for the entry point)

### To use from Dagger:

#### Building:
* `dagger call with-sdk --sdk python with-source --dir test/lambda-py build`

#### Interactive shell:
* `dagger call with-sdk --sdk python with-source --dir test/lambda-py build terminal`

#### Export the zip for Lambda:
* **Either**: `dagger call with-sdk --sdk python with-source --dir test/lambda-py zip-file export --path lambda.zip`
* **Or**: `dagger call with-sdk --sdk python with-source --dir test/lambda-py build file --path ../lambda.zip export --path ./lambda.zip`

#### Publish the zip to S3:
* `dagger call with-credentials --access-key env:AWS_ACCESS_KEY_ID --secret-key env:AWS_SECRET_ACCESS_KEY --ses-token env:AWS_SESSION_TOKEN with-sdk --sdk python with-source --dir test/lambda-py publish --bucket_name $BUCKET_NAME --object-key $OBJECT_NAME`

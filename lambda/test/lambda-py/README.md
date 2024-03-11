# Sample Poetry Lambda app

* Authenticate with AWS in your terminal

### To run the python yourself:

* `poetry run python lambda_py/handler.py`

### To prepare for Lambda:

* `poetry run pip install -t dist/lambda .`
* `cd dist/lambda`
* `zip -x '*.pyc' -r ../lambda.zip .`

The resulting `lambda.zip` should be uploaded to Lambda. 

**Note**: The handler for the function must be set to `lambda_py.handler.handle`
This is formed of: 
* `lambda_py` (the package name)
* `handler` (the file name that contains the entry function)
* `handle` (the function name for the entry point)

### To use from Dagger:

#### Building:
* `dagger call -m "github.com/mjb141/daggerverse/lambda@main" with-sdk --sdk python with-source --source . build`

#### Interactive shell:
* `dagger shell -m "github.com/mjb141/daggerverse/lambda@main" with-sdk --sdk python with-source --source . build`

#### Export the zip for Lambda:
* `dagger download -m "github.com/mjb141/daggerverse/lambda@main" with-sdk --sdk python with-source --source . export`

#### Publish the zip to S3:
* `dagger call -m "github.com/mjb141/daggerverse/lambda@main" with-credentials --access-key $AWS_ACCESS_KEY_ID --secret-key $AWS_SECRET_ACCESS_KEY --ses-token $AWS_SESSION_TOKEN with-sdk --sdk python with-source --source . publish --bucket_name $BUCKET_NAME --object-key $OBJECT_NAME`

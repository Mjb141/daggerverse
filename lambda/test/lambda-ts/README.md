# Sample Typescript Lambda app

* Authenticate with AWS in your terminal

### To prepare for Lambda:

* `npm run clean` (removes `dist/` directory if it exists)
* `npm run build` (creates the `dist/` directory with the build javascript file(s))
* `npm run zip` (zips up the contents of the `dist/` directory)

The resulting `lambda.zip` should be uploaded to Lambda. 

**Note**: The handler for the function must be set to `index.handler`
This is formed of: 
* `index` (the file name that contains the entry function)
* `handler` (the function name for the entry point)

### To use from Dagger:

#### Building:
* `dagger call with-sdk --sdk node with-source --dir test/lambda-ts build`

#### Interactive shell:
* `dagger call with-sdk --sdk node with-source --dir test/lambda-ts build terminal`

#### Export the zip for Lambda:
* **Either**: `dagger call with-sdk --sdk node with-source --dir test/lambda-ts zip-file export --path lambda.zip`
* **Or**: `dagger call with-sdk --sdk node with-source --dir test/lambda-py build file --path ../lambda.zip export --path ./lambda.zip`

#### Publish the zip to S3:
* `dagger call with-credentials --access-key env:AWS_ACCESS_KEY_ID --secret-key env:AWS_SECRET_ACCESS_KEY --ses-token env:AWS_SESSION_TOKEN with-sdk --sdk node with-source --dir test/lambda-ts publish --bucket_name $BUCKET_NAME --object-key $OBJECT_NAME`

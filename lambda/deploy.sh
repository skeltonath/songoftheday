#!/bin/bash

pushd () {
    command pushd "$@" > /dev/null
}

popd () {
    command popd "$@" > /dev/null
}

echo "Removing old zip"
rm song-of-the-day-lambda.zip

echo "Creating zip and adding dependencies"
pushd $VIRTUAL_ENV/lib/python3.6/site-packages/
zip -rq9 $VIRTUAL_ENV/song-of-the-day-lambda.zip *
popd

echo "Adding lambda function to zip"
zip -gq $VIRTUAL_ENV/song-of-the-day-lambda.zip lambda_function.py

echo "Uploading lambda to S3"
aws --profile schreef s3api put-object --bucket song-of-the-day --key song-of-the-day-lambda.zip --body $VIRTUAL_ENV/song-of-the-day-lambda.zip

echo "Updating lambda function"
aws --profile schreef lambda update-function-code --function-name song-of-the-day --s3-bucket song-of-the-day --s3-key song-of-the-day-lambda.zip --publish
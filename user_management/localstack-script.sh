#!/bin/bash

awslocal s3api \
create-bucket --bucket $S3_BUCKET_NAME \
--create-bucket-configuration LocationConstraint=eu-central-1 \
--region eu-central-1

awslocal ses verify-email-identity --email $EMAIL_IDENTITY

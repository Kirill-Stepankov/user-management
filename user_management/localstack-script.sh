#!/bin/bash


awslocal s3api \
create-bucket --bucket pic-storage \
--create-bucket-configuration LocationConstraint=eu-central-1 \
--region eu-central-1

#!/usr/bin/env python3
import json
import sys
import boto3
s3 = boto3.resource("s3")
for bucket_name in sys.argv[1:]:
    try:
        response = s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'})
        print (response)
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "AddPerm",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": ["s3:GetObject"],
                    "Resource": ["arn:aws:s3:::" + bucket_name + "/*"]
                }
            ]
        }
        # converting to a json format
        policy = json.dumps(policy)
        # adding policy to newly created bucket
        boto3.client('s3').put_bucket_policy(Bucket=bucket_name, Policy=policy)
        print("Bucket given read permissions")
    except Exception as error:
        print (error)

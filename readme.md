DevOps assignment Oct 2017

Scripts to automate creating and uploading to an AWS instance

AWS credentials are required
- install aws via pip if not installed
- input credentials with the 'aws configure' command

A key file is required
- Download into the containing folder or run the 'create_key_pair.py' script

The run_newwebserver script takes a key file as a parameter
This script will
- create a new ec2 instance using a pre-configured security group
- update and patch the instance
- upload a script to check for and, if required, launch nginx
- print some stats to a local file

The file_upload script takes four parameters:
- 1. The public IP of the instance
     Use list_instances.py to view the IP addresses of previously created active instances
- 2. The associated key_pair
- 3. The bucket containing the file
-    Use list_buckets.py to view buckets
-    Use create_bucket.py to create a new bucket
-    create_bucket takes one parameter, the name of the bucket
     this must be unique
     example: bucket-name-$(date +"%F-%s) is likely to be unique
- 4. The file name
e.g. ./file_upload.py 54.154.104.231 new_key.pem e.g. ./file_upload.py 54.154.104.231 new_key.pem
The script will append the file in an image tag to the host's index page
A sample image file 'meme.png' is included

The terminate_instances script with shut down all instances
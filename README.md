# Raze

Destroy multiple AWS resources based on resource tags.

## What is Raze?

Raze is a tool to destroy AWS resources that have not been created via infrastructure-as-code (IaC) tools, based on a set of provided tags.

## Why Raze?

The word [raze](https://dictionary.cambridge.org/dictionary/english/raze) is an Antonym for the word [terraform](https://dictionary.cambridge.org/dictionary/english/terraform). As Terraform is a useful tool for creating & managing resources, Raze is the opposite of this in that it destroys resources that are not under Terraform (or any other IaC) management.

## Prerequisites

* Python >= 3.6
* Pip

```bash
$ git clone https://gitlab.com/thesoy_sauce/raze.git
$ pip3 install -r requirements.txt
```

## Usage

```bash
usage: raze.py [-h] --tags TAGS [--output file_name]
               [--delete-csv {True,False}] [--s3upload {True,False}]
               [--bucket bucket_name] [--key object_key]

optional arguments:
  -h, --help            show this help message and exit
  --tags TAGS           A comma separated list of tag key/value pairs. E.g.
                        name=tagName,contact=me@domain.com
  --output file_name    Output CSV file path. Defaults to /tmp/raze-resource-
                        arns.csv
  --deletecsv {True,False}
                        Delete the generated CSV file from local disk if S3
                        upload is successful
  --s3upload {True,False}
                        If True, upload the CSV file defined by --output to S3
  --bucket bucket_name  The S3 bucket name to upload to if --s3upload is set
  --key object_key      The S3 object key if --s3upload is set
```

### Basic Usage - No S3 upload
```bash
$ python3 raze.py --tags "project=amazingproject,contact=me@domain.com"
2020-02-14 16:30:30 Found credentials in shared credentials file: ~/.aws/credentials
arn:aws:ec2:eu-west-1:1234567890:volume/vol-abcdef0123456789
arn:aws:ec2:eu-west-1:123456789:instance/i-abcdef0123456789
```

### Full Usage - With S3 Upload

```bash
$ python3 raze.py --output resource-arns.csv --bucket my-s3-bucket --key raze/resource-arns.csv --tags "project=amazingproject,contact=me@domain.com"
2020-02-14 16:35:46 Found credentials in shared credentials file: ~/.aws/credentials
2020-02-14 16:35:46 Extracting tags for resource: arn:aws:ec2:eu-west-1:1234567890:volume/vol-abcdef0123456789
2020-02-14 16:35:46 Extracting tags for resource: arn:aws:ec2:eu-west-1:1234567890:instance/i-abcdef0123456789
arn:aws:ec2:eu-west-1:1234567890:volume/vol-abcdef0123456789
arn:aws:ec2:eu-west-1:1234567890:instance/i-abcdef0123456789
/tmp/resource-arns.csv  528 / 528.0  (100.00%)
2020-02-14 16:35:46 Upload to S3 successful!

$ aws s3 ls s3://my-s3-bucket/raze/
2020-02-14 16:35:47        528 resource-arns.csv
```

### Raze CSV File

```text
$ cat ./resource-arns.csv
"ResourceArn","TagKey","TagValue"
"arn:aws:ec2:eu-west-1:1234567890:volume/vol-abcdef0123456789","contact","me@domain.com"
"arn:aws:ec2:eu-west-1:1234567890:volume/vol-abcdef0123456789","project","amazingproject"
"arn:aws:ec2:eu-west-1:1234567890:instance/i-abcdef0123456789","Name","luke-test"
"arn:aws:ec2:eu-west-1:1234567890:instance/i-abcdef0123456789","contact","me@domain.com"
"arn:aws:ec2:eu-west-1:1234567890:instance/i-abcdef0123456789","project","amazingproject"
```

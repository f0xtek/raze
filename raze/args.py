import argparse
import logging
import sys


class ArgParser(argparse.ArgumentParser):
    def __init__(self):
        super(ArgParser, self).__init__()
        self.add_argument(
            "--tags",
            required=True,
            type=str,
            help="A comma separated list of tag key/value pairs. E.g. name=tagName,contact=me@domain.com"
        )
        self.add_argument(
            "--output",
            required=False,
            default="/tmp/raze-resource-arns.csv",
            type=str,
            help="Output CSV file path. Defaults to /tmp/raze-resource-arns.csv",
            metavar="file_name"
        )
        self.add_argument(
            "--deletecsv",
            required=False,
            type=bool,
            choices=[True, False],
            help="Delete the generated CSV file from local disk if S3 upload is successful"
        )
        self.add_argument(
            "--s3upload",
            required=False,
            default=False,
            type=bool,
            help="If True, upload the CSV file defined by --output to S3",
            choices=[True, False]
        )
        self.add_argument(
            "--bucket",
            required=False,
            type=str,
            help="The S3 bucket name to upload to if --s3upload is set",
            metavar="bucket_name"
        )
        self.add_argument(
            "--key",
            required=False,
            default="raze/resource-arns.csv",
            type=str,
            help="The S3 object key if --s3upload is set",
            metavar="object_key"
        )

    def parse(self):
        return self.parse_args()

    def check(self):
        args = self.parse()
        if args.s3upload:
            if args.bucket is None:
                logging.error("ERROR: Must specify S3 bucket name when enabling S3 upload.\n")
                self.print_help()
                sys.exit(1)

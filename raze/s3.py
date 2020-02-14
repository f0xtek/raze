import logging
import boto3
from botocore.exceptions import ClientError
import raze.progress

class S3Upload:
    def __init__(self, csvfile, bucket, key):
        self.csvfile = csvfile
        self.bucket = bucket
        self.key = key

    def execute(self):
        """
        Upload the CSV report to the specified S3 bucket
        """
        if self.key is None:
            key = f'raze/{self.csvfile}'

        s3_client = boto3.client('s3')
        try:
            response = s3_client.upload_file(
                self.csvfile,
                self.bucket,
                self.key,
                Callback=raze.progress.ProgressPercentage(self.csvfile)
            )
        except ClientError as e:
            logging.error(e)
            return False
        return True

import logging
import sys
import boto3
from botocore.exceptions import ClientError


class ResourceGroupsTagging:
    def __init__(self, tag_filters):
        self.tag_filters = tag_filters

    def get(self, token=""):
        restag = boto3.client('resourcegroupstaggingapi')
        try:
            resp = restag.get_resources(
                TagFilters=self.tag_filters,
                ResourcesPerPage=50,
                PaginationToken=token
            )
            return resp
        except ClientError as e:
            logging.error(e)
            sys.exit(1)


class ArnList:
    def __init__(self):
        self._values = []

    def append(self, resource_tag_mapping):
        for resource in resource_tag_mapping:
            self._values.append(resource['ResourceARN'])

    def get(self):
        return self._values

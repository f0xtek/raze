import csv
import logging


class CSVFile:
    def __init__(self, output, tag_list=None):
        self.output = output
        self.tag_list = tag_list

    def write(self):
        """
        Write a list of resources that have tags defined in tags_list
        to a CSV file
        """
        field_names = ['ResourceArn', 'TagKey', 'TagValue']
        try:
            with open(self.output, 'w') as csvfile:
                writer = csv.DictWriter(
                    csvfile,
                    quoting=csv.QUOTE_ALL,
                    delimiter=',',
                    dialect='excel',
                    fieldnames=field_names)

                writer.writeheader()
                for resource in self.tag_list:
                    logging.info("Extracting tags for resource: %s", resource['ResourceARN'])
                    for tag in resource['Tags']:
                        row = dict(
                            ResourceArn=resource['ResourceARN'],
                            TagKey=tag['Key'],
                            TagValue=tag['Value']
                        )
                        writer.writerow(row)
        except Exception as e:
            logging.error(e)

import logging
import os
import sys
import raze.args
import raze.resources
import raze.s3
import raze.csv


def main():
    """
    main function
    """
    tags = args.tags.split(",")
    tag_filters = []
    for tag in tags:
        tag_key_val = tag.split("=")
        tag_filters.append(
            {
                'Key': tag_key_val[0],
                'Values': [
                    tag_key_val[1]
                ]
            }
        )
    resource_groups_tagging = raze.resources.ResourceGroupsTagging(tag_filters)
    response = resource_groups_tagging.get()
    arns = raze.resources.ArnList()

    arns.append(response['ResourceTagMappingList'])
    if args.s3upload:
        csvfile.tag_list = response['ResourceTagMappingList']
        csvfile.write()

    while 'PaginationToken' in response and response['PaginationToken']:
        token = response['PaginationToken']
        response = resource_groups_tagging.get(token)
        arns.append(response['ResourceTagMappingList'])
        if args.s3upload:
            csvfile.tag_list = response['ResourceTagMappingList']
            csvfile.write()

    [print(arn) for arn in arns.get()]

    if args.s3upload:
        s3_uploader = raze.s3.S3Upload(args.output, args.bucket, args.key)
        if s3_uploader.execute():
            logging.info("Upload to S3 successful!")
        else:
            logging.error("Upload to S3 failed. Exiting!")
            sys.exit(1)
        if args.deletecsv is not None:
            try:
                os.remove(args.output)
            except Exception as e:
                logging.error(f"Exception deleting CSV file: {e}\n")


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
    arg_parser = raze.args.ArgParser()
    arg_parser.check()
    args = arg_parser.parse()
    if args.s3upload:
        csvfile = raze.csv.CSVFile(args.output)
    main()

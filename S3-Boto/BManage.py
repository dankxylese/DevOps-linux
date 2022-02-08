import logging
import boto3
from botocore.exceptions import ClientError
import os

def main():
    bucket_name_save = ""
    #bucket_region_save = ""
    bucket_name_saved = False
    while True:
        print("")
        print("")
        print("")
        print("")
        print("----")
        print("1 - Create a bucket")
        print("2 - List all buckets")
        print("3 - Delete folder or everything")
        print("4 - Delete a bucket (only if its empty)")
        print("5 - Upload file")
        print("6 - List files")
        print("7 - Download file")
        print("----")
        print("9 - Save a Bucket name and region you want to work on")
        print("0 - Quit")
        print("----")
        action = input("What do you want to do from above?: ").lower()

        if action == "0":
            break
        if action == "9":
            name = input("Input Bucket name to keep in memory: ").lower()
            #hints()  # Print region name hints
            #region = input("Input Region name to keep in memory: ").lower()
            bucket_name_saved = True
            bucket_name_save = name
            #bucket_region_save = region


        if action == "1":  # Create a Bucket
            if bucket_name_saved:  # if bucket name and region already exist (through option 9)
                create_bucket(bucket_name_save, bucket_region_save)
            else:
                name = input("Input Bucket name: ").lower()
                #hints()  # Print region name hints
                #region = input("Input Region name: ").lower()
                create_bucket(name, "eu-west-1")

                save = input("Save bucket name in memory? (y/n): ").lower()

                if save == "y":
                    bucket_name_saved = True
                    bucket_name_save = name
                    #bucket_region_save = region
                    print("Saved")

        if action == "2":  # List all Buckets
            list_buckets()

        if action == "3":  # Delete folder or all files
            if bucket_name_saved:  # if bucket name and region already exist
                prefix = input("Input folder to delete (leave empty for everything): ").lower()
                delete_all_files(bucket_name_save, prefix)
            else:
                name = input("Input Bucket name to wipe clean: ").lower()
                prefix = input("Input folder to delete (leave empty for everything): ").lower()
                delete_all_files(name, prefix)

        if action == "4":  # Delete Bucket
            if bucket_name_saved:  # if bucket name and region already exist
                if delete_bucket(bucket_name_save):  # return true on success
                    print("Bucket Deleted")
                else:
                    print("Bucket Deletion Failed!")
            else:
                name = input("Input Bucket name to delete: ").lower()
                if delete_bucket(name):  # return true on success
                    print("Bucket Deleted")
                else:
                    print("Bucket Deletion Failed!")

        if action == "5":  # Upload a file
            if bucket_name_saved:  # if bucket name and region already exist
                file = input("Input file name to upload: ").lower()
                if upload_file(file, bucket_name_save):  # return true on success
                    print("File Uploaded")
                else:
                    print("File Upload Failed!")
            else:
                name = input("Input Bucket name to delete: ").lower()
                file = input("Input file name to upload: ").lower()
                if upload_file(file, name):  # return true on success
                    print("File Uploaded")
                else:
                    print("File Upload Failed!")
        if action == "6":  # List Files
            if bucket_name_saved:  # if bucket name and region already exist
                work_on_same = input("Would you like to work on the saved Bucket? (y/n): ").lower()
                if work_on_same == "y":  # Work on saved bucket?
                    prefix = input("Input folder to view (leave empty for root dir): ").lower()
                    list_files_in_bucket(bucket_name_save, prefix)
                else:
                    name = input("Input Bucket name to view: ").lower()
                    prefix = input("Input folder to view (leave empty for root dir): ").lower()
                    list_files_in_bucket(name, prefix)
            else:  # not saved
                name = input("Input Bucket name to view: ").lower()
                prefix = input("Input folder to view (leave empty for root dir): ").lower()
                list_files_in_bucket(name, prefix)
        if action == "7":  # Download file
            if bucket_name_saved:  # if bucket name and region already exist
                file_name = input("Input file to download: ").lower()
                download_file_s(file_name, bucket_name_save)
            else:
                bucket_name = input("Input Bucket name to download from: ").lower()
                file_name = input("Input file to download: ").lower()
                download_file_s(file_name, bucket_name)


def hints():
    print("HINTS")
    print("eu-west-1 - Ireland")
    print("eu-west-2 - London")
    
def download_file_s(file_name, bucket):
    #s3 = boto3.resource('s3')
    s3 = boto3.client('s3')
    try:
        response = s3.download_file(
            Bucket=bucket,
            Key=file_name,
            Filename=file_name
        )
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise

def list_buckets():
    # Retrieve the list of existing buckets
    s3 = boto3.client('s3')
    response = s3.list_buckets()

    # Output the bucket names
    print('Existing buckets:')
    for bucket in response['Buckets']:
        print(f'  {bucket["Name"]}')

def list_files_in_bucket(name, prefix=""):
    s3_client = boto3.client('s3')
    s3_resource = boto3.resource('s3')

    bucket = s3_resource.Bucket(name)
    count = bucket.objects.filter(Prefix=prefix)


    response = s3_client.list_objects_v2(Bucket=name, Prefix=prefix)
    if len(list(count)) == 0:
        print("Nothing to show - Bucket empty")
        return False
    else:
        for object in response['Contents']:
            print(object['Key'])

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def delete_all_files(name, prefix=""):
    s3_client = boto3.client('s3')

    response = s3_client.list_objects_v2(Bucket=name, Prefix=prefix)

    for object in response['Contents']:
        print('Deleting', object['Key'])
        s3_client.delete_object(Bucket=name, Key=object['Key'])

def delete_bucket(bucket_name):
    try:
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucket_name)
        bucket.delete()
    except ClientError as e:
        print(logging.error(e))
        return False
    return True

def create_bucket(bucket_name, region=None):
    # Create bucket
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        print(logging.error(e))
        return False
    return True



main()
import boto3
import botocore
import logging
import os
import csv


def get_ec2_session():
    session = boto3.session.Session(region_name=os.getenv("AWS_DEFAULT_REGION"))
    ec2 = session.resource(
        "ec2",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
    )
    return ec2

def get_s3_connection():
    s3 = boto3.client("s3")
    return s3


def is_bucket_available(bucket_name):
    s3 = get_s3_connection()
    list_of_buckets = s3.list_buckets()
    bucket_list_names = [bucket["Name"] for bucket in list_of_buckets["Buckets"]]
    if bucket_name not in bucket_list_names:
        return False
    else:
        return True


def upload_instance_file_to_s3(file_name):
    s3 = get_s3_connection()
    bucket_name = "abhishek-coda-bucket-ewrsd"
    if is_bucket_available(bucket_name):
        s3.upload_file(file_name, bucket_name, file_name)
    else:
        s3.create_bucket(Bucket=bucket_name)
        s3.upload_file(file_name, bucket_name, file_name)


def write_instances_to_csv(instance_id, name):
    file_name = "instances_list.csv"
    with open("file_name", "w+") as instance_file:
        file_writer = csv.writer(instance_file)
        file_writer.writerow([instance_id, name])
    upload_instance_file_to_s3(file_name)



def get_instances():
    ec2 = get_ec2_session()
    ec2_ = boto3.resource("ec2")
    inst_list = ec2_.instances.all()
    for inst in inst_list.all():
        write_instances_to_csv(inst.instance_id, inst.tags[0]["Value"])


if __name__ == "__main__":
    get_instances()

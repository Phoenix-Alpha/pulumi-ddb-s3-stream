import pulumi
from pulumi_aws import s3

from utils import format_resource_name


# Bucket for static assets
bucket = s3.Bucket(
    resource_name=format_resource_name(name='eu-west-1'),
)

pulumi.export('s3_bucket', bucket.bucket)
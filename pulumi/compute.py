import os
import json

import pulumi
from pulumi_aws import lambda_, iam

from utils import format_resource_name, filebase64sha256
from storage import bucket

# https://www.pulumi.com/docs/intro/concepts/config/
config = pulumi.Config()
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST_DIR = os.path.join(PROJECT_DIR, 'dist')

# Create role for Lambda
role = iam.Role(
    resource_name=format_resource_name(name='role'),
    description=f'Role used by Lambda to run the `{pulumi.get_project()}-{pulumi.get_stack()}` project',
    assume_role_policy=json.dumps({
      "Version": "2012-10-17",
      "Statement": [{
        "Sid": "",
        "Effect": "Allow",
        "Action": "sts:AssumeRole", 
        "Principal": {
          "Service": [
            "lambda.amazonaws.com"
          ]
        },
      }]
    }),
)

# Attach the basic Lambda execution policy to our Role
iam.RolePolicyAttachment(
    resource_name=format_resource_name(name='policy-attachment'),
    policy_arn='arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole',
    role=role.name,
)

# Create Lambda layer
LAYER_PATH = os.path.join(DIST_DIR, 'layer.zip')
layer = lambda_.LayerVersion(
    resource_name=format_resource_name(name='layer'),
    layer_name=format_resource_name(name='layer'),
    compatible_runtimes=['python3.7'],
    description=f'Layer containing the dependencies for the `{pulumi.get_project()}` ({pulumi.get_stack()}) project',
    code=LAYER_PATH,
    source_code_hash=filebase64sha256(LAYER_PATH),
)

# Create Lambda function
PACKAGE_PATH = os.path.join(DIST_DIR, 'function.zip')
function = lambda_.Function(
    resource_name=format_resource_name(name='function'),
    description=f'Lambda function running the f`{pulumi.get_project()}` ({pulumi.get_stack()}) project',
    handler=config.require('serverless_handler'),
    layers=[layer.arn],
    memory_size=128,
    role=role.arn,
    runtime="python3.7",
    tags={
        'PROJECT': pulumi.get_project()
    },
    timeout=30,
    tracing_config=None, # TODO: add AWS X-Ray tracing
    code=PACKAGE_PATH,
    source_code_hash=filebase64sha256(PACKAGE_PATH),
    environment={
      'variables' : {
        'BUCKET_NAME': bucket.bucket,
      }
    },
)

# Exports
pulumi.export('function_role_name', role.name)
pulumi.export('layer_name',  layer.layer_name)
pulumi.export('function_name',  function.name)
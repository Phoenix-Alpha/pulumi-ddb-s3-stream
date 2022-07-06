[![Deploy](https://get.pulumi.com/new/button.svg)](https://app.pulumi.com/new)

# Overview

The purpose of this bucket is to set up best practices for quickly developing Pulumi projects in Python.

## Directory structure

```
.
├── Makefile
├── Pulumi.yaml
├── README.md
├── handler.py
├── pulumi
│   ├── __main__.py
│   ├── component.py
│   ├── compute.py
│   ├── dynamic_providers
│   │   ├── __init__.py
│   │   └── github
│   │       ├── __init__.py
│   │       └── label.py
│   ├── label.py
│   ├── stacks
│   │   └── Pulumi.dev.yaml
│   ├── storage.py
│   └── utils.py
└── requirements
    ├── dynamic_providers.txt
    ├── global.txt
    └── lambda.txt
```

Note that each Pulumi resource is separated by category (ex: compute, storage...)
[__main__.py](./pulumi/__main__.py) merely contains import statements.

## Dynamic Provider

Pulumi [Dynamic Providers](https://www.pulumi.com/docs/intro/concepts/programming-model/#dynamicproviders) allows you to easily code in Python a provising logic for resources that do not yet have a Terraform provider.

The boilerplate is inspired upon the [Github example](https://www.pulumi.com/docs/intro/concepts/programming-model/#example-github-labels-rest-api) in the documentation.

The dynamic provider itself is in [pulumi/dynamic_providers/github](./pulumi/dynamic_providers/github) but the resource declaration has been moved to [pulumi/label.py](./pulumi/label.py).

Since most dynamic providers will require SDKs, we've created a separate requirements file for that purpose.

## Lambda

The [Makefile](./Makefile) contains basic boilerplate for packaging a Lambda (which you may or may not need depending on your project).

In order to notify Pulumi wether the Lambda needs to be updated, we're using a hashing mechanism (see [utils.py](./pulumi/utils.py) that checks the packages zip file : everytime you make a new zip, Pulumi detects the change and performs the update of the function during the next `pulumi up`.

Lambda also has its own requirements file in order to limit the package size : we only put in [requirements/lambda.txt](./requirements/lambda.txt) what is actually needed for the Lambda to run.
If your Lambda doesn't require extra `pip` packages then you can simply ignore the Layer part of the Makefile and in [compute.py](./pulumi/compute.py).

# Getting started

A good place to start with Pulumi is the [Documentation](https://www.pulumi.com/docs/).

Most of the AWS-related documentation in Pulumi is somewhat lacking, so the best place to get info regarding AWS is to look at the [Terraform counterpart](https://www.terraform.io/docs/providers/aws/) (since Pulumi is merely a wrapper around it).

Ultimately, the best documentation for Pulumi is its source code available on [Github](https://github.com/pulumi/pulumi-aws/tree/master/sdk/python/pulumi_aws).

from aws_cdk import (
    aws_pinpoint as pinpoint,
    aws_s3 as s3,
    CfnParameter,
    RemovalPolicy,
    Stack
)
from typing import Dict


def build_stack(
    stack: Stack,
    stack_context: Dict[str, str],
    stack_params: Dict[str, CfnParameter]
) -> None:

    pinpoint.CfnApp(
        stack, 'EMTPinpointApp',
        name=f'''EMTPinpointApp{stack_context['ENV']}'''
    )
    # TODO - IN CONSOLE: Get Pinpoint Application ID

    s3.Bucket(
        stack, "EMTS3Bucket",
        bucket_name=stack_params['S3BucketName'].value_as_string,
        encryption=s3.BucketEncryption.S3_MANAGED,
        removal_policy=RemovalPolicy.DESTROY
    )
    # TODO - IN CONSOLE: grant_public_access() to bucket objects
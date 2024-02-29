#!/usr/bin/env python3
import aws_cdk as cdk

from emt_infra.emt_stack_manager import EmtStackManager


app = cdk.App()

EmtStackManager(
    app, "EmtBackendStack",
    env=cdk.Environment(region="us-east-2"),
    selected_stack="backend"
)
EmtStackManager(
    app, "EmtInfraStack",
    env=cdk.Environment(region="us-east-2"),
    selected_stack="infra"
)

app.synth()

#!/usr/bin/env python3
import aws_cdk as cdk

from emt_infra.emt_stack_manager import EmtStackManager
# from emt_infra.emt_backend_stack import EmtBackendStack


app = cdk.App()

EmtStackManager(
    app, "EmtBackendStack",
    env=cdk.Environment(region="us-east-2"),
    selected_stack="backend"
)
# EmtInfraStack(
#     app, "EmtInfraStack",
#     env=cdk.Environment(region="us-east-2")
# )

app.synth()

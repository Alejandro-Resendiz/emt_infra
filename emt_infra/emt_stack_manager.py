from aws_cdk import (
    Stack,
    CfnParameter,
)
from constructs import Construct
from emt_infra.emt_backend_stack import (
    build_stack as build_backend_stack
)
# from emt_infra_stack import build_stack as build_infra_stack


class EmtStackManager(Stack):

    def __init__(
        self, scope: Construct, construct_id: str, selected_stack=None, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Stack Environment
        ENV_CTX = scope.node.get_context("env")

        # Stack Parameters
        # TODO - Remove Role Name
        LAMBDA_ROLE_NAME_PARAM = CfnParameter(
            self, 'LambdaRoleName',
            type='String',
            default='LambdaPinpointRole'
        )

        # Stacks
        if selected_stack == "infra":
            pass
        elif selected_stack == "backend":
            build_backend_stack(
                self,
                stack_context={
                    'ENV': ENV_CTX,
                },
                stack_params={
                    'LambdaRoleName': LAMBDA_ROLE_NAME_PARAM,
                }
            )

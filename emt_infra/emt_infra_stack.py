from aws_cdk import (
    aws_pinpoint as pinpoint,
    CfnParameter,
    Stack
)
from constructs import Construct


class EmtInfraStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ENV_param = CfnParameter(
            self, 'ENVNameParam',
            type='String',
            default='DEV',
            allowed_values=['DEV', 'PROD']
        )

        pinpoint.CfnApp(
            self, 'EMTPinpointApp',
            name=f'EMTPinpointApp{ENV_param.value_as_string}'
        )


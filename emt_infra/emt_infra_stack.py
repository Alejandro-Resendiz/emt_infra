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
        # TODO: Get Pinpoint Application ID from console

        # TODO: Remove if not needed
        # emt_campaigns_table_name = f'EMTRestApiTable{ENV_param.value_as_string}'
        # emt_campaigns_table = dynamodb.Table(
        #     self, 'EMTRestApiTable',
        #     table_name=emt_campaigns_table_name,
        #     partition_key=dynamodb.Attribute(
        #         name='campaign_id',
        #         type=dynamodb.AttributeType.STRING
        #     ),
        #     billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
        # )

        # CfnOutput(
        #     self,
        #     id='EMTCampaignsTableName',
        #     value=emt_campaigns_table.table_name,
        #     description='Pinpoint API URL'
        # )

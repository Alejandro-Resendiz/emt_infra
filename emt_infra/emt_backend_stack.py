from aws_cdk import (
    aws_apigatewayv2 as apigw2,
    aws_iam as iam,
    aws_lambda as _lambda,
    CfnParameter,
    Duration,
    Stack
)
from typing import Dict


def build_stack(
    stack: Stack,
    stack_context: Dict[str, str],
    stack_params: Dict[str, CfnParameter]
) -> None:

    emt_lambda_role = iam.Role.from_role_name(
        stack, 'EMTLambdaRole',
        role_name=stack_params['LambdaRoleName'].value_as_string
    )

    emt_lambda = _lambda.Function(
        stack, 'EMTLambdaHandler',
        function_name=f'''EMTRestApiHandler{stack_context['ENV']}''',
        runtime=_lambda.Runtime.PYTHON_3_9,
        timeout=Duration.seconds(15),
        code=_lambda.Code.from_asset('emt_infra'),
        handler='src.lambda_handlers.handler_manager',
        environment={
                'REGION_NAME': stack.region,
                # 'EMT_PINPOINT_APP_ID': ,
        },
        role=emt_lambda_role
    )

    # emt_api = apigw2.CfnApi(
    #     stack, 'EMTApiGwApi',
    #     name=f'''EMTApiGwApi{stack_context['ENV']}''',
    #     protocol_type="HTTP",
    #     cors_configuration=apigw2.CfnApi.CorsProperty(
    #         allow_credentials=False,
    #         allow_headers=["allowHeaders"],
    #         allow_methods=["allowMethods"],
    #         allow_origins=["allowOrigins"],
    #         expose_headers=["exposeHeaders"],
    #         max_age=300
    #     ),
    #     # credentials_arn="credentialsArn",
    #     target=emt_lambda.function_arn
    # )

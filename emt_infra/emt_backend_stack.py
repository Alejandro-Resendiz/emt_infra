from aws_cdk import (
    aws_apigatewayv2 as apigwv2,
    aws_iam as iam,
    aws_lambda as _lambda,
    CfnParameter,
    Duration,
    Stack
)
from aws_cdk.aws_apigatewayv2_integrations import HttpLambdaIntegration
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
    emt_email_lambda = _lambda.Function(
        stack, 'EMTEmailLambdaHandler',
        function_name=f'''EMTRestEmailApiHandler{stack_context['ENV']}''',
        runtime=_lambda.Runtime.PYTHON_3_9,
        timeout=Duration.seconds(15),
        code=_lambda.Code.from_asset('emt_infra'),
        handler='src.lambda_handlers.email_handler',
        environment={
                'EMT_PINPOINT_APP_ID': '84c08d3b84a54b77a984f905762f6911',  # TODO: Remove App ID
        },
        role=emt_lambda_role
    )
    emt_file_lambda = _lambda.Function(
        stack, 'EMTFileLambdaHandler',
        function_name=f'''EMTRestFileApiHandler{stack_context['ENV']}''',
        runtime=_lambda.Runtime.PYTHON_3_9,
        timeout=Duration.seconds(15),
        code=_lambda.Code.from_asset('emt_infra'),
        handler='src.lambda_handlers.file_handler',
        environment={
                'EMT_S3_BUCKET_NAME': stack_params['S3BucketName'].value_as_string
        },
        role=emt_lambda_role
    )

    emt_api = apigwv2.HttpApi(
        stack, 'EMTApiGwApi',
        api_name=f'''EMTApiGwApi{stack_context['ENV']}''',
        cors_preflight=apigwv2.CorsPreflightOptions(
            allow_headers=[
                "Content-Type",
                "X-Amz-Date",
                "Authorization",
                "X-Api-Key",
                "X-Amz-Security-Token"
            ],
            allow_methods=[
                apigwv2.CorsHttpMethod.HEAD,
                apigwv2.CorsHttpMethod.OPTIONS,
                apigwv2.CorsHttpMethod.GET,
                apigwv2.CorsHttpMethod.POST,
                apigwv2.CorsHttpMethod.DELETE
            ],
            allow_origins=["*"],
            max_age=Duration.days(10)
        ),
        create_default_stage=False
    )

    emt_email_integration = HttpLambdaIntegration(
        'EMTEmailLambdaIntegration', emt_email_lambda,
    )
    emt_file_integration = HttpLambdaIntegration(
        'EMTFileLambdaIntegration', emt_file_lambda,
        parameter_mapping=apigwv2.ParameterMapping().append_query_string(
            "filename",
            apigwv2.MappingValue.request_query_string("filename")
        )
    )

    emt_api.add_routes(
        path="/email",
        methods=[apigwv2.HttpMethod.POST],
        integration=emt_email_integration,
    )
    emt_api.add_routes(
        path="/email",
        methods=[apigwv2.HttpMethod.GET],
        integration=emt_email_integration,
    )
    emt_api.add_routes(
        path="/file",
        methods=[apigwv2.HttpMethod.POST],
        integration=emt_file_integration,
    )
    emt_api.add_routes(
        path="/file/{key}",
        methods=[apigwv2.HttpMethod.DELETE],
        integration=emt_file_integration,
    )

    apigwv2.HttpStage(
        stack, "EmtApiGwStage",
        stage_name="v1",
        auto_deploy=True,
        http_api=emt_api
    )

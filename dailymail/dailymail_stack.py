import constructs
from aws_cdk import (
    Stack,
    aws_lambda as lambda_,
    Duration,
    aws_events_targets,
    aws_events as events,
    aws_iam as iam,
    aws_s3,
    aws_s3_deployment,
    CfnParameter,
    aws_ses,
    aws_dynamodb,
    aws_apigateway
)
from constructs import Construct


class DailymailStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        email = CfnParameter(self, "email", type="String", description="email address")
        scheduled_lambda = lambda_.Function(self, "MyDailyMail",
                                            handler='lambda_function.lambda_handler',
                                            runtime=lambda_.Runtime.PYTHON_3_8,
                                            code=lambda_.Code.from_asset(path="src"),
                                            )
        bucket = aws_s3.Bucket(self, "TestBucket", bucket_name="testbucketcdk1241210",)
        bucket.grant_read(scheduled_lambda)
        deployment = aws_s3_deployment.BucketDeployment(self, "TestDeployment",
                                                        sources=[aws_s3_deployment.Source.asset(path="resource")],
                                                        destination_bucket=bucket,
                                                        )
        email_identity = aws_ses.EmailIdentity(self, "my_email", identity=aws_ses.Identity.email(email.value_as_string))
        scheduled_lambda.add_to_role_policy(iam.PolicyStatement(effect=iam.Effect.ALLOW,
                                                                resources=[f"arn:aws:ses:eu-north-1:916886530732:identity/{email}"],
                                                                actions=["ses:SendEmail", "ses:SendRawEmail",
                                                                         "ses:SendTemplatedEmail",
                                                                         ]
                                                                ))
        table = aws_dynamodb.TableV2(self, "Table", partition_key=aws_dynamodb.Attribute(name="email", type=aws_dynamodb.AttributeType.STRING),
                                     sort_key=aws_dynamodb.Attribute(name="date", type=aws_dynamodb.AttributeType.STRING),
                                     contributor_insights=True,
                                     table_class=aws_dynamodb.TableClass.STANDARD_INFREQUENT_ACCESS,
                                     point_in_time_recovery=True,
                                     table_name="DailyTable",
                                     )
        scheduled_lambda.add_to_role_policy(iam.PolicyStatement(effect=iam.Effect.ALLOW,
                                                                resources=[table.table_arn],
                                                                actions=["dynamodb:BatchGetItem",
                                                                         "dynamodb:BatchWriteItem",
                                                                         "dynamodb:DeleteItem",
                                                                         "dynamodb:GetItem",
                                                                         "dynamodb:PutItem",
                                                                         "dynamodb:Query",
                                                                         "dynamodb:UpdateItem"
                                                                         ]
                                                                ))
        principal = iam.ServicePrincipal("events.amazonaws.com")
        scheduled_lambda.grant_invoke(principal)
        rule = events.Rule(self, "Rule", schedule=events.Schedule.rate(Duration.hours(24)))

        rule.add_target(aws_events_targets.LambdaFunction(scheduled_lambda, event=events.RuleTargetInput.from_object(
            {"bucket": "testbucketcdk1241210", "address": email, "content": "email_content.txt"}), retry_attempts=1))

        api = aws_apigateway.LambdaRestApi(self, "DailyApi", rest_api_name="DailyApi01", handler=scheduled_lambda)
        mail_resource = api.root.add_resource("mail")
        mail_resource.add_method("POST")
        deployment = aws_apigateway.Deployment(self, "Deployment", api=api)
        api_principal = iam.ServicePrincipal("apigateway.amazonaws.com")
        scheduled_lambda.grant_invoke(api_principal)
        
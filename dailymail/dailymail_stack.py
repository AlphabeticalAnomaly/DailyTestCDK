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
)
from constructs import Construct


class DailymailStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        email = CfnParameter(self, "email", type="string", description="email address")
        scheduled_lambda = lambda_.Function(self, "MyDailyMail",
                                            handler='lambda_function.lambda_handler',
                                            runtime=lambda_.Runtime.PYTHON_3_8,
                                            code=lambda_.Code.from_asset('lambda'),
                                            )
        bucket = aws_s3.Bucket(self, "TestBucket", bucket_name="testbucketcdk1241210",)
        bucket.grant_read(scheduled_lambda)
        deployment = aws_s3_deployment.BucketDeployment(self, "TestDeployment",
                                                        sources=[aws_s3_deployment.Source.asset(path="./resource")],
                                                        destination_bucket=bucket,
                                                        )

        scheduled_lambda.add_to_role_policy(iam.PolicyStatement(effect=iam.Effect.ALLOW,
                                                                resources=[f"arn:aws:ses:eu-north-1:916886530732:identity/{email}"],
                                                                actions=["ses:SendEmail", "ses:SendRawEmail",
                                                                         "ses:SendTemplatedEmail",
                                                                         ]
                                                                ))
        principal = iam.ServicePrincipal("events.amazonaws.com")
        scheduled_lambda.grant_invoke(principal)

        rule = events.Rule(self, "Rule", schedule=events.Schedule.rate(Duration.hours(24)))

        rule.add_target(aws_events_targets.LambdaFunction(scheduled_lambda, event=events.RuleTargetInput.from_object(
            {"bucket": bucket.bucket_name, "address": f"{email}", "content": "email_content.txt"}), retry_attempts=1))

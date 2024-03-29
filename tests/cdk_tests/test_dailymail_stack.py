import aws_cdk as core
import aws_cdk.assertions as assertions
from dailymail.dailymail_stack import DailymailStack


def test_synthesizes_properly():
    app = core.App()
    stack = DailymailStack(app, "MyDailyMail")
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties(
        "AWS::Lambda::Function",
        {
            "Handler": "lambda_function.lambda_handler",
            "Runtime": "python3.8"
        },
    )

    template.has_resource_properties(
        "AWS::Lambda::Permission",
        {
            "Action": "src:InvokeFunction",
            "Principal": "events.amazonaws.com"
        }
    )

    template.has_resource_properties(
        "AWS::Lambda::LayerVersion",
        {
            "Content":
                {
                    "S3Bucket": {
                        "Fn::Sub": "cdk-hnb659fds-assets-${AWS::AccountId}-${AWS::Region}"
                    }
                }
        }
    )

    template.has_parameter(
        "TestBucket560B80BC",
        {
            "type": "AWS::S3::Bucket",
            "Properties":
                {
                  "BucketName": "testbucketcdk1241210"
                }
        }
    )

    template.has_resource_properties(
        "AWS::Events::Rule",
        {
            "ScheduleExpression": "rate(1 day)",
            "State": "ENABLED"
        }
    )


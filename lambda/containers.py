from dependency_injector import containers, providers
import boto3


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=["decode_function.py", "mail_client.py"])

    s3_client = providers.Singleton(
        boto3.client('s3'),

    )

    ses_client = providers.Singleton(
        boto3.client('ses')
    )

from dependency_injector import containers, providers
import boto3


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=["decode_function.py", "mail_client.py"])

    boto3_client_s3 = providers.Singleton(
        boto3.client('s3'),

    )

    boto3_client_ses = providers.Singleton(
        boto3.client('ses')
    )

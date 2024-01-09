from dependency_injector import containers, providers
import boto3.session


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=["decode_function.py", "mail_client.py"])

    session = providers.Resource(
        boto3.session.Session
    )

    s3_client = providers.Singleton(
        session.provided.call(),
        service_name='s3',

    )

    ses_client = providers.Singleton(
        session.provided.call(),
        service_name='ses',
    )





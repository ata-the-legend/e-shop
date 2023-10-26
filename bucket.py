import boto3
import logging
from django.conf import settings
import logging
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)


class Bucket:
    """CDN bucket manager

    init method creates connection.

    NOTE:
        None of the methods are async. Use public interface in tasks.py modules instead.
    """

    def __init__(self) -> None:
        # https://docs.arvancloud.ir/fa/developer-tools/sdk/object-storage/object-list/
        self.storage_setting = settings.STORAGES['default']['OPTIONS']
        session = boto3.session.Session()
        try:
            self.s3_resource = session.resource(
                service_name=settings.AWS_SERVICE_NAME,
                endpoint_url=self.storage_setting['endpoint_url'],
                aws_access_key_id=self.storage_setting['access_key'],
                aws_secret_access_key=self.storage_setting['secret_key'],
        )
            self.bucket_name = self.storage_setting['bucket_name']
        except Exception as exc:
            logging.error(exc)  

    def get_objects(self):
        try:
            bucket = self.s3_resource.Bucket(self.bucket_name)
            # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/objectsummary/index.html
            return bucket.objects.all()

        except ClientError as e:
            logging.error(e)

    def delete_object(self, object_name: str):
        try:
            bucket = self.s3_resource.Bucket(self.bucket_name)
            object = bucket.Object(object_name)

            response = object.delete(
                VersionId='string',
            )
        except ClientError as e:
            logging.error(e)


bucket = Bucket()
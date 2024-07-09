import tempfile
import warnings

from airflow.providers.google.cloud.hooks.gcs import GCSHook

from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class ContentToGoogleCloudStorageOperator(BaseOperator):
    """
    Uploads a text content to Google Cloud Storage.
    Optionally can compress the content for upload.

    :param content: Content to upload. (templated)
    :type src: str
    :param dst: Destination path within the specified bucket, it must be the full file path
        to destination object on GCS, including GCS object (ex. `path/to/file.txt`) (templated)
    :type dst: str
    :param bucket: The bucket to upload to. (templated)
    :type bucket: str
    :param gcp_conn_id: (Optional) The connection ID used to connect to Google Cloud Platform.
    :type gcp_conn_id: str
    :param mime_type: The mime-type string
    :type mime_type: str
    :param delegate_to: The account to impersonate, if any
    :type delegate_to: str
    :param gzip: Allows for file to be compressed and uploaded as gzip
    :type gzip: bool
    """
    template_fields = ('content', 'dst', 'bucket')

    @apply_defaults
    def __init__(self,
                 content,
                 dst,
                 bucket,
                 gcp_conn_id='google_cloud_default',
                 mime_type='application/octet-stream',
                 delegate_to=None,
                 gzip=False,
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)

        self.content = content
        self.dst = dst
        self.bucket = bucket
        self.gcp_conn_id = gcp_conn_id
        self.mime_type = mime_type
        self.delegate_to = delegate_to
        self.gzip = gzip

    def execute(self, context):
        """
        Uploads the file to Google cloud storage
        """
        hook = GCSHook(
            gcp_conn_id=self.gcp_conn_id,
            delegate_to=self.delegate_to
        )

        with tempfile.NamedTemporaryFile(prefix="gcs-local") as file:
            file.write(self.content.encode())
            file.flush()
            hook.upload(
                bucket_name=self.bucket,
                object_name=self.dst,
                filename=file.name,
                gzip=self.gzip,
            )

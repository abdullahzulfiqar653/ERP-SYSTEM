from storages.backends.s3boto3 import S3Boto3Storage
import os


class MediaStorage(S3Boto3Storage):
    location = 'media'
    file_overwrite = False
    default_acl = 'private'
    custom_domain = False


class StaticStorage(S3Boto3Storage):
    location = 'static'
    default_acl = 'public-read'


class PublicMediaStorage(S3Boto3Storage):
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False


class DownloadablePublicMediaStorage(S3Boto3Storage):
    print("here")
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False

    def get_object_parameters(self, name):
        object_params = self.object_parameters.copy()
        object_params.update(
            {'ContentDisposition': f'attachment; filename="{os.path.basename(name)}"'})
        print(object_params)
        return object_params


class PrivateMediaStorage(S3Boto3Storage):
    location = 'private'
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False


class DownloadablePrivateMediaStorage(S3Boto3Storage):

    location = 'private'
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False

    def get_object_parameters(self, name):
        object_params = self.object_parameters.copy()
        object_params.update(
            {'ContentDisposition': f'attachment; filename="{os.path.basename(name)}"'})
        return object_params

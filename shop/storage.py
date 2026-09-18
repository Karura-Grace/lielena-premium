from urllib.parse import quote
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class SupabasePublicStorage(S3Boto3Storage):
    def url(self, name, parameters=None, expire=None, http_method=None):
        name = quote(name, safe="/")
        return (
            f"https://{settings.SUPABASE_PROJECT_REF}.supabase.co"
            f"/storage/v1/object/public/"
            f"{settings.SUPABASE_STORAGE_BUCKET}/{name}"
        )
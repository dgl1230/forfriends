from storages.backends.s3boto import S3BotoStorage
from boto.s3.connection import S3Connection, Bucket, Key

from settings.deployment import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME

StaticRootS3BotoStorage = lambda: S3BotoStorage(location='static')
MediaRootS3BotoStorage  = lambda: S3BotoStorage(location='media')




def delete_s3_pic(user, image):

	conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

	b = Bucket(conn, AWS_STORAGE_BUCKET_NAME)

	k = Key(b)

	k.key = 'media/profiles/%s/'+image
	b.delete_key(k)
	return 

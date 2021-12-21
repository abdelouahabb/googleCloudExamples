from wand.image import Image
from google.cloud import storage

client = storage.Client()

PREFIX = "thumbnail"

def make_thumbnail(data, context):
    # Don't generate a thumbnail for a thumbnail
    if data['name'].startswith(PREFIX):
        return

    # Get the bucket which the image has been uploaded to
    bucket = client.get_bucket(data['bucket'])

    # Download the image and resize it
    thumbnail = Image(blob=bucket.get_blob(data['name']).download_as_string())
    thumbnail.resize(100, 100)

    # Upload the thumbnail with the filename prefix
    thumbnail_blob = bucket.blob(f"{PREFIX}-{data['name']}")
    thumbnail_blob.upload_from_string(thumbnail.make_blob(), content_type="image/jpeg")
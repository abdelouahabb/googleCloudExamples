import proto
from google.cloud import vision, storage

vision_client = vision.ImageAnnotatorClient()
storage_client = storage.Client()

def hello_gcs(event, context):
  # get the name of the bucket (without gs://)
  bucket = storage_client.bucket(event['bucket'])
  # name the file, each image will have its own result
  blob = bucket.blob(event['name']+'_result.json')
  # let's build the full image uri
  image_uri = "gs://" + event['bucket'] + "/" + event['name']
  # we want to execute the code only when the user uploads the image
  # here we can also use content types, this is a generic trick
  # dont rely on image extension, we need something advanced to check
  # if the file is a real image (its header), 
  # but for the simplicity of the example, let's make things easy
  #if event['contentType'] in ['image/apng', 'image/avif', 'image/gif', 'image/jpeg', 'image/png', 'image/svg+xml', 'image/webp']:
  if image_uri.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
    response = vision_client.annotate_image({
      'image': {'source': {'image_uri': image_uri}},
      'features': [{'type_': vision_client.Feature.Type.FACE_DETECTION}]
      })
    print("______here we go______")
    # the result is a special type, we need to convert it to something readable
    texts = proto.Message.to_json(response)
    # reupload the response result to the same bucket
    blob.upload_from_string(texts)
    print("______finished_______")
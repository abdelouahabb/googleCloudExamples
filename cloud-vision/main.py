'''
google-cloud-storage
google-cloud-vision
protobuf
'''

import proto
from google.cloud import vision, storage

vision_client = vision.ImageAnnotatorClient()
storage_client = storage.Client()

def hello_gcs(event, context):
  bucket = storage_client.bucket(event['bucket'])
  blob = bucket.blob(event['name']+'_result.json')
  image_uri = "gs://" + event['bucket'] + "/" + event['name']
  #if event['contentType'] in ['image/apng', 'image/avif', 'image/gif', 'image/jpeg', 'image/png', 'image/svg+xml', 'image/webp']:
  if image_uri.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
    response = vision_client.annotate_image({
      'image': {'source': {'image_uri': image_uri}},
      'features': [{'type_': vision_client.Feature.Type.FACE_DETECTION}]
      })
    print("______here we go______")
    texts = proto.Message.to_json(response)
    blob.upload_from_string(texts)
    print("______finished_______")
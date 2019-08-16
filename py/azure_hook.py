import io
import base64
from azure.storage.blob import BlockBlobService
from PIL import Image
from datetime import datetime


def get_blobs_with_prefix(blobs, prefix):
    results = []

    for blob in blobs:
        blob_name = blob.name

        if "/" in blob_name:
            blob_name = blob_name.split("/")[1]

        blob_prefix = ""
        if "_" in blob_name:
            blob_prefix = blob_name.split("_")[0]

        if blob_prefix == prefix:
            results.append(blob)

    return results


def fetchImages(prefix, connection_string, container):
    blob_service = BlockBlobService(connection_string=connection_string)

    prefixed_blobs = get_blobs_with_prefix(
        blob_service.list_blobs(container), prefix)

    if len(prefixed_blobs) <= 0:
        raise ValueError("Blobs with prefix not found")

    selfie, ids = None, []

    # Todo: Make this more generic
    for blob in prefixed_blobs:
        blob_stream = io.BytesIO()
        # Stream the blob and convert it to a bytearray for easy serialization
        blob_service.get_blob_to_stream(
            container, blob.name, blob_stream)
        try:
            image = Image.open(blob_stream)
            if "selfie" in blob.name != -1:
                selfie = image
            elif "id" in blob.name != -1:
                ids.append(image)
            print("[INFO]: Added {}".format(blob.name))
        except:
            # Todo: Should probably error here 
            print("[INFO]: Unable to load {}".format(blob.name))
       

    # Some sanity checks
    if selfie == None:
        print("A selfie with that prefix could not be found")
        raise ValueError("A selfie with that prefix could not be found")

    if len(ids) <= 0:
        print("At least one ID is required")
        raise ValueError("At least one ID is required")

    print("[INFO]: Added selfie and ids for prefix: {}".format(prefix))
    return {"selfie": selfie, "ids": ids}


# Todo: Remove this
if __name__ == "__main__":
    CONN_STRING = "DefaultEndpointsProtocol=https;AccountName=mintfintechrgdiag431;AccountKey=j642+deFffJ5aQED0VjLwC54l/hWb7rclvWEidoHjwGg8EsORRNB8fOa8R12iO74FeS1gLs3SwDaMv2lRRPUuw==;EndpointSuffix=core.windows.net"
    result = fetchImages("012345", CONN_STRING, "1029380128")

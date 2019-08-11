import io
import base64
from PIL import Image
from azure.storage.blob import BlockBlobService, PublicAccess
from pandas import DataFrame
from datetime import datetime

ACCOUNT_NAME = "analyticsintelligence"
ACCOUNT_KEY = "RifgPf2kS0wH4RFEcWMh35d0IhwESyjw/AdHG7IXw7YLkVsAxWsYEQ8mErZ9IXHIhqgemvhUDqGWve2+FegpHg=="
ROOT_CONTAINER = "test-blob"

hashes, selfies, ids = [], [], []

output_table = DataFrame()

try:
    blob_service = BlockBlobService(ACCOUNT_NAME, ACCOUNT_KEY)

    def get_all_vpaths():
        vpaths = {}

        # Fetch all the blobs from the storage container
        generator = blob_service.list_blobs(ROOT_CONTAINER)

        for blob in generator:
            # This based on the assumption that nesting is only 2 levels deep
            if blob.name.index("/") == -1:
                continue

            # Make sure the folder name it can be parsed to an integer
            timestamp = int(blob.name.split("/")[0])

            if timestamp in vpaths:
                vpaths[timestamp].append(blob)
            else:
                vpaths[timestamp] = [blob]

        return vpaths

    def group_blobs_by_hash(blobs):
        results = {}

        for blob in blobs:
            blob_name = blob.name

            if blob_name.index("/") != -1:
                blob_name = blob_name.split("/")[1]

            hash = ""
            if blob_name.index("_") != -1:
                hash = blob_name.split("_")[0]

            if hash in results:
                results[hash].append(blob)
            else:
                results[hash] = [blob]

        return results

    def vpath_points_to_today(vpath):
        date = datetime.fromtimestamp(vpath)
        today = datetime.now()
        return date.month == today.month and date.day == today.day and date.year == today.year

    vpaths = get_all_vpaths()
    vpath_today_key = list(filter(vpath_points_to_today,  vpaths.keys()))

    # Todo: Assert that only one vpath matches is returned as a filter result any more
    # would signify a glitch somewhere

    if any(vpath_today_key):
        # We've found the bucket for today, now we can pull stuff off it
        key = vpath_today_key[0]
        vpath_blobs = vpaths[key]

        # Todo: Differentiate the already processed blob pairs from the processed ones
        # using the metadata on the blob. Right now we're just re-processing all of them again

        for hash, blobs in group_blobs_by_hash(vpath_blobs).items():
            hashes.append(hash)

            for blob in blobs:
                blob_stream = io.BytesIO()
                # Stream the blob and convert it to a bytearray for easy serialization
                blob_service.get_blob_to_stream(
                    ROOT_CONTAINER, blob.name, blob_stream)
                byte_array = bytearray(
                    base64.b64encode(blob_stream.getbuffer()))

                if "selfie" in blob.name != -1:
                    selfies.append(byte_array)
                elif "id" in blob.name != -1:
                    ids.append(byte_array)

            print("[INFO]: Added selfie and id for hash id: {}".format(hash))

except Exception as e:
    print(e)

output_table["Hash"] = hashes
output_table["Selfie"] = selfies
output_table["Id"] = ids


print(output_table)

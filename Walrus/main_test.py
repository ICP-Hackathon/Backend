import main

response1 = main.send_file(" slfkjfsdf store123123sdfsdf 12312alefjo1ij3ej1l123123kjfls1231241254")
# parsed_data = json.loads(response)

blob_id = ""
if 'newlyCreated' in response1 :
  blob_id = response1['newlyCreated']['blobObject']['blobId']
elif 'alreadyCertified' in response1 :
  blob_id = response1['alreadyCertified']['blobId']



response2 = main.get_blob(blob_id)

Tagasauris API Client
=====================

Examples
--------


Creating job

    import hashlib, uuid
    from tagasauris_api.api import TagasaurisClient

    ext_id = hashlib.md5(str(uuid.uuid4())).hexdigest()

    c = TagasaurisClient(login='***', password='***')

    result = c.create_job(
        id=ext_id,
        title='Aug3Test',
        task={
            "id" : "tagging",
            "instruction" : "test job instruction, visible to mturkers",
            "paid" : "0.0",
            "keywords" : "some keywords"
        },
        mediaobjects=['adb9523a1d36***',]
    )


Sending MediaObjects

>Remember: if you store pictures in S3 bucket, make it publicly available (API won't alert you) 

    # by default host is http://devel.tagasauris.com
    client = TagasaurisClient(login=login, password=passwd)

    mo_data = {
        'id': some_id,
        'title': picture_name,
        'mimetype': 'image/jpeg',
        'url': "https://s3.amazonaws.com/" + bucket_name + picture_name,
        'labels': [
            {'name': 'friday-party'},
            {'name': 'easter-egg'}
        ],
        'attributes': {
            'photographer': 'John Doe' 
        }
    }
    
    client.mediaobject_send(mo_data)

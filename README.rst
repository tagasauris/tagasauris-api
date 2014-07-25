=====================
Tagasauris API Client
=====================

Examples
--------

::

    import hashlib, uuid
    from tagapi.api import TagasaurisClient

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

class TagasaurisApiException(Exception):
    """ Tagapi exception """

    def __init__(self, reason, response=None):
        self.reason = unicode(reason)
        self.response = response

    def __str__(self):
        return self.reason

    def __unicode__(self):
        return self.reason


class TagasaurisUnauthorizedException(TagasaurisApiException):
    """ Not authorized to Tagasauris. """


class TagasaurisApiMaxRetries(TagasaurisApiException):
    """ Max retries exceeded """

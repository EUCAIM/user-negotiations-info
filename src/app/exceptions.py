
class OidcException(Exception):

    def __init__(self, message, *args):
        super().__init__(message)

class BaseException(Exception): 

    def __init__(self, title, status, detail):
        super().__init__(detail)
        self.title = title
        self.status = status
        self.detail = detail
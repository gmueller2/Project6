
class DuplicateOid(Exception):
    def __init__(self, message, oid):
        super().__init__(message)
        self.oid = oid


class DuplicateEmail(Exception):
    def __init__(self, message, email):
        super().__init__(message)
        self.email = email


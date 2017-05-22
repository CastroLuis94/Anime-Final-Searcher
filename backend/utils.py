from hashlib import sha256
from config import SALT_1, SALT_2


def hash_(password):
    sha = sha256(
        "{0}{1}{2}".format(
            SALT_1,
            password,
            SALT_2
        ).encode()
    ).hexdigest()
    return "sha256${0}$".format(sha)

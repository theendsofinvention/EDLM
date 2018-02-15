# coding=utf-8

import hashlib

from edlm import LOGGER

LOGGER = LOGGER.getChild(__name__)


def get_hash(data, method: str = 'md5'):
    """
    Computes hash from data

    Args:
        data: data
        method: hash method (defaults to MD5)

    Returns: hash value

    """
    if not isinstance(data, bytes):
        data = bytes(data, 'utf-8')

    try:
        func = getattr(hashlib, method)
    except AttributeError:
        raise RuntimeError('cannot find method "{}" in hashlib'.format(method))
    else:
        hash_ = func(data).hexdigest()
        LOGGER.debug('hash for binary data: %s', hash_)

        return hash_

import datetime
import importlib.resources


def datetime_utc_now():
    """Compatibility function getting the current utc date/time"""
    try:
        return datetime.datetime.now(datetime.UTC)
    except AttributeError:
        return datetime.datetime.utcnow()


def read_binary_resource(package, file):
    """Compatibility function reading a binary resource with a python package"""
    try:
        return (importlib.resources.files(package) / file).read_bytes()
    except AttributeError:
        return importlib.resources.read_binary(package, file)

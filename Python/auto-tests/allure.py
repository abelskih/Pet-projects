class _AttachmentType:
    PNG = "image/png"


attachment_type = _AttachmentType()


def step(_title=None):
    def decorator(func):
        return func

    return decorator


def attach(*args, **kwargs):
    return None

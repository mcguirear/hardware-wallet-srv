from common.vo.base_vo import BaseVO


def copy_vo(source, target):
    data = target.__dict__
    for (k, v) in data.items():
        if hasattr(source, k):
            setattr(target, k, getattr(source, k))

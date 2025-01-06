from django.db.models import Q


def generate_list_cache_key(model, filter_obj):

    if isinstance(filter_obj, dict):
        return "cache_key:" + str(tuple(sorted(filter_obj.items())))
    elif isinstance(filter_obj, tuple):
        return "cache_key:" + str(filter_obj)
    elif isinstance(filter_obj, Q):
        return "cache_key:" + str(filter_obj)
    else:
        print(type(filter_obj))
        raise ValueError(
            "Unsupported filter object type. Only dict and tuple are allowed."
        )

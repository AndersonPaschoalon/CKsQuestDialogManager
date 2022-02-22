def text(val: str):
    """Scape quetation marquer, to allow simple cotation marker."""
    return val.replace('"', '\"')



#def is_primitive(thing):
#    primitive = (int, str, bool, str)
#    return isinstance(thing, primitive)

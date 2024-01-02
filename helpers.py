def getAllInnerClasses(cls):
    import inspect
    classes = []
    for name in dir(cls):
        attr = getattr(cls, name)
        if inspect.isclass(attr) and \
        attr.__module__ == cls.__module__:
            classes.append(attr)
            
    return classes
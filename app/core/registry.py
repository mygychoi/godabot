class Registry:
    registry: set

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, "registry"):
            cls.registry = set()
        else:
            cls.registry.add(cls)

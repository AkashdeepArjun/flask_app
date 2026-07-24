from typing  import Any,TypeVar,Type

T=TypeVar('T')

class InstanceManager:
    # A single dictionary storing {ClassType: UniqueInstance}
    _instances: dict[type[Any], Any] = {}

    @classmethod
    def get_instance(cls, class_type: Type[T],*args:Any,**kwargs:Any) -> T:
        """Enforces a single instance per type T."""
        if class_type not in cls._instances:
            print(f"Creating brand new instance of {class_type.__name__}")
            cls._instances[class_type] = class_type(*args,**kwargs)
        return cls._instances[class_type]
    
        @classmethod
        def get(cls, class_type: Type[T]) -> T:
            """Helper to fetch an already created instance without args."""
            if class_type not in cls._instances:
                raise RuntimeError(f"Instance of {class_type.__name__} has not been initialized yet!")
            return cls._instances[class_type]
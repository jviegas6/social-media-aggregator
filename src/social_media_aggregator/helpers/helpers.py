import inspect
from functools import wraps


def validate_arguments(*expected_arg_types, exception_class=ValueError):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # Get function signature
            sig = inspect.signature(func)
            bound_arguments = sig.bind(self, *args, **kwargs)
            bound_arguments.arguments = {
                k: v for k, v in bound_arguments.arguments.items() if k != "self"
            }
            bound_arguments.apply_defaults()
            print(bound_arguments.arguments)
            print(expected_arg_types)
            # Check arguments
            for (name, value), expected in zip(
                bound_arguments.arguments.items(), expected_arg_types
            ):
                expected_type, mandatory = (
                    expected if isinstance(expected, tuple) else (expected, True)
                )

                if mandatory and value is None:
                    raise exception_class(
                        f"Argument '{name}' is mandatory but received None."
                    )
                elif isinstance(value, str) and mandatory and value == "":
                    raise exception_class(
                        f"Argument '{name}' is a mandatory string but received an empty string."
                    )
                elif not isinstance(value, expected_type) and value is not None:
                    raise exception_class(
                        f"Argument '{name}' with value '{value}' is not of type {expected_type}."
                    )

            return func(self, *args, **kwargs)

        return wrapper

    return decorator

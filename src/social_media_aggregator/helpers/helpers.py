import inspect
from functools import wraps
import logging


# class LoggingLevel:
#     """A class to signify an argument should be a valid logging level."""

#     @staticmethod
#     def is_valid(level):
#         return level in [
#             logging.DEBUG,
#             logging.INFO,
#             logging.WARNING,
#             logging.ERROR,
#             logging.CRITICAL,
#         ]

LoggingLevel = object()
valid_logging_levels = [
    logging.DEBUG,
    logging.INFO,
    logging.WARNING,
    logging.ERROR,
    logging.CRITICAL,
]


def validate_arguments(
    *expected_arg_types, exception_class=ValueError, custom_exception_class=None
):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            sig = inspect.signature(func)
            bound_arguments = sig.bind(self, *args, **kwargs)
            bound_arguments.apply_defaults()

            bound_arguments.arguments = {
                k: v for k, v in bound_arguments.arguments.items() if k != "self"
            }

            for name, (value, expected) in zip(
                bound_arguments.arguments.keys(),
                zip(bound_arguments.arguments.values(), expected_arg_types),
            ):
                expected_type, mandatory = (
                    expected if isinstance(expected, tuple) else (expected, True)
                )

                if expected_type is LoggingLevel:  # Special handling for logging level
                    if not value in valid_logging_levels:
                        raise custom_exception_class(
                            f"Argument '{name}' with value '{value}' is not a valid logging level."
                        )
                elif mandatory and value is None:
                    raise exception_class(
                        f"Argument '{name}' is mandatory but received None."
                    )
                elif isinstance(value, str) and mandatory and value == "":
                    raise exception_class(
                        f"Argument '{name}' is a mandatory string but received an empty string."
                    )
                elif not isinstance(value, expected_type):
                    raise exception_class(
                        f"Argument '{name}' with value '{value}' is not of type {expected_type}."
                    )

            return func(self, *args, **kwargs)

        return wrapper

    return decorator

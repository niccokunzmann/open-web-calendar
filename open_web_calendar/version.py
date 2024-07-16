try:
    from ._version import __version__, __version_tuple__, version, version_tuple
except ModuleNotFoundError:
    __version__ = _version = "0.0dev0"
    __version_tuple__ = version_tuple = (0, 0, "dev0")

__all__ = [
    "__version__",
    "version",
    "__version_tuple__",
    "version_tuple",
]
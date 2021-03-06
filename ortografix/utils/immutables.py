"""Custom immutable objects."""

from ortografix.exceptions.method import InvalidMethodError
from ortografix.exceptions.parameter import InvalidParameterError

__all__ = ('FrozenDict', 'ImmutableConfig')


class FrozenDict(dict):
    """Immutable dict following the frozenset semantics."""

    def __setitem__(self, key, value):
        """Set method used for testing."""
        raise InvalidMethodError('Cannot assign value to a FrozenDict')


class ImmutableConfig(FrozenDict):
    """Immutable Configuration.

    Converts an input dict (of dict(s)) to a FrozenDict (of FrozenDict(s))
    """

    def __init__(self, config):
        """Instantiate."""
        if not isinstance(config, dict):
            raise InvalidParameterError(
                'ImmutableConfig requires instance of dict as input parameter')
        super().__init__(self._freeze(config))

    def _get_frozen_value(self, input_value):
        if isinstance(input_value, dict):
            for key, value in input_value.items():
                if isinstance(value, dict):
                    input_value[key] = self._get_frozen_value(value)
            return FrozenDict(input_value)
        return input_value

    def _freeze(self, config):
        """Convert all dicts in config to FrozenDicts."""
        frozen_config = {}
        for key, value in config.items():
            frozen_config[key] = self._get_frozen_value(value)
        return FrozenDict(frozen_config)

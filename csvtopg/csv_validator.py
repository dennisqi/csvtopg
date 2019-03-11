import pandas as pd
from cerberus import Validator
from cerberus import errors


class CSVValidator(Validator):
    def _validate_nullable(self, nullable, field, value):
        """ {'type': 'boolean'} """
        if value is None or pd.isnull(value):
            if not nullable:
                self._error(field, errors.NOT_NULLABLE)
            self._drop_remaining_rules(
                'empty', 'forbidden', 'items', 'keyschema', 'min', 'max',
                'minlength', 'maxlength', 'regex', 'schema', 'type',
                'valueschema')

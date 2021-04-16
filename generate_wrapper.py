from typing import Any
from openapi_spec_validator.readers import read_from_filename
from jinja2 import Template

spec_dict, spec_url = read_from_filename('example-api.yaml')


def openapi_type_to_python(property: Any, quote: bool = True) -> str:
    if property.get('$ref') is not None:
        res = f"{property['$ref'].rsplit('/', maxsplit=1)[1]}"
        return f"'{res}'" if quote else res

    if property['type'] == 'string':
        return 'str'
    elif property['type'] == 'boolean':
        return 'bool'
    elif property['type'] == 'integer':
        return 'int'
    elif property['type'] == 'number':
        return 'float'
    elif property['type'] == 'array':
        return f'List[{openapi_type_to_python(property["items"])}]'
    else:
        return 'object'


with open('template.py', 'r+') as f:
    template = Template(f.read())
    template.globals['openapi_type_to_python'] = openapi_type_to_python  # type: ignore


with open('output.py', 'w') as f:
    f.write(template.render(api=spec_dict))

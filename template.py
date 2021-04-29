# DO NOT EDIT
# This file was generated from the API's specification.


from enum import Enum
from typing import List, Literal, TypedDict


class APIServer(Enum):
    {% for server in api.servers -%}
        {{ server.description.split(' ')[0].upper() }} = '{{ server.url }}'
    {% endfor %}


{% for schemaName, schema in api.components.schemas.items() -%}
    {% if schema.type == "string" -%}
        {{ schemaName }} = Literal[
            {%- for constant in schema.enum -%}
                '{{ constant }}', 
            {%- endfor -%}]
    {%- elif schema.type == "object" -%}
        class {{ schemaName }}(TypedDict):
    {% for propertyName, property in schema.properties.items() -%}
        {{ propertyName }}: {{ openapi_type_to_python(property) }}
    {% endfor %}
    {%- endif %}
{% endfor -%}


{% for responseName, response in api.components.responses.items() -%}
    {% set responseData = response.content['application/json'].schema.allOf -%}
    class {{ responseName }}({{ openapi_type_to_python(responseData[0], quote=False) }}):
    {% for propertyName, property in responseData[1].properties.items() -%}
        {{ propertyName }}: {{ openapi_type_to_python(property) }}
    {% endfor %}
{% endfor -%}


{% for requestBodyName, requestBody in api.components.requestBodies.items() -%}
    {% set properties = requestBody.content['application/json'].schema.properties -%}
    class {{ requestBodyName }}(TypedDict, total=False):
    """
    {{ requestBody.description | replace('<br />', '\n   ') }}
    """
    {% for propertyName, property in properties.items() -%}
        {{ propertyName }}: {{ openapi_type_to_python(property) }}
    {% endfor %}
{% endfor -%}


{% for parameterName, parameter in api.components.parameters.items() -%}
    {%- if parameter.in == "query" -%}
    class {{ parameterName }}(TypedDict, total=False):
    {{ parameter.name }}: {{ openapi_type_to_python(parameter.schema) }}
    {% endif %}
{% endfor -%}

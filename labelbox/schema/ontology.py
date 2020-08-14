"""Client side object for interacting with the ontology."""
import abc
from dataclasses import dataclass
from functools import cached_property

from typing import Any, Callable, Dict, List, Optional, Union

from labelbox.orm import query
from labelbox.orm.db_object import DbObject, Updateable, BulkDeletable
from labelbox.orm.model import Entity, Field, Relationship
from labelbox.utils import snake_case, camel_case



@dataclass
class OntologyEntity:
    required: bool
    name: str


@dataclass
class Option:
    label: str
    value: str
    feature_schema_id: Optional[str] = None
    schema_node_id: Optional[str] = None

    @classmethod
    def from_json(cls, json_dict):
        _dict = convert_keys(json_dict, snake_case)
        return cls(**_dict)


@dataclass
class Classification(OntologyEntity):
    type: str
    instructions: str
    options: List[Option]
    feature_schema_id: Optional[str] = None
    schema_node_id: Optional[str] = None

    @classmethod
    def from_json(cls, json_dict):
        _dict = convert_keys(json_dict, snake_case)
        _dict['options'] = [
            Option.from_json(option)
            for option in _dict['options']
        ]
        return cls(**_dict)


@dataclass
class Tool(OntologyEntity):
    tool: str
    color: str
    classifications: List[Classification]
    feature_schema_id: Optional[str] = None
    schema_node_id: Optional[str] = None

    @classmethod
    def from_json(cls, json_dict):
        _dict = convert_keys(json_dict, snake_case)
        _dict['classifications'] = [
            Classification.from_json(classification)
            for classification in _dict['classifications']
        ]
        return cls(**_dict)


class Ontology(DbObject):
    """ A ontology specifies which tools and classifications are available
    to a project.

    NOTE: This is read only for now.

    >>> project = client.get_project(name="<project_name>")
    >>> ontology = project.ontology()
    >>> ontology.normalized

    """

    name = Field.String("name")
    description = Field.String("description")
    updated_at = Field.DateTime("updated_at")
    created_at = Field.DateTime("created_at")
    normalized = Field.Json("normalized")
    object_schema_count = Field.Int("object_schema_count")
    classification_schema_count = Field.Int("classification_schema_count")

    projects = Relationship.ToMany("Project", True)
    created_by = Relationship.ToOne("User", False, "created_by")

    @cached_property
    def tools(self) -> List[Tool]:
        return [
            Tool.from_json(tool)
            for tool in self.normalized['tools']
        ]

    @cached_property
    def classifications(self) -> List[Classification]:
        return [
            Classification.from_json(classification)
            for classification in self.normalized['classifications']
        ]


def convert_keys(json_dict: Dict[str, Any], converter: Callable) -> Dict[str, Any]:
    if isinstance(json_dict, dict):
        return {
            converter(key): convert_keys(value, converter)
            for key, value in json_dict.items()
        }
    if isinstance(json_dict, list):
        return [
            convert_keys(ele, converter)
            for ele in json_dict
        ]
    return json_dict

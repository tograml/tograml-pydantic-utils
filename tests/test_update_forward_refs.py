from __future__ import annotations

from typing import Any, Dict, List

import pydantic
import pytest
from tograml_pydantic_utils.update_forward_refs_helper import (
    update_forward_refs_helper,
)


@pytest.fixture
def update_forward_refs() -> None:
    test_function_arguments: Dict[str, Any] = {}

    update_forward_refs_helper(("ModelNameFirst", "ModelNameSecond"), test_function_arguments)
    yield


class Container(pydantic.BaseModel):
    contains: List[Item]


class Item(pydantic.BaseModel):
    name: str


@pytest.mark.xfail(raises=pydantic.errors.ConfigError)
def test_container_create_error() -> None:
    container = Container(contains=[Item(name="name")])
    assert container.contains == [Item(name="name")]


@pytest.mark.update_forward_refs(
    ("Container", "Item"),
    (Container, Item),
)
def test_container_create_successfully() -> None:
    container = Container(contains=[Item(name="name")])
    assert container.contains == [Item(name="name")]

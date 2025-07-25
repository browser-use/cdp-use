# This file is auto-generated by the CDP protocol generator.
# Do not edit this file manually as your changes will be overwritten.
# Generated from Chrome DevTools Protocol specifications.

"""CDP Extensions Domain Commands"""

from typing import Any, Dict, List
from typing_extensions import NotRequired, TypedDict

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .types import StorageArea

class LoadUnpackedParameters(TypedDict):
    path: "str"
    """Absolute file path."""


class LoadUnpackedReturns(TypedDict):
    id: "str"
    """Extension id."""



class UninstallParameters(TypedDict):
    id: "str"
    """Extension id."""





class GetStorageItemsParameters(TypedDict):
    id: "str"
    """ID of extension."""
    storageArea: "StorageArea"
    """StorageArea to retrieve data from."""
    keys: "NotRequired[List[str]]"
    """Keys to retrieve."""


class GetStorageItemsReturns(TypedDict):
    data: "Dict[str, Any]"



class RemoveStorageItemsParameters(TypedDict):
    id: "str"
    """ID of extension."""
    storageArea: "StorageArea"
    """StorageArea to remove data from."""
    keys: "List[str]"
    """Keys to remove."""





class ClearStorageItemsParameters(TypedDict):
    id: "str"
    """ID of extension."""
    storageArea: "StorageArea"
    """StorageArea to remove data from."""





class SetStorageItemsParameters(TypedDict):
    id: "str"
    """ID of extension."""
    storageArea: "StorageArea"
    """StorageArea to set data in."""
    values: "Dict[str, Any]"
    """Values to set."""



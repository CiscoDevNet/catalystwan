# Grabs API meta data collected while decorating API methods and bakes into serializable registry
# TODO: versions and tenancy modes not showing up in markdown
from dataclasses import dataclass
from inspect import getsourcefile, getsourcelines
from pathlib import Path, PurePath
from typing import Any, Dict, List, Optional, Protocol, Set
from urllib.request import pathname2url

from packaging.specifiers import SpecifierSet  # type: ignore

from vmngclient.endpoints import BASE_PATH, APIEndpointRequestMeta, TypeSpecifier, request, versions, view
from vmngclient.utils.session_type import SessionType  # type: ignore

SOURCE_BASE_PATH = "https://github.com/CiscoDevNet/vManage-client/blob/main/"


def relative(absolute: str) -> str:
    local = PurePath(Path.cwd())
    return str(PurePath(absolute).relative_to(local))


def create_sourcefile_link(local: str) -> str:
    return SOURCE_BASE_PATH + pathname2url(relative(local))


def generate_origin_string(typespec: TypeSpecifier) -> str:
    string = ""
    depth = 0

    def add_origin(origin: str):
        nonlocal string, depth
        string = string[:-depth] + f"{origin}[]" + string[-depth:]
        depth = depth + 1

    seqtype = getattr(typespec.sequence_type, "__name__", None) or getattr(typespec.sequence_type, "_name", None)

    if typespec.is_optional:
        add_origin("Optional")

    if seqtype:
        add_origin(str(seqtype))

    string = string[:-depth] + "{}" + string[-depth:]

    return string


class MarkdownRenderer(Protocol):
    def md(self) -> str:
        ...


@dataclass
class CodeLink(MarkdownRenderer):
    link_text: str
    sourcefile: Optional[str]
    lineno: Optional[int]

    @staticmethod
    def from_func(func) -> "CodeLink":
        if sourcefile := getsourcefile(func):
            return CodeLink(
                link_text=func.__qualname__,
                sourcefile=create_sourcefile_link(sourcefile),
                lineno=getsourcelines(func)[1],
            )
        raise Exception("Cannot locate source for {func}")

    def __lt__(self, other: "CodeLink"):
        return self.link_text < other.link_text

    def md(self) -> str:
        if self.sourcefile:
            return f"[**{self.link_text}**]({self.sourcefile}#L{self.lineno})"
        return self.link_text


@dataclass
class CompositeTypeLink(CodeLink, MarkdownRenderer):
    origin: str = "{}"

    @staticmethod
    def builtin(name: str) -> "CompositeTypeLink":
        return CompositeTypeLink(link_text=name, sourcefile=None, lineno=None, origin="")

    @staticmethod
    def json() -> "CompositeTypeLink":
        return CompositeTypeLink(link_text="JSON", sourcefile=None, lineno=None, origin="")

    @staticmethod
    def from_type_specifier(typespec: TypeSpecifier) -> Optional["CompositeTypeLink"]:
        if typespec.present:
            if typespec.is_json:
                return CompositeTypeLink.json()
            if payloadtype := typespec.payload_type:
                if payloadtype.__module__ == "builtins":
                    return CompositeTypeLink.builtin(payloadtype.__name__)
                elif sourcefile := getsourcefile(payloadtype):
                    return CompositeTypeLink(
                        link_text=payloadtype.__name__,
                        sourcefile=create_sourcefile_link(sourcefile),
                        lineno=getsourcelines(payloadtype)[1],
                        origin=generate_origin_string(typespec),
                    )
        return None

    def md(self) -> str:
        if self.origin:
            return self.origin.format(f"[**{self.link_text}**]({self.sourcefile}#L{self.lineno})")
        return super().md()


@dataclass
class Endpoint(MarkdownRenderer):
    http_request: str
    supported_versions: str
    supported_tenancy_modes: str
    method: CodeLink
    payload_type: Optional[CompositeTypeLink]
    return_type: Optional[CompositeTypeLink]

    @staticmethod
    def from_meta(
        meta: APIEndpointRequestMeta,
        versions: Optional[SpecifierSet],
        tenancy_modes: Optional[Set[SessionType]],
    ) -> "Endpoint":
        return Endpoint(
            http_request=meta.http_request,
            supported_versions=str(versions) if versions else "",
            supported_tenancy_modes=", ".join(sorted([tm.name for tm in tenancy_modes])) if tenancy_modes else "",
            method=CodeLink.from_func(meta.func),
            payload_type=CompositeTypeLink.from_type_specifier(meta.payload_spec),
            return_type=CompositeTypeLink.from_type_specifier(meta.return_spec),
        )

    def __lt__(self, other: "Endpoint"):
        self.method < other.method

    def md(self) -> str:
        return "|".join(
            [
                self.http_request,
                self.supported_versions,
                self.method.md(),
                self.payload_type.md() if self.payload_type else "",
                self.return_type.md() if self.return_type else "",
                self.supported_tenancy_modes,
            ]
        )


class EndpointRegistry(MarkdownRenderer):
    def __init__(
        self,
        meta_lookup: Dict[Any, APIEndpointRequestMeta],
        versions_lookup: Dict[Any, SpecifierSet],
        tenancy_modes_lookup: Dict[Any, Set[SessionType]],
    ):
        self.items: List[Endpoint] = []
        self.base_path = BASE_PATH
        for funcname, meta in meta_lookup.items():
            versions = versions_lookup.get(funcname, None)
            tenancy_modes = tenancy_modes_lookup.get(funcname, None)
            self.items.append(Endpoint.from_meta(meta=meta, versions=versions, tenancy_modes=tenancy_modes))

    def md(self) -> str:
        info = f"All URIs are relative to *{self.base_path}*\n"
        table_header = (
            "HTTP request | Supported Versions | Method | Payload Type | Return Type | Tenancy Mode\n"
            "------------ | ------------------ | ------ | ------------ | ----------- | ------------\n"
        )
        # sorting insures that generated markdown will be exact same each time same set of methods are documented
        self.items.sort()
        table_content = "\n".join([item.md() for item in self.items])
        return info + table_header + table_content + "\n"


if __name__ == "__main__":
    from unittest.mock import MagicMock

    from vmngclient.endpoints.endpoints_container import APIEndpointContainter

    # this instantiates APIEndpoints classes triggering method decorators
    # endpoints not attached to container will be not documented !
    _ = APIEndpointContainter(MagicMock())

    endpoint_registry = EndpointRegistry(
        meta_lookup=request.request_lookup,
        versions_lookup=versions.versions_lookup,
        tenancy_modes_lookup=view.view_lookup,
    )
    with open("ENDPOINTS.md", "w") as f:
        f.write("**THIS FILE IS AUTO-GENERATED DO NOT EDIT**\n\n")
        f.write(endpoint_registry.md())

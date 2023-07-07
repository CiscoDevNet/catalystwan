# Grabs API meta data collected while decorating API methods and bakes into serializable registry
# TODO: versions and tenancy modes not showing up in markdown
from dataclasses import dataclass
from inspect import getsourcefile, getsourcelines
from pathlib import Path, PurePath
from typing import Any, Dict, List, Optional, Protocol, Set

from packaging.specifiers import SpecifierSet  # type: ignore

from vmngclient.primitives import BASE_PATH, APIPrimitivesRequestMeta, TypeSpecifier, request, versions, view
from vmngclient.utils.session_type import SessionType  # type: ignore


def relative(absolute: str) -> str:
    local = PurePath(Path.cwd())
    return str(PurePath(absolute).relative_to(local))


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
                sourcefile=relative(sourcefile),
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
    origin: Optional[str]

    @staticmethod
    def from_type_specifier(typespec: TypeSpecifier) -> Optional["CompositeTypeLink"]:
        if typespec.present:
            if payloadtype := typespec.payload_type:
                if payloadtype.__module__ == "builtins":
                    return CompositeTypeLink(payloadtype.__name__, None, None, None)
                elif sourcefile := getsourcefile(payloadtype):
                    seqtype = getattr(typespec.sequence_type, "__name__", None)
                    return CompositeTypeLink(
                        link_text=payloadtype.__name__,
                        sourcefile=relative(sourcefile),
                        lineno=getsourcelines(payloadtype)[1],
                        origin=seqtype,
                    )
        return None

    def md(self) -> str:
        if self.origin:
            return f"{self.origin}[[**{self.link_text}**]({self.sourcefile}#L{self.lineno})]"
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
        func,
        meta: APIPrimitivesRequestMeta,
        versions: Optional[SpecifierSet],
        tenancy_modes: Optional[Set[SessionType]],
    ) -> "Endpoint":
        return Endpoint(
            http_request=meta.http_request,
            supported_versions=str(versions) if versions else "",
            supported_tenancy_modes=str(tenancy_modes) if tenancy_modes else "",
            method=CodeLink.from_func(func),
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
        meta_lookup: Dict[Any, APIPrimitivesRequestMeta],
        versions_lookup: Dict[Any, SpecifierSet],
        tenancy_modes_lookup: Dict[Any, Set[SessionType]],
    ):
        self.items: List[Endpoint] = []
        self.base_path = BASE_PATH
        for func, meta in meta_lookup.items():
            versions = versions_lookup.get(func, None)
            tenancy_modes = tenancy_modes_lookup.get(func, None)
            self.items.append(Endpoint.from_meta(func, meta=meta, versions=versions, tenancy_modes=tenancy_modes))

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

    from vmngclient.primitives.primitive_container import APIPrimitiveContainter

    # this instantiates api primitive classes triggering method decorators
    # API primitives not attached to container will be not documented !
    _ = APIPrimitiveContainter(MagicMock())

    endpoint_registry = EndpointRegistry(
        meta_lookup=request.meta_lookup, versions_lookup=versions.meta_lookup, tenancy_modes_lookup=view.meta_lookup
    )
    with open("ENDPOINTS.md", "w") as f:
        f.write("**THIS FILE IS AUTO-GENERATED DO NOT EDIT**\n\n")
        f.write(endpoint_registry.md())

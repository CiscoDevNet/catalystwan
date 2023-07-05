# Grabs API meta data collected while decorating API methods and bakes into serializable registry
from dataclasses import dataclass
from inspect import getsourcefile, getsourcelines
from pathlib import Path, PurePath
from typing import List, Optional

from vmngclient.primitives import TypeSpecifier, request, versions, view
from vmngclient.session import create_vManageSession  # noqa: E261, F401 this is needed so decorators can evaluate meta


def relative(absolute: str) -> str:
    local = PurePath(Path.cwd())
    return str(PurePath(absolute).relative_to(local))


@dataclass
class CodeLink:
    link_text: str
    sourcefile: str
    lineno: int

    @staticmethod
    def from_func(func) -> "CodeLink":
        if sourcefile := getsourcefile(func):
            return CodeLink(
                link_text=func.__qualname__,
                sourcefile=relative(sourcefile),
                lineno=getsourcelines(func)[1],
            )
        raise Exception("Cannot locate source for {func}")


@dataclass
class CompositeTypeLink(CodeLink):
    origin: Optional[str]

    @staticmethod
    def from_type_specifier(typespec: TypeSpecifier) -> Optional["CompositeTypeLink"]:
        if typespec.present:
            if payloadtype := typespec.payload_type:
                if sourcefile := getsourcefile(payloadtype):
                    seqtype = getattr(typespec.sequence_type, "__name__", None)
                    return CompositeTypeLink(
                        link_text=payloadtype.__name__,
                        sourcefile=relative(sourcefile),
                        lineno=getsourcelines(payloadtype)[1],
                        origin=seqtype,
                    )
        return None


@dataclass
class Endpoint:
    http_request: str
    supported_versions: str
    supported_tenancy_modes: str
    method: CodeLink
    payload_type: Optional[CompositeTypeLink]
    return_type: Optional[CompositeTypeLink]


endpoint_registry = []
for func, meta in request.meta_lookup.items():
    _versions = versions.meta_lookup.get(func, None)
    _tenancy_modes = view.meta_lookup.get(func, None)
    endpoint_registry.append(
        Endpoint(
            http_request=meta.http_request,
            supported_versions=str(_versions) if _versions else "",
            supported_tenancy_modes=str(_tenancy_modes) if _tenancy_modes else "",
            method=CodeLink.from_func(func),
            payload_type=CompositeTypeLink.from_type_specifier(meta.payload_spec),
            return_type=CompositeTypeLink.from_type_specifier(meta.return_spec),
        )
    )


def render_markdown(endpoint_registry: List[Endpoint]) -> str:
    # crude way to demonstrate
    md = "All URIs are relative to */dataservice*\n"
    md += "HTTP request | Supported Versions | Method | Payload Type | Return Type | Tenancy Mode \n"
    md += "------------ | ------------- | ------------- | ------------- | ------------- | ------------- "
    for e in endpoint_registry:
        md += f"\n{e.http_request} | {e.supported_versions} | [**{e.method.link_text}**]({e.method.sourcefile}#L{e.method.lineno}) | "  # noqa
        if p := e.payload_type:
            if origin := p.origin:
                md += f"{origin}[[**{p.link_text}**]({p.sourcefile}#L{p.lineno})] | "
            else:
                md += f"[**{p.link_text}**]({p.sourcefile}#{p.lineno}) | "
        if r := e.return_type:
            if origin := r.origin:
                md += f"{origin}[[**{r.link_text}**]({r.sourcefile}#L{r.lineno})] | "
            else:
                md += f"[**{r.link_text}**]({r.sourcefile}#{r.lineno}) | "
        md += e.supported_tenancy_modes
    return md


with open("ENDPOINTS.md", "w") as f:
    f.write(render_markdown(endpoint_registry))

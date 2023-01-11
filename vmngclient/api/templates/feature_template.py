from pathlib import Path

from jinja2 import DebugUndefined, Environment, FileSystemLoader, meta  # type: ignore
from pydantic import BaseModel  # type: ignore


class FeatureTemplate(BaseModel):
    name: str
    description: str
    payload_path: Path

    def generate_payload(self) -> str:
        env = Environment(
            loader=FileSystemLoader(self.payload_path.parent),
            trim_blocks=True,
            lstrip_blocks=True,
            undefined=DebugUndefined,
        )
        # print(env.loader.list_templates())
        template = env.get_template(self.payload_path.name)
        output = template.render(self.dict())

        ast = env.parse(output)
        if meta.find_undeclared_variables(ast):
            print(meta.find_undeclared_variables(ast))
            raise Exception
        return output

    def generate_cli(self) -> str:
        raise NotImplementedError()

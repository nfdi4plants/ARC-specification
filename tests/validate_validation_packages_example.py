# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "jsonschema==4.25.1",
#   "pyyaml==6.0.2",
#   "validationpackage-codecs==0.1.0a4",
# ]
# ///

import json
from hashlib import sha256
from importlib.metadata import version
from importlib.resources import files
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator
from validation_package_codecs import (
    SchemaUris,
    ValidationPackagesConfigYaml,
)


repository = Path(__file__).resolve().parents[1]
specification = (repository / "ARC specification.md").read_text(encoding="utf-8")
_, canonical_heading, canonical_section = specification.partition(
    "#### Canonical example\n"
)
assert canonical_heading, "canonical example section is missing"
canonical_section, migration_heading, _ = canonical_section.partition(
    "\n#### Migration from schema-less files"
)
assert migration_heading, "canonical example section has no closing migration heading"

marker = "```yaml\n"
parts = canonical_section.split(marker)
assert len(parts) == 2, (
    f"expected exactly one normative YAML block, found {len(parts) - 1}"
)
example = parts[1].split("\n```", 1)[0] + "\n"

assert version("validationpackage-codecs") == "0.1.0a4"
decoded = ValidationPackagesConfigYaml.decode_or_fail(example)
assert not decoded.IsLegacy

selection = decoded.Canonical.ValidationPackages[0]
assert selection.Name == "configurable-validation"
assert len(selection.Inputs) == 3
assert selection.Inputs[2].Value.Value == "release candidate"
assert SchemaUris.ValidationPackagesConfigV1 in example

schema_resource = files("validation_package_codecs").joinpath(
    "schemas", "validation-packages.schema.json"
)
schema_bytes = schema_resource.read_bytes()
assert sha256(schema_bytes).hexdigest() == (
    "724a13ae20b5925a40c054290d5d62e0e78d2c60307d302411d0d0d242858914"
)
schema = json.loads(schema_bytes)
Draft202012Validator.check_schema(schema)
Draft202012Validator(schema).validate(yaml.safe_load(example))

print("canonical example matches ValidationPackage.Codecs 0.1.0a4")

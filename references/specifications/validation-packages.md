# DataPLANT ARC Validation Package Specification

* Version: 1.0.0-draft.1
<!-- Proposed permalink: <https://w3id.org/arc/specifications/validation-packages/1.0.0-draft.1> -->
* Authors:
  * Kevin Schneider - [https://orcid.org/0000-0002-2198-5262](https://orcid.org/0000-0002-2198-5262)
  * Jonathan Bauer - [https://orcid.org/0000-0002-5624-2055](https://orcid.org/0000-0002-5624-2055)
* License: [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/)

* **Table of contents**
  * [Overview](#overview)
  * [Validation Package Structure](#validation-package-structure)
    * [Frontmatter Metadata](#frontmatter-metadata)
    * [Validation Cases](#validation-cases)
    * [Output Files](#output-files)
  * [Execution Environment](#execution-environment)
  * [ARC Validation Package Registry](#arc-validation-package-registry)
  * [Supported Programming Languages](#supported-programming-languages)
  * [Examples](#examples)
  * [License](#license)

## Overview

This document specifies the DataPLANT reference representation and execution
contract for the [ARC validation concepts](../../ARC%20specification.md#validation).
It defines how an executable validation package describes its identity and
inputs, receives an ARC, and reports its results. The concepts are independent
of this representation; other implementations can use different package or
result formats.

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHOULD**, **SHOULD NOT**,
and **MAY** in this document are to be interpreted as described in
[BCP 14](https://www.rfc-editor.org/info/bcp14) when, and only when, they
appear in all capitals.

A conforming package consists of one supported executable script, embedded
metadata, one or more validation cases, and the ability to create the standard
result files. A conforming runner supplies the standard process arguments,
preserves argument boundaries, and provides an execution environment for the
script language.

## Validation Package Structure

A validation package MUST be a self-contained, single-file script. Its
identity is the pair of its globally unique package name and complete
[Semantic Version 2.0](https://semver.org/). Published files use the name
`{name}@{version}.{extension}`; for example,
`arc-specification@3.0.0.fsx`.

The script MUST:

* place its metadata before any executable package code;
* define every validation case it can validate the supplied ARC against;
* distinguish failed requirements from errors that prevented evaluation; and
* write the standard output files below `.arc-validate-results/{name}@{version}/` in the supplied output directory.

Validation case definitions MUST be contained in the package script and MUST
NOT be loaded from external sources such as shared software libraries or
network services at execution time.

Package software dependencies MUST be declared inside the script using the mechanism specified for its programming language.
A package MUST NOT rely on unrecorded software installed on a particular runner.

### Frontmatter Metadata

Package metadata is an embedded YAML mapping. Its machine-readable companion
is the [validation-package frontmatter schema](../schemas/validation-package-frontmatter.schema.json),
identified by
`<insert w3c PID here later>`.
`$schema` selects an offline decoder as well as associating an editor schema;
runners MUST NOT fetch and execute or trust an arbitrary schema URI while
parsing a package.

Readers MUST reject unknown fields, duplicate keys, aliases, anchors, explicit
tags, merge keys, and multiple YAML documents. Schema-less metadata MAY be
read for compatibility with immutable packages published before this contract;
new packages and canonical writers MUST include `$schema`.

#### Root metadata contract

The following fields form the metadata contract:

| Field | Required | Meaning |
| --- | --- | --- |
| `$schema` | yes | The exact frontmatter schema identifier this document adheres to. |
| `Name` | yes | Non-empty package name. It MUST agree with the registry directory and filename. |
| `MajorVersion` | yes | Non-negative Semantic Version major component. |
| `MinorVersion` | yes | Non-negative Semantic Version minor component. |
| `PatchVersion` | yes | Non-negative Semantic Version patch component. |
| `Summary` | yes | Single-sentence package summary of at most 50 words. |
| `Description` | yes | Longer human-readable description of the package's scope. |
| `PreReleaseVersionSuffix` | no | Semantic Version prerelease suffix without the leading hyphen. |
| `BuildMetadataVersionSuffix` | no | Semantic Version build suffix without the leading plus sign. |
| `ProgrammingLanguage` | no | Script language, normally supplied by frontmatter extraction. |
| `Publish` | no | Registry-staging instruction; omission means `false`. It has no effect at runtime. |
| `Authors` | no | Ordered package author and maintainer records. |
| `Tags` | no | Search terms with optional ontology source and accession. |
| `ReleaseNotes` | no | Human-readable changes in this package version. |
| `CQCHookEndpoint` | no | Endpoint associated with the package for an ARC application. |
| `Inputs` | no | Ordered package-specific command-input declarations. |

#### Authors

Each `Authors` entry is an object with the following fields and no others:

| Field | Required | Meaning |
| --- | --- | --- |
| `FullName` | yes | Non-empty full name of the package author or maintainer. |
| `Email` | no | Contact email address. |
| `Affiliation` | no | Name of the affiliated institution or organization. |
| `AffiliationLink` | no | Link identifying the affiliated institution or organization. |

#### Tags

Each `Tags` entry is an object with the following fields and no others:

| Field | Required | Meaning |
| --- | --- | --- |
| `Name` | yes | Non-empty human-readable tag name. |
| `TermSourceREF` | no | Name or identifier of the controlled-vocabulary source. |
| `TermAccessionNumber` | no | Accession identifying the term in that source. |

#### Inputs

Package-specific inputs use a deliberately limited subset of
[CWL `CommandLineTool.inputs`](https://www.commonwl.org/v1.2/CommandLineTool.html).
Each `Inputs` entry is an object with the following fields and no others:

| Field | Required | Meaning |
| --- | --- | --- |
| `id` | yes | Non-empty, exact, case-sensitive ID that is unique within the package. |
| `type` | yes | One supported scalar type, optionally followed by `?` for nullability. |
| `label` | no | Short human-readable label. |
| `doc` | no | Longer human-readable input documentation. |
| `inputBinding` | yes | Command-line binding object for this input. |

The supported types are `boolean`, `int`, `long`, `float`, `double`, and
`string`, plus the nullable forms `boolean?`, `int?`, `long?`, `float?`,
`double?`, and `string?`. General CWL unions, arrays, records, enums, files,
directories, defaults, expressions, and positional inputs are not part of this
version.

##### Input binding

Each `inputBinding` value is an object with the following fields and no
others:

| Field | Required | Meaning |
| --- | --- | --- |
| `prefix` | yes | Non-empty, exact command-line token emitted for the input. It MUST be unique within the package. |
| `position` | no | Integer used to order package-specific arguments; omission means `0`. |

`prefix` MUST NOT be `--`, `-i`, `-o`, `--source-branch`, or
`--source-commit-hash`, which are reserved by the standard execution contract.
A runner orders configured inputs by ascending `position` and then by input ID
using ordinal comparison. A boolean `true` emits the prefix only; `false` and
null emit nothing. Every other value emits the prefix and value as separate
process arguments.

#### Frontmatter embedding

Frontmatter MUST be the first construct in the package file and MUST use the
format defined for the respective
[supported programming language](#supported-programming-languages). If the
package code reuses the frontmatter, its language-specific value declaration
MUST be bound to the exact name `PACKAGE_METADATA`. The extracted frontmatter
MUST be valid YAML and MUST conform to the
[frontmatter schema](../schemas/validation-package-frontmatter.schema.json)
identified by `$schema`. A runner MUST extract the frontmatter before
executing the package code.

### Validation Cases

A package organizes its validation cases into **critical** and
**non-critical** groups. A failed or errored critical case means the ARC does
not qualify under that package version. Non-critical cases communicate
recommendations or quality indicators without changing that critical
qualification.

Each case SHOULD have a stable, human-readable name and MUST produce exactly
one of these outcomes:

| Outcome | Meaning |
| --- | --- |
| passed | The ARC satisfies the case. |
| failed | The case was evaluated and its requirement was not satisfied. |
| errored | The case could not be evaluated, for example because of malformed input or an execution failure. |
| skipped | The case was intentionally not evaluated and records that fact. |

Cases MUST be deterministic for the same immutable ARC state, package version,
declared inputs, and execution environment. A package SHOULD avoid network or
time-dependent checks unless those dependencies and their effect on
reproducibility are explicitly documented.

### Output Files

For every execution, the package MUST create these files in
`.arc-validate-results/{name}@{version}/` beneath the supplied output
directory:

| File | Purpose |
| --- | --- |
| `validation_summary.json` | Machine-readable aggregate result, package identity, optional payload, and source provenance. |
| `validation_report.xml` | JUnit-compatible case-level result report. |
| `badge.svg` | Human-readable visual summary suitable for an ARC or repository page. |

`validation_summary.json` MUST conform to the
[validation-summary schema](../schemas/validation-summary.schema.json). It
contains `Critical`, `NonCritical`, and `ValidationPackage`. Each result group
contains `HasFailures`, `Total`, `Passed`, `Failed`, and `Errored`.
`HasFailures` is true exactly when `Failed` or `Errored` is non-zero, and
`Total` MUST be at least the sum of the three reported outcome counts; any
remainder represents skipped cases.

The `ValidationPackage` object identifies the exact name and version that ran
and repeats its summary and description. It MAY contain `CQCHookEndpoint`.
The top level MAY contain arbitrary JSON-compatible package output in
`Payload`, and MAY contain `SourceBranch` and `SourceCommitHash` when supplied
by the runner. A payload MUST NOT replace the standard result counts or package
identity.

`validation_report.xml` MUST represent all executed and skipped cases and
SHOULD follow the conventional JUnit `testsuites`, `testsuite`, and `testcase`
structure. Failures and errors MUST remain distinguishable. When source
provenance is supplied, the report SHOULD retain it as suite properties.

`badge.svg` MUST display the package name and a value derived from the same
summary. It MUST indicate critical failures distinctly from a successful or
partially successful result. When source provenance is embedded in the badge,
it MUST be metadata and MUST NOT alter the displayed validation outcome.

## Execution Environment

A runner invokes a validation package with an argument list, never by
interpolating values into a shell command. It supplies the following standard
arguments:

| Argument | Required | Meaning |
| --- | --- | --- |
| `-i <path>` | yes | Absolute path to the ARC directory to validate. |
| `-o <path>` | yes | Base directory under which the result directory is created. |
| `--source-branch <branch>` | no | Source branch associated with this validation. |
| `--source-commit-hash <hash>` | no | Immutable source revision associated with this validation. |

The runner MUST preserve every path and value as one process argument. It MUST
provide read access to the ARC and write access to the output directory. A
package SHOULD treat the ARC as read-only and MUST NOT write outside the
supplied output directory as part of normal validation.

The reference runner is the
[`arc-validate` CLI](https://github.com/nfdi4plants/arc-validate). The
[`ARCExpect` library](https://github.com/nfdi4plants/arc-validate/tree/dev/src/ARCExpect)
provides portable metadata, argument, case, summary, JUnit, and badge support
for package authors. CQC-specific package selection and resolved execution are
specified separately in the
[Continuous Quality Control specification](continuous-quality-control.md).

## ARC Validation Package Registry

The [ARC Validation Package Registry (AVPR)](https://avpr.nfdi4plants.org/)
is the reference service for discovering and distributing validation
packages. Package names are globally unique within AVPR, and the combination
of name and complete Semantic Version identifies one immutable published
artifact.

Packages enter AVPR through its repository staging and review workflow. The
staging directory, filename, and frontmatter identity MUST agree. Setting
`Publish: true` marks a staged version as eligible for publication; it does not
permit overwriting an existing published identity. Fixes or behavior changes
therefore require a new package version.

Registry metadata is discovery information. A runner MUST validate the
metadata embedded in the installed artifact and MUST NOT infer package inputs
from an unversioned or different package release.

## Supported Programming Languages

This version supports these single-file package formats:

| Language | Extension | Dependency declaration | Reference invocation |
| --- | --- | --- | --- |
| F# | `.fsx` | `#r "nuget: Package, Version"` directives | `dotnet fsi {package}.fsx ...` |
| Python | `.py` | [PEP 723 inline script metadata](https://packaging.python.org/en/latest/specifications/inline-script-metadata/) | `uv run {package}.py ...` |

### Language-specific frontmatter embedding

F# packages place frontmatter in an initial multiline comment. Python packages
place it in an initial triple-quoted string. Adding another language requires
a specified frontmatter extraction rule, dependency mechanism, safe process
invocation, and conformance tests for all standard outputs. JavaScript package
execution is not defined by this version.

## Examples

The following F# frontmatter declares an immutable package identity and one
nullable flag:

```fsharp
let [<Literal>] PACKAGE_METADATA = """(*
---
$schema: "https://avpr.nfdi4plants.org/schemas/v1/validation-package-frontmatter.schema.json"
Name: example-validation
MajorVersion: 1
MinorVersion: 0
PatchVersion: 0
Summary: Checks a small set of example ARC requirements.
Description: Demonstrates the validation-package metadata and execution contract.
Publish: false
Inputs:
  - id: strict
    type: boolean?
    label: Strict validation
    inputBinding:
      prefix: --strict
---
*)"""
```

After installation, the reference runner can execute the package directly:

```shell
arc-validate validate \
  --arc-directory ./my-arc \
  --out-directory ./results \
  --package example-validation \
  --package-version 1.0.0 \
  --source-branch main \
  --source-commit-hash 0123456789abcdef \
  -- \
  --strict
```

The resulting directory is:

```text
results/
└── .arc-validate-results/
    └── example-validation@1.0.0/
        ├── badge.svg
        ├── validation_report.xml
        └── validation_summary.json
```

## License

Copyright 2022-2026 [DataPLANT](https://nfdi4plants.org).

Licensed under the [Creative Commons License CC BY, Version 4.0](https://creativecommons.org/licenses/by/4.0/); you may not use this file except in compliance with the License.

This license allows re-users to distribute, remix, adapt, and build upon the material in any medium or format, so long as attribution is given to the creator. The license allows for commercial use. Credit must be given to the creator.

# DataPLANT ARC Continuous Quality Control Specification

* Version: 1.0.0-draft.1
<!-- Proposed permalink: <https://w3id.org/arc/specifications/continuous-quality-control/1.0.0-draft.1> -->
* Authors:
  * Kevin Schneider - [https://orcid.org/0000-0002-2198-5262](https://orcid.org/0000-0002-2198-5262)
  * Jonathan Bauer - [https://orcid.org/0000-0002-5624-2055](https://orcid.org/0000-0002-5624-2055)
* License: [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/)

* **Table of contents**
  * [Overview](#overview)
  * [Execution Environment](#execution-environment)
    * [CI/CD](#cicd)
    * [The arc-validate CLI Tool](#the-arc-validate-cli-tool)
  * [Validation Package Selection](#validation-package-selection)
  * [Validation Plan](#validation-plan)
  * [Validation History and Provenance Tracking](#validation-history-and-provenance-tracking)
  * [ARC Applications](#arc-applications)
  * [Examples](#examples)
  * [License](#license)

## Overview

This document specifies the DataPLANT reference implementation profile for the
[Continuous Quality Control (CQC) concept](../../ARC%20specification.md#continuous-quality-control).
It connects five independently versioned contracts:

1. executable [validation packages](validation-packages.md);
2. the ARC-owned `.arc/validation_packages.yml` selection configuration;
3. a resolved `validation_plan.json` used by CI orchestration;
4. package result summaries and reports; and
5. a Git-based provenance and history profile for CQC results.

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHOULD**, **SHOULD NOT**,
and **MAY** in this document are to be interpreted as described in
[BCP 14](https://www.rfc-editor.org/info/bcp14) when, and only when, they
appear in all capitals.

The reference flow is resolve once, execute exact versions, and retain results
with their source identity:

```text
.arc/validation_packages.yml
        │
        ▼
arc-validate config resolve ──► validation_plan.json
        │
        ├──► install exact package version ──► validate immutable ARC revision
        └──► install exact package version ──► validate immutable ARC revision
                                                   │
                                                   ▼
                                      summary, report, badge, provenance
```

Resolution and execution are separate so every child job uses the decision
made by one parent job. Package input values remain in the source
configuration; they are not copied into generated CI definitions or the
validation plan.

## Execution Environment

### CI/CD

A CQC pipeline MAY be triggered by a push, merge request, tag, schedule, or
manual request. Every run MUST validate an immutable source revision and MUST
identify that revision in its retained provenance. A moving branch name alone
is not sufficient source identity.

The reference pipeline has one parent resolution job and one child execution
job per selected validation package:

1. The parent checks out the source revision and reads the configuration once.
2. The parent resolves and preflights every selection before creating any
   package child jobs.
3. The parent persists `validation_plan.json` as a diagnostic artifact.
4. Each child installs the exact resolved package version.
5. Each child verifies the unchanged configuration bytes and executes that
   exact package against the same source revision.
6. The pipeline collects the standard validation-package outputs and updates
   the CQC result history.

If `.arc/validation_packages.yml` is absent, no author-selected package job is
created. A platform MAY still run explicitly documented built-in checks. A
present configuration with an empty `validation_packages` sequence succeeds
without package child jobs. A present but invalid configuration MUST fail the
parent before child generation.

Validation packages are executable third-party code. The CI implementation
SHOULD isolate package processes, grant the least filesystem and network
access needed, protect credentials from package jobs, set resource limits,
and treat the checked-out ARC as read-only. These controls are deployment
policy; they do not change package validation semantics.

### The arc-validate CLI Tool

[`arc-validate`](https://github.com/nfdi4plants/arc-validate) is the reference
resolver, package manager, and runner. The parent creates a plan with:

```shell
arc-validate config resolve \
  --validation-config .arc/validation_packages.yml \
  > validation_plan.json
```

Standard output MUST contain only the complete JSON plan. Diagnostics use
standard error. The reference CLI classifies malformed configuration or
unsatisfied selections as exit code `4` and registry transport or response
failures as exit code `5`; structural command misuse remains `2`, and
unexpected defects remain `3`.

For each plan entry, a child installs and runs the resolved identity:

```shell
arc-validate package install configurable-validation --version 1.2.7

arc-validate validate \
  --arc-directory . \
  --package configurable-validation \
  --package-version 1.2.7 \
  --validation-config .arc/validation_packages.yml \
  --validation-config-sha256 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef \
  --source-branch main \
  --source-commit-hash fedcba9876543210
```

Config-driven execution requires `--package`, `--package-version`, and
`--validation-config` together. It is mutually exclusive with manual package
arguments after `--`. The digest is optional for a direct interactive call but
MUST be supplied by generated CI jobs.

The child MUST load the exact installed package version, revalidate inputs
against that version's embedded declarations, and construct an argument list
without a shell. It MUST NOT query the registry or re-resolve “latest”; a newer
package may have been published after the parent created the plan.

## Validation Package Selection

Each ARC branch MAY contain zero or one selection file at the canonical path
`.arc/validation_packages.yml`. The versioned machine-readable companion is
the [validation-packages configuration schema](../schemas/validation-packages.schema.json),
identified by
`https://avpr.nfdi4plants.org/schemas/v1/validation-packages.schema.json`.

A canonical document is a mapping with these fields and no others:

| Field | Required | Meaning |
| --- | --- | --- |
| `$schema` | yes | MUST equal the v1 configuration schema identifier. |
| `arc_specification` | no | Complete Semantic Version of the ARC specification to use for built-in ARC validation. |
| `validation_packages` | yes | Ordered package selections; the sequence MAY be empty. |

`$schema` is an immutable wire-format discriminator and editor association.
Readers MUST use an exact local allowlist, MUST NOT fetch an arbitrary schema
URI during parsing, and MUST reject unsupported identifiers. An incompatible
future format receives a new URI rather than a numeric version field inside
this document.

Each package selection contains:

| Field | Required | Meaning |
| --- | --- | --- |
| `name` | yes | Non-empty, exact, case-sensitive package name, unique within this file. |
| `version` | yes | Complete Semantic Version used as the exact identity or rolling floor. |
| `roll_forward` | no | `disable`, `latest_patch`, or `latest_minor`; omission means `disable`. |
| `inputs` | no | Mapping from exact package input declaration ID to a supported scalar value. |

Version policies have these semantics:

| Policy | Selection rule |
| --- | --- |
| `disable` | Select exactly `version`, including prerelease or build metadata. |
| `latest_patch` | Select the highest published stable version in the same major and minor line whose precedence is at least the requested floor. |
| `latest_minor` | Select the highest published stable version in the same major line whose precedence is at least the requested floor. |

For a rolling policy, the floor itself need not be published, but both the
floor and selected version MUST be stable. Rolling never crosses a major
version and fails if no eligible release exists. Prerelease or build metadata
is therefore valid only with `disable`.

An `inputs` key is a package declaration `id`, not an
`inputBinding.prefix` or human-readable `label`. The selected package version's
metadata is authoritative for the ID, type, nullability, and requiredness.
Supported configuration values are:

| Declared type | Accepted configuration value |
| --- | --- |
| `boolean` | Lowercase YAML `true` or `false`. |
| `int` | JSON-form integer in the signed 32-bit range. |
| `long` | JSON-form integer in the signed 64-bit range. |
| `float` | JSON-form integer or number representable as a finite IEEE-754 single-precision value. |
| `double` | JSON-form integer or number representable as a finite IEEE-754 double-precision value. |
| `string` | Quoted YAML string. |

A `?` suffix makes the declared type nullable. Every non-nullable input,
including a boolean with value `false`, MUST be explicitly present. A nullable
input MAY be omitted or set to lowercase `null`. Unknown IDs, missing required
values, invalid nulls, range failures, and implicit coercions MUST fail.
Integer-to-floating widening is allowed; floating-to-integer and
string/boolean coercions are not.

Input values use a strict JSON-compatible YAML scalar profile. Readers MUST
reject composite values, unquoted strings, YAML convenience scalars such as
`yes`, `no`, `on`, `off`, and `~`, implicit empty nulls, hexadecimal or octal
numbers, numeric separators, leading-zero integers, non-finite values, aliases,
anchors, tags, merge keys, duplicate keys, multiple documents, and unknown
fields. Numeric lexemes MUST be retained until declaration validation and
argument materialization so a JavaScript consumer cannot round a valid signed
64-bit integer.

JSON Schema covers the JSON-compatible structure but cannot enforce all YAML
lexical, uniqueness, declaration, range, or resolution rules. The released
AVPR Model and Codecs are the executable reference for those rules. A consumer
MUST NOT replace that contract with shell-oriented YAML extraction.

## Validation Plan

The parent resolver emits the canonical persisted file
`validation_plan.json`. Its structural contract is the
[validation-plan schema](../schemas/validation-plan.schema.json), identified by
`https://nfdi4plants.github.io/arc-validate/schemas/v1/validation_plan.schema.json`.

The plan is a closed object containing:

| Field | Required | Meaning |
| --- | --- | --- |
| `$schema` | yes | Exact v1 plan schema identifier. |
| `config_sha256` | yes | Lowercase SHA-256 of the exact configuration bytes. |
| `arc_specification` | no | Canonical ARC specification version copied from the configuration. |
| `validation_packages` | yes | Ordered, fully resolved package identities. |

Each package entry is a closed object with these fields:

| Field | Required | Meaning |
| --- | --- | --- |
| `name` | yes | Exact package name copied from the configuration selection. |
| `requested_version` | yes | Complete Semantic Version copied from the selection's `version`. |
| `roll_forward` | yes | Effective policy: `disable`, `latest_patch`, or `latest_minor`. |
| `resolved_version` | yes | Exact package version the child MUST install and execute. |

The resolver preserves configuration selection order in the plan. This does
not impose execution order on child jobs, which MAY run concurrently.

The digest is calculated over the file's exact bytes, including a UTF-8 byte
order mark when present. The resolver MUST finish registry discovery,
version resolution, metadata retrieval, declaration validation, and input
preflight before emitting any plan. An invalid selection MUST NOT produce a
partial plan.

The plan deliberately excludes configured input values. CI needs only the
package name, resolved version, configuration path, and digest. Keeping values
in the source configuration avoids re-encoding them through JSON, generated CI
YAML, environment variables, or shell syntax.

Plan consumers MUST dispatch the `$schema` value through a local allowlist and
MUST NOT dereference it at runtime. The schema validates document structure;
the resolver additionally guarantees package-name uniqueness and the exact or
rolling relationship between requested and resolved versions.

## Validation History and Provenance Tracking

The reference profile keeps CQC result files in a dedicated `cqc` branch of
the ARC repository so generated results do not modify the source branch. The
branch:

* MUST be an orphan branch named `cqc`;
* MUST NOT be merged into an ARC source branch; and
* MUST store current package outputs under
  `{source-branch}/{package-name}@{resolved-version}/`.

Each package result directory contains all three files defined by the
[validation-package output contract](validation-packages.md#output-files):

```text
cqc branch root/
└── {source-branch}/
    └── {package-name}@{resolved-version}/
        ├── badge.svg
        ├── validation_report.xml
        └── validation_summary.json
```

An execution is identified by the source repository, source commit hash,
source branch at execution time, package name, exact package version, and
validation configuration digest. The retained package result files identify
the source and package identity; the retained validation plan supplies the
configuration digest and resolution decision. The CQC commit message MUST
contain the validated source commit hash. `validation_summary.json` MUST
contain matching `SourceBranch` and `SourceCommitHash` values, and the JUnit
report and badge SHOULD embed the same source provenance using their
format-specific metadata facilities.

`validation_plan.json` SHOULD be retained as a CI artifact alongside the run
that produced the results. Its `config_sha256` binds parent resolution to the
configuration bytes rechecked by every child. Together, the plan, result
summary, source revision, and immutable package identity provide the minimum
information needed to reproduce which checks ran and why that version was
chosen.

Later executions update the current result paths in new `cqc` commits; the Git
history retains prior results. A failed or cancelled job MUST NOT present stale
files as results for a newer source commit. Pipeline or installation failure
is distinct from a validation-case failure and SHOULD be exposed separately by
the CI system when no conforming package outputs were produced.

## ARC Applications

An **ARC application** is a service that performs an action using an ARC and a
validation result. Examples include preparing a repository submission,
requesting publication, generating a transformed representation, or proposing
metadata corrections.

A validation package SHOULD determine whether an ARC meets the application's
preconditions; it SHOULD NOT perform the external action itself. This keeps a
quality assessment reproducible and separates it from operations that require
authorization, user confirmation, or changes to external systems.

A package MAY declare `CQCHookEndpoint` in its metadata, and the same endpoint
MAY appear in `validation_summary.json`. A CQC system MAY notify that endpoint
or expose it as a user action after validation. The HTTP method, authentication,
authorization, retry, and payload-delivery contract are application-specific
and are not defined by this version.

Implementations MUST treat hook endpoints as untrusted destinations, MUST NOT
place credentials or unrestricted ARC content in a URL, and MUST obtain the
authorization required for any data transfer or state-changing action. A hook
failure MUST NOT rewrite the validation outcome.

## Examples

This canonical configuration selects the newest stable `1.2.x` release at or
above `1.2.3` and supplies three declared inputs:

```yaml
$schema: "https://avpr.nfdi4plants.org/schemas/v1/validation-packages.schema.json"
arc_specification: 3.0.0-draft.2
validation_packages:
  - name: configurable-validation
    version: 1.2.3
    roll_forward: latest_patch
    inputs:
      strict: true
      minimum-files: 2
      report-title: "release candidate"
```

If AVPR reports `1.2.7` as the highest eligible release, resolution emits a
plan with this shape:

```json
{
  "$schema": "https://nfdi4plants.github.io/arc-validate/schemas/v1/validation_plan.schema.json",
  "config_sha256": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
  "arc_specification": "3.0.0-draft.2",
  "validation_packages": [
    {
      "name": "configurable-validation",
      "requested_version": "1.2.3",
      "roll_forward": "latest_patch",
      "resolved_version": "1.2.7"
    }
  ]
}
```

After the child verifies the digest and runs that exact version, the retained
results for `main` have this layout:

```text
cqc branch root/
└── main/
    └── configurable-validation@1.2.7/
        ├── badge.svg
        ├── validation_report.xml
        └── validation_summary.json
```

## License

Copyright 2022-2026 [DataPLANT](https://nfdi4plants.org).

Licensed under the [Creative Commons License CC BY, Version 4.0](https://creativecommons.org/licenses/by/4.0/); you may not use this file except in compliance with the License.

This license allows re-users to distribute, remix, adapt, and build upon the material in any medium or format, so long as attribution is given to the creator. The license allows for commercial use. Credit must be given to the creator.

# Consistency review: ARC specification split RFC

Review date: 2026-09-18.

Reviewed draft: [spec-split.md](spec-split.md).

These are observations and suggested wording for continuing the discussion. They are not accepted specification decisions. The review did not change the RFC, specifications, implementation code, or existing plans. No tests were run for this document review.

## Overall assessment and related work

The direction is consistent with the existing [modular validation specifications plan](../../arc-validate-package-registry/plans/modular-validation-specifications.md), but this RFC is substantially broader. The earlier plan separates validation contracts from implementations; this RFC also reconsiders what qualifies as an ARC.

The earlier plan explicitly excludes ISA-XLSX. Workspace representations, the ARC Base Model, and publication interoperability therefore extend its scope rather than merely restating it.

The older [validation-package configuration plan](../../arc-validate-package-registry/plans/validation-packages-config.md) records the monolithic specification proposal as superseded before normative acceptance. Its implementation history and the modular plan's later alignment notes should not be treated as proof that all proposed contracts are finalized. These are local planning records; live issue and deployment status was not rechecked.

Suggested relationship paragraph:

> This RFC extends the existing modular validation specification work into a broader architecture for ARC specifications. It distinguishes extraction of existing requirements into profiles from proposed changes to the ARC definition. Workspace representations, the Base Model, and publication interoperability require additional decisions beyond the validation workstream.

## 1. Separate core concepts, normative profiles, and reference implementations

The draft currently presents a two-way split. That leaves unclear whether extracted requirements remain normative. The existing validation plan distinguishes three layers:

| Layer | Purpose |
| --- | --- |
| Core model | Defines ARC concepts and their relationships |
| Specifications and profiles | Define interoperable representations and conformance requirements |
| Reference implementations | Implement those contracts in software and infrastructure |

A concrete format can remain normative for a particular profile without being a universal requirement for every ARC implementation. Removing requirements from the core should not implicitly turn them into informative software documentation.

Suggested wording:

> The proposal separates the ARC's core concepts, normative specifications and profiles for interoperable representations, and their reference implementations. Requirements moved out of the core remain binding for implementations claiming conformance to the corresponding profile.

Suggested title:

> Modularizing the ARC specification: core concepts, interoperability profiles, and reference implementations

## 2. Frame the proposed ARC definition as the central conformance decision

The draft's "one? two? all?" questions are appropriate for a discussion issue. They currently combine several distinct decisions:

- Which concepts define an ARC?
- Which concepts must a workspace implementation support?
- How complete must an individual ARC be at a particular lifecycle stage?
- Which representation profiles must a particular ARC state satisfy?

The [ARC RO-Crate profile collection](https://nfdi4plants.github.io/arc-ro-crate-profile/profiles/) allows profiles to be used independently or in combination. That alone does not establish that every such combination qualifies as an ARC.

Suggested framing:

> A central question is which minimum commitments distinguish an ARC from another research object. We should distinguish support for the ARC Base Model, completeness of an individual ARC at a particular lifecycle stage, and conformance to specific representation profiles.

Possible alternatives to discuss, without deciding them in this review:

- All three principles, with lifecycle-dependent completeness.
- A required subset of principles.
- Named conformance levels or combinations.

An unfinished ARC does not necessarily imply that its workspace supports only part of the model. Likewise, theoretical exportability to RO-Crate needs an agreed mapping or profile before it becomes a useful conformance criterion.

The three empty Base Model sections would benefit from one concrete definition each:

- **Administrative metadata:** administrative context, such as attribution and rights.
- **Semantic designation:** meaning assigned to data and data fragments.
- **Process provenance:** relationships describing how research entities are generated or transformed.

These definitions are suggested starting points, not a settled minimum metadata contract.

## 3. Broaden workspace and distinguish the two kinds of provenance

"Materialization ... on disk" retains a filesystem assumption while the proposal opens other implementation choices. It permits non-Git filesystems, but excludes database-backed or service-native workspaces by definition. Whether that exclusion is intended remains a discussion choice.

If broader implementations should qualify:

> An ARC workspace is an environment for creating, maintaining, and working with an ARC. The current filesystem-based scaffold is one realization of this concept.

Also distinguish research-process provenance from the history of changes to the ARC. A process graph and Git history serve different purposes.

Suggested wording:

> Process provenance describes how research entities and results were produced. ARC-state provenance describes the evolution of the research object itself. The split should specify which guarantees belong to the core and how workspace or infrastructure profiles realize them.

Removing Git as a universal requirement leaves a separate decision about identifying states and recording their evolution. This is a substantive conformance change: the current specification requires Git and says that removing the `.git` directory invalidates an ARC.

## 4. Clarify what RO-Crate compatibility guarantees

The publication section should say whether RO-Crate is a required interchange representation, a publication representation, or both. Explain why it is the shared interoperability choice while ISA, CWL, and Git become profile-specific choices.

"Capturing the same information" could imply preservation of spreadsheet presentation, workspace configuration, arbitrary payload, or complete Git history. Specify the intended scope of preservation.

Suggested wording:

> Each workspace profile should define how its ARC information maps to the shared RO-Crate representation, which semantics are preserved, and how extensions or unmapped information are handled.

Keep representability, profile conformance, and publication readiness distinct:

> The RO-Crate representation can describe an ARC at any lifecycle stage. Being expressible in that representation is separate from satisfying a particular repository's publication requirements.

The cited [publication infrastructure paper](https://link.springer.com/article/10.1007/s42979-026-05010-8) already describes RO-Crate representations being available during the ARC lifecycle, before publication.

The meta issue should also identify where the current "publishable" and "reproducible" requirements will live after the split.

## 5. Use the existing validation plan to fill the validation/CQC placeholders

The modular plan already identifies these separate contracts:

- Validation packages.
- Package configuration.
- Execution plans.
- Validation summaries.
- A CQC provenance profile.

These should not all be classified as DataHUB implementation details. Validation itself can also happen locally, outside hosted infrastructure.

Suggested text:

> The core specification describes validation as an assessment of an identified ARC state against explicit requirements. Separate specifications define interoperable package, configuration, execution-plan, and result formats. Infrastructure profiles define how validation is triggered and how results are retained. DataHUB's Git-based CQC workflow is one implementation of these concepts.

Retain the distinction between a failed requirement and a failed evaluation. Results should remain associated with the source state, package version, and execution inputs.

At meta-issue level, it is sufficient to identify these boundaries and link the detailed workstream. There is no need to reproduce every schema or CLI decision.

## 6. Separate document reorganization from changes to ARC requirements

Moving existing requirements into modules and allowing non-ISA or non-Git ARCs are different changes. The latter needs an explicit compatibility and conformance discussion.

Refine "move everything ISA(XLSX) and CWL related": abstract process, input/output, and workflow/run concepts may belong in the core even when their current expression uses ISA or CWL.

Suggested checklist item:

> Extract representation-independent entity, annotation, and process relationships into the core; move concrete directory layouts, file formats, serialization rules, and execution bindings into named profiles.

Moving paragraphs alone will not decouple releases. The existing specification explicitly ties ISA-XLSX's version to the ARC specification; the earlier validation plan proposes independently versioned modules and immutable versioned identifiers. The broader RFC needs to explain compatibility between core, workspace, RO-Crate, and infrastructure profile versions.

Suggested checklist additions:

- [ ] Assign existing requirements to their destination documents.
- [ ] Define conformance and lifecycle expectations.
- [ ] Specify workspace-to-RO-Crate mappings and preservation guarantees.
- [ ] Establish independent module versions, stable identifiers, and compatibility relationships.
- [ ] Describe migration for existing ARCs and tooling, including the status of the existing ISA-XLSX/CWL/Git representation.
- [ ] Assign resource identity and references, licensing metadata, additional payload, reproducibility, and publication readiness to the appropriate layer.
- [ ] Separate specification acceptance from implementation updates and infrastructure rollout.

## Accuracy and editorial observations

- **Released baseline versus local work:** The CQC example matches the [released specification](https://github.com/nfdi4plants/ARC-specification/blob/release/ARC%20specification.md#continuous-quality-control). At review time, the local `spec-reference-split` branch already contained draft extraction work in [ARC specification.md](../ARC%20specification.md), version `3.0.0-draft.2`, with separate [validation-package](../references/specifications/validation-packages.md) and [CQC](../references/specifications/continuous-quality-control.md) documents. Label the released baseline and work underway explicitly; local drafts are not evidence of normative acceptance.
- **Plant-science scope is explicit in current wording:** The [README](../README.md) describes ARCs as "for plant sciences," and the specification introduction mentions plant biological research. The motivation therefore concerns existing wording as well as outside perception. Suggested wording: "The specification and tooling originate in plant research, but the underlying principles can be expressed without a plant-specific dependency. This proposal makes that broader applicability explicit."
- **Qualify mandatory ISA/CWL wording:** Investigation metadata is mandatory, while CWL requirements apply to the corresponding workflow/run components. Suggested wording: "The current specification prescribes a Git-based directory representation, mandatory investigation metadata in ISA-XLSX, and ISA-XLSX/CWL descriptions for the corresponding study, assay, workflow, and run components."
- **Standards versus their adoption:** Describe ISA and CWL as standards adopted by DataPLANT's reference representation rather than implying that those standards are themselves DataPLANT-specific.
- **Small cleanup for later:** Fill the empty ARC Workspace link, complete the bibliography and checklist placeholders, and normalize terminology such as RO-Crate, GitLab, and DataPLANT's. The two referenced images were present next to the draft.

## Suggested starting point for the next session

First agree on the three-layer distinction and the questions governing ARC conformance. Then expand the Base Model, workspace, and publication sections around those decisions, and incorporate the existing validation workstream. Keep organizational extraction and intentional changes to requirements separately identifiable throughout the RFC.

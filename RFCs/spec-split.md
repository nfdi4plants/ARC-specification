# [Discussion/RFC] Separate core ARC concepts from workspace and infrastructure implementations

## Motivation

The ARC in how DataPLANT supports it and develops tooling for is a historically grown fusion of core concepts and plant research-specific or -adjacent usage of standards and/or perspectives. However, the ARC concept itself is in no way domain specific for plant research or even biology - but might look like it from the outside due to the usage of e.g. ISA.

The general direction of the work we are doing on ARCs and related infrastructure and tooling gives a clear picture: we built a system with specific implementations for solid foundational concepts. Now the push is to distill the core concepts from the implementation details, ensuring that the ARC framework remains flexible and adaptable to various research domains.

in this Discussion/RFC, i want to lay out the foundations and plan on how to decouple the core ARC specification from DataPLANT's domain-specific implementations of these concepts. That way, we can prevent the ARC from being seen as a domain-specific FDO (which it is not!), while defining the guard rails for implementing ARC-based systems in other domains of research.

Some examples on why this is necessary:

- **The current ARC specification defines an ARC as a strict folder structure in which MANDATORY ISA and CWL-formatted metadata files reside**

  While in its core completely in line with the ARC's core process-centric view on RDM, ISA is percieved as an experimental biologists standard. Furthermore, the usage of ISA-XLSX for initially reducing usage barriers has been discussed many times and does not need to be repeated here.

  The ARC as a concept has evolved in a way that this is only one realization of an ARC. Other systems should be able to use all of our initial choices, some, or even none. I will explain this further in the [ARC Workspace section](#arc-workspaces).

- **The current specification conflates concepts with DataPLANT's infrastructure-specific decisions**

  Case in point: [Continuous Quality Control](https://github.com/nfdi4plants/ARC-specification/blob/release/ARC%20specification.md#continuous-quality-control). Here, DataPLANT's specific infrastructure choices - for example tracking validation provenance in a git branch with a specific name or how to configure what validation package should be run on the ARC DataHUB - lies on the same level as core ARC concept descriptions. This is not only unecessary (people should be able to implement this in their own systems according to their needs) but also makes iterating on these implementations slower since they are coupled to actual releases of the FULL specification.

## Proposed Approach

The proposed approach is to define what an ARC is conceptually, independently of workspace and infrastructure implementations. The core specification describes the concepts and their relationships without prescribing a particular data model implementation, workspace format, or tool.

The [ARC Base Model](#the-arc-base-model) provides a domain-neutral reference realization of these concepts and a foundation for managing ARC workspaces. Other implementations can realize the same concepts. The shared interoperability contract is compatibility with the core ARC concepts and the ability to eventually export ARC information according to the ARC RO-Crate profiles. The required concepts, profile combinations, and timing of export remain open questions in this RFC.

I identified the following key areas where the separation should be applied:

- [Core ARC concepts](#core-arc-concepts)
- [The ARC Base Model](#the-arc-base-model)
- [ARC Workspaces](#arc-workspaces)
- [Embedding ARCs into (cloud?) infrastructure](#embedding-arcs-into-infrastructure)
  - [ARC Validation](#arc-validation)
  - [Continuous Quality Control](#continuous-quality-control)
- [ARC Publication Space and RO-crate as the core harmonization layer](#publication-space-and-ro-crate-as-the-core-harmonization-layer) 

### Core ARC concepts

The core specification should describe the following concepts independently of their realization in software or their representation in a workspace. Which concepts are required, and to what extent, remains a discussion point.

![Core ARC annotation principles](core-annotation-principles.png)

#### Administrative Metadata

#### Semantic Designation / Annotation

(cite and reference below: https://www.degruyterbrill.com/de/document/doi/10.1515/jib-2025-0052/html)

#### Process Provenance

### The ARC Base Model

The [ARC Base Model](https://github.com/HLWeil/ARC-base-model) is a domain-neutral reference realization of the core ARC concepts. This "Layer 0" implementation provides a foundation for managing ARC workspaces, on which domain-specific decorations and tooling can build.

The conceptual ARC specification should be understandable independently of this implementation. Workspaces can use the ARC Base Model or another implementation compatible with the core concepts and capable of eventual export according to the ARC RO-Crate profiles. ISA/CWL-based representations, their decorations, and their mappings belong to the respective domain and tooling implementations.

### ARC Workspaces

An ARC workspace is an environment for creating, maintaining, and working with an ARC, intended for active use by researchers and other stakeholders involved in the research data management process. Its realization can use different data models, storage systems, formats, and tools.

The current specification defines an ARC workspace as a strict folder structure with mandatory ISA-formatted metadata files.

In a push for connecting the ARC to the wider RDM landscape, we invested significant resources into developing the RO-Crate representation of the ARC.

The development of the ARC RO-Crate profiles helped distill the [core ARC concepts](#core-arc-concepts) by requiring us to evaluate their meaning and requirements independently of the previously chosen workspace standards. The [ARC Base Model](#the-arc-base-model) provides a concrete reference realization of these concepts. (cite and reference below: https://osf.io/preprints/biohackrxiv/7y2jh_v1 , https://www.degruyterbrill.com/de/document/doi/10.1515/jib-2025-0050/html)

![two sides of the same coin: ARC Scaffold and ARC RO-Crate](two-sides-of-the-same-coin.png)

This led to the first conceptual evolution of the ARC: **two sides of the same coin**. For each state of the ISA/CWL workspace, we were now able to attach the a RO-Crate representation, capturing the same information in a more flexible and interoperable format. Note that in this iteration, the ARC worspace was called the _ARC Scaffold_

Opening up the ARC workspace as a concept with different implementations and standards used is the logical next step. Workspaces may choose their internal representations and tools, provided their ARC information is compatible with the core concepts and can eventually be exported according to the ARC RO-Crate profiles. Using the ARC Base Model implementation is optional.

**Which core concepts a workspace must support, and what information is required at a particular lifecycle stage, remain questions for discussion.** These concern the conceptual commitments and eventual export, independently of the implementation chosen to manage the workspace.

### Embedding ARCs into infrastructure

#### DataHUB

- slight problem of PLANTdataHUB being the core paper that is usually referenced to cite that someone worked with our infrastructure (cite and reference below: https://onlinelibrary.wiley.com/doi/full/10.1111/tpj.16474)

- the choice of gitlab was right, we can implement a lot based on it

- however, other future ARC implementations might not even be git repos

- a spec rework should reflect these as OUR impementation choices, ARCs in other systems might not even be git repos as long as they can track states in some provenance framework

#### ARC Validation

- Conceptual AND specific spec is combined here, i proipose a simple split

cite and reference below:   
https://osf.io/preprints/biohackrxiv/zah28
https://onlinelibrary.wiley.com/doi/full/10.1111/tpj.16474

#### Continuous Quality Control

- Conceptual AND specific spec is combined here, i proipose a simple split

### Publication Space and RO-crate as the core harmonization layer

Publication space generalizes two sides of the same coin in the RO-Crate dimension. We identified RO-Crate as the FDO harmonization layer. Compatible export according to the ARC RO-Crate profiles provides the shared interoperability contract across workspace implementations.

**An ARC could therefore be defined as a research object that applies core ARC concepts in a workspace of any implementation and whose information can eventually be expressed according to the ARC RO-Crate profiles.** This proposed generalized definition does not require use of the ARC Base Model implementation. It remains provisional, with the following questions still open:

- Which core concepts must an ARC apply, and to what extent?
- Which ARC RO-Crate profiles or combinations must its exported representation satisfy?
- At what lifecycle stage must a conforming export be available?

The commitment to eventual export does not by itself require a complete, conforming RO-Crate to exist throughout active workspace development.

cite and reference below: https://link.springer.com/article/10.1007/s42979-026-05010-8

## Implementation checklist

- [ ] Describe the core ARC concepts and their relationships independently of the ARC Base Model implementation.
- [ ] Position the ARC Base Model as the domain-neutral reference realization and a foundation for workspace management.
- [ ] Define ARC workspaces independently of particular data models, storage systems, formats, and tools, with compatibility grounded in the core concepts and eventual ARC RO-Crate export.
- [ ] Place ISA-XLSX/CWL workspace representations, decorations, and mappings with their respective implementations, without making them core ARC requirements or requiring a normative ARC profile for every workspace.
- [ ] Resolve which core concepts and ARC RO-Crate profile combinations are required, and when a conforming export must be available.

## References

- [1]: Bla
- [2]: Another reference
- [3]: Yet another reference
- [4]: Yet another reference
- [5]: Yet another reference

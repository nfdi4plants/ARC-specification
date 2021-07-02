# Annotated Research Context Specification, v1-rfc 

Please provide feedback via Github issues or a pull request.

**Editors:**
  - Timo Mühlhaus &lt;muehlhaus@bio.uni-kl.de&gt;
  - Dirk von Suchodoletz &lt;dirk.von.suchodoletz@rz.uni-freiburg.de&gt;
  - Christoph Garth &lt;garth@cs.uni-kl.de&gt;

**Github repository:**  https://github.com/nfdi4plants/specs

This specification is Copyright 2021 by [DataPLANT – Nationale Forschungsdateninfrastruktur](nfdi4plants.de). 

Licensed under the Creative Commons License CC BY, Version 4.0; you may not use this file except in compliance with the License. You may obtain a copy of the License at https://creativecommons.org/about/cclicenses/. This license allows re-users to distribute, remix, adapt, and build upon the material in any medium or format, so long as attribution is given to the creator. The license allows for commercial use. Credit must be given to the creator. 

**Table of Contents**
- [Introduction](#introduction)
- [ARC Structure and Content](#arc-structure-and-content)
  - [High-Level Schema](#high-level-schema)
  - [Example ARC structure](#example-arc-structure)
  - [ARC Representation](#arc-representation)
  - [Assay Data and Metadata](#assay-data-and-metadata)
  - [Workflow Description](#workflow-description)
  - [Run Description](#run-description)
  - [External Data](#external-data)
  - [Additional Payload](#additional-payload)
  - [Top-level Metadata and Workflow Description](#top-level-metadata-and-workflow-description)
    - [Investigation and Study Metadata](#investigation-and-study-metadata)
    - [Top-Level Run Description](#top-level-run-description)
  - [ISA-XLSX Format](#isa-xlsx-format)
- [Shareable and Publishable ARCs](#shareable-and-publishable-arcs)
- [Mechanism for quality control of ARCs](#mechanism-for-quality-control-of-arcs)
- [Best Practices](#best-practices)
  - [Additional (auxiliary) Payload](#additional-auxiliary-payload)
  - [Community specific data formats](#community-specific-data-formats)
  - [Compression and Encryption](#compression-and-encryption)
  - [Directory and File Naming Conventions](#directory-and-file-naming-conventions)
- [Appendix: Conversion of ARCs to RO Crates](#appendix-conversion-of-arcs-to-ro-crates)

## Introduction

This document intends to develop and describe a specification for a standardized way of creating a working environment and packaging file-based research data and necessary additional contextual information for working, collaboration, preservation, reproduction, re-use, and archiving as well as distribution.

This document specifies a data storage schema and representation, named *Annotated Research Context*(ARC), for organizing file-based data and processing workflows with associated metadata in both human and machine-readable formats. ARCs combine existing standards, leveraging the properties of the investigation-study-assay ISA model, for metadata and the Common Workflow Language (CWL) for representing processing specification. While aiming to be compatible with similar standards and schemas, ARCs are specifically oriented towards common practices in experimental plant biology.

An ARC is intended to capture research data, analysis and metadata and their evolution in scenarios ranging from single experimental setups to complete research cycles in plant biological research. Its design intent is to not only assist researchers in meeting FAIR requirements, but to also minimize the workload for doing so. ARCs are self-contained and include assay/measurement data, workflow, and computation results, accompanied by metadata and history, in one package. Toward this, ARCs combine two widely used standards: the [ISA metadata model](https://isa-specs.readthedocs.io/en/latest/isamodel.html) and the [Common Workflow Language](https://www.commonwl.org).

ARCs are furthermore designed with straightforward conversion to other types of research data archive in mind, such as e.g. [Research Object Crates](https://www.researchobject.org/ro-crate/), to facilitate straightforward operation with widely used archives (e.g. PRIDE, GEO, ENA etc.). Therefore, ARCs aggregate administrative, experimental, and workflow meta data within a common structure.

This specification is intended as a practical guide for software authors to create tools for generating and consuming research data packages.

The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, MAY, and OPTIONAL in this document are to be interpreted as described in [RFC 2119](https://datatracker.ietf.org/doc/html/rfc2119).  This specification is  based on the [ISA model](https://isa-specs.readthedocs.io/en/latest/isamodel.html) and the [Common Workflow Specification (v1.2)](https://www.commonwl.org/v1.2/).

## ARC Structure and Content

ARCs are based on a strict separation of data and metadata content into raw data (assays), externals, computation results (runs) and computational workflows (workflows) generating the latter. The scope or granularity of an ARC aligns with the necessities of individual projects or large experimental setups. 

### High-Level Schema

Logically, each ARC is a directory containing the following elements: 

- *Assays* correspond to analytical measurements (in the interpretation of the ISA model) and are treated as immutable data. Each assay is a collection of files, together with a corresponding metadata file, stored in a subdirectory of the top-level subdirectory `assays`. Assay-level metadata is stored in [ISA-XLSX](##isa-xlsx-format) format in a file `isa.assay.xlsx`, which MUST exist for each assay. Further details on `isa.assay.xlsx` are specified [below](#assay-metadata). Assay data files MUST be placed in a `dataset` subdirectory.

- *Workflows* represent data analysis routines (in the sense of CWL tools and workflows) and are a collection of files, together with a corresponding CWL description, stored in a single directory under the top-level `workflows` subdirectory. A per-workflow executable CWL description is stored in `workflow.cwl`, which MUST exist for all ARC workflows. Further details on workflow descriptions are given [below](#workflow-descriptions).

- *Runs* capture data products (i.e., results of computational analysis) derived from assays, other runs, or external data using workflows. Each run is a collection of files, stored in the top-level `runs` subdirectory. It MUST be accompanied by a per-run CWL workflow description, stored in `<run_name>.cwl` and further described [below](#run-descriptions).

- *Externals* are external data (e.g., knowledge files) that need to be included and cannot be referenced due to external limitations. Metadata information SHOULD be stored according to the ISA model and CWL in case of workflow information; see [below](#external-data-annotation) for details.

- *Top-level metadata and workflow description* tie together the elements of an ARC in the contexts of investigation and associated studies (in the ISA definition), captured in the files `isa.investigation.xlsx` in [ISA-XLSX format](#isa-xlsx-format), which MUST be present. Optionally, study-level metadata MAY be present in `isa.studies.xlsx`. Furthermore, top-level reproducibility information MUST be provided in the CWL `arc.cwl`, which also MUST exist.

All other files contained in an ARC (e.g, a `README.txt`, a pre-print PDFs, additional annotation files, etc.) are referred to as *additional payload*, and MAY be located anywhere within the ARC structure. However, an ARC MUST be [reproducible](#reproducible-arcs) and [complete](#complete-arcs) even if these files are deleted. Further considerations on additional payload are described [below](#additional-payload).

Note: 

- Subdirectories and other files in the top-level `assays`, `workflows`, `runs`, and `externals` directories are viewed as additional payload unless they are accompanied by the corresponding mandatory description (`isa.assay.xlsx`, `workflow.cwl`, `run.cwl`, `isa.external.xlsx`) specified below. This is intended to allow gradual migration from existing data storage schemes to the ARC schema. For example, *data files* for an assay may be stored in a subdirectory of `assays/`, but are only identified as an assay of the ARC if metadata is present and complete, including a reference from top-level metadata.

- TODO: Distribution of metadata across many files. Redundancy etc.

### Example ARC structure
``` 
<top-level directory> 
|   isa.investigation.xlsx 
|   isa.studies.xlsx
|   arc.cwl 
|   arc.yml            
\--- assays
    \--- <assay_name> 
            |    isa.assay.xlsx  
            \--- dataset 
            \--- protocol [optional / add. payload]
\--- workflows  
    \--- <workflow_name> 
            | workflow.cwl 
            | docker-compose.yml [optional / add. payload]
\--- runs   
    \--- <run_name> 
        |    [files;...] (different result files) 
        |    run.cwl 
        |    run.yml            
\--- externals 
        |    [ knowledge files ] # external reference  
        |    isa.xlsx           
``` 

### ARC Representation

ARCs are a Git repositories, as defined and supported by the [Git C implementation](https://git-scm.org) (version XX or newer) with [Git-LFS extension](https://git-lfs.github.com) (version 2.12.0), or fully compatible implementations. 

ARC terminology implicitly borrows from Git and Git-LFS terminology. For example, an ARC commit is simply a Git commit, and the ARC history is the repository history. Furthermore, an ARC can contain multiple branches, etc.

Tree objects (resp. directories) and blobs (i.e., files) of all branch heads in the repository MUST adhere to the [ARC schema](#arc-structure-and-contents-schema). ARCs allow all typical Git operations (e.g. clone, branch) etc.

All representation suitable for Git-LFS repositories are also a valid representations of ARCs. This includes both bare repositories (without a checked out working copy) and non-bare repositories (i.e. a `.git` directory with one or more attached working copies). In particular, it is possible and intended to maintain ARCs on local user filesystems and via Git repository hosting services. No requirements are made of state and contents of working copies.

Notes:

- Archival representation (e.g. `.zip` or `.tar.gz`) are valid ARC representations if archives are created to preserve file attributes, i.e. if unarchiving preserves Git interoperability. Furthermore, Git's [bundle mechanism](https://git-scm.com/docs/git-bundle) can be used to create archives of complete ARCs or individual branches. For archiving purposes, `git bundle create --all` or an equivalent should be used.

- Elements of an ARC are implicitly content-addressable using standard Git mechanisms via SHA1 hashes.

- Removing the `.git` top-level subdirectory (and thereby all provenance information captured within the Git history) invalidates an ARC.

### ISA-XLSX Format

ISA-XLSX follows the ISA model specification saved in a XLSX format. The XLSX format uses the SpreadsheetML markup language and schema to represent a spreadsheet document. Conceptually, using the terminology of the Spreadsheet ML specification [ISO/IEC 29500-1](https://www.loc.gov/preservation/digital/formats/fdd/fdd000398.shtml#:~:text=The%20XLSX%20format%20uses%20the,a%20rectangular%20grid%20of%20cells.), the document comprises one or more worksheets in a workbook. Every worksheet MUST contain one table object storing the metadata. Comments or axillary information MAY be stored alongside with table objects in a worksheet.

### Assay Data and Metadata

All measurement data sets are considered as assays and are considered immutable input data. Assays data MUST be placed into a unique subdirectory of the top-level `assays` folder. All ISA metadata specific to a single assay (e.g., measurement type and technology, i.e. all terms with term names beginning with ASSAY) MUST be annotated in a in the file `isa.assay.xlsx` at the root of the assay's subdirectory. This workbook MUST containing a single assay that can be organized in one or many worksheets. Worksheets MUST be named uniquely within the same workbook. A worksheet named `study` MUST store the STUDY ASSAYS section defined on investigation-level of the ISA model that is duplicated from the ARC's top-level `isa.investigation.xlsx`. Additional worksheets MUST contain table object with fields organized on a per-row basis. The first row MUST be used for column headers. A `Source` MUST be indicated with the column heading `Source Name`. Every table object MUST define at least one source per row. A Sample MUST be indicated with the column heading Sample Name. The source sample relation MUST follow a unique path in a directed acyclic graph, but MAY distributed across different worksheets.

Notes:

- To ensure reusability of entire assays across multiple ARCs, redundancy between assay-specfic, assay-level metadata and investigation-level metadata is intentional. 

- It is RECOMMENDED to order worksheets according to the source sample relation for readability.

- It is RECOMMENDED to adopt the structure outlined [below](#best-practices) to organize assay data files and other supporting information.

- There are no requirements on specific assay-level metadata. Conversion of ARCs into other repository or archival format (e.g. PRIDE, GEO, ENA etc.) may however mandate the presence of specific terms (cf. [below](#arc-conversion)) required in the destination format.

- An implementation that ensures assay annotation consistent with these requirements is provided by the [SWATE tool](https://github.com/nfdi4plants/Swate).

- While assays can in principle contain arbitrary data formats, it is highly RECOMMENDED to use community-supported, open formats (see [Best Practices](#best-practices)).

### Workflow Description

*Workflows* in ARCs are computational steps that are used in computational analysis of an ARC's assays and other data transformation to generate a [run result](#run-description). Typical examples include data cleaning and pre-processing, computational analysis, or visualization. Workflows are used and combined to generate [run results](#run-description), and allow re-use of processing steps across multiple [run results](#run-description).

Workflows execution and metadata MUST be described using the [Common Workflow Language](https://www.commonwl.org/) (CWL), [v1.2](https://www.commonwl.org/v1.2/) or higher, in a file `workflow.cwl`, which MUST be placed in the subdirectory containing all files specific to this workflow under the top-level `workflows` directory. This file MUST contain either of:

- A CWL [tool description](https://www.commonwl.org/v1.2/CommandLineTool.html). Tool descriptions must be self-contained and not refer to any files outside the workflow subdirectory. All paths used within the tool description MUST be relative to itself.

- A CWL [workflow description](https://www.commonwl.org/v1.2/Workflow.html). Such descriptions MAY utilize other ARC workflows as [nested workflows](https://www.commonwl.org/user_guide/22-nested-workflows/index.html), but MUST use relative paths in this case. Files outside the ARC root directory MUST NOT be referenced.

Notes:

- There are no requirements on the structure or granularity of workflows. An ARC may contain no workflows at all if it contains no [run results](#run-description), or may utilize a single workflow to generate a single run result containing all computational output.

- While workflows typically are (and should be) *generic*, i.e. a single workflow can be applied to different data of the same type, this is not a requirement. It is allowed to hard-code assay file paths and other parameters if workflow re-useability is not a priority.

- It is highly recommended that tool descriptions contain a reproducable execution environment description in the form of a [Docker](https://www.commonwl.org/user_guide/07-containers/index.html) container description.

- It is expected that workflow and tool descriptions are be authored semi-automatically, e.g. using the [arcCommander](https://github.com/nfdi4plants/arcCommander) tool.

- It is strongly encouraged to include author and contributor metadata in tool descriptions and workflow descriptions as [CWL metadata](https://www.commonwl.org/user_guide/17-metadata/index.html).

### Run Description

**Runs** in an ARC represent all artefacts that result from some computation on the data within the ARC, i.e. [assays](#assay-data-and-metadata) and [external data](#external-data). These results (e.g. plots, tables, data files, etc. ) MUST reside inside one or more subdirectory of the top-level `runs` directory.

Each such subdirectory must contain a workflow description `run.cwl`, given in [Common Workflow Language](https://www.commonwl.org/) (CWL), [v1.2](https://www.commonwl.org/v1.2/) or higher, that describes how the files contained with the run are derived from assay or external data, or other runs. `run.cwl` MUST be placed in the subdirectory under the top-level `runs` directory. A parameter file `run.yml` MAY be given to specify run-specific input parameters.

`run.cwl` MAY (and sensibly, should) refer to assay data files, external data files, workflow descriptions, and files in other run results; such references MUST use relative paths. Furthermore, `run.cwl` MUST specify as outputs all result files. `run.cwl` MUST BE executable without referring to [additional payload files](#additional-auxiliary-payload) or files outside the ARC.

Notes:

- Run descriptions are intended to ensure that the computational analysis encapsulated within an ARC can be fully reproduced.

- Any files produced by executing the run description which are not specified as CWL outputs in `run.cwl` are considered additional ARC payload. Furthermore, all files of all subdirectories under `run` that are not referenced from the [top-level workflow](#top-level-workflow) are considered additional payload.

- It is expected that run descriptions are be authored semi-automatically, e.g. using the [arcCommander](https://github.com/nfdi4plants/arcCommander) tool.

- It is strongly encouraged to include author and contributor metadata in run descriptions as [CWL metadata](https://www.commonwl.org/user_guide/17-metadata/index.html).

### External Data

External data refers to data that is neither originating within the investigation/study scope of the ARC nor can be referenced externally, but is required to ensure reproducability. Examples include early use of ontologies, mapping files, gene information, etc. All correspondig data MUST be placed in the ARC's top-level `external` directory.

The union of external data forms a *virtual* assay; as such, it MUST adhere to the metadata requirements of assays and hence MUST contain, for each file, annotation in a file `isa.external.xlsx`, located under the top-level `external` directory.

Note:

- Each external data file can be interpreted as a virtual sample in the *externals* assay. Due to the conceptual difference to the immutable measurements represented by the assays in `assays`, external files are stored in a different location to ensure that this distinction explict.

### Additional Payload

ARCs can include additional payload according to users’ requirements, e.g. presentation, reading material, or manuscripts. While these files can be placed anywhere in the ARC, it is strongly advised to organize these in additional subdirectories. 
Especially for the storage of protocols, it is RECOMMENDED to place protocols (assay SOP) in text form with the corresponding assay in /assays/<assay_name>/protocol/<protocol_name>. 

Note:

- All data missing proper anotation (e.g. assays, workflows, runs, or externals ) is considered additional payload independant of its location within the ARC. 

### Top-level Metadata and Workflow Description

*Top-level metadata and workflow description* tie together the elements of an ARC in the contexts of investigation and associated studies (in the ISA definition), captured in the files `isa.investigation.xlsx` in [ISA-XLSX format](#isa-xlsx-format), which MUST be present. Optionally, study-level metadata MAY be present in `isa.studies.xlsx`. Furthermore, top-level reproducibility information MUST be provided in the CWL `arc.cwl`, which also MUST exist.

#### Investigation and Study Metadata

ARC root directory is identifiable by the presence of the `isa.investigation.xlsx` investigation file in XLSX format following the ISA Model at investigation level. It contains top-level information about the investigation and MUST link all assays and studies within an ARC. Study and assay objects are registered and grouped with an investigation to record other metadata within the relevant contexts. The study file is optional and can be used to group assays into studies within one investigation. Multiple studies MUST be stored using one worksheet per study in \isa.studies.xlsx in the root of the ARC. The study-level SHOULD define ´Factors´ of a study and also MAY contain overlapping information also to be found in all assays grouped by the study.

#### Top-Level Run Description

The file `arc.cwl` MUST exist at the root directory of each ARC. It describes which runs are executed (and specifically, their ordering) to produce the computational results contained within the ARC.

`arc.cwl` MUST be a CWL v1.2 workflow description and adhere to the same requirements as [run descriptions](#run-description). In particular, references to assay data files, external data, nested workflows MUST use relative paths. An optional file `arc.yml` MAY be provided to specify input parameters. 

## Shareable and Publishable ARCs
ARCs can be shared in any state. They are considered *publishable* (e.g. for the purpose of minting a DOI) when fulfilling the following conditions:

- Investigation-level metadata contains minimally the following terms:

  - Investigation Identifier 
  - Investigation Title 
  - Investigation Description 
  - INVESTIGATION CONTACTS and/or [Comment]ORCID-ID of the PI(s)

- The ARC MUST NOT be *empty*: it MUST contain minimally a single assay or a single workflow.

Notes: 
  - The attribute *publishable* does not imply that data and metadata contained in an ARC are suitable for publication in a specific outlet (e.g. PRIDE, GEO, EBI). While it may be straightforward to convert the ARC schema into one required by specific publishers or repositories, additional metadata requirements may be enforced during conversion. These are intentionally not captured in this specification.
  - Minimal administrative metadata ensure compliance with DataCite for DOI creation
  - (TODO: provisions to enable reproducibility - what do we want to require here?)

## Mechanism for quality control of ARCs 

ARCs are supposed to be living research objects and as such are at no point in time complete. Nevertheless, a mechanism to report the current state and quality of an ARC is indispensable. Therefore, ARCs will be scored according to the amount of metadata information available, the quality of data and metadata (this metric will be established in the next version), manual curation and review, and the re-use of ARCs by other researcher measured by physical includes of the data and referencing.

To foster FAIRification, badges will be earned by reaching certain scores for a transparent review process.  
 
## Best Practices

In the next section we provide you with Best Practices to make the use of an ARC even more efficient and valuable for open science. 

#### Community specific data formats 
It is recommend to use of community specific data formats covering most common measurement techniques. 
Using the following recommended formats will ensure improoved accessability and findability:   
- mzML (raw data metabolomics and proteomics) 
- mzTAB (analysis data metabolomics and proteomics)
- Fastq.gz (compressed NGS Short Read Sequencing, Long Read Sequencing) 
- fastq (NGS Short Read Sequencing, Long Read Sequencing) 
- BAM (??)
- SAM (??)

Notes: 
  - In case of storing vendor-spesific data within an ARC, it is strongly encuraged to accompany them by the corresponding open formats or provide a workflow for convertion or processing. (TODO: Hm, I would consider that as a task for the longterm access squad/technology watch!?)

#### Compression and Encryption 

Compression is preferrable to save on disk space and speed up data transfers but not required. Without compression workflows are simpler as often no transparent compression and decompression is available. Uncompressed files are usually easier to index and better searchable. 

Encryption is not advised (but could be an option to share sensitive data in an otherwise open ARC).

#### Directory and File Naming Conventions 

Required files defined in the ARC structure need to be named accordingly. Files and folders specified < > can be named freely. 
As the ARC might be used by different persons and in different workflow contexts, we recommend a concise filename without blanks and special characters. A good choice is to stick to small and capital letters without umlauts and similar special characters. Numbers, hyphen, and underscores are suitable as well. Modern working environments can handle blanks in filenames but might confuse automatically run scripts and thus should be avoided. Depending on the intended amount of people the ARC is shared with, certain information might prove useful to provide a fast overview in human readable form in the filename, e.g. by providing abbreviations of the project, sub project, person creating or working on a particular data set. Date and time information might be encoded as well if it provides a better ordering or information for the particular purpose. 


 ## Appendix: Conversion of ARCs to RO Crates

*(would be great if we could include this)*
  

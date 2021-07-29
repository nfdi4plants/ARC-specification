# Annotated Research Context Specification, v1-rfc 

Please provide feedback via Github issues or a pull request.

**Github repository:**  https://github.com/nfdi4plants/ARC-specfication

This specification is Copyright 2021 by [DataPLANT – Nationale Forschungsdateninfrastruktur](nfdi4plants.de). 

Licensed under the Creative Commons License CC BY, Version 4.0; you may not use this file except in compliance with the License. You may obtain a copy of the License at https://creativecommons.org/about/cclicenses/. This license allows re-users to distribute, remix, adapt, and build upon the material in any medium or format, so long as attribution is given to the creator. The license allows for commercial use. Credit must be given to the creator. 

**Table of Contents**
- [Introduction](#introduction)
  - [Extensions](#extensions)
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

This document describes a specification for a standardized way of creating a working environment and packaging file-based research data and necessary additional contextual information for working, collaboration, preservation, reproduction, re-use, and archiving as well as distribution. This organization unit is named *Annotated Research Context* (ARC) and is designed to be both human and machine actionable. 

ARCs are digital objects that fulfill all FAIR principles and are therefore referred to as FAIR Digital Objects (FDO).

An ARC is intended to capture research data, analysis and metadata and their evolution in scenarios ranging from single experimental setups to complex experimental designs in plant biological research. Its design intent is to assist researchers in meeting FAIR requirements, and also minimize the workload for doing so. ARCs are self-contained and include assay/measurement data, workflow, and computation results, accompanied by metadata and history, in one package. Toward this, ARCs combine existing standards, leveraging the properties of the [ISA metadata model](https://isa-specs.readthedocs.io/en/latest/isamodel.html), for administrative and experimental metadata and the [Common Workflow Language (CWL)](https://www.commonwl.org) for representing processing specification.

ARCs are furthermore designed to enable straightforward conversion to other types of research data archives, such as e.g. [Research Object Crates](https://www.researchobject.org/ro-crate/), to facilitate straightforward operation with widely used archives (e.g. PRIDE, GEO, ENA etc.). Therefore, ARCs aggregate administrative, experimental, and workflow meta data within a common structure.

This specification is intended as a practical guide for software authors to create tools for generating and consuming research data packages.


The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, MAY, and OPTIONAL in this document are to be interpreted as described in [RFC 2119](https://datatracker.ietf.org/doc/html/rfc2119).  This specification is  based on the [ISA model](https://isa-specs.readthedocs.io/en/latest/isamodel.html) and the [Common Workflow Specification (v1.2)](https://www.commonwl.org/v1.2/).

### Extensions

The ARC specification can be extended in a backwards compatible way and will evolve over time. This is accomplished through community-driven ARC discussion forum and pull request mechanism.

All changes that are not backwards compatible with the current ARC specification will be implemented in ARCs 2.0

## ARC Structure and Content

ARCs are based on a strict separation of data and metadata content into raw data (assays), externals, computation results (runs) and computational workflows (workflows) generating the latter. The scope or granularity of an ARC aligns with the necessities of individual projects or large experimental setups. 

### High-Level Schema

Logically, each ARC is a directory containing the following elements: 

- *Assays* correspond to analytical measurements (in the interpretation of the ISA model) and are treated as immutable data. Each assay is a collection of files, together with a corresponding metadata file, stored in a subdirectory of the top-level subdirectory `assays`. Assay-level metadata is stored in [ISA-XLSX](#isa-xlsx-format) format in a file `isa.assay.xlsx`, which MUST exist for each assay. Further details on `isa.assay.xlsx` are specified [below](#assay-data-and-metadata). Assay data files MUST be placed in a `dataset` subdirectory.

- *Workflows* represent data analysis routines (in the sense of CWL tools and workflows) and are a collection of files, together with a corresponding CWL description, stored in a single directory under the top-level `workflows` subdirectory. A per-workflow executable CWL description is stored in `workflow.cwl`, which MUST exist for all ARC workflows. Further details on workflow descriptions are given [below](#workflow-description).

- *Runs* capture data products (i.e., results of computational analysis) derived from assays, other runs, or external data using workflows (located in the aforementioned *Workflows* directory). Each run is a collection of files, stored in the top-level `runs` subdirectory. It MUST be accompanied by a per-run CWL workflow description, stored in `<run_name>.cwl` and further described [below](#run-description).

- *Externals* are external data (e.g., knowledge files) that need to be included and cannot be referenced due to external limitations. Metadata information SHOULD be stored according to the ISA model and CWL in case of workflow information; see [below](#external-data) for details.

- *Top-level metadata and workflow description* tie together the elements of an ARC in the contexts of investigation and associated studies (in the ISA definition), captured in the files `isa.investigation.xlsx` in [ISA-XLSX format](#isa-xlsx-format), which MUST be present. Optionally, study-level metadata MAY be present in `isa.studies.xlsx`. Furthermore, top-level reproducibility information MUST be provided in the CWL `arc.cwl`, which also MUST exist.

All other files contained in an ARC (e.g., a `README.txt`, a pre-print PDFs, additional annotation files, etc.) are referred to as *additional payload*, and MAY be located anywhere within the ARC structure. However, an ARC MUST be [reproducible](#reproducible-arcs) and [publishable](#shareable-and-publishable-arcs) even if these files are deleted. Further considerations on additional payload are described [below](#additional-payload).

Note: 

- Subdirectories and other files in the top-level `assays`, `workflows`, `runs`, and `externals` directories are viewed as additional payload unless they are accompanied by the corresponding mandatory description (`isa.assay.xlsx`, `workflow.cwl`, `run.cwl`, `isa.external.xlsx`) specified below. This is intended to allow gradual migration from existing data storage schemes to the ARC schema. For example, *data files* for an assay may be stored in a subdirectory of `assays/`, but are only identified as an assay of the ARC if metadata is present and complete, including a reference from top-level metadata.

### Example ARC structure
``` 
<top-level directory> 
|   isa.investigation.xlsx 
|   isa.studies.xlsx
|   arc.cwl 
|   arc.yml [optional]            
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
        |    run.yml [optional]           
\--- externals 
        |    [ knowledge files ] # external reference  
        |    isa.externals.xlsx           
``` 

### ARC Representation

ARCs are Git repositories, as defined and supported by the [Git C implementation](https://git-scm.org) (version 2.26 or newer) with [Git-LFS extension](https://git-lfs.github.com) (version 2.12.0), or fully compatible implementations. 

ARC terminology implicitly borrows from Git and Git-LFS terminology. For example, an ARC commit is simply a Git commit, and the ARC history is the repository history. Furthermore, an ARC can contain multiple branches, etc.

Tree objects (resp. directories) and blobs (i.e., files) of all branch heads in the repository MUST adhere to the [ARC schema](#arc-structure-and-content). ARCs allow all typical Git operations (e.g. clone, branch).

All representation suitable for Git-LFS repositories are also valid representations of ARCs. This includes both bare repositories (without a checked out working copy) and non-bare repositories (i.e. a `.git` directory with one or more attached working copies). In particular, it is possible and intended to maintain ARCs on local user filesystems and via Git repository hosting services. No requirements are made for state and contents of working copies.

Notes:

- Archival representation (e.g. `.zip` or `.tar.gz`) are valid ARC representations if archives are created to preserve file attributes, i.e. if unarchiving preserves Git interoperability. Furthermore, Git's [bundle mechanism](https://git-scm.com/docs/git-bundle) can be used to create archives of complete ARCs or individual branches. For archiving purposes, `git bundle create --all` or an equivalent should be used.

- Elements of an ARC are implicitly content-addressable using standard Git mechanisms via SHA1 hashes.

- Removing the `.git` top-level subdirectory (and thereby all provenance information captured within the Git history) invalidates an ARC.

### ISA-XLSX Format

ISA-XLSX follows the ISA model specification (v1.0) saved in a XLSX format. The XLSX format uses the SpreadsheetML markup language and schema to represent a spreadsheet document. Conceptually, using the terminology of the Spreadsheet ML specification [ISO/IEC 29500-1](https://www.loc.gov/preservation/digital/formats/fdd/fdd000398.shtml#:~:text=The%20XLSX%20format%20uses%20the,a%20rectangular%20grid%20of%20cells.), the document comprises one or more worksheets in a workbook. Every worksheet MUST contain one table object storing the metadata. Comments or auxillary information MAY be stored alongside with table objects in a worksheet.

### Assay Data and Metadata

All measurement data sets are considered as assays and are considered immutable input data. Assay data MUST be placed into a unique subdirectory of the top-level `assays` folder. All ISA metadata specific to a single assay MUST be annotated in the file `isa.assay.xlsx` at the root of the assay's subdirectory. This workbook MUST contain a single assay that can be organized in one or many worksheets. Worksheets MUST be named uniquely within the same workbook. A worksheet named `assay` MUST store the STUDY ASSAYS section defined on investigation-level of the ISA model and is not required in the `isa.investigation.xlsx `. These include the terms `Study Assay Measurement Type`, `Study Assay Measurement Type Term Accession Number`, `Study Assay Measurement Type Term Source REF`, `Study Assay Technology Type`, `Study Assay Technology Type Term Accession Number`, `Study Assay Technology Type Term Source REF`, and `Study Assay Technology Platform`. 
Additional worksheets MUST contain a table object with fields organized on a per-row basis. The first row of the table object MUST be used for column headers. A `Source` MUST be indicated with the column heading `Source Name`. Every table object MUST define at least one source per row. A `Sample` MUST be indicated with the column heading `Sample Name`. The source sample relation MUST follow a unique path in a directed acyclic graph, but MAY be distributed across different worksheets.

<table>

<tr><td>

|   |   |
|-|-|
| Study Assay Measurement Type | "value" |
| Study Assay Measurement Type Term Accession Number | "value" |
| Study Assay Measurement Type Term Source REF | "value" |
| ... | ... |

</td><td>

| Source Name | building block* | Sample Name |
|-|-|-|
mrv1 | descriptorA | s1 |
mrv2 | descriptorB | s2 |
_

</td><td>

| Source Name | building block* | Sample Name |
|-|-|-|
s1 | descriptorC | n1 |
s1 | descriptorD | n2 |
s2 | descriptorD | n3 |

</td></tr>
    <tr>
        <th style="text-align:center">[*assay*]</th>
        <th style="text-align:center">[*worksheet1*]</th>
        <th style="text-align:center">[*worksheet2*]</th>
    </tr>
</table>


Notes:

- There are no requirements on specific assay-level metadata per formal ARC definition. Conversion of ARCs into other repository or archival format (e.g. PRIDE, GEO, ENA etc.) may however mandate the presence of specific terms required in the destination format.

- To ensure reusability of assays, it is strongly RECOMMENDED to include necessary metadata mandated by typical metadata schemes necessary for reproduction. This process is facilitated by the use of templates that can be found [here](https://github.com/nfdi4plants/SWATE_templates).

- It is RECOMMENDED to order worksheets according to the source sample relation for readability.

- It is RECOMMENDED to adopt the structure outlined [below](#best-practices) to organize assay data files and other supporting information.

- An implementation that ensures assay annotation consistent with these requirements is provided by the [SWATE tool](https://github.com/nfdi4plants/Swate).

- While assays can in principle contain arbitrary data formats, it is highly RECOMMENDED to use community-supported, open formats (see [Best Practices](#best-practices)).

### Workflow Description

*Workflows* in ARCs are computational steps that are used in computational analysis of an ARC's assays and other data transformation to generate a [run result](#run-description). Typical examples include data cleaning and pre-processing, computational analysis, or visualization. Workflows are used and combined to generate [run results](#run-description), and allow re-use of processing steps across multiple [run results](#run-description).

Workflow execution and metadata MUST be described using the [Common Workflow Language](https://www.commonwl.org/) (CWL), [v1.2](https://www.commonwl.org/v1.2/) or higher, in a file `workflow.cwl`, which MUST be placed in the subdirectory containing all files specific to this workflow under the top-level `workflows` directory. This file MUST contain either of:

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

- It is expected that run descriptions are authored semi-automatically, e.g. using the [arcCommander](https://github.com/nfdi4plants/arcCommander) tool.

- It is strongly encouraged to include author and contributor metadata in run descriptions as [CWL metadata](https://www.commonwl.org/user_guide/17-metadata/index.html).

### External Data

External data refers to data that is neither originating within the investigation/study scope of the ARC nor can be referenced externally, but is required to ensure reproducability. Examples include early use of ontologies, mapping files, gene information, etc.. All correspondig data MUST be placed in the ARC's top-level `externals` directory.

The union of external data forms a *virtual* assay; as such, it MUST adhere to the metadata requirements of assays and hence MUST contain, for each file, annotation in a file `isa.external.xlsx`, located under the top-level `externals` directory.

Note:

- Each external data file can be interpreted as a virtual sample in the *externals* assay. Due to the conceptual difference to the immutable measurements represented by the assays in `assays`, external files are stored in a different location to ensure that this distinction is explict.

### Additional Payload

ARCs can include additional payload according to user requirements, e.g. presentations, reading material, or manuscripts. While these files can be placed anywhere in the ARC, it is strongly advised to organize these in additional subdirectories. 
Especially for the storage of protocols, it is RECOMMENDED to place protocols (assay SOPs) in text form with the corresponding assay in /assays/<assay_name>/protocol/<protocol_name>. 

Note:

- All data missing proper annotation (e.g. assays, workflows, runs, or externals) is considered additional payload independent of its location within the ARC. 

### Top-level Metadata and Workflow Description

*Top-level metadata and workflow description* tie together the elements of an ARC in the contexts of investigation and associated studies (in the ISA definition), captured in the files `isa.investigation.xlsx` in [ISA-XLSX format](#isa-xlsx-format), which MUST be present. Optionally, study-level metadata MAY be present in `isa.studies.xlsx`. Furthermore, top-level reproducibility information MUST be provided in the CWL `arc.cwl`, which also MUST exist.

#### Investigation and Study Metadata

The ARC root directory is identifiable by the presence of the `isa.investigation.xlsx` investigation file in XLSX format following the ISA Model at investigation level. It contains top-level information about the investigation and MUST link all assays and studies within an ARC. Study and assay objects are registered and grouped with an investigation to record other metadata within the relevant contexts. The study file is optional and can be used to group assays into studies within one investigation. Multiple studies MUST be stored using one worksheet per study in \isa.studies.xlsx in the root of the ARC. The study-level SHOULD define ´Factors´ of a study and also MAY contain overlapping information also to be found in all assays grouped by the study.

#### Top-Level Run Description

The file `arc.cwl` MUST exist at the root directory of each ARC. It describes which runs are executed (and specifically, their order) to produce the computational results contained within the ARC.

`arc.cwl` MUST be a CWL v1.2 workflow description and adhere to the same requirements as [run descriptions](#run-description). In particular, references to assay data files, external data, nested workflows MUST use relative paths. An optional file `arc.yml` MAY be provided to specify input parameters. 

## Shareable and Publishable ARCs
ARCs can be shared in any state. They are considered *publishable* (e.g. for the purpose of minting a DOI) when fulfilling the following conditions:

- Investigation-level (administrative) metadata contains minimally the following terms:

  - Investigation Identifier 
  - Investigation Title 
  - Investigation Description 
  - INVESTIGATION CONTACTS section and/or [Comment]ORCID of the PI(s) 
      - Investigation Person Last Name
      - Investigation Person First Name
      - Investigation Person Mid Initials
      - Investigation Person Email      
      - Investigation Person Affiliation

- The ARC MUST NOT be *empty*: it MUST contain minimally a single assay or a single workflow.

-  ARC MUST be [reproducible](#reproducible-arcs) 

Notes: 
  - The attribute *publishable* does not imply that data and metadata contained in an ARC are suitable for publication in a specific outlet (e.g. PRIDE, GEO, EBI) nor that metadata is complete or enables reusability of data. While it may be straightforward to convert the ARC schema into one required by specific publishers or repositories, additional metadata requirements may be enforced during conversion. These are intentionally not captured in this specification.

  - It might be worth to notice that experimental metadata necessary for publication in a specific outlet is encoded by templates that can be found [here](https://github.com/nfdi4plants/SWATE_templates).

  - Minimal administrative metadata ensure compliance with DataCite for DOI creation

### Reproducible ARCs

Reproducability of ARCs referes mainly to its *Runs*. With an ARC it MUST be possible to reproduce the run data. Therefore, necessary software MUST be available in *Workflows*. In the case of non-deterministic software the run results should represent typical examples.


## Mechanism for Quality Control of ARCs 

ARCs are supposed to be living research objects and as such are at no point in time complete. Nevertheless, a mechanism to report the current state and quality of an ARC is indispensable. Therefore, ARCs will be scored according to the amount of metadata information available (specifically with established minimal metadata standards such as MinSeqE, MIAPPE, etc.), the quality of data and metadata (this metric will be established in the next version), manual curation and review, and the re-use of ARCs by other researchers measured by physical includes of the data and referencing.

To foster FAIRification, badges will be earned by reaching certain scores for a transparent review process.  
 
## Best Practices

In the next section we provide you with Best Practices to make the use of an ARC even more efficient and valuable for open science. 

#### Community Specific Data Formats 
It is recommend to use community specific data formats covering most common measurement techniques. 
Using the following recommended formats will ensure improved accessibility and findability:   
- mzML (raw data metabolomics and proteomics) 
- mzTAB (analysis data metabolomics and proteomics)
- Fastq.gz (compressed NGS Short Read Sequencing, Long Read Sequencing) 
- fastq (NGS Short Read Sequencing, Long Read Sequencing) 
- SAM (Sequence Alignment/Map format)
- BAM (Compressed binary version of a SAM file that is used to represent aligned sequences)

Notes: 
  - In case of storing vendor-specific data within an ARC, it is strongly encouraged to accompany them by the corresponding open formats or provide a workflow for conversion or processing where this is possible and considered standard.

#### Compression and Encryption 

Compression is preferable to save disk space and speed up data transfers but not required. Without compression workflows are simpler as often no transparent compression and decompression is available. Uncompressed files are usually easier to index and better searchable. 

Encryption is not advised (but could be an option to share sensitive data in an otherwise open ARC).

#### Directory and File Naming Conventions 

Required files defined in the ARC structure need to be named accordingly. Files and folders specified < > can be named freely. 
As the ARC might be used by different persons and in different workflow contexts, we recommend concise filenames without blanks and special characters. Therefore, filenames SHOULD stick to small and capital letters without umlauts, accented and similar special characters. Numbers, hyphens, and underscores are suitable as well. Modern working environments can handle blanks in filenames but might confuse automatically run scripts and thus SHOULD be avoided. Depending on the intended amount of people the ARC is shared with, certain information might prove useful to provide a fast overview in human readable form in the filename, e.g. by providing abbreviations of the project, sub project, person creating or working on a particular dataset. Date and time information might be encoded as well if it provides a better ordering or information for the particular purpose.


## Appendix: Conversion of ARCs to RO Crates

[Research Object Crate](https://www.researchobject.org/ro-crate/) is a lightweight approach, based on schema.org, to packaging research data together with their metadata. An ARC can be augmented into an RO Crate by placing a metadata file `ro-crate-metadata.json` into the top-level ARC folder, which must conform to the [RO Crate specification](https://www.researchobject.org/ro-crate/1.1/). The ARC root folder is then simultaneously the RO-Crate Root. It is recommended to adhere to the following conventions when creating this file:

- The root data entity description are taken from the "Investigation Description" term in `isa.investigation.xlsx`.
- The root data entity authors are taken from the "Investigation Contacts" in `isa.investigation.xlsx`:
- The root data entity citations are copied from the "Investigation Publications" section in `isa.investigation.xlsx`.
- Per assay linked from `isa.investigation.xlsx`, one Dataset entity is provided in `ro-crate-metadata.json`. The Dataset id corresponds to the relative path of the assay ISA file under `assays/`, e.g. "sample-data/assay.isa.xlsx". Other metadata is taken from the corresponding terms in the corresponding `assay.isa.xlsx`.
- The root data entity contains an child Dataset entity named `assays`, which lists the ids of all assays linked from `isa.investigation.xlsx`.

It is expected that future versions of this specification will provide additional guidance on a comprehensive conversion of ARC metadata into RO-Crate metadata.

   

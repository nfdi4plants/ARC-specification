# Annotated Research Context Specification, v1-rfc 

Please provide feedback via Github issues or a pull request.

**Editors:**
  - Timo Mühlhaus &lt;muehlhaus@bio.uni-kl.de&gt;
  - Dirk von Suchodoletz &lt;dirk.von.suchodoletz@rz.uni-freiburg.de&gt;
  - Christoph Garth &lt;garth@cs.uni-kl.de&gt;

**Github repository:**  
  https://github.com/nfdi4plants/specs

This specification is Copyright 2021 by [DataPLANT – Nationale Forschungsdateninfrastruktur](nfdi4plants.de). 

Licensed under the Creative Commons License CC BY, Version 4.0; you may not use this file except in compliance with the License. You may obtain a copy of the License at https://creativecommons.org/about/cclicenses/. This license allows re-users to distribute, remix, adapt, and build upon the material in any medium or format, so long as attribution is given to the creator. The license allows for commercial use. Credit must be given to the creator. 

- [Annotated Research Context Specification, v1-rfc](#annotated-research-context-specification-v1-rfc)
  - [Introduction](#introduction)
  - [ARC Structure and Content](#arc-structure-and-content)
    - [High-Level Schema](#high-level-schema)
    - [Directory and File Naming Conventions](#directory-and-file-naming-conventions)
    - [Example ARC structure](#example-arc-structure)
    - [ARC representation](#arc-representation)
    - [Assay Metadata](#assay-metadata)
    - [Workflow Description](#workflow-description)
    - [Run Description](#run-description)
    - [External Data](#external-data)
    - [Top-level Metadata and Workflow](#top-level-metadata-and-workflow)
      - [Investigation and Study Metadata](#investigation-and-study-metadata)
      - [Reproducibility Description](#reproducibility-description)
    - [Auxiliary Payload](#auxiliary-payload)
      - [Community specific data formats](#community-specific-data-formats)
      - [Compression and Encryption](#compression-and-encryption)
    - [ISA-XLSX Format](#isa-xlsx-format)
  - [Shareable and Publishable ARCs](#shareable-and-publishable-arcs)
  - [ARC Provenance](#arc-provenance)
  - [Conversion of ARCs to RO Crates](#conversion-of-arcs-to-ro-crates)
  - [Mechanism for quality control of ARCs](#mechanism-for-quality-control-of-arcs)
  - [TODO: Open Questions](#todo-open-questions)

## Introduction

This document intends to develop and describe a specification for a standardized way of creating a working environment and packaging file-based research data and necessary additional contextual information for working, collaboration, preservation, reproduction, re-use, and archiving as well as distribution.

This document specifies a data storage schema and representation, named *Annotated Research Context*(ARC), for organizing file-based data and processing workflows with associated metadata in both human and machine-readable formats. ARCs combine existing standards, leveraging the properties of the investigation-study-assay ISA model, for metadata and the Common Workflow Language (CWL) for representing processing specification. While aiming to be compatible with similar standards and schemas, ARCs are specifically oriented towards common practices in experimental plant biology.

An ARC is intended to capture research data, analysis and metadata and their evolution in scenarios ranging from single experimental setups to complete research cycles in plant biological research. Its design intent is to not only assist researchers in meeting FAIR requirements, but to also minimize the workload for doing so. ARCs are self-contained and include assay/measurement data, workflow, and computation results, accompanied by metadata and history, in one package.  

This specification is intended as a practical guide for software authors to create tools for generating and consuming research data packages.

The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, MAY, and OPTIONAL in this document are to be interpreted as described in [RFC 2119](https://datatracker.ietf.org/doc/html/rfc2119).  This specification is furthermore based on the [ISA model](https://isa-specs.readthedocs.io/en/latest/isamodel.html) and the [Common Workflow Specification (v1.2)](https://www.commonwl.org/v1.2/).

## ARC Structure and Content

The ARC structure aims for a strict separation of data and metadata content into raw data (assays), externals, computation results (runs) and computational workflows (workflows) generating the latter. The scope or granularity of an ARC aligns with the necessities of the individual projects or experimental setups covered by the respective ARC. 

### High-Level Schema

Logically, each ARC is a directory containing the following elements: 

- *Assays* correspond to analytical measurements (in the interpretation of the ISA model) and are treated as immutable data. Each assay is a collection of files, together with a corresponding metadata file, stored in a directory in the top-level subdirectory `assays`. Assay-level metadata is stored in [ISA-XLSX](##isa-xlsx) format in a file `isa.assay.xlsx`, which MUST exist for each assay. Further details on `isa.assay.xlsx` are specified [below](#assay-metadata).

- *Workflows* represent data analysis routines (in the sense of CWL tools and workflows) and are a collection of files, together with a corresponding CWL description, stored in a single directory under the top-level `workflows` subdirectory. A per-workflow executable CWL description is stored in `workflow.cwl`, which MUST exist for all ARC workflows. Further details on workflow descriptions are given [below](#workflow-descriptions).

- *Runs* capture data products (i.e., results of computational analysis) derived from assays, other runs, or external data using workflows. Each run is a collection of files, stored in the top-level `runs` subdirectory. It MUST be accompanied by a per-run CWL workflow description, stored in `<run_name>.cwl` and further described [below](#run-descriptions).

- *Externals* are external data (e.g., knowledge files) that need to be included and cannot be referenced due to external limitations. Metadata information SHOULD be stored according to the ISA model and CWL in case of workflow information; see [below](#external-data-annotation) for details.

- *Top-level metadata and workflow* ties together the elements of an ARC in the contexts of investigation and associated studies (in the ISA definition), captured in the files `isa.investigation.xlsx` and `isa.studies.<study_name>.xlsx` in [ISA-XLSX format](#isa-xlsx), which MUST be present. Furthermore, top-level reproducibility information MUST be provided in the CWL `arc.cwl`, which also MUST exist.

All other files contained in an ARC (e.g, a `README.txt`, a pre-print PDFs, additional annotation files, etc.) are referred to as *additional payload*, and can be located anywhere within the ARC structure. However, an ARC MUST be [reproducible](#reproducible-arcs) and [complete](#complete-arcs) even if these files are deleted. Further considerations on additional payload are described [below](#additional-payload).

Note: Subdirectories and other files in the top-level `assays`, `workflows`, `runs`, and `externals` directories are viewed as additional payload unless they are accompanied by the corresponding mandatory description (`isa.assay.xlsx`, `workflow.cwl`, `run.cwl`, `isa.external.xlsx`) specified below. This is intended to allow gradual migration from existing data storage schemes to the ARC schema. For example, *data files* for an assay can be stored in a subdirectory of `assays/`, but are only identified as an assay of the ARC if metadata is present and complete, including a reference from top-level metadata.

### Directory and File Naming Conventions 

*(do we really need this?)*

Required files defined in the ARC structure need to be named accordingly. Files and folders specified < > can be named freely. 

As the ARC might be used by different persons and in different workflow contexts, we recommend a concise filename without blanks and special characters. A good choice is to stick to small and capital letters without umlauts and similar special characters. Numbers, hyphen, and underscores are suitable as well. Modern working environments can handle blanks in filenames but might confuse automatically run scripts and thus should be avoided. Depending on the intended amount of people the ARC is shared with, certain information might prove useful to provide a fast overview in human readable form in the filename, e.g. by providing abbreviations of the project, sub project, person creating or working on a particular data set. Date and time information might be encoded as well if it provides a better ordering or information for the particular purpose. 

### Example ARC structure
``` 
<top-level directory> 
|   isa.investigation.xlsx 
|   isa.studies.study1.xlsx
|   isa.studies.study2.xlsx
|   arc.cwl 
|   arc.yml            
\--- assays
    \--- <assay_name> 
            |    isa.assay.xlsx  
            \--- dataset 
            \--- protocol 
\--- workflows  
    \--- <workflow_name> 
            | workflow.cwl 
            | docker-compose.yml (optional) 
\--- runs   
    \--- <run_name> 
        |    [files;...] (different result files) 
        |    run.cwl 
        |    run.yml            
\--- externals 
        |    [ knowledge files ] # external reference  
        |    isa.xlsx           
``` 

### ARC representation

ARCs are a Git repositories, as defined and supported by the [Git C implementation](https://git-scm.org) (version XX or newer) with [Git-LFS extension](https://git-lfs.github.com) (version 2.12.0), or fully compatible implementations. 

ARC terminology implicitly borrows from Git and Git-LFS terminology. For example, an ARC commit is simply a Git commit, and the ARC history is the repository history. Furthermore, an ARC can contain multiple branches, etc.

Tree objects (resp. directories) and blobs (i.e., files) of all branch heads in the repository MUST adhere to the [ARC schema](#arc-structure-and-contents-schema). ARCs allow all typical Git operations (e.g. clone, branch) etc.

All representation suitable for Git[-LFS] repositories are also a valid representations of ARCs. This includes both bare repositories (without a checked out working copy) and non-bare repositories (i.e. a `.git` directory with one or more attached working copies). In particular, it is possible and intended to maintain ARCs on local user filesystems and via Git repository hosting services. No requirements are made of the state and contents of working copies.

### Assay Metadata

*(not cleaned up / merged)*

All measurement data sets are considered as assays and are consider immutable input data. Assays SHOULD be placed into the assays folder separated by individually named folders. Each record within assays MUST be placed within a folder whose name indicates a basic reference to the data it contains. In the folder 
 \assays\<assay_name> 
, an assay groups descriptions of sample provenance (e.g. experimental processing) following the ISA assay Model, additional protocol material and the dataset itself. If an assay exists, the measurement data MUST be placed in the folder  
\assays\<assay_name>\dataset  
and are stored here. Corresponding to this dataset assay-related metadata MUST be stored in the ISA assay Model file 
\assays\<assay_name>\isa.assay.xlsx 
and include descriptions of the measurement type and technology used, and sample characteristics and parameters according to what study protocols are applied (see isa_specification).  
Additionally, it is RECOMMENDED to place the corresponding protocol (assay SOP) in text form under:  
\assays\<assay_name>\protocols 
Important note:  It should be noted that all assay related information stored in the ISA investigation (e.g., measurement type and technology) MUST be placed in an additional worksheet in isa.assay.xlsx. Here redundancy is necessary to ensure independent reusability of assays in different independent ARCs. 

### Workflow Description

*Workflows* in ARCs embody one or more computational steps that are used in computational analysis of an ARC's assays and other data to generate a [run result](#run-description). Typical examples include data cleaning and pre-processing, computational analysis, or visualization.

...

All programmatic and computational components of an ARC MUST be individually sorted into  
    \workflows\<workflow_name> 
in the form of application or code and their environment including packages and other includes. A top-level Dockerfile in which all code/workflow should be executable is RECOMMENDED. Metadata to describe the workflow MUST be provided in CWL-abstract. To ensure reusability the CWL-abstract gives metadata in form of a tool description and does not include concrete parameters leading to actual results.  
\workflows\<workflow_name>\workflow.cwl 
The parameter necessary for workflow execution that are input, and output specific MUST be specified in runs.

### Run Description

*(not cleaned up / merged)*

Runs are all artefacts that result from some computation within an ARC. The results (e.g. plots, tables, etc. ) of your run aka. workflow execution or analysis MUST reside in  
\runs\<runResult_name> 
These results can be either generated by the application of a workflow on assay data and/or previous runs as well as standalone computation (e.g. simulations). The link between the respective input and the resulting run MUST be specified by the parameters in  
\runs\<runResult_name>.yml 
and the corresponding execution MUST be specified in  
\runs\<runResult_name>.cwl 
to produce run results accordingly. 

### External Data

*(not cleaned up / merged)*

In general, all information NEED to reside in an ARC or MUST be referenced and linked properly. However, there are scenarios where the proper referencing information is not possible (e.g. early use of ontologies, mapping files, gene information, … without proper version number). Externals is the place to snapshot and hard include (not just reference) this information. 
\externals\[e.g. mapman-ontology-301120.txt;...] 
Data in externals are treated as virtual samples (data sets) and therefore MUST be described according to the ISA assay model in  
\externals\isa.assay.xlsx 

### Top-level Metadata and Workflow

*(not cleaned up / merged)*

#### Investigation and Study Metadata

ARCs contain raw measurement data, externals, computation results and computational workflows in the respective sub-folders assays, workflows, runs and externals placed in the root (details see: ARC content categories).  
The name of the ARC root directory is not defined, but a root directory is identifiable by the presence of the investigation file: 
\isa.investigation.xlsx  

The investigation file (in XLSX format) contains top-level information about the investigation and links to studies and assays. An investigation is used to record metadata relating to the description of the investigation context and administrative metadata, such as the title and description of the investigation as well as about involved people and publications. 

Study and assay objects are registered and grouped with an Investigation to record other metadata within the relevant contexts. (https://isa-specs.readthedocs.io/en/latest/isamodel.html#investigation) 
The study file is optional and can be used to group assays into studies within one investigation. Multiple studies can be stored using one worksheet per study: 
    \isa.studies.xlsx  
In contrast to the original ISA specifications, only [factors] are included. Several studies may be related to a single investigation. Each study serves as a steppingstone for achieving the investigation aim (e.g. investigating salt tolerance in Arabidopsis) 


To (re)produce the run results corresponding to the workflows stored in an ARC, all workflows need to be registered within 
    \arc.cwl 
This allows to execute all computations defined in the workflow structure in order to (re)produce corresponding runs results using all necessary parameters defined in:  
    \arc.yml 

#### Reproducibility Description

*(about `arc.cwl`)*

### Auxiliary Payload

*(not cleaned up / merged)*

To allow re-using and reproduction all contained (meta)data NEEDs to be understood and properly interpretable. In general, the use of human and machine-readable formats is RECOMMENDED and strongly encouraged (details see: Community specific data formats). However, ARC payload files MUST be openly accessible. This is ensured if the file is accompanied by readable open formats (preferred), referencing a schema definition, or interpreting software stored under workflows.  

Everything not meeting these criteria is regarded as auxiliary payload and therefore is not strictly considered ARC content. This might result in an ‘empty’ ARC only containing auxiliary payload. 

Auxiliary payload MUST be ignored by any processing. Also, auxiliary payload might be restricted in size or retention depending on the repository for ARC sharing and publication.  

#### Community specific data formats 

List of preferred sequencing, metabolomics etc. file types. 
Standards like  
- mzML 
- mzTAB 
- Fastq.gz (compressed NGS Short Read Sequencing, Long Read Sequencing) 
- fastq (NGS Short Read Sequencing, Long Read Sequencing) 
- BAM 
- SAM 
are preferred as they can be used/computed directly ... 

#### Compression and Encryption 

*(this should not be included)*

Compression is preferrable to save on disk space and speed up data transfers but not required. Without compression workflows are simpler as often no transparent compression and decompression is available. Uncompressed files are usually easier to index and better searchable. 

Encryption is not advised (but could be an option to share sensitive data in an otherwise open ARC) .

### ISA-XLSX Format

The investigation file follows the vanilla ISA model specification saved in the XLSX format.

## Shareable and Publishable ARCs

*(not cleaned up / merged)*


An ARC exists in the continuum between shared and publishable state and is designed to continuously evolve. This reflects necessities of an ongoing research process and at the same time understands publication as a particular snapshot of this process in time. Accordingly, ARCs are not rigorously checked, but all parts involved in automatic workflows or processing MUST adhere the workflow dependent minimal requirements. However, at a certain point in time a data publication is intended and trigger by the user. This means that a defined fixed state or snapshot will be produced that can be permanently referenced on a public repository with a DOI assigned to the snapshot.  
Minimal publishable ARC MUST comply the following: 
isa.investigation.xlsx MUST contain all information required by DataCite (V??), that is: 
Project name 
Project ID or Grant ID 
(Short) project description 
Grant provider 
Program name (if applicable) 
Principal Investigator(s) (PI) 
ORCID-ID of the PI(s) 
Contact information of the responsible person of the data 
Creation date (and embargo periods, ...) 
ARC MUST not be empty. Note: auxiliary payload is not considered as ARC payload in a data publication.  
In order to publish individual assay or workflow to a technology-specific endpoint data repository (e.g. proteome exchange, GEO, metabolights, …) a minimal publishable ARC is required. Additionally, the requirements of the specific endpoint data repository are automatically backpropagated to the ARC. This means that certain fields in the ISA Model become mandatory due to demands of the end point repository. However, the annotation logic in the ARC will not change. 
The comfort of publishing can be increased by using the repository specific Swate templates from the beginning of the documentation process. The templates found under (https://github.com/nfdi4plants/SWATE_templates) help to avoid unnecessary workload pilling up at time of publication. 


A publishable ARC is an ARC that fulfills all package-level and assay-level metadata requirements and ensures that all files in all runs can be (re-)generated by executing the top-level workflow `arc.cwl` with (optional) parameters stated in `arc.yml`.

It is important to notice that requirements for a publishable ARC is dependent of the target requirements and therefore might be enforced during the publishing process. However, the ARC ensures a common representation of these information that can be shared across different publication targets or end point repositories.  

ARCs are not intended to be packaged directly; rather, this specification defines conversions of ARCs into other standard formats such as e.g. the Research Object Crate format (see Community-specific formats below). It is intended that a complete ARC contains all necessary metadata to enable such conversions. 

Additionally, ARCs can include auxiliary payload according to users’ requirements, e.g. presentation, reading material, or manuscripts. While these files can be placed anywhere in the ARC, it is strongly advised to organize these in additional subdirectories to avoid polluting the ARC root directory.  
Important note:  A shareable ARC does not need to reach any kind of completeness. Data entities in the ARC if existing MUST be in place according to the ARC structure. Other data entities will be regarded as auxiliary payload that can be submitted, but else ignored by any processing.  

## ARC Provenance

*(Is this section really needed?)*

The ARC is meant to exist in an evolving form for long periods, thus provenance information is crucial. It provides different sources of provenance information: 
Metadata from the isa.investigation.xlsx file 
Information produced by the workflow runs by individual tools 
History of the underlying versioning system (who changed what when) 
 
Version numbers, strict documentation of changes (what/by whom), a process to revert that, ... 
 
## Conversion of ARCs to RO Crates

*(would be great if we could include this)*

## Mechanism for quality control of ARCs 

*(Would push this to a future version of the ARC spec)*

ARCs are supposed to be living research objects and as such are at no point in time complete. Nevertheless, a mechanism to report the current state and quality of an ARC is indispensable. Therefore, ARCs will be scored according to the amount of metadata information available, the quality of data and metadata (this metric will be established in version 1.0), manual curation and review, and the re-use of ARCs by other researcher measured by physical includes of the data and referencing.

To foster FAIRification, badges will be earned by reaching certain scores for a transparent review process.  
 
 
## TODO: Open Questions
Stichpunkte aus dem operational Speaker-JF vom 25.05.2021: 
Thema Workflow: Einziges requirement ist ein CWL file 
ARC-CWL in Root-Verzeichnis, sodass Reihenfolge und Abhängigkeiten abgebildet werden können 
Requirements for ARC vs. Optional Features (Zweites nach Wenn-Dann-Logik) 
Restriktionen müssen auch durchgesetzt werden, deshalb eine Regulierung nicht über das Erzwingen einzelner Punkte sondern über das Scoring der ARCs geschehen (Blech, Silber, Gold, usw.). Stichwort: ArchivementAchievement-Baum 
*** 
 
It is possible to publish: 
Just all or partial raw data with complete annotation (Single data sets vs. Complete experiments of  a CRC, project, …) 
Workflow specifications and descriptions to be run by third party on their data (without any raw or processed data contained) 
Results data (with necessary run information for reproduction)  
Tools and information about them  
A complete ARC containing all relevant raw, derived data associated with workflows, tools and runs  
Comments on ARCs to be published on some well known public repository? 
For an ARC publication requiring a DOI certain further criteria are required 
Single branches either Assay or Workflow including metadata or processing 
Workflows executable  
Runs need to be reproduceable  
Assays need to contain annotation 
there will be different versions of publishable ARCs dependent on previously defined content 
publishable ARCs needs to be pure (pristine) -> Manually curated ( maybe freezing/bagit ignores comment files or additional material ) 
Additional criteria defined by repositories 
ARCs will be packed for publishing into a single file using BagIT or OCFL. Provenance information is gathered from various inputs and added. Checksums will be automatically generated for each contained file (part of BagIt specification).  
Certain metadata information is getting extracted from ISA metadata files (to be available for publishing e.g. on Invenio) 
Data publication granularity 
Generally, there is no size limit to a published ARC (repositories might impose single object size limits) 
 
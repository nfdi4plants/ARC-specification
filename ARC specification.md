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
    - [Example ARC structure](#example-arc-structure)
    - [ARC representation](#arc-representation)
    - [Assay Data and Metadata](#assay-data-and-metadata)
    - [Workflow Description](#workflow-description)
    - [Run Description](#run-description)
    - [External Data](#external-data)
    - [Top-level Metadata and Workflow Description](#top-level-metadata-and-workflow-description)
      - [Investigation and Study Metadata (-> Timo)](#investigation-and-study-metadata---timo)
      - [Workflow Description (-> Christoph)](#workflow-description---christoph)
      - [Compression and Encryption](#compression-and-encryption)
    - [ISA-XLSX Format (-> Timo)](#isa-xlsx-format---timo)
  - [Shareable and Publishable ARCs](#shareable-and-publishable-arcs)
  - [ARC Provenance](#arc-provenance)
  - [Conversion of ARCs to RO Crates](#conversion-of-arcs-to-ro-crates)
  - [Mechanism for quality control of ARCs](#mechanism-for-quality-control-of-arcs)
  - [Best Practices](#best-practices)
    - [Directory and File Naming Conventions](#directory-and-file-naming-conventions)
    - [Auxiliary Payload](#auxiliary-payload)
      - [Community specific data formats](#community-specific-data-formats)
  - [TODO: Open Questions](#todo-open-questions)

## Introduction

This document intends to develop and describe a specification for a standardized way of creating a working environment and packaging file-based research data and necessary additional contextual information for working, collaboration, preservation, reproduction, re-use, and archiving as well as distribution.

This document specifies a data storage schema and representation, named *Annotated Research Context*(ARC), for organizing file-based data and processing workflows with associated metadata in both human and machine-readable formats. ARCs combine existing standards, leveraging the properties of the investigation-study-assay ISA model, for metadata and the Common Workflow Language (CWL) for representing processing specification. While aiming to be compatible with similar standards and schemas, ARCs are specifically oriented towards common practices in experimental plant biology.

An ARC is intended to capture research data, analysis and metadata and their evolution in scenarios ranging from single experimental setups to complete research cycles in plant biological research. Its design intent is to not only assist researchers in meeting FAIR requirements, but to also minimize the workload for doing so. ARCs are self-contained and include assay/measurement data, workflow, and computation results, accompanied by metadata and history, in one package.  

** easy conversion to other formats / repositories ** (Christoph  )

This specification is intended as a practical guide for software authors to create tools for generating and consuming research data packages.

The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, MAY, and OPTIONAL in this document are to be interpreted as described in [RFC 2119](https://datatracker.ietf.org/doc/html/rfc2119).  This specification is furthermore based on the [ISA model](https://isa-specs.readthedocs.io/en/latest/isamodel.html) and the [Common Workflow Specification (v1.2)](https://www.commonwl.org/v1.2/).

## ARC Structure and Content

The ARC structure aims for a strict separation of data and metadata content into raw data (assays), externals, computation results (runs) and computational workflows (workflows) generating the latter. The scope or granularity of an ARC aligns with the necessities of the individual projects or experimental setups covered by the respective ARC. 

### High-Level Schema

Logically, each ARC is a directory containing the following elements: 

- *Assays* correspond to analytical measurements (in the interpretation of the ISA model) and are treated as immutable data. Each assay is a collection of files, together with a corresponding metadata file, stored in a subdirectory of the top-level subdirectory `assays`. Assay-level metadata is stored in [ISA-XLSX](##isa-xlsx) format in a file `isa.assay.xlsx`, which MUST exist for each assay. Further details on `isa.assay.xlsx` are specified [below](#assay-metadata). Assay data files MUST be placed in a `dataset` subdirectory.

- *Workflows* represent data analysis routines (in the sense of CWL tools and workflows) and are a collection of files, together with a corresponding CWL description, stored in a single directory under the top-level `workflows` subdirectory. A per-workflow executable CWL description is stored in `workflow.cwl`, which MUST exist for all ARC workflows. Further details on workflow descriptions are given [below](#workflow-descriptions).

- *Runs* capture data products (i.e., results of computational analysis) derived from assays, other runs, or external data using workflows. Each run is a collection of files, stored in the top-level `runs` subdirectory. It MUST be accompanied by a per-run CWL workflow description, stored in `<run_name>.cwl` and further described [below](#run-descriptions).

- *Externals* are external data (e.g., knowledge files) that need to be included and cannot be referenced due to external limitations. Metadata information SHOULD be stored according to the ISA model and CWL in case of workflow information; see [below](#external-data-annotation) for details.

- *Top-level metadata and workflow description* tie together the elements of an ARC in the contexts of investigation and associated studies (in the ISA definition), captured in the files `isa.investigation.xlsx` in [ISA-XLSX format](#isa-xlsx), which MUST be present. Optionally, study-level metadata CAN be present in `isa.studies.xlsx`. Furthermore, top-level reproducibility information MUST be provided in the CWL `arc.cwl`, which also MUST exist.

All other files contained in an ARC (e.g, a `README.txt`, a pre-print PDFs, additional annotation files, etc.) are referred to as *additional payload*, and can be located anywhere within the ARC structure. However, an ARC MUST be [reproducible](#reproducible-arcs) and [complete](#complete-arcs) even if these files are deleted. Further considerations on additional payload are described [below](#additional-payload).

Note: 
- Subdirectories and other files in the top-level `assays`, `workflows`, `runs`, and `externals` directories are viewed as additional payload unless they are accompanied by the corresponding mandatory description (`isa.assay.xlsx`, `workflow.cwl`, `run.cwl`, `isa.external.xlsx`) specified below. This is intended to allow gradual migration from existing data storage schemes to the ARC schema. For example, *data files* for an assay can be stored in a subdirectory of `assays/`, but are only identified as an assay of the ARC if metadata is present and complete, including a reference from top-level metadata.

- @ Distribution of metadata across many files.

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

### ARC representation

ARCs are a Git repositories, as defined and supported by the [Git C implementation](https://git-scm.org) (version XX or newer) with [Git-LFS extension](https://git-lfs.github.com) (version 2.12.0), or fully compatible implementations. 

ARC terminology implicitly borrows from Git and Git-LFS terminology. For example, an ARC commit is simply a Git commit, and the ARC history is the repository history. Furthermore, an ARC can contain multiple branches, etc.

Tree objects (resp. directories) and blobs (i.e., files) of all branch heads in the repository MUST adhere to the [ARC schema](#arc-structure-and-contents-schema). ARCs allow all typical Git operations (e.g. clone, branch) etc.

All representation suitable for Git-LFS repositories are also a valid representations of ARCs. This includes both bare repositories (without a checked out working copy) and non-bare repositories (i.e. a `.git` directory with one or more attached working copies). In particular, it is possible and intended to maintain ARCs on local user filesystems and via Git repository hosting services. No requirements are made of the state and contents of working copies.

Note: implicit content addressing and hashing via Git mechanisms

Note: removing .git -> no longer an ARC

### Assay Data and Metadata

All measurement data sets are considered as assays and are consider immutable input data. Assays data MUST be placed into a unique subdirectory of the top-level `assays` folder. 

All ISA metadata specific to a single assay (e.g., measurement type and technology, i.e. all terms with term names beginning with `ASSAY`) must be annotated in a in the file `isa.assay.xlsx` at the root of the assay's subdirectory. All investigation-level assay metadata specific to an assay MUST be duplicated from the ARC's top-level `isa.investigation.xlsx` in a separate worksheet

Notes:

- To ensure reusability of entire assays across multiple ARCs, redundancy between assay-specfic, assay-level metadata and investigation-level metadata is intentional. 
  
- It is recommended to adopt the structure outlined [below](#best-practices) to organize assay data files and other supporting information.

- There are no requirements on specific assay-level metadata. Conversion of ARCs into other repository or archival format (e.g. PRIDE, GEO, ENA etc.) may however mandate the presence of specific terms (cf. [below](#arc-conversion)) required in the destination format.

- An implementation that ensures assay annotation consistent with these requirements is provided by the [SWATE tool]().

- While assays can in principle contain arbitrary data formats, it is highly recommended to use community-supported, open formats (see [Best Practices](#best-practices)).

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

External data refer to data that is neither originating within the investigation/study scope of the ARC nor can be referenced externally, but is required to ensure reproducability. Examples include early use of ontologies, mapping files, gene information, etc. All correspondig data MUST be placed in the ARC's top-level `external` directory.

The union of external data forms a *virtual* assay; as such, it MUST adhere to the metadata requirements of assays and hence MUST contain, for each file, annotation in a file `isa.external.xlsx`, located under the top-level `external` directory.

Note:

- Each external data file can be interpreted as a virtual sample in the *externals* assay. Due to the conceptual difference to the immutable measurements represented by the assays in `assays`, external files are stored in a different location to ensure that this distinction explict.


### Top-level Metadata and Workflow Description

*(not cleaned up / merged)*

- *Top-level metadata and workflow description* tie together the elements of an ARC in the contexts of investigation and associated studies (in the ISA definition), captured in the files `isa.investigation.xlsx` in [ISA-XLSX format](#isa-xlsx), which MUST be present. Optionally, study-level metadata CAN be present in `isa.studies.xlsx`. Furthermore, top-level reproducibility information MUST be provided in the CWL `arc.cwl`, which also MUST exist.


#### Investigation and Study Metadata (-> Timo)

*(not cleaned up / merged)*

ARC root directory is identifiable by the presence of the investigation file: 
\isa.investigation.xlsx  

The investigation file (in XLSX format) contains top-level information about the investigation and links to studies and assays. An investigation is used to record metadata relating to the description of the investigation context and administrative metadata, such as the title and description of the investigation as well as about involved people and publications. 

Study and assay objects are registered and grouped with an Investigation to record other metadata within the relevant contexts. (https://isa-specs.readthedocs.io/en/latest/isamodel.html#investigation) 
The study file is optional and can be used to group assays into studies within one investigation. Multiple studies can be stored using one worksheet per study: 
    \isa.studies.xlsx  
In contrast to the original ISA specifications, only [factors] are included. Several studies may be related to a single investigation. Each study serves as a steppingstone for achieving the investigation aim (e.g. investigating salt tolerance in Arabidopsis) 


#### Workflow Description (-> Christoph)

*(about `arc.cwl`)*

To (re)produce the run results corresponding to the workflows stored in an ARC, all workflows need to be registered within 
    \arc.cwl 
This allows to execute all computations defined in the workflow structure in order to (re)produce corresponding runs results using all necessary parameters defined in:  
    \arc.yml 

### ISA-XLSX Format

ISA-XLSX follows the ISA model specification saved in a XLSX format. The XLSX format uses the SpreadsheetML markup language and schema to represent a spreadsheet document. Conceptually, using the terminology of the Spreadsheet ML specification in [ISO/IEC 29500-1](https://www.loc.gov/preservation/digital/formats/fdd/fdd000398.shtml#:~:text=The%20XLSX%20format%20uses%20the,a%20rectangular%20grid%20of%20cells.), the document comprises one or more worksheets in a workbook.
A workbook MUST contain a single assay that can be organized in one or many worksheets. Worksheets MUST be named uniquely within the same workbook. A worksheet named study MUST store the STUDY ASSAYS section defined on investigation-level of the ISA model that is duplicated in the isa.investigation.xlsx. Additional worksheets MUST contain table object with fields organized on a per-row basis. The first row MUST be used for column headers. Comments or axillary information MAY be stored alongside with table objects in a worksheet. A ´Source´ MUST be indicated with the column heading ´Source Name´. Every table object MUST define at least one source per row. A Sample MUST be indicated with the column heading Sample Name. The source sample relation MUST follow a unique path in directed acyclic graph, but MAY distributed across different worksheets.

Notes: 
  - It RECOMMENDED to order worksheets according to the source sample relation for readability.

## Shareable and Publishable ARCs
ARCs can be shared in any state. They are considered *publishable* (e.g. for the purpose of minting a DOI) when fulfilling the following conditions:

- Investigation-level metadata contains minimally the following DataCite terms:

  - Project name 
  - Project ID or Grant ID 
  - (Short) project description 
  - Grant provider 
  - Program name (if applicable) 
  - Principal Investigator(s) (PI) 
  - ORCID-ID of the PI(s) [if available]
  - Contact information of the responsible person of the data 
  - Creation date (and embargo periods, ...) 

- The ARC MUST NOT be *empty*: it MUST contain minimally a single assay or a single workflow.

Notes: 
  - The attribute *publishable* does not imply that data and metadata contained in an ARC are suitable for publication in a specific outlet (e.g. PRIDE, GEO, EBI). While it may be straightforward to convert the ARC schema into one required by specific publishers or repositories, additional metadata requirements may be enforced during conversion. These are intentionally not captured in this specification.



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
 
## Best Practices

*(not cleaned up / merged)*

Additionally, it is RECOMMENDED to place the corresponding protocol (assay SOP) in text form under:  


### Directory and File Naming Conventions 

*(do we really need this?)*

Required files defined in the ARC structure need to be named accordingly. Files and folders specified < > can be named freely. 

As the ARC might be used by different persons and in different workflow contexts, we recommend a concise filename without blanks and special characters. A good choice is to stick to small and capital letters without umlauts and similar special characters. Numbers, hyphen, and underscores are suitable as well. Modern working environments can handle blanks in filenames but might confuse automatically run scripts and thus should be avoided. Depending on the intended amount of people the ARC is shared with, certain information might prove useful to provide a fast overview in human readable form in the filename, e.g. by providing abbreviations of the project, sub project, person creating or working on a particular data set. Date and time information might be encoded as well if it provides a better ordering or information for the particular purpose. 

### Compression and Encryption 

*(this should not be included)*

Compression is preferrable to save on disk space and speed up data transfers but not required. Without compression workflows are simpler as often no transparent compression and decompression is available. Uncompressed files are usually easier to index and better searchable. 

Encryption is not advised (but could be an option to share sensitive data in an otherwise open ARC) .

### Auxiliary Payload

*(not cleaned up / merged)*
Everything not meeting these criteria is regarded as auxiliary payload and therefore is not strictly considered ARC content. This might result in an ‘empty’ ARC only containing auxiliary payload. 

Auxiliary payload MUST be ignored by any processing. Also, auxiliary payload might be restricted in size or retention depending on the repository for ARC sharing and publication.  

#### Community specific data formats 
It is recommend to use of community specific data formats covering most common measurement techniques. 
Using the following recommended formats will ensure improoved accessability and findability:   
- mzML (raw data metabolomics and proteomics) 
- mzTAB (analysis data metabolomics and proteomics)
- Fastq.gz (compressed NGS Short Read Sequencing, Long Read Sequencing) 
- fastq (NGS Short Read Sequencing, Long Read Sequencing) 
- BAM 
- SAM 

Notes: 
  - In case of storing vendor-spesific data within an ARC, it is strongly encurage to accompany them by the corresponding open formats or provide a workflow for convertion or processing.
  

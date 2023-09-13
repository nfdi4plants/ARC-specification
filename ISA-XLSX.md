# ISA-XLSX format

For detail on ISA framework terminology, please read the [ISA Abstract Model specification](isamodel.md).

This document describes the ISA Abstract Model reference implementation specified in the ISA-XLSX format. The XLSX format uses the SpreadsheetML markup language and schema to represent a spreadsheet document. Conceptually, using the terminology of the Spreadsheet ML specification [ISO/IEC 29500-1](https://www.loc.gov/preservation/digital/formats/fdd/fdd000398.shtml#:~:text=The%20XLSX%20format%20uses%20the,a%20rectangular%20grid%20of%20cells.), the document comprises one or more worksheets in a workbook. Every worksheet MUST contain one table object storing the metadata. Comments or auxillary information MAY be stored alongside with table objects in a worksheet.

Below we provide the schemas and the content rules for valid ISA-XLSX documents. 

## Format

ISA-XLSX uses three types of files to capture the experimental metadata:
  - Investigation file
  - Study file
  - Assay file (with associated data files)

The Investigation file contains all the information needed to understand the overall goals and means used in an
experiment; experimental steps (or sequences of events) are described in the Study and in the Assay file(s). For each
Investigation file there may be one or more Studies defined with a corresponding Study file; for each Study there may
be one or more Assays defined with corresponding Assay files.

In order to facilitate identification of ISA-XLSX component files, specific naming patterns MUST follow:

- `isa.investigation.xlsx` for identifying the Investigation file
- `isa.study.xlsx` for identifying Study file(s)
- `isa.assay.xlsx` for identifying Assay file(s)

Sheets described in this specification MUST follow one of the two given formats:

> - `Top-level metadata sheets` for listing top-level metadata
> - `Annotation Table sheets` for describing experimental workflows

Sheets which do not follow any of these two formats are considerered additional payload and are ignored in this specification.

All labels are case-sensitive:

Dates SHOULD be supplied in the [ISO8601](http://www.iso.org/iso/home/standards/iso8601.htm) format.

For maximal portability file names SHOULD contain only ASCII characters not excluded
already (that is `A-Za-z0-9._!#$%&+,;=@^(){}'[]` - we exclude space as many utilities
do not accept spaces in file paths): non-English alphabetic characters cannot be guaranteed
to be supported in all locales. It would be good practice to avoid the shell metacharacters
`(){}'[]$."`.

## Top-level metadata sheets

The purpose of top-level metadata sheets is aggregating and listing top-level metadata. Each sheet consists of sections consisting of a section header and key-value fields. Section headers MUST be completely written in upper case (e.g. STUDY), field headers MUST have the first letter of each word in upper case (e.g. Study Identifier); with the exception of the referencing label (REF).

In the following sections, examples of each section block are given beside the specification of each section.

For a full example of a complete Investigation File, please see [https://git.io/vD1va](https://git.io/vD1va).

> #### ATTENTION
> Rows in which the first character in the first column is Unicode
> [U+0023](http://www.fileformat.info/info/unicode/char/0023/index.htm)  (the `#` character) > MUST be interpreted as
> comments, where reference implementation parsers SHOULD ignore those lines entirely.

> Rows where the label `Comment[<comment name>]` appear can also appear within any of the > section blocks. Where these appear, the comment name must be unique within the context of a single block (e.g. you cannot have multiple occurences of `Comment[external DB REF]` within `STUDY ASSAYS`. Also, the value cells MUST match the number of values indicated by the rest of the section in context.

### Ontology Source Reference section

The Ontology Source section of the Investigation file is used to declare Ontology Sources used elsewhere in the ISA-XLSX
files within the context of an Investigation.

Where a row labelled with `Term Source REF` suffixed in the Investigation
file, the value of the cell SHOULD match one of the `Term Source Name` value declared in this section.

Where a column labelled with `Term Source REF` in a Study file or Assay file associated with the Investigation, the value
of the cell SHOULD match one of the `Term Source Name` value declared in this section.

This section implements a list of `Ontology Source` from the ISA Abstract Model.

This section MUST contain zero or more values.

**ONTOLOGY SOURCE REFERENCE**

This section MUST contain the following labels, with the specified datatypes for values supported:

| Label                   | Datatype                  | Description                                                                                                                                                                     |
|-------------------------|---------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Term Source Name        | String                    | The name of the source of a term; i.e. the source controlled vocabulary or ontology. These names will be used in all corresponding Term Source REF fields that occur elsewhere. |
| Term Source File        | String (file name or URI) | A file name or a URI of an official resource.                                                                                                                                   |
| Term Source Version     | String                    | The version number of the Term Source to support terms tracking.                                                                                                                |
| Term Source Description | String                    | Use for disambiguating resources when homologous prefixes have been used.                                                                                                       |

For example, the `ONTOLOGY SOURCE REFERENCE` section of an ISA-XLSX `isa.investigation.xlsx` file may look as follows:

```default
ONTOLOGY SOURCE REFERENCE
Term Source Name	"CHEBI"	"EFO"	"OBI"	"NCBITAXON"	"PATO"
Term Source File	"http://data.bioontology.org/ontologies/CHEBI"	"http://data.bioontology.org/ontologies/EFO"	"http://data.bioontology.org/ontologies/OBI"	"http://data.bioontology.org/ontologies/NCBITAXON"	"http://data.bioontology.org/ontologies/PATO"
Term Source Version	"78"	"111"	"21"	"2"	"160"
Term Source Description	"Chemical Entities of Biological Interest Ontology"	"Experimental Factor Ontology"	"Ontology for Biomedical Investigations"	"National Center for Biotechnology Information (NCBI) Organismal Classification"	"Phenotypic Quality Ontology"
```

### Investigation section

This section is organized in several subsections, described in detail below. The Investigation section provides a
flexible mechanism for grouping two or more Study files where required. When only one Study is created, the values in
this section SHOULD be left empty and the relevant metadata values recorded in the Study section only.

These sections implement an `Investigation` from the ISA Abstract Model.

**INVESTIGATION**

This section MUST contain zero or one values.

This section MUST contain the following labels, with the specified datatypes for values supported:

| Label                             | Datatype                                    | Description                                                                                  |
|-----------------------------------|---------------------------------------------|----------------------------------------------------------------------------------------------|
| Investigation Identifier          | String                                      | A identifier or an accession number provided by a repository. This SHOULD be locally unique. |
| Investigation Title               | String                                      | A concise name given to the investigation.                                                   |
| Investigation Description         | String                                      | A textual description of the investigation.                                                  |
| Investigation Submission Date     | String formatted as ISO8601 date YYYY-MM-DD | The date on which the investigation was reported to the repository.                          |
| Investigation Public Release Date | String formatted as ISO8601 date YYYY-MM-DD | The date on which the investigation was released publicly.                                   |

For example, the `INVESTIGATION` section of an ISA-XLSX `isa.investigation.xlsx` file may look as follows:

```default
INVESTIGATION
Investigation Identifier	"BII-I-1"
Investigation Title	"Growth control of the eukaryote cell: a systems biology study in yeast"
Investigation Description	"Background Cell growth underlies many key cellular and developmental processes, yet a limited number of studies have been carried out on cell-growth regulation. Comprehensive studies at the transcriptional, proteomic and metabolic levels under defined controlled conditions are currently lacking. Results Metabolic control analysis is being exploited in a systems biology study of the eukaryotic cell. Using chemostat culture, we have measured the impact of changes in flux (growth rate) on the transcriptome, proteome, endometabolome and exometabolome of the yeast Saccharomyces cerevisiae. Each functional genomic level shows clear growth-rate-associated trends and discriminates between carbon-sufficient and carbon-limited conditions. Genes consistently and significantly upregulated with increasing growth rate are frequently essential and encode evolutionarily conserved proteins of known function that participate in many protein-protein interactions. In contrast, more unknown, and fewer essential, genes are downregulated with increasing growth rate; their protein products rarely interact with one another. A large proportion of yeast genes under positive growth-rate control share orthologs with other eukaryotes, including humans. Significantly, transcription of genes encoding components of the TOR complex (a major controller of eukaryotic cell growth) is not subject to growth-rate regulation. Moreover, integrative studies reveal the extent and importance of post-transcriptional control, patterns of control of metabolic fluxes at the level of enzyme synthesis, and the relevance of specific enzymatic reactions in the control of metabolic fluxes during cell growth. Conclusion This work constitutes a first comprehensive systems biology study on growth-rate control in the eukaryotic cell. The results have direct implications for advanced studies on cell growth, in vivo regulation of metabolic fluxes for comprehensive metabolic engineering, and for the design of genome-scale systems biology models of the eukaryotic cell."
Investigation Submission Date	"2007-04-30"
Investigation Public Release Date	"2009-03-10"
```

**INVESTIGATION PUBLICATIONS**

This section MUST contain zero or more values.

This section MUST contain the following labels, with the specified datatypes for values supported:

| Label                                                  | Datatype                                                                                           | Description                                                                                                                                                                                |
|--------------------------------------------------------|----------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Investigation Publication PubMed ID                                | String formatted as valid PubMed ID                                                                | The PubMed IDs of the described publication(s) associated with this investigation.                                                                              |
| Investigation Publication DOI                          | String formatted as valid DOI                                                                      | A Digital Object Identifier (DOI) for that publication (where available).                                                                                 |
| Investigation Publication Author List                  | String                                                                                      | The list of authors associated with that publication.                                                                                |
| Investigation Publication Title                        | String                                                                                             | The title of publication associated with the investigation.                                                                              |
| Investigation Publication Status                       | String, or Ontology Annotation by providing accompanying Term Accession Number and Term Source REF | A term describing the status of that publication (i.e. submitted, in preparation, published).                                                                                 |
| Investigation Publication Status Term Accession Number | String or URI                                                                                      | The accession number from the Term Source associated with the selected term.                                                                                       |
| Investigation Publication Status Term Source REF       | String                                                                                             | Identifies the controlled vocabulary or ontology that this term comes from. The Source REF has to match one the Term Source Name declared in the in the Ontology Source Reference section. |

For example, the `INVESTIGATION PUBLICATIONS` section of an ISA-XLSX `isa.investigation.xlsx` file may look as follows:

```default
INVESTIGATION PUBLICATIONS
Investigation Publication PubMed ID	"17439666"
Investigation Publication DOI	"doi:10.1186/jbiol54"
Investigation Publication Author List	"Castrillo JI, Zeef LA, Hoyle DC, Zhang N, Hayes A, Gardner DC, Cornell MJ, Petty J, Hakes L, Wardleworth L, Rash B, Brown M, Dunn WB, Broadhurst D, O'Donoghue K, Hester SS, Dunkley TP, Hart SR, Swainston N, Li P, Gaskell SJ, Paton NW, Lilley KS, Kell DB, Oliver SG."
Investigation Publication Title	"Growth control of the eukaryote cell: a systems biology study in yeast."
Investigation Publication Status	"indexed in Pubmed"
Investigation Publication Status Term Accession Number	""
Investigation Publication Status Term Source REF	""
```

**INVESTIGATION CONTACTS**

This section MUST contain zero or more values.

This section MUST contain the following labels, with the specified datatypes for values supported:

| Label                                            | Datatype                                                                                    | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
|--------------------------------------------------|---------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Investigation Person Last Name                   | String                                                                                      | The last name of a person associated with the investigation.                                                                              |
| Investigation Person First Name                  | String                                                                                      | Investigation Person Name                                                                                        |
| Investigation Person Mid Initials                | String                                                                                      | The middle initials of a person associated with the investigation.                                                                              |
| Investigation Person Email                       | String formatted as email                                                                   | The email address of a person associated with the investigation.                                                                              |
| Investigation Person Phone                       | String                                                                                      | The telephone number of a person associated with the investigation.                                                                              |
| Investigation Person Fax                         | String                                                                                      | The fax number of a person associated with the investigation.                                                                              |
| Investigation Person Address                     | String                                                                                      | The address of a person associated with the investigation.                                                                              |
| Investigation Person Affiliation                 | String                                                                                      | The organization affiliation for a person associated with the investigation.                                                                              |
| Investigation Person Roles                       | String or Ontology Annotation if accompanied by Term Accession Numbers and Term Source REFs | Term to classify the role(s) performed by this person in the context of the investigation, which means that the roles reported here need not correspond to roles held withing their affiliated organization. Multiple annotations or values attached to one person can be provided by using a semicolon (“;”) Unicode (U0003+B) as a separator (e.g.: submitter;funder;sponsor) .The term can be free text or from, for example, a controlled vocabulary or an ontology. If the latter source is used the Term Accession Number and Term Source REF fields below are required. |
| Investigation Person Roles Term Accession Number | String                                                                                      | The accession number from the Term Source associated with the selected term.                                                                                       |
| Investigation Person Roles Term Source REF       | String                                                                                      | Identifies the controlled vocabulary or ontology that this term comes from. The Source REF has to match one of the Term Source Names declared in the Ontology Source Reference section.                                                                                    |

For example, the `INVESTIGATION CONTACTS` section of an ISA-XLSX `isa.investigation.xlsx` file may look as follows:

```default
INVESTIGATION CONTACTS
Investigation Person Last Name	"Stephen"	"Castrillo"	"Zeef"
Investigation Person First Name	"Oliver"	"Juan"	"Leo"
Investigation Person Mid Initials	"G"	"I"	"A"
Investigation Person Email	""	""	""
Investigation Person Phone	""	""	""
Investigation Person Fax	""	""	""
Investigation Person Address	"Oxford Road, Manchester M13 9PT, UK"	"Oxford Road, Manchester M13 9PT, UK"	"Oxford Road, Manchester M13 9PT, UK"
Investigation Person Affiliation	"Faculty of Life Sciences, Michael Smith Building, University of Manchester"	"Faculty of Life Sciences, Michael Smith Building, University of Manchester"	"Faculty of Life Sciences, Michael Smith Building, University of Manchester"
Investigation Person Roles	"corresponding author"	"author"	"author"
Investigation Person Roles Term Accession Number	""	""	""
Investigation Person Roles Term Source REF	""	""	""
```

### Study section

This section is organized in several subsections, described in detail below. This section also represents a
**repeatable block**, which is replicated according to the number of Studies to report (i.e. two Studies, two Study
blocks are represented in the Investigation file). The subsections in the block are arranged vertically; the intent
being to enhance readability and presentation, and possibly to help with parsing. These subsections MUST remain within
this repeatable block, although their order MAY vary; the fields MUST remain within their subsection.

These sections implement the metadata for a `Study` from the ISA Abstract Model and a list of `Assay` (i.e. `Study` and
`Assay` **without** graphs; graphs are implemented in ISA-XLSX as `Annotation Table sheets`).

**STUDY**

This section MUST contain zero or one values.

This section MUST contain the following labels, with the specified datatypes for values supported:

| Label                     | Datatype                             | Description                                                                                                                                                                                            |
|---------------------------|--------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Study Identifier          | String                               | A unique identifier, either a temporary identifier supplied by users or one generated by a repository or other database. For example, it could be an identifier complying with the LSID specification. |
| Study Title               | String                               | A concise phrase used to encapsulate the purpose and goal of the study.                                                                                                                                |
| Study Description         | String                               | A textual description of the study, with components such as objective or goals.                                                                                                                        |
| Study Submission Date     | String formatted as ISO8601 date     | The date on which the study is submitted to an archive.                                                                                                                                                |
| Study Public Release Date | String formatted as ISO8601 date     | The date on which the study SHOULD be released publicly.                                                                                                                                               |
| Study File Name           | String formatted as file name or URI | A field to specify the name of the Study Table file corresponding the definition of that Study. There can be only one file per cell.                                                                   |

For example, the `STUDY` section of an ISA-XLSX `isa.investigation.xlsx` file may look as follows:

```default
Study Identifier	"BII-S-3"
Study Title	"Metagenomes and Metatranscriptomes of phytoplankton blooms from an ocean acidification mesocosm experiment"
Study Description	"Sequencing the metatranscriptome can provide information about the response of organisms to varying environmental conditions. We present a methodology for obtaining random whole-community mRNA from a complex microbial assemblage using Pyrosequencing. The metatranscriptome had, with minimum contamination by ribosomal RNA, significant coverage of abundant transcripts, and included significantly more potentially novel proteins than in the metagenome. This experiment is part of a much larger experiment. We have produced 4 454 metatranscriptomic datasets and 6 454 metagenomic datasets. These were derived from 4 samples."
Study Submission Date	"2008-08-15"
Study Public Release Date	"2008-08-15"
Study File Name	"studies/BII-S-3/isa.study.xlsx"
```

**STUDY DESIGN DESCRIPTORS**

This section MUST contain zero or more values.

This section MUST contain the following labels, with the specified datatypes for values supported:

| Label                                   | Datatype   | Description                                                                                                                                                                                                                                                                                                                             |
|-----------------------------------------|------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Study Design Type                       | String     | A term allowing the classification of the study based on the overall experimental design, e.g cross-over design or parallel group design. The term can be free text or from, for example, a controlled vocabulary or an ontology. If the latter source is used the Term Accession Number and Term Source REF fields below are required. |
| Study Design Type Term Accession Number | String     | The accession number from the Term Source associated with the selected term.                                                                                                                                                                                                                                                            |
| Study Design Type Term Source REF       | String     | Identifies the controlled vocabulary or ontology that this term comes from. The Study Design Term Source REF has to match one the Term Source Name declared in the Ontology Source Reference section.                                                                                                                                   |

For example, the `STUDY DESIGN DESCRIPTORS` section of an ISA-XLSX `isa.investigation.xlsx` file may look as follows:

```default
STUDY DESIGN DESCRIPTORS
Study Design Type	"time series design"
Study Design Type Term Accession Number	"http://purl.obolibrary.org/obo/OBI_0500020"
Study Design Type Term Source REF	"OBI"
```

**STUDY PUBLICATIONS**

This section MUST contain zero or more values.

This section MUST contain the following labels, with the specified datatypes for values supported:

| Label                                          | Datatype                                                                                           | Description                                                                                                                                                                                |
|------------------------------------------------|----------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Study PubMed ID                                | String formatted as valid PubMed ID                                                                | The PubMed IDs of the described publication(s) associated with this study.                                                                                                                 |
| Study Publication DOI                          | String formatted as valid DOI                                                                      | A Digital Object Identifier (DOI) for that publication (where available).                                                                                                                  |
| Study Publication Author List                  | String                                                                                             | The list of authors associated with that publication.                                                                                                                                      |
| Study Publication Title                        | String                                                                                             | The title of publication associated with the investigation.                                                                                                                                |
| Study Publication Status                       | String, or Ontology Annotation by providing accompanying Term Accession Number and Term Source REF | A term describing the status of that publication (i.e. submitted, in preparation, published).                                                                                              |
| Study Publication Status Term Accession Number | String or URI                                                                                      | The accession number from the Term Source associated with the selected term.                                                                                                               |
| Study Publication Status Term Source REF       | String                                                                                             | Identifies the controlled vocabulary or ontology that this term comes from. The Source REF has to match one the Term Source Name declared in the in the Ontology Source Reference section. |

For example, the `STUDY PUBLICATIONS` section of an ISA-XLSX `isa.investigation.xlsx` file may look as follows:

```default
STUDY PUBLICATIONS
Study PubMed ID	"18725995"	"18783384"
Study Publication DOI	"10.1371/journal.pone.0003042"	"10.1111/j.1462-2920.2008.01745.x"
Study Publication Author List	"Gilbert JA, Field D, Huang Y, Edwards R, Li W, Gilna P, Joint I."	"Gilbert JA, Thomas S, Cooley NA, Kulakova A, Field D, Booth T, McGrath JW, Quinn JP, Joint I."
Study Publication Title	"Detection of large numbers of novel sequences in the metatranscriptomes of complex marine microbial communities."	"Potential for phosphonoacetate utilization by marine bacteria in temperate coastal waters."
Study Publication Status	"indexed in PubMed"	"indexed in PubMed"
Study Publication Status Term Accession Number	""	""
Study Publication Status Term Source REF	""	""
```

**STUDY FACTORS**

This section MUST contain zero or more values.

This section MUST contain the following labels, with the specified datatypes for values supported:

| Label                                   | Datatype   | Description                                                                                                                                                                                                                                                                                                                                                                              |
|-----------------------------------------|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Study Factor Name                       | String     | The name of one factor used in the Study and/or Assay files. A factor corresponds to an independent variable manipulated by the experimentalist with the intention to affect biological systems in a way that can be measured by an assay. The value of a factor is given in the Study or Assay file, accordingly. If both Study and Assay have a Factor Value, these must be different. |
| Study Factor Type                       | String     | A term allowing the classification of this factor into categories. The term can be free text or from, for example, a controlled vocabulary or an ontology. If the latter source is used the Term Accession Number and Term Source REF fields below are required.                                                                                                                         |
| Study Factor Type Term Accession Number | String     | The accession number from the Term Source associated with the selected term.                                                                                                                                                                                                                                                                                                             |
| Study Factor Type Term Source REF       | String     | Identifies the controlled vocabulary or ontology that this term comes from. The Source REF has to match one of the Term Source Name declared in the Ontology Source Reference section.                                                                                                                                                                                                   |

For example, the `STUDY FACTORS` section of an ISA-XLSX `isa.investigation.xlsx` file may look as follows:

```default
STUDY FACTORS
Study Factor Name	"dose"	"compound"	"collection time"
Study Factor Type	"dose"	"chemical substance"	"time"
Study Factor Type Term Accession Number	"http://www.ebi.ac.uk/efo/EFO_0000428"	"http://purl.obolibrary.org/obo/CHEBI_59999"	"http://purl.obolibrary.org/obo/PATO_0000165"
Study Factor Type Term Source REF	"EFO"	"CHEBI"	"PATO"
```

**STUDY ASSAYS**

This section MUST contain zero or more values.

This section MUST contain the following labels, with the specified datatypes for values supported:

| Label                                              | Datatype   | Description                                                                                                                                                                                                                                                                                                         |
|----------------------------------------------------|------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Study Assay Measurement Type                       | String     | A term to qualify the endpoint, or what is being measured (e.g. gene expression profiling or protein identification). The term can be free text or from, for example, a controlled vocabulary or an ontology. If the latter source is used the Term Accession Number and Term Source REF fields below are required. |
| Study Assay Measurement Type Term Accession Number | String     | The accession number from the Term Source associated with the selected term.                                                                                                                                                                                                                                        |
| Study Assay Measurement Type Term Source REF       | String     | The Source REF has to match one of the Term Source Name declared in the Ontology Source Reference section.                                                                                                                                                                                                          |
| Study Assay Technology Type                        | String     | Term to identify the technology used to perform the measurement, e.g. DNA microarray, mass spectrometry. The term can be free text or from, for example, a controlled vocabulary or an ontology. If the latter source is used the Term Accession Number and Term Source REF fields below are required.              |
| Study Assay Technology Type Term Accession Number  | String     | The accession number from the Term Source associated with the selected term.                                                                                                                                                                                                                                        |
| Study Assay Technology Type Term Source REF        | String     | Identifies the controlled vocabulary or ontology that this term comes from. The Source REF has to match one of the Term Source Names declared in the Ontology Source Reference section.                                                                                                                             |
| Study Assay Technology Platform                    | String     | Manufacturer and platform name, e.g. Bruker AVANCE                                                                                                                                                                                                                                                                  |
| Study Assay File Name                              | String     | A field to specify the name of the Assay Table file corresponding the definition of that assay. There can be only one file per cell.                                                                                                                                                                                |

For example, the `STUDY ASSAYS` section of an ISA-XLSX `isa.investigation.xlsx` file may look as follows:

```default
STUDY ASSAYS
Study Assay File Name	"assays/gilbert-Gx/isa.assay.xlsx"	"assays/gilbert-Tx/isa.assay.xlsx"
Study Assay Measurement Type	"metagenome sequencing"	"transcription profiling"
Study Assay Measurement Type Term Accession Number	""	""
Study Assay Measurement Type Term Source REF	"OBI"	"OBI"
Study Assay Technology Type	"nucleotide sequencing"	"nucleotide sequencing"
Study Assay Technology Type Term Accession Number	""	""
Study Assay Technology Type Term Source REF	"OBI"	"OBI"
Study Assay Technology Platform	"454 GS FLX"	"454 GS FLX"
```

**STUDY PROTOCOLS**

This section MUST contain zero or more values.

This section MUST contain the following labels, with the specified datatypes for values supported:

| Label                                                | Datatype   | Description                                                                                                                                                                                                                                                                                                                                                                                        |
|------------------------------------------------------|------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Study Protocol Name                                  | String     | The name of the protocols used within the ISA-XLSX document. The names are used as identifiers within the ISA-XLSX document and will be referenced in the Study and Assay files in the Protocol REF columns. Names can be either local identifiers, unique within the ISA Archive which contains them, or fully qualified external accession numbers.                                                |
| Study Protocol Type                                  | String     | Term to classify the protocol. The term can be free text or from, for example, a controlled vocabulary or an ontology. If the latter source is used the Term Accession Number and Term Source REF fields below are required.                                                                                                                                                                       |
| Study Protocol Type Term Accession Number            | String     | The accession number from the Term Source associated with the selected term.                                                                                                                                                                                                                                                                                                                       |
| Study Protocol Type Term Source REF                  | String     | Identifies the controlled vocabulary or ontology that this term comes from. The Source REF has to match one of the Term Source Name declared in the Ontology Source Reference section.                                                                                                                                                                                                             |
| Study Protocol Description                           | String     | A free-text description of the protocol.                                                                                                                                                                                                                                                                                                                                                           |
| Study Protocol URI                                   | String     | Pointer to protocol resources external to the ISA-Tab that can be accessed by their Uniform Resource Identifier (URI).                                                                                                                                                                                                                                                                             |
| Study Protocol Version                               | String     | An identifier for the version to ensure protocol tracking.                                                                                                                                                                                                                                                                                                                                         |
| Study Protocol Parameters Name                       | String     | A semicolon-delimited (“;”) list of parameter names, used as an identifier within the ISA-XLSX document. These names are used in the Study and Assay files (in the “Parameter Value []” column heading) to list the values used for each protocol parameter. Refer to section Multiple values fields in the Investigation File on how to encode multiple values in one field and match term sources |
| Study Protocol Parameters Term Accession Number      | String     | The accession number from the Term Source associated with the selected term.                                                                                                                                                                                                                                                                                                                       |
| Study Protocol Parameters Term Source REF            | String     | Identifies the controlled vocabulary or ontology that this term comes from. The Source REF has to match one of the Term Source Name declared in the Ontology Source Reference section.                                                                                                                                                                                                             |
| Study Protocol Components Name                       | String     | A semicolon-delimited (“;”) list of a protocol’s components; e.g. instrument names, software names, and reagents names. Refer to section Multiple values fields in the Investigation File on how to encode multiple components in one field and match term sources.                                                                                                                                |
| Study Protocol Components Type                       | String     | Term to classify the protocol components listed for example, instrument, software, detector or reagent. The term can be free text or from, for example, a controlled vocabulary or an ontology. If the latter source is used the Term Accession Number and Term Source REF fields below are required.                                                                                              |
| Study Protocol Components Type Term Accession Number | String     | The accession number from the Source associated to the selected terms.                                                                                                                                                                                                                                                                                                                             |
| Study Protocol Components Type Term Source REF       | String     | Identifies the controlled vocabulary or ontology that this term comes from. The Source REF has to match a Term Source Name previously declared in the ontology section                                                                                                                                                                                                                             |

For example, the `STUDY PROTOCOLS` section of an ISA-XLSX `isa.investigation.xlsx` file may look as follows:

```default
STUDY PROTOCOLS
Study Protocol Name	"environmental material collection - standard procedure 1"	"nucleic acid extraction - standard procedure 2"	"mRNA extraction - standard procedure 3"	"genomic DNA extraction - standard procedure 4"	"reverse transcription - standard procedure 5"	"library construction"	"pyrosequencing - standard procedure 6"	"sequence analysis - standard procedure 7"
Study Protocol Type	"sample collection"	"nucleic acid extraction"	"nucleic acid extraction"	"nucleic acid extraction"	"reverse transcription"	"library construction"	"nucleic acid sequencing"	"data transformation"
Study Protocol Type Term Accession Number	""	""	""	""	""	""	""	""
Study Protocol Type Term Source REF	""	""	""	""	""	""	""	""
Study Protocol Description	"Waters samples were prefiltered through a 1.6 um GF/A glass fibre filter to reduce Eukaryotic contamination. Filtrate was then collected on a 0.2 um Sterivex (millipore) filter which was frozen in liquid nitrogen until nucelic acid extraction. CO2 bubbled through 11000 L mesocosm to simulate ocean acidification predicted conditions. Then phosphate and nitrate were added to induce a phytoplankton bloom."	"Total nucleic acid extraction was done as quickly as possible using the method of Neufeld et al, 2007."	"RNA MinElute + substrative Hybridization + MEGAclear For transcriptomics, total RNA was separated from the columns using the RNA MinElute clean-up kit (Qiagen) and checked for integrity of rRNA using an Agilent bioanalyser (RNA nano6000 chip). High integrity rRNA is essential for subtractive hybridization. Samples were treated with Turbo DNA-free enzyme (Ambion) to remove contaminating DNA. The rRNA was removed from mRNA by subtractive hybridization (Microbe Express Kit, Ambion), and absence of rRNA and DNA contamination was confirmed using the Agilent bioanalyser. The mRNA was further purified with the MEGAclearTM kit (Ambion). Reverse transcription of mRNA was performed using the SuperScript III enzyme (Invitrogen) with random hexamer primers (Promega). The cDNA was treated with RiboShredderTM RNase Blend (Epicentre) to remove trace RNA contaminants. To improve the yield of cDNA, samples were subjected to random amplification using the GenomiPhi V2 method (GE Healthcare). GenomiPhi technology produces branched DNA molecules that are recalcitrant to the pyrosequencing methodology. Therefore amplified samples were treated with S1 nuclease using the method of Zhang et al.2006."	""	"superscript+random hexamer primer"	""	"1. Sample Input and Fragmentation: The Genome Sequencer FLX System supports the sequencing of samples from a wide variety of starting materials including genomic DNA, PCR products, BACs, and cDNA. Samples such as genomic DNA and BACs are fractionated into small, 300- to 800-base pair fragments. For smaller samples, such as small non-coding RNA or PCR amplicons, fragmentation is not required. Instead, short PCR products amplified using Genome Sequencer fusion primers can be used for immobilization onto DNA capture beads as shown below."	""
Study Protocol URI	""	""	""	""	""	""	""	""
Study Protocol Version	""	""	""	""	""	""	""	""
Study Protocol Parameters Name	"filter pore size"	""	""	""	""	"library strategy;library layout;library selection"	"sequencing instrument"	""
Study Protocol Parameters Name Term Accession Number	""	""	""	""	""	";;"	""	""
Study Protocol Parameters Name Term Source REF	""	""	""	""	""	";;"	""	""
Study Protocol Components Name	""	""	""	""	""	""	""	""
Study Protocol Components Type	""	""	""	""	""	""	""	""
Study Protocol Components Type Term Accession Number	""	""	""	""	""	""	""	""
Study Protocol Components Type Term Source REF	""	""	""	""	""	""	""	""
```

**STUDY CONTACTS**

This section MUST contain zero or more values.

This section MUST contain the following labels, with the specified datatypes for values supported:

| abel                                     | Datatype                                                                                    | Description                                                                                 |
|------------------------------------------|---------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Study Person Last Name                   | String                                                                                      | The last name of a person associated with the study.                                                                                      |
| Study Person First Name                  | String                                                                                      | Study Person Name                                                                                        |
| Study Person Mid Initials                | String                                                                                      | The middle initials of a person associated with the study.                                                                              
|
| Study Person Email                       | String formatted as email                                                                   | The email address of a person associated with the study.                                                                                      |
| Study Person Phone                       | String                                                                                      | The telephone number of a person associated with the study.                                                                                      |
| IStudy Person Fax                        | String                                                                                      | The fax number of a person associated with the study.                                                                                      |
| Study Person Address                     | String                                                                                      | The address of a person associated with the study.                                                                                      |
| Study Person Affiliation                 | String                                                                                      | The organization affiliation for a person associated with the study.                                                                                      |
| Study Person Roles                       | String or Ontology Annotation if accompanied by Term Accession Numbers and Term Source REFs | Term to classify the role(s) performed by this person in the context of the study, which means that the roles reported here need not correspond to roles held withing their affiliated organization. Multiple annotations or values attached to one person can be provided by using a semicolon (“;”) Unicode (U0003+B) as a separator (e.g.: submitter;funder;sponsor) .The term can be free text or from, for example, a controlled vocabulary or an ontology. If the latter source is used the Term Accession Number and Term Source REF fields below are required. |
| Study Person Roles Term Accession Number | String                                                                                      | The accession number from the Term Source associated with the selected term.                                                                                       |
| Study Person Roles Term Source REF       | String                                                                                      | Identifies the controlled vocabulary or ontology that this term comes from. The Source REF has to match one of the Term Source Names declared in the Ontology Source Reference section.                                                                                    |

For example, the `STUDY CONTACTS` section of an ISA-XLSX `isa.investigation.xlsx` file may look as follows:

```default
Study Person Last Name	"Gilbert"	"Field"	"Huang"	"Edwards"	"Li"	"Gilna"	"Joint"
Study Person First Name	"Jack"	"Dawn"	"Ying"	"Rob"	"Weizhong"	"Paul"	"Ian"
Study Person Mid Initials	"A"	""	""	""	""	""	""
Study Person Email	"jagi@pml.ac.uk"	""	""	""	""	""	""
Study Person Phone	""	""	""	""	""	""	""
Study Person Fax	""	""	""	""	""	""	""
Study Person Address	"Prospect Place, Plymouth, United Kingdom"	"CEH Oxford, Oxford, United Kingdom"	"San Diego State University, San Diego, California, United States of America"	"Argonne National Laboratory, Argonne, Illinois, United States of America"	"San Diego State University, San Diego, California, United States of America"	"San Diego State University, San Diego, California, United States of America"	"Prospect Place, Plymouth, United Kingdom"
Study Person Affiliation	"Plymouth Marine Laboratory"	"NERC Centre for Ecology and Hydrology"	"California Institute for Telecommunications and Information Technology"	"Department of Computer Science, Mathematics and Computer Science Division,"	"California Institute for Telecommunications and Information Technology"	"California Institute for Telecommunications and Information Technology"	"Plymouth Marine Laboratory"
Study Person Roles	"principal investigator role;SRA Inform On Status;SRA Inform On Error"	"principal investigator role"	"principal investigator role"	"principal investigator role"	"principal investigator role"	"principal investigator role"	"principal investigator role"
Study Person Roles Term Accession Number	";;"	""	""	""	""	""	""
Study Person Roles Term Source REF	";;"	""	""	""	""	""	""
```

### Assay section

This section is organized in several subsections, described in detail below. The subsections in the block are arranged vertically; the intent being to enhance readability and presentation, and possibly to help with parsing. These subsections MUST remain within
this block; the fields MUST remain within their subsection.

These sections implement the metadata for an `Assay` from the ISA Abstract Model.

**ASSAY**

This section MUST contain zero or one values.

This section MUST contain the following labels, with the specified datatypes for values supported:


| Label                                              | Datatype   | Description                                                                                                                                                                                                                                                                                                         |
|----------------------------------------------------|------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Assay Measurement Type                       | String     | A term to qualify the endpoint, or what is being measured (e.g. gene expression profiling or protein identification). The term can be free text or from, for example, a controlled vocabulary or an ontology. If the latter source is used the Term Accession Number and Term Source REF fields below are required. |
| Study Assay Measurement Type Term Accession Number | String     | The accession number from the Term Source associated with the selected term.                                                                                                                                                                                                                                        |
| Assay Measurement Type Term Source REF       | String     | The Source REF has to match one of the Term Source Name declared in the Ontology Source Reference section.                                                                                                                                                                                                          |
| Assay Technology Type                        | String     | Term to identify the technology used to perform the measurement, e.g. DNA microarray, mass spectrometry. The term can be free text or from, for example, a controlled vocabulary or an ontology. If the latter source is used the Term Accession Number and Term Source REF fields below are required.              |
| Assay Technology Type Term Accession Number  | String     | The accession number from the Term Source associated with the selected term.                                                                                                                                                                                                                                        |
| Assay Technology Type Term Source REF        | String     | Identifies the controlled vocabulary or ontology that this term comes from. The Source REF has to match one of the Term Source Names declared in the Ontology Source Reference section.                                                                                                                             |
| Assay Technology Platform                    | String     | Manufacturer and platform name, e.g. Bruker AVANCE                                                                                                                                                                                                                                                                  |
| Assay File Name                              | String     | A field to specify the name of the Assay Table file corresponding the definition of that assay. There can be only one file per cell.                                                                                                                                                                                |

For example, the `ASSAY` section of an ISA-XLSX `isa.assay.xlsx` file may look as follows:

```default
ASSAY
Study Assay File Name	"assays/gilbert-Gx/isa.assay.xlsx"	"assays/gilbert-Tx/isa.assay.xlsx"
Study Assay Measurement Type	"metagenome sequencing"	"transcription profiling"
Study Assay Measurement Type Term Accession Number	""	""
Study Assay Measurement Type Term Source REF	"OBI"	"OBI"
Study Assay Technology Type	"nucleotide sequencing"	"nucleotide sequencing"
Study Assay Technology Type Term Accession Number	""	""
Study Assay Technology Type Term Source REF	"OBI"	"OBI"
Study Assay Technology Platform	"454 GS FLX"	"454 GS FLX"
```

**ASSAY PERFORMERS**

This section MUST contain zero or more values.

This section MUST contain the following labels, with the specified datatypes for values supported:

| Label                                     | Datatype                                                                                    | Description                                                                                 |
|------------------------------------------|---------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Assay Person Last Name                   | String                                                                                      | The last name of a person associated with the Assay.                                                                                      |
| Assay Person First Name                  | String                                                                                      | Assay Person Name                                                                                        |
| Assay Person Mid Initials                | String                                                                                      | The middle initials of a person associated with the Assay.                                                                              
|
| Assay Person Email                       | String formatted as email                                                                   | The email address of a person associated with the Assay.                                                                                      |
| Assay Person Phone                       | String                                                                                      | The telephone number of a person associated with the Assay.                                                                                      |
| Assay Person Fax                        | String                                                                                      | The fax number of a person associated with the assay.                                                                                      |
| Assay Person Address                     | String                                                                                      | The address of a person associated with the assay.                                                                                      |
| Assay Person Affiliation                 | String                                                                                      | The organization affiliation for a person associated with the assay.                                                                                      |
| Assay Person Roles                       | String or Ontology Annotation if accompanied by Term Accession Numbers and Term Source REFs | Term to classify the role(s) performed by this person in the context of the assay, which means that the roles reported here need not correspond to roles held withing their affiliated organization. Multiple annotations or values attached to one person can be provided by using a semicolon (“;”) Unicode (U0003+B) as a separator (e.g.: submitter;funder;sponsor) .The term can be free text or from, for example, a controlled vocabulary or an ontology. If the latter source is used the Term Accession Number and Term Source REF fields below are required. |
| Assay Person Roles Term Accession Number | String                                                                                      | The accession number from the Term Source associated with the selected term.                                                                                       |
| Assay Person Roles Term Source REF       | String                                                                                      | Identifies the controlled vocabulary or ontology that this term comes from. The Source REF has to match one of the Term Source Names declared in the Ontology Source Reference section.                                                                                    |

For example, the `ASSAY PERFORMERS` section of an ISA-XLSX `isa.assay.xlsx` file may look as follows:

```default
Assay Person Last Name	"Gilbert"	"Field"	"Huang"	"Edwards"	"Li"	"Gilna"	"Joint"
Assay Person First Name	"Jack"	"Dawn"	"Ying"	"Rob"	"Weizhong"	"Paul"	"Ian"
Assay Person Mid Initials	"A"	""	""	""	""	""	""
Assay Person Email	"jagi@pml.ac.uk"	""	""	""	""	""	""
Assay Person Phone	""	""	""	""	""	""	""
Assay Person Fax	""	""	""	""	""	""	""
Assay Person Address	"Prospect Place, Plymouth, United Kingdom"	"CEH Oxford, Oxford, United Kingdom"	"San Diego State University, San Diego, California, United States of America"	"Argonne National Laboratory, Argonne, Illinois, United States of America"	"San Diego State University, San Diego, California, United States of America"	"San Diego State University, San Diego, California, United States of America"	"Prospect Place, Plymouth, United Kingdom"
Assay Person Affiliation	"Plymouth Marine Laboratory"	"NERC Centre for Ecology and Hydrology"	"California Institute for Telecommunications and Information Technology"	"Department of Computer Science, Mathematics and Computer Science Division,"	"California Institute for Telecommunications and Information Technology"	"California Institute for Telecommunications and Information Technology"	"Plymouth Marine Laboratory"
Assay Person Roles	"principal investigator role;SRA Inform On Status;SRA Inform On Error"	"principal investigator role"	"principal investigator role"	"principal investigator role"	"principal investigator role"	"principal investigator role"	"principal investigator role"
Assay Person Roles Term Accession Number	";;"	""	""	""	""	""	""
Assay Person Roles Term Source REF	";;"	""	""	""	""	""	""
```

## Annotation Table sheets

In the `Annotation Table sheets`, column headers MUST have the first letter of each word in upper case, with the exception of the referencing label (REF).

The content of the annotation table MUST be placed in an `xlsx table` whose name starts with `annotationTable`. Each sheet MUST contain at most one such annotation table. Only cells inside this table are considered as part of the formatted metadata.

`Annotation Table sheets` are structured with fields organized on a per-row basis. The first row MUST be used for column headers. Each body row is an implementation of a `Process` node.

### Inputs and Outputs

Each annotation table sheet MUST contain an `Input` and an `Output` column, which denote the Input and Output node of the `Process` node respectively. They MUST be formatted in the pattern `Input [<InputNodeType>]`.


A `Source` MUST be indicated with the node type `Source Name`. `Sources` MUST not be used as `Output` nodes.

A `Sample` MUST be indicated with the node type `Sample Name`.

An `Extract Material` MUST be indicated with the node type `Extract Name`.

An `Labeled Extract Material` MUST be indicated with the node type `Labeled Extract Name`.

`Source Names`, `Sample Names`, `Extract Names` and `Labeled Extract Names` MUST be unique across an ARC. If two of these entities with the same name exist in the same ARC, they are considered the same entity.

`Image File`, `Raw Data File` or `Derived Data File` node types MUST correspond to a relevant `Data` node to provide names or URIs of file locations. 

### Protocol Columns

`Protocol REF` columns MAY be used to specify the name of the `Protocol` node implemented by the `Process` node. Per Annotation Table sheet there MUST be at most one `Protocol REF` column. The value MUST be free text.

`Protocol Version` columns MAY be used to specify the version of the `Protocol` node implemented by the `Process` node. Per Annotation Table sheet there MUST be at most one `Protocol REF` column. The value MUST be free text.

`Protocol Description` columns MAY be used to specify the description of the `Protocol` node implemented by the `Process` node. Per Annotation Table sheet there MUST be at most one `Protocol REF` column. The value MUST be free text.

`Protocol Type` columns MAY be used to specify the type of the `Protocol` node implemented by the `Process` node. Per Annotation Table sheet there MUST be at most one `Protocol REF` column. The value MUST be free text, or an `Ontology Annotation`.

### Ontology Annotations

Where a value is an `Ontology Annotation` in a table file, `Term Accession Number` and `Term Source REF` fields MUST follow the column cell in which the value is entered. These two columns SHOULD contain further ontological information about the header. In this case, following the static header string, separated by a sinlge space, there MUST be a short ontology term identifier formatted as CURIEs (prefixed identifiers) of the form `<IDSPACE>:<LOCALID>` (specified [here](http://obofoundry.org/id-policy)) inside `()` brackets.
For example, a characteristic type `organism` with a value of `Homo sapiens` can be qualified with an `Ontology Annotation` of a term from NCBI Taxonomy as follows:

| Characteristics [organism]   | Term Source REF (OBI_0100026)  | Term Accession Number (OBI_0100026) |
|-----------------------------|-------------------|------------------------------------------------------|
| Homo sapiens                | NCBITaxon         | [http://…/NCBITAXON/9606](http://.../NCBITAXON/9606) |

An `Ontology Annotation` MAY be applied to any appropriate `Characteristic`, `Parameter`, `Factor`, `Component` or `Protocol Type`.

This implements `Ontology Annotation` from the ISA Abstract Model.

### Unit

Where a value is numeric, a `Unit` MAY be used to qualify the quantity. In this case, following the column in which a `Unit`
is used, a `Unit` heading MUST be present, and MAY be further annotated as an `Ontology Annotation`.

For example, to qualify the value `300` with a `Unit` `Kelvin` qualified as an `Ontology Annotation` from the Units Ontology declared
in the Ontology Sources with `UO`:

|   Parameter [temperature] | Unit   | Term Source REF (PATO:0000146)  | Term Accession Number (PATO:0000146)  |
|--------------------------------|--------|-------------------|------------------------------------------------------|
|                            300 | Kelvin | UO                | [http://…/obo/UO_0000012](http://.../obo/UO_0000012) |



### Characteristics

`Characteristics` are used as an attribute column following `Sources` and `Samples`. This column contains terms describing each material according to the characteristics category indicated in the column header in the pattern `Characteristic [<category term>]`.
For example, a column header `Characteristic [organ part]` would contain terms describing an organ part. `Characteristic` SHOULD be used as an attribute column following `Input [Source Name]`, or `Input [Sample Name]`. The value MUST be free text, numeric, or an `Ontology Annotation`.

For example, a characteristic type Organism with a value of Homo sapiens can be qualified with an Ontology Annotation of a term from NCBI Taxonomy as follows:

| Characteristic [organ part]   | Term Source REF (UBERON:0000064)  | Term Accession Number (UBERON:0000064)  |
|-------------------------------|-------------------|-------------------------|
| Liver                         | MeSH              | D008099                 |

### Factors

A `Factor` is an independent variable manipulated by an experimentalist with the intention to affect biological systems in a way that can be measured by an assay. This field holds the actual data for the `Factor` named between the
square brackets (as declared in the `Study Factors` section of a top-level metadata sheet) so MUST match; for example, `Factor [compound]`. The value MUST be free text, numeric, or an `Ontology Annotation`.

| Factor [Gender]   | Term Source REF (NCIT:C17357)  | Term Accession Number (NCIT:C17357)  |
|------------------------|-------------------|-------------------------|
| Male                   | MeSH              | D008297                 |


### Components

A `Component` is a consumable or reusable physical entity used in the experimental workflow. It is formatted in the pattern `Component [<category term>]`. The value MUST be free text, numeric, or an `Ontology Annotation`.

| Component [Measurement Device]   | Term Source REF (NCIT_C81182)  | Term Accession Number (NCIT_C81182)  |
|------------------------|-------------------|-------------------------|
| Illumina MiniSeq                   | OBI              | [http://…/obo/OBI_0003114](http://purl.obolibrary.org/obo/OBI_0003114)                 |

### Parameters

`Parameters` are all additional information about the experimental setup, that do not fall under the aformentioned 3 categories. It is formatted in the pattern `Parameter [<category term>]`. The value MUST be free text, numeric, or an `Ontology Annotation`.

| Parameter [time] | Unit   | Term Source REF (PATO_0000165)  | Term Accession Number (PATO:0000165)  |
|--------------------------------|--------|-------------------|------------------------------------------------------|
|                            300 | Kelvin | UO                | [http://…/obo/UO_0000032](http://purl.obolibrary.org/obo/UO_0000032) |

#### Examples

For example, a simple source to sample may be represented as:

| Source Name   | Protocol REF      | Sample Name   |
|---------------|-------------------|---------------|
| source1       | sample collection | sample1       |

Where a graph splits or pools, we use the `Name` column to represent the same nodes.

For example, if we split a source into two samples, we  might represent this as:

| Source Name   | Protocol REF      | Sample Name   |
|---------------|-------------------|---------------|
| source1       | sample collection | sample1       |
| source1       | sample collection | sample2       |

If we pool two sources into a single sample, we might represent this as:

| Source Name   | Protocol REF      | Sample Name   |
|---------------|-------------------|---------------|
| source1       | sample collection | sample1       |
| source2       | sample collection | sample1       |

## Investigation File

The Investigation file fulfils four needs:

1. to declare key entities, such as factors, protocols, which may be referenced in the other files
2. to track provenance of the terminologies (controlled vocabularies or ontologies) there are used, where applicable
3. to relate Assay files to Studies
4. to relate each Study file to an Investigation (this only becomes necessary when two or more Study files need to be grouped).

The `Investigation File` MUST contain one `Top-Level Metadata sheet`. This sheet MUST be named `isa_investigation` and MUST contain the following sections:

- `ONTOLOGY SOURCE REFERENCE`
- `INVESTIGATION`
- `INVESTIGATION PUBLICATIONS`
- `INVESTIGATION CONTACTS`
- `STUDY`
- `STUDY DESIGN DESCRIPTORS`
- `STUDY PUBLICATIONS`
- `STUDY FACTORS`
- `STUDY ASSAYS`
- `STUDY PROTOCOLS`
- `STUDY CONTACTS`

The `Investigation File` implements the `Investigation` graph from the ISA Abstract Model.

## Study File

The `Study` represents a set of logically connected experiments. A `Study File` contains contextualising information for one or more `Assays`, metadata about the study design, study factors used, and study protocols, as well as information similarly to the Investigation including title and description of the study, and related people and scholarly publications, but also details the sample collection process needed to perform the connected `Assays`.

The `Study File` MUST contain one `Top-Level Metadata sheet`. This sheet MUST be named `isa_study` and MUST contain the following sections:

- `STUDY`
- `STUDY DESIGN DESCRIPTORS`
- `STUDY PUBLICATIONS`
- `STUDY FACTORS`
- `STUDY ASSAYS`
- `STUDY PROTOCOLS`
- `STUDY CONTACTS`

Additionally, the `Study File` SHOULD contain one or more `Annotation Table sheets`, which record provenance of biological samples, from source material through a collection process to sample material.

Therefore, the main entities of the `Study File` should be `Sources` and `Samples`.

The `Study File` implements the `Study` graph from the ISA Abstract Model.

## Assay File

The `Assay` represents one experimental measurement. An `Assay File` metadata about the assay design, information about the people performing the experiment, and most importantly, details about the preparation execution of the experimental measurement.

The `Assay File` MUST contain one `Top-Level Metadata sheet`. This sheet MUST be named `isa_assay` and MUST contain the following sections:

- `ASSAY`
- `ASSAY PERFORMERS`

Additionally, the `Assay File` SHOULD contain one or more `Annotation Table sheets`, which record preparation of biological samples, measurement of these samples and basic computations performed on the resulting data.

Therefore, the main entities of the `Assay File` should be `Samples` and `Data`.

The `Assay File` implements the `Assay` graph from the ISA Abstract Model.
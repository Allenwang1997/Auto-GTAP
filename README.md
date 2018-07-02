# Auto-GTAP Read Me

Auto-GTAP project is a project to create a modern cross-platform project format for CGE research.

## Overview

In principle, a GTAP simulation can be run with a single command. However, the reality is that the process tends to be much more complicated. A typical GTAP-based research project will need to build balance a database, calculate shocks, and shuffle around various files at each stage, in addition to running the simulation itself, all before finally exporting simulation results.

While the simulation is an automated process, these ambient task require require user interaction. Auto-GTAP aims to provide a unified framework to lift these ambient tasks into the build toolchain. The goal is to increase the speed and replicability of GTAP-based analyses, by reducing the amount of manual orchestration required historically.

## Why Auto-GTAP?

The Global Trade Analysis Project (GTAP) model is frequently used to estimate the effect of government policies on international trade. However, the biggest advantage of the GTAP model is not the original model itself, but the ecosystem around it. The original version introduced in 1995 has been updated to [version 7](https://jgea.org/resources/jgea/ojs/index.php/jgea/article/view/47) and contributors have developed other versions of it focusing on topics such as energy energy (GTAP-E), biofuels (GTAP-BIO), and land use (GTAP-AEZ). Perhaps the greatest advantage of the GTAP model is data availability. GTAP (the orginization behidn the GTAP model) also provides detailed and regularly updated databases of the world economy. As a result of these tools and data, many non-GTAP models are built using the [GTAP database](https://www.gtap.agecon.purdue.edu/about/data_models.asp).

As a result of the popularity of the GTAP model and database, developers have created a number of software tools for dealing with the anciliary issues that crop up in these research projects, especially with databases. There are tools automating the process of data [aggregation](https://www.gtap.agecon.purdue.edu/products/packages.asp) (GTPAg2), [disaggregation](https://www.gtap.agecon.purdue.edu/resources/splitcom.asp) (SplitCom), revision (GTAP-Adjust and [AlterTax](https://www.copsmodels.com/webhelp/rungtap/index.html?hc_altertax.htm)). The existence of these tools makes it easy for developers to customize the model for their specific project, as they do not have to reinvent the wheel.

However, some parts of a GTAP-based research have not been automated. In particular, there is no overarching framework controlling both the model and all these tools: the process of running the tools, specifiying their settings, and moving the output to the input of other tools must all be done manually.

Until now. Auto-GTAP provides a unified framework for running all parts of a GTAP-based research project.

## Getting started

### Prerequisites

TODO: describe the environment

Mandatory:
-Python
-pyyaml

Optional (but required for example)
-GEMPACK (requires license)
-Raw GTAP Data
 
 
### Clone the repository 
 
 ```bash
cd your_project_directory

git clone https://github.com/andre-barbe/Auto-GTAP.git
```

### Create a Python virtual environment
 
```bash
python -m venv venv 
```

### Initialize the workspace

```bash
./setup.ps1
```

-Create WorkFiles folder
-Put Raw GTAP Data in subfolder of InputFiles for your aggregation program

## Example projects

- [Productivity Increase](examples/productivity_increase)

## Documentation

- [Components of Auto-GTAP](docs/components-of-auto-gtap.md)

## References

- [Corong et al. 2017](https://jgea.org/resources/jgea/ojs/index.php/jgea/article/view/47)
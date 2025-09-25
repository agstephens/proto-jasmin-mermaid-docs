# proto-jasmin-mermaid-docs

Here are some prototype JASMIN mermaid docs. All components are in this single MarkDown file at the moment. The idea is that there are various Mermaid Flowcharts that link to different parts of the docs, and to other flowcharts.


**Note about internal links:**
I haven't worked out how to use internal links within Mermaid `href` elements so I'm using the full URL to this page for now: https://github.com/agstephens/proto-jasmin-mermaid-docs/blob/main/README.md

# Managing a Python Workflow on JASMIN - starting with a Jupyter Notebook

Users will often start their journey with a Python script (`*.py`) or Jupyter Notebook (`*.ipynb`). They will typically do exploratory work using the [JASMIN Notebook Service](https://help.jasmin.ac.uk/docs/interactive-computing/jasmin-notebooks-service/), and then may scale up their workflow by migrating to the Slurm cluster (using the ORCHID partition in the case of GPU/ML work). This flowchart is designed to help you understand the various stages that are involved in setting up, testing, running and scaling a scientific workflow on JASMIN.

```mermaid
---
config:
  theme: 'default'
  themeVariables:
    fontSize: 12pt
---
 flowchart TD
    START --> PY_IPYNB{User has Python script or Jupyter Notebook file}

    C1@{ shape: brace-r, label: "<b>Prerequesites</b>:
        User has <a href='http://help.jasmin.ac.uk/docs/getting-started/get-login-account/'>jasmin-login</a> 
        and <a href='https://help.jasmin.ac.uk/docs/batch-computing/orchid-gpu-cluster/#request-access-to-orchid'>orchid</a> roles" } ~~~ PY_IPYNB

    PY_IPYNB -->|'.ipynb' file| START_NBS[<a href="https://help.jasmin.ac.uk/docs/interactive-computing/jasmin-notebooks-service/#using-the-jasmin-notebook-service">Start Notebook Service</a>]
    PY_IPYNB -->|'.py' file| CONVERT_PY[Convert to Ipython Notebook]

    PY_IPYNB ~~~ C2@{ shape: brace-l, label: "Simple method: paste sections of Python script into Notebook cells"}

    CONVERT_PY --> START_NBS
    START_NBS ~~~ C3@{ shape: brace-r, label: "Plan data inputs and outputs.<br/>Do you have space to write your data files?"}
    
    START_NBS --> DATA_NEEDS[<a href="https://github.com/agstephens/proto-jasmin-mermaid-docs/blob/main/README.md#managing-data-access">Manage Data Requirements</a><br/>E.g. CEDA Archive, GWS, external access]

    DATA_NEEDS --> SW_NEEDS{<a href="https://github.com/agstephens/proto-jasmin-mermaid-docs/blob/main/README.md#software-management">Options for managing software needs</a>}

    SW_NEEDS -->|Use built-in Jaspy environment with no modifications| TEST_RUN[Test run workflow with small data volume]
    SW_NEEDS -->|Plan to build a local Python virtual environment| VENV_INSTALL[<a href="https://github.com/agstephens/proto-jasmin-mermaid-docs/blob/main/README.md#building-virtual-environments">Install and build a Python virtual environment</a>]
    SW_NEEDS -->|Plan to use Dask-Gateway and will build a local Conda environment| CONDA_INSTALL[<a href="https://github.com/agstephens/proto-jasmin-mermaid-docs/blob/main/README.md#using-dask-gateway">Install and build a Conda environment for Dask-Gateway</a>]

    DATA_NEEDS ~~~ C4@{ shape: brace-l, label: "<b>WARNING!</b><br/><a href='https://github.com/agstephens/proto-jasmin-mermaid-docs/blob/main/README.md#managing-your-home-directory'>Check your HOME directory<br/>doesn't fill up!</a>"}
    VENV_INSTALL --> TEST_RUN

    TEST_RUN --> FULL_RUN{Is Notebook Service suitable for the full workflow?}

    C5@{ shape: brace-r, label: "<b>Test and iterate - consider:</b>
    - Is data I/O efficient?
    - Is GPU being utilised (if required)
    - Is GPU/CUDA usage optimised (if required)
    - Are local disk read/writes optimised?"} ~~~ FULL_RUN

    TEST_RUN ~~~ C6@{ shape: brace-l, label: "**Notebook Service has limited resource**
    - Migrate to batch system (LOTUS/ORCHID)?
    - Convert to using Dask-Gateway (with Conda env)?
    - Migrate to alternative platform (e.g. ISAMBARD-AI)?"}

    FULL_RUN -->|Yes| COMPLETE[<a href="https://github.com/agstephens/proto-jasmin-mermaid-docs/blob/main/README.md#workflow-completion">Complete the workflow and tidy up</a>]
    FULL_RUN -->|No| MIGRATE[<a href="https://github.com/agstephens/proto-jasmin-mermaid-docs/blob/main/README.md#workflow-migration">Migrate workflow to LOTUS or alternative platform</a>]
```

---

## Managing Data Access

When working with data on JASMIN you may need to access scientific data from multiple sources, including:
- The CEDA Archive (reading files locally)
- JASMIN Group Workspaces (reading files locally)
- Data held on Object Store or other locations
- Scratch Disk
- External sources

To optimise your workflows, it is often useful to set up _data reader_ functions or classes that receive your data requirements (e.g. experiment, variable, temporal range, spatial selection) and return either a list/iterator of file paths or data objects (such as `xarray Dataset`, `cfpython FieldLists` or `iris Cubes`).

### Setting up data readers

**Internal notes...that we could build on...:**
- use a common approach to various packages
- local (`/badc`) vs remote (`https`) access
- Usability on ISAMBARD AI and CoLab, as well as JASMIN
- Generic approaches to loading/templating
- Applications/mapping to Machine Learning Data Loaders in common packages (`pytorch, tensorflow, JAX`)
- Potential use of CEDA DataPoint
- Delayed (_lazy_) loading of the actual data until it is needed
- Loading of different feature types:
  - 7D data all the way down to 1D data
  - In tools like `xarray` and `cfpython`:
    - this would involve adding in new dimensions and concatenating along them.
    - this would only work if `t, z, y, x` are identical - so might be irrelevant for much of CMIP.

---

## Software Management

Managing software environments on JASMIN can be confusing unless you clearly understand some of the key distinctions. This section tells you what you need to know in order to create and build environments that will work on the various JASMIN systems:
1. JASMIN Notebook Service:
   - CPU-based - standard
   - CPU-based - with Dask-Gateway for parallel scaling
   - GPU-based - for Machine Learning and CUDA-optimised code
2. Scientific Analysis Servers and Batch System (LOTUS):
   - CPU-based - `sci` servers and main LOTUS cluster
   - GPU-based - GPU interactive node and ORCHID cluster - for Machine Learning and CUDA-optimised code

```mermaid
---
  theme: 'default'
  themeVariables:
    fontSize: 9pt
---
flowchart TD
    NEED[Need software on JASMIN] --> REQS

    REQS[<a href="https://github.com/agstephens/proto-jasmin-mermaid-docs/blob/main/README.md#managing-your-dependencies-using-a-requirements-file">Capture software dependencies</a>]

    REQS --> JNS[Using JASMIN Notebook Service or<br/> servers #40;<code>sci</code> servers / LOTUS#41;]

    JNS -->|Yes| DASK{Planning to use Dask-Gateway<br/>with Conda environment?}

    USE_DASK[<a href="https://github.com/agstephens/proto-jasmin-mermaid-docs/blob/main/README.md#using-dask-gateway">See instructions on Dask-Gateway</a>]
    DASK -->|Yes| USE_DASK
    DASK -->|No| GPU_JNS{Do you need access to GPUs?<br/>#40;For Machine Learning / CUDA#41;}

    GPU_JNS -->|Yes| START_JNS_GPU[Start Notebook Service with GPUs]
    GPU_JNS -->|No| START_JNS_CPU[Start Notebook Service with CPUs]

    START_JNS_GPU --> CHECK_GPU[Check access to GPUs]

    JNS_BASH[Start Bash terminal in Notebook Service]

    CHECK_GPU --> JNS_BASH    
    START_JNS_CPU --> JNS_BASH

    JNS_BASH --> VENV_JNS[<a href="">Create virtual environment in Bash session</a>]
    VENV_JNS --> KERNEL[<a href="">Create IPython Kernel and install it</a>]
    KERNEL --> RELOAD[Reload page #40;by refreshing browser#41;]

    RELOAD --> LAUNCH_NB[Start the Notebook Launcher and select your new kernel]
    LAUNCH_NB --> TEST_IMP_JNS[Test software imports]

    TEST_IMP_JNS --> RUN_NB[Run the Jupyter Notebook]

    JNS -->|No| GPU_SCI{Do you need access to GPUs?<br/>#40;For Machine Learning / CUDA#41;}
    GPU_SCI -->|Yes| LOGIN_GPU[Login to interactive GPU node]
    GPU_SCI -->|No| LOGIN_CPU[Login to <code>sci</code> server]

    LOGIN_GPU --> JASPY_BASE[Assume software to be built on<br/>top of <a href="https://help.jasmin.ac.uk/docs/software-on-jasmin/jaspy-envs/"><code>Jaspy</code> environment<a/>]
    JASPY_BASE --> _1[#darr;] --> _2[#darr;] --> VENV_SCI[<a href="">Create virtual environment in Bash session</a>]

    VENV_SCI --> _3[#darr;] --> _4[#darr;] --> _5[#darr;] --> TEST_IMP_SCI[Test software imports]
    TEST_IMP_SCI --> RUN_SCI[Run the workflow]

    JNS_BASH ~~~ C1@{ shape: braces, label: "NOTE: Special <code>pip</code> command<br/>to avoid <code>~/.local</code> directory" }
    TEST_IMP_SCI ~~~ C2@{ shape: brace-l, label: "You may need to<br/><a href="https://github.com/agstephens/proto-jasmin-mermaid-docs/blob/main/README.md#workflow-migration">migrate to Slurm</a>"}

```

### Python Best Practice

This sections outlines some best practice advice for how you write, structure, test, publish and deploy Python packages. These are based on sound guidelines for code reusability and sharing.

...more here...including:
- Refactoring a Python script/notebook into a script and a library
- Running a Python script with inputs from:
  - The command-line
  - Configuration files
  - Environment variables
- Structuring your code for re-use and sharing
- Managing your software dependencies
  - Using `requirements` files
    - simple...to...advanced
- Using GitHub for tracing, testing, sharing, publication
- Publishing to PyPI

### Managing Software Dependencies

Most scripts and notebooks will import software packages or libraries. In the case of Python, some libraries are provided as part of the [Python Standard Library](https://docs.python.org/library/index.html) (such as `math` and `os`). However, scientific work typically uses many external open-source libraries (such as `pandas` and `numpy`).

In order to make your code reproducible and sharable, we strongly advise that you record your software dependencies using `requirements` files, as discussed below.

#### Managing your dependencies using a "requirements" file

The simplest way to package up your software dependencies is to list them in a `requirements.txt` file, such as:

```bash
$ cat requirements.txt
numpy
pandas
sklearn
```

The environment can then be installed with a single `pip` command:

```bash
$ pip install -r requirements.txt
```
##### Advanced and reusable use of "requirements" files

...more info here about `pip compile` etc...


### Building Virtual Environments

...what python venvs are...how to build them...etc

## Using Dask-Gateway

...overview...

### Building Conda Environments for use with Dask-Gateway

...how to setup a conda env that will work across the Notebook and Sci/Batch estates seamlessly...

---

## Managing Data Workflows on JASMIN

When building a data workflow on 

### Workflow Migration

Many users will develop a workflow in a Jupyter Notebook and scale it up on to the LOTUS cluster. In the case of Machine Learning workflows, they will also require use of the GPU-nodes on LOTUS, known as ORCHID. This flowchart helps you navigate the various stages required to move from a single Notebook file through to a large-scale deployed and completed workflow.

```mermaid
---
config:
  theme: 'default'
  themeVariables:
    fontSize: 9pt
---
flowchart TD
    NB[<a href="https://github.com/agstephens/proto-jasmin-mermaid-docs/blob/main/README.md#python-best-practice">Convert Jupyter Notebook to a Python script and library</a>]

    NB --> CODE_READY[Code refactored into a script and library of reusable components]

    NB ~~~ C1@{ shape: brace-l, label: "Factor out changeable settings to</b>:
        - command-line arguments
        - configuration files"}

    CODE_READY --> DEPS[<a href="https://github.com/agstephens/proto-jasmin-mermaid-docs/blob/main/README.md#managing-software-dependencies">Capture software dependencies</a>]

    CODE_READY ~~~ C2@{ shape: brace-l, label: "'requirements.txt' file<br/>listing dependencies"}

    CODE_READY --> GPU_REQ[Do you require GPUs?]

    GPU_REQ -->|No| CPU_NODE[Create environment on <code>sci</code> server] --> WRAPPER
    GPU_REQ -->|Yes| GPU_NODE[Login to interactive GPU node<br/>to create GPU-aware environment] --> WRAPPER

    WRAPPER[Write Bash wrapper script:<br/><code>setup-env.sh</code>] --> TEST_RUN[Run 1 iteration on Slurm node]

    WRAPPER ~~~ C2@{ shape: brace-r, label: "<b>Best practice considerations:</b>
    - Implement restarts
    - Avoid re-work
    - Save results
    - Employ <i>map-reduce</i> pattern
    - Use Slurm Job Arrays
    - Use multiple GPUs (if relevant)
    - Optimise use of GPUs (if relevant)"}

    TEST_RUN --> REFINE[Refine resource needs #40;per job#41;:
    - Duration, CPU, Memory, GPU, exclusive/shared node]

    TEST_RUN ~~~ C3@{ shape: brace-l, label: "Accurate resource requests<br/>mean your <b>jobs run quicker!</b>"}

    REFINE --> FULL_RUN[Submit and run entire workflow]

    FULL_RUN -->|Yes| COMPLETE[<a href="https://github.com/agstephens/proto-jasmin-mermaid-docs/blob/main/README.md#workflow-completion">Complete the workflow and tidy up</a>]

```

### Workflow Completion

Once you have completed your workflow on JASMIN, there are a number of possible follow-up tasks that you should consider:
- Publish your code to:
  - A GitHub (or other) public/private repository
  - PyPI
- Publish your results to:
  - A scientific journal
  - A blog post
- Publish data data to:
  - The CEDA Archive
  - Another data catalogue/repository
- Publish your Machine Learning model (if relevant) to:
  - HuggingFace
- Deploy your model/algorithm as an application/service:
  - On JASMIN
  - To the Cloud
 
Additionally, we strongly encourage you to _tidy up_ the content that remain on JASMIN, which might include:
- local software environments/packages
- temporary and cache files
- data stored on `scratch` disk or GWSs
- data stored on Object Store or in the Transfer Cache
- Others???

## Managing your HOME directory

Your `$HOME` directory has a quota of 100GB, but users often fill this up. When you home directory is full, you may see strange behaviours on JASMIN that do not immediately indicate the problem is that you have exceeded your quota. Although _data_ is the common cause of exceedence, modern software installations can also be many GBs in size. In particularly, ML packages such as `pytorch` and `tensorflow` can severely bloat a software environment.

### Checking your $HOME directory usage

To check your current `$HOME` directory usage, on a `sci` server, type:

```bash
pdu -sh $HOME
``` 

### What is filling up your $HOME directory?

Here are some common locations within your `$HOME` directory where large files may be found:
- `.local/lib*/python*/site-packages` (NOTE: the `*` represent wild-cards, you may have multiple instances of each)
- `.miniconda`
- `miniconda`
- `.conda`
- `conda`
- large downloads like the `Miniconda` installation file
- other packages that have been installed under `dot` directories: `~/.*`

### Tips for clearing space in your $HOME directory

- Can you move data from your `$HOME` directory to a Group Workspace?
- Can you move large code installations to a [_Small-files_ Group Workspace](https://help.jasmin.ac.uk/docs/short-term-project-storage/faqs-storage/#2-issues-with-small-files)? 

# proto-jasmin-mermaid-docs

Here are some prototype JASMIN mermaid docs. All components are in this single MarkDown file at the moment. The idea is that there are various Mermaid Flowcharts that link to different parts of the docs, and to other flowcharts.

**Note about internal links:**
I haven't worked out how to use internal links within Mermaid `href` elements so I'm using the full URL to this page for now: https://github.com/agstephens/proto-jasmin-mermaid-docs/blob/main/README.md

# Managing a Python Workflow on JASMIN - starting with a Jupyter Notebook

Users will often start their journey with a Python script (`*.py`) or Jupyter Notebook (`*.ipynb`). They will typically do exploratory work using the [JASMIN Notebook Service](https://help.jasmin.ac.uk/docs/interactive-computing/jasmin-notebooks-service/), and then may scale up their workflow by migrating to the Slurm cluster (using the ORCHID partition in the case of GPU/ML work). This flowchart is designed to help you understand the various stages that are involved in setting up, testing, running and scaling a scientific workflow on JASMIN.

```mermaid
flowchart TD
    START --> PY_IPYNB{User has Python or Jupyter Notebook file}

    START ~~~ L2_COMMENT@{ shape: brace-l, label: "<b>Pre-requesites</b>:
        User has <a href='http://help.jasmin.ac.uk/docs/getting-started/get-login-account/'>jasmin-login</a> 
        and <a href='https://help.jasmin.ac.uk/docs/batch-computing/orchid-gpu-cluster/#request-access-to-orchid'>orchid</a> roles" }

    PY_IPYNB -->|'.ipynb' file| START_NBS[<a href="https://help.jasmin.ac.uk/docs/interactive-computing/jasmin-notebooks-service/#using-the-jasmin-notebook-service">Start Notebook Service</a>]
    PY_IPYNB -->|'.py' file| CONVERT_PY[Convert to Ipython Notebook]

    PY_IPYNB ~~~ L3_COMMENT@{ shape: brace-r, label: "Simple method: paste sections of Python script into Notebook cells"}

    CONVERT_PY --> START_NBS --> DATA_NEEDS[<a href="https://github.com/agstephens/proto-jasmin-mermaid-docs/blob/main/README.md#managing-data-access">Manage Data Requirements</a><br/>E.g. CEDA Archive, GWS, external access]



```

[hello](#Here)

sfs
sd
fs
ds


sdf
sdf
sdf


sd
f
sdf

dsf
dsf

f
f
dsf
dsf
dsf
sdf
sfs


## Here

fsdf sdf
sf
ds
f

sd
f
dsf
s
dsf
dsf
sdfsd

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


## Example mermaid diagram

```mermaid

flowchart TD
    A[Christmas] -->|Get money| B(I link to GitHub)
    B --> C{I link to this doc}
    C -->|One| D[Laptop]
    C -->|Two| E[iPhone]
    C -->|Three| F[fa:fa-car Car]
    D[an <b>important</b> <a href='https://github.com/agstephens/proto-jasmin-mermaid-docs/blob/main/README.md#Here'>link</a>]
    click B href "https://github.com" "Link to GitHub"
    click C "https://github.com/agstephens/proto-jasmin-mermaid-docs/blob/main/README.md#Here"
```



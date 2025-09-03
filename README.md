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
        and <a href='https://help.jasmin.ac.uk/docs/batch-computing/orchid-gpu-cluster/#request-access-to-orchid'><u>orchid</u></a> roles" }

    PY_IPYNB -->|'.ipynb' file| START_NBS[<a href="https://help.jasmin.ac.uk/docs/interactive-computing/jasmin-notebooks-service/#using-the-jasmin-notebook-service">Start Notebook Service</a>]
    PY_IPYNB -->|'.py' file| CONVERT_PY[Convert to Ipython Notebook]

    PY_IPYNB ~~~ L3_COMMENT@{ shape: brace-r, label: "Simple method: paste sections of Python script into Notebook cells"}

    CONVERT_PY --> START_NBS --> DATA_NEEDS[<a href="#Managing Data Access"><u>Manage Data Requirements</u></a><br/>E.g. CEDA Archive, GWS, external access]
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

## Mermaid

 skdj sdf
 dsf
 dsf
 sf
 
 
 sdf 
 sf
 sf
  sf
  s fs
   fs
    s
    
    
    s fds
    

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



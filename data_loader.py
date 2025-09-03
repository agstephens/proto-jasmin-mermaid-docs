"""
This is a really simple example Data Loader class to demonstrate the idea.
"""

class DatasetLoader:
    _basedir = "."
    _template = "file_{number:02d}"
    _comps = {"number": range(1, 11)}

    def __init__(self, basedir=None, template=None, comps=None, name="dataset", loader="xarray"):
        self.basedir = basedir or self._basedir
        self.dsname = name
        self.template = template or self._template
        self._setup_loader(loader)
        self._stack = None

    def _setup_loader(self, loader):
        ...load package here and create an object called
        self.loader = ...

    def load(self, **sels):
        files = self._select(**sels)
        return self.loader(files)

    def _select(self, **sels):
        ...apply selections to components (comps)...
        ...allow clever pluralised selection so "year" and "years" both work
        return dict of selectors

    def __iter__ (self):
        return self

    def __next__ (self):
        # Allows the class instance to work as an iterator (often used by ML packages)
        if not self._stack:
            stack = self.load()
        yield stack.pop() # or deque, or something like that


# Example usage
era5 = DatasetLoader("/badc/era5/data", template="{var_id}/{year}.nc",
                     comps={"var_id": ["t", "u", "v"], 
                            "year": range(1999, 2011)},
                     name="era5")

ds = era5.load(var_id=["t"], year=[2001, 2020])

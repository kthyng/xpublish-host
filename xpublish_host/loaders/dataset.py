import logging
from pathlib import Path

import xarray as xr

L = logging.getLogger(__name__)


def load_dataset_zarr(json_path: str | Path, chunks=None):

    # do this to 1. use dask and 2. ensure chunks match between
    # encoding and dask arrays
    # https://github.com/xpublish-community/xpublish/issues/207
    chunks = chunks or {}
    
    print(f"Chunks are {chunks}.")
    
    print(f"using json from {json_path}")

    ds = xr.open_dataset(
        "reference://", engine="zarr",
        backend_kwargs={
            "storage_options": {
                "fo": json_path,
            },
            "consolidated": False
        },
        chunks=chunks,
    )

    # remove chunks encoding, same issue as above
    # https://github.com/xpublish-community/xpublish/issues/207
    print("removing chunks from all variable encoding")
    for varname in ds.data_vars:
        del ds[varname].encoding["chunks"]

    # ds = ds.reset_encoding()
    return ds

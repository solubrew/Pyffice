# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
        docid:
        name:
        description: >
        version: 0.0.0.0.0.0
        authority: filesystem
        security: seclvl2
        <(WT)>: -32
"""

# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from os.path import abspath, dirname, join, exists
import datetime as dt

# ======================================3rd Party Library Modules=====================================================||
from pandas import DataFrame

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma
from pyffice.document import PyfficeUnit

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "items.yaml")


class PyfficeTable(PyfficeUnit):
    SERIALIZATION_VERSION = (1, 0, 0)
    """"""

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeDataFrame")).override(cfg)

    def load_unit(self, unit=None):
        """Load a unit dict into this document.
        
        Args:
            unit: Parameter.
        
        Returns:
            Self for chaining.
        """
        logma.info(f"Load Unit {unit}")
        if unit is None:
            unit = self.config.dikt.get("unit", {})
        super().load_unit(unit)
        self.set_dataframe(unit.get("data", []), unit.get("columns", []))
        return self

    def set_dataframe(self, data, columns=None):
        """Set the dataframe.
        
        Args:
            data: Parameter.
            columns: Parameter.
        
        Returns:
            Self for chaining.
        """
        if not isinstance(data, DataFrame):
            if columns is None:
                if len(data) > 0:
                    columns = [str(x) for x in range(len(data[0]))]
                else:
                    columns = []
            data = DataFrame(data, columns=columns)
        self.data = data
        return self

class PyfficePart(PyfficeUnit):
    """"""
    SERIALIZATION_VERSION = (1, 0, 0)

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(pxcfg).select("PyfficePart").override(cfg)


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||

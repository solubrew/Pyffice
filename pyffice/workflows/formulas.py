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
from os.path import abspath, dirname, join
import datetime as dt

# ======================================3rd Party Library Modules=====================================================||
# from pycel import ExcelCompiler
# from pycel.excelformula import ExcelFormula

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from ogma.logma import Logma
from pyffice.document import PyfficeDocumentManager, PyfficeUnit

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "formulas.yaml")


class PyfficeFormulasLibrary(PyfficeDocumentManager):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(condor.Instruct(pxcfg).select("PyfficeFormulasLibrary")).override(cfg)
        self.compiler = ExcelCompiler
        self.formulas = None

    def get_formulas_list(self):
        """"""
        if self.formulas is None:
            self.set_formulas()
        return [x for x in self.formulas]

    def load_document(self, document):
        """"""
        if document is None:
            document = self.config.dikt.get("document", {})
        super().load_document(document)
        self.set_formulas(document.get("formulas", {}))
        return self

    def set_formulas(self, formulas=None):
        """"""
        if formulas is None:
            formulas = condor.Instruct(pxcfg).select("Formulas").dikt
        if formulas != self.formulas:
            self.add_change("formulas", self.formulas, formulas, "set")
            self.formulas = formulas
        return self

    def to_dict(self):
        """"""
        doc = super().to_dict()
        return doc


class PyfficeFormula(PyfficeUnit, ExcelFormula):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        PyfficeUnit.__init__(self, self.config)
        self.config.override(condor.Instruct(pxcfg).select("PyfficeFormula")).override(cfg)
        self.formula = self.config.dikt.get("formula", None)
        self.formula_tag = "<{" + self.formula + "}>"

    def convert(self):
        """"""

    def load_unit(self, unit):
        """"""
        if unit is None:
            unit = self.config.dikt.get("unit", {})
        super().load_unit(unit)
        self.formula = self.config.dikt.get("formula", None)
        self.formula_tag = "<{" + self.formula + "}>"
        return self

    def parse(self):
        """"""
        result = ""
        return result

    def execute(self):
        """"""
        result = ""
        return result

    def to_dict(self):
        """"""
        doc = super().to_dict()
        return doc


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||

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
try:
    from pycel.excelformula import ExcelFormula
    from pycel import ExcelCompiler
except ImportError:

    def class_builder():
        """"""

        class GenericClass(object):
            valid = False

        return GenericClass

    ExcelFormula = class_builder()
    ExcelCompiler = class_builder()


# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma
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

        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeFormulasLibrary")).override(cfg)
        self.compiler = ExcelCompiler
        self.formulas = None

    def get_formula(self, formula):
        """"""
        if self.formulas is None:
            self.set_formulas()
        return self.formulas.get(formula, None) or f"Formula {formula} Unknown"

    def get_formulas_list(self):
        """"""
        if self.formulas is None:
            self.set_formulas()
        return list(self.formulas.keys())

    def load_document(self, document=None):
        """"""
        if document is None:
            document = self.config.dikt.get("document", {})
        super().load_document(document)
        self.set_formulas(document.get("formulas", {}))
        return self

    def set_formulas(self, formulas=None):
        """"""
        # SPEED: offload this to a separate process or lazy load the list in pieces
        if formulas is None:
            formulas = kahndor.Instruct(pxcfg).select("Formulas").dikt
        formulas = formulas or {}
        if formulas != self.formulas:
            self.add_change("formulas", self.formulas, formulas, "set")
            # TODO implement factory methods for execution, etc for each formula using the config file
            self.formulas = {x: PyfficeFormula(y) for x, y in formulas.items()}
        if self.formulas is None:
            self.formulas = {}
        return self

    def to_dict(self):
        """"""
        doc = super().to_dict() or {}
        return doc


class PyfficeFormula(PyfficeUnit):
    """A Functional Formula object for use in various Pyffice Documents"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeFormula").override(cfg))
        self.formula = self.config.dikt.get("formula", None)
        self.formula_tag = "<{" + self.formula + "}>"
        self.use_tags = self.config.get("tags", [])
        self.description = self.config.get("description", None)
        self.parameters = {}

    def add_parameter(self, parameter, value):
        """"""
        self.parameters[parameter] = value

    def convert(self):
        """"""
        # TODO convert the formula to be compatability with a specific protocol

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
        # TODO separate string formula into its defined attributes

    def execute(self):
        """"""
        # TODO execute the formula and return the result

    def to_dict(self):
        """"""
        doc = super().to_dict()
        return doc


class PyfficeFormulaABS(PyfficeFormula):
    """A Functional Formula object for use in various Pyffice Documents"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeFormula").override(cfg))

    def execute(self):
        """"""
        result = abs(list(self.parameters.values())[0])
        return result

    def validate(self):
        """"""
        if len(self.parameters.values()) > 1:
            raise Exception("Too Many Parameters")


class PyfficeFormulaSUM(PyfficeFormula):
    """A Functional Formula object for use in various Pyffice Documents"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeFormula").override(cfg))

    def execute(self):
        """"""
        result = sum(self.parameters.values())
        return result

    def validate(self):
        """"""
        if len([x for x in self.parameters.values() if not is_number(x)]) > 0:
            raise Exception("Non Number Values in Parameters")


def is_number(value):
    """"""
    if isinstance(value, (int, float)):
        return True
    return False


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||

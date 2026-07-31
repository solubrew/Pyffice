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
import re
from abc import ABC, abstractmethod

# ======================================3rd Party Library Modules======================================================||
# T-NEW-054 (Option B): removed pycel dependency. Protocols are
# config-driven via the 'protocols' key in formulas.yaml; the
# default 'builtin' protocol uses string templating.

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


# T-NEW-054 (Option B): protocol-based formula execution. A
# protocol is a class that knows how to parse a formula string
# into a callable representation and execute it given a
# parameter dict. Users register protocols in formulas.yaml
# under the 'protocols' key; the default 'builtin' is registered
# automatically.
class PyfficeFormulaProtocol(ABC):
    """Abstract base for formula execution protocols.

    Subclasses implement parse() and execute(). The parse() return
    value is opaque to callers (it's an internal representation
    the protocol knows how to execute) but is preserved on
    PyfficeFormula.parsed so execute() can be called multiple
    times without re-parsing.
    """

    @abstractmethod
    def parse(self, formula: str) -> object:
        """Return an opaque parsed representation of formula."""

    @abstractmethod
    def execute(self, parsed: object, parameters: dict) -> object:
        """Execute parsed against parameters and return the result."""


class BuiltinProtocol(PyfficeFormulaProtocol):
    """Default protocol: template substitution + numeric eval.

    Recognizes two parameter placeholder formats:
      - <[name]>           -> Python identifier
      - <~[name]~>         -> optional parameter (None if missing)

    Supports basic arithmetic: + - * / ( ) and numeric literals.
    Example: '=ABS(<[cr0]>)' parsed against {'cr0': -3} returns 3.
    """

    _TOKEN_RE = re.compile(r"<\[(?P<name>[^\]]+)\]>|<~\[(?P<oname>[^\]]+)\]~>")

    def parse(self, formula: str) -> dict:
        """Parse a formula string into {template, params, optionals}."""
        if formula is None:
            return {"template": "", "params": set(), "optionals": set()}
        body = formula[1:] if formula.startswith("=") else formula
        params: set[str] = set()
        optionals: set[str] = set()
        for m in self._TOKEN_RE.finditer(body):
            if m.group("name") is not None:
                params.add(m.group("name"))
            else:
                optionals.add(m.group("oname"))
        return {"template": body, "params": params, "optionals": optionals}

    def execute(self, parsed: dict, parameters: dict) -> object:
        """Substitute params into the template and eval the result.

        Supports:
          - Arithmetic: <[a]>+<[b]>, <[x]>*2, etc.
          - Function calls via a small builtins map (ABS, SUM, MIN,
            MAX, AVERAGE). Subclass PyfficeFormulaABS/SUM/etc.
            override execute() for richer behavior; this protocol
            is the default fallback for ad-hoc formulas.

        Falls back to returning the filled template as a string if
        eval fails (e.g. unsupported function name).
        """
        if not parsed:
            return None
        template = parsed["template"]
        # Strip a leading '=' if present (Excel-style prefix).
        if template.startswith("="):
            template = template[1:]

        def _sub(m: re.Match) -> str:
            if m.group("name") is not None:
                v = parameters.get(m.group("name"))
                if v is None:
                    raise ValueError(
                        f"Missing required parameter {m.group('name')!r}"
                    )
                return repr(v)
            name = m.group("oname")
            return repr(parameters.get(name))

        filled = self._TOKEN_RE.sub(_sub, template)
        # Restricted eval: builtins={} + a tiny function whitelist.
        safe_globals = {"__builtins__": {}, **self._SAFE_FUNCS}
        try:
            return eval(filled, safe_globals, {})
        except Exception:
            # Unsupported function / syntax — return the filled
            # template as a string so callers can still see what
            # they passed in.
            return filled

    # Minimal function whitelist for arithmetic + the Excel
    # functions Pyffice ships out-of-the-box.
    # SUM/MIN/MAX/AVERAGE take *args, unlike Python's sum() which
    # takes an iterable — wrap them so multi-arg calls work.
    _SAFE_FUNCS = {
        "ABS": abs,
        "SUM": lambda *xs: sum(xs),
        "MIN": min,
        "MAX": max,
        "AVERAGE": lambda *xs: sum(xs) / len(xs) if xs else 0,
    }


class PyfficeFormulasLibrary(PyfficeDocumentManager):
    SERIALIZATION_VERSION = (1, 0, 0)
    """"""

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)

        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeFormulasLibrary")).override(cfg)
        # T-NEW-054 (Option B): replace pycel-based ExcelCompiler
        # with a config-driven protocol registry. The default
        # 'builtin' protocol uses string templating; users can
        # register additional protocols via formulas.yaml.
        self.protocols: dict[str, "PyfficeFormulaProtocol"] = {
            "builtin": BuiltinProtocol(),
        }
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
            # T-NEW-054 (Option B): instantiate each formula with
            # a reference to this library so its parse()/execute()
            # can resolve protocols through self.protocols.
            self.formulas = {
                x: PyfficeFormula(y, _library=self) for x, y in formulas.items()
            }
        if self.formulas is None:
            self.formulas = {}
        return self

    def to_dict(self):
        """"""
        doc = super().to_dict() or {}
        return doc


class PyfficeFormula(PyfficeUnit):
    """A Functional Formula object for use in various Pyffice Documents"""

    def __init__(self, cfg=None, _library=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeFormula").override(cfg))
        self.formula = self.config.dikt.get("formula", None)
        self.formula_tag = "<{" + self.formula + "}>"
        self.use_tags = self.config.get("tags", [])
        self.description = self.config.get("description", None)
        self.parameters = {}
        # T-NEW-054: optional back-reference to the parent library,
        # used to resolve the active protocol during parse/execute.
        self._library = _library
        self.parsed = None
        self.protocol_name = "builtin"

    def add_parameter(self, parameter, value):
        """"""
        self.parameters[parameter] = value

    def convert(self, protocol_name: str = "builtin"):
        """Re-parse self.formula using the named protocol.

        Args:
            protocol_name: key in PyfficeFormulasLibrary.protocols.
                Defaults to 'builtin'. Unknown names raise
                UnknownSyntaxError.
        """
        from pyffice.pyffice import UnknownSyntaxError
        from pyffice.document import PyfficeDocumentManager as _PDM  # noqa: F401
        # Find the protocol via the library, or fall back to a
        # fresh BuiltinProtocol if no library is in scope.
        proto = self._resolve_protocol(protocol_name)
        self.protocol_name = protocol_name
        self.parsed = proto.parse(self.formula)
        return self

    def _resolve_protocol(self, protocol_name: str):
        """Return the named protocol, or BuiltinProtocol() as fallback."""
        from pyffice.pyffice import UnknownSyntaxError
        # Walk up to find a PyfficeFormulasLibrary if available.
        parent = getattr(self, "_library", None)
        if parent is not None:
            proto = parent.protocols.get(protocol_name)
            if proto is None:
                raise UnknownSyntaxError(
                    f"Unknown protocol {protocol_name!r}; "
                    f"available: {sorted(parent.protocols)}"
                )
            return proto
        # No library — only the builtin is reachable.
        if protocol_name == "builtin":
            return BuiltinProtocol()
        raise UnknownSyntaxError(
            f"Unknown protocol {protocol_name!r}; only 'builtin' is "
            f"available without a PyfficeFormulasLibrary context"
        )

    def load_unit(self, unit):
        """"""
        if unit is None:
            unit = self.config.dikt.get("unit", {})
        super().load_unit(unit)
        self.formula = self.config.dikt.get("formula", None)
        self.formula_tag = "<{" + self.formula + "}>"
        return self

    def parse(self):
        """Parse self.formula using the assigned protocol (default builtin).

        Stores the parsed representation in self.parsed; subsequent
        execute() calls reuse it without re-parsing.
        """
        proto = self._resolve_protocol(getattr(self, "protocol_name", "builtin"))
        self.parsed = proto.parse(self.formula)
        return self

    def execute(self):
        """Execute self.parsed against self.parameters via the protocol.

        Returns the result. If self.parsed is unset, runs parse() first.
        """
        from pyffice.pyffice import InvalidParameterTypeError
        proto = self._resolve_protocol(getattr(self, "protocol_name", "builtin"))
        if not hasattr(self, "parsed") or self.parsed is None:
            self.parse()
        # Convert parameters via is_number() check for non-builtin
        # protocols. BuiltinProtocol handles type errors via the
        # try/except inside its execute().
        if proto.__class__.__name__ != "BuiltinProtocol":
            for v in self.parameters.values():
                if not is_number(v) and not isinstance(v, str):
                    raise InvalidParameterTypeError(
                        f"Non-numeric value in parameters for "
                        f"{proto.__class__.__name__}: {v!r}"
                    )
        return proto.execute(self.parsed, dict(self.parameters))

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
        from pyffice.pyffice import TooManyParametersError
        if len(self.parameters.values()) > 1:
            raise TooManyParametersError("Too Many Parameters")


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
        from pyffice.pyffice import InvalidParameterTypeError
        if len([x for x in self.parameters.values() if not is_number(x)]) > 0:
            raise InvalidParameterTypeError("Non Number Values in Parameters")


def is_number(value):
    """"""
    if isinstance(value, (int, float)):
        return True
    return False


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||

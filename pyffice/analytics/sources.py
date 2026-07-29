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

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma
from pyffice.document import PyfficeDocument, PyfficeUnit, PyfficeDocumentManager
from pyffice.items.items import PyfficeTable

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "sources.yaml")


class PyfficeSourceManager(PyfficeDocumentManager):
    SERIALIZATION_VERSION = (1, 0, 0)
    """"""

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeSourceManager").override(cfg))
        self.sources = None

    def add_source(self, source, type_="file"):
        """"""
        source = {"name": source.name, "type": type_, "path": source.path}
        self.add_change("sources", self.sources, source, "add")
        self.sources.add(source)
        return self

    def load_document(self, document=None):
        """"""
        logma.info(f"Load Document {document}")
        if document is None:
            document = self.config.dikt.get("document", {})
            if document is None:
                document = {}
        super().load_document(document)
        self.set_sources(document.get("sources", []))
        return self

    def set_sources(self, sources):
        """"""
        if sources is None:
            sources = []
        if self.sources != sources:
            self.add_change("sources", self.sources, sources)
            self.sources = sources
        return self

    def to_dict(self):
        """"""
        doc = super().to_dict()
        doc["document"] = {"sources": self.sources}
        return doc


class PyfficeDataSet(PyfficeDocumentManager):
    """"""

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeDataSet").override(cfg))
        self.path = None
        self.sources = None
        self.relationships = None
        self.views = set()

    def add_source(self, source, type_="file"):
        """"""
        source = {"name": source.name, "type": type_, "path": source.path}
        self.add_change("sources", self.sources, source, "add")
        self.sources.add(source)
        return self

    def add_relationship(self, left_view, right_view, relationship_type=None, relationship_name=None):
        """"""
        if relationship_name is None:
            relationship_name = f"{left_view.name}-{right_view.name}"
        if relationship_type is None:
            relationship_type = "one_to_one"
        relationship = {"name": relationship_name, "left": left_view, "right": right_view, "type": relationship_type}
        self.add_change("relationships", self.relationships, relationship, "add")
        self.relationships.add(relationship)
        return self

    def add_view(self, datatable, name=None):
        """"""
        cfg = {"table": datatable, "filters": {}, "name": name}
        view = PyfficeDataView(cfg)
        self.add_change("views", self.views, view, "add")
        self.views.add(view)
        return self

    def del_source(self, source):
        """"""
        self.add_change("sources", self.sources, source, "del")
        self.sources.remove(source)
        return self

    def del_relationship(self, relationship):
        """"""
        self.add_change("relationships", self.relationships, relationship, "del")
        self.relationships.remove(relationship)
        return self

    def del_view(self, view):
        """"""
        self.add_change("views", self.views, view, "del")
        self.views.remove(view)
        return self

    def load_document(self, document=None):
        """"""
        logma.info(f"Load Document {document}")
        if document is None:
            document = self.config.dikt.get("document", {})
            if document is None:
                document = {}
        super().load_document(document)
        self.set_sources(document.get("sources", self.config.dikt.get("sources", [])))
        self.set_relationships(document.get("relationships", self.config.dikt.get("relationships", [])))
        self.set_views(document.get("views", self.config.dikt.get("views", [])))
        return self

    def set_relationships(self, relationships):
        """"""
        relationships = set(relationships)
        if relationships != self.relationships:
            self.add_change("relationships", self.relationships, relationships)
            self.relationships = relationships
        return self

    def set_sources(self, sources):
        """"""
        sources = set(sources)
        if sources != self.sources:
            self.add_change("sources", self.sources, sources)
            self.sources = sources
        return self

    def set_views(self, views):
        """"""
        views = set(views)
        if views != self.views:
            self.add_change("views", self.views, views)
            self.views = views
        return self

    def to_dict(self):
        """"""
        doc = super().to_dict()
        doc["document"] = {
            "sources": self.sources,
            "relationships": self.relationships,
            "views": [x.to_dict() for x in self.views],
        }
        return doc


class PyfficeDataView(PyfficeDocument):
    """"""

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeDataView")).override(cfg)
        self.columns = None
        self.filters = None
        self.records = None
        self.summarizations = None
        self.type = None

    def add_filter(self, column, operator, value):
        """"""
        filter_ = {"operator": operator, "column": column, "value": value}
        self.add_change("filters", self.filters, filter_, "add")
        self.filters.add(filter_)
        return self

    def add_summarization(self, column, formula, name=None):
        """"""
        summarization = {"column": column, "formula": formula, "name": name}
        self.add_change("summarizations", self.summarizations, summarization, "add")
        self.summarizations.add(summarization)
        return self

    def apply_filters(self, df):
        """"""
        for filter_ in self.filters:
            match filter_["operator"]:
                case "equal":
                    df = df[df[filter_["column"]] == filter_["value"]]
                case "not_equal":
                    df = df[df[filter_["column"]] != filter_["value"]]
                case "less_than":
                    df = df[df[filter_["column"]] < filter_["value"]]
                case "less_than_equal":
                    df = df[df[filter_["column"]] <= filter_["value"]]
                case "greater_than":
                    df = df[df[filter_["column"]] > filter_["value"]]
                case "greater_than_equal":
                    df = df[df[filter_["column"]] >= filter_["value"]]
                case "like":
                    df = df[df[filter_["column"]].str.contains(filter_["value"])]
                case "not_like":
                    df = df[~df[filter_["column"]].str.contains(filter_["value"])]
                case "startswith":
                    df = df[df[filter_["column"]].str.startswith(filter_["value"])]
                case "not_startswith":
                    df = df[~df[filter_["column"]].str.startswith(filter_["value"])]
                case "endswith":
                    df = df[df[filter_["column"]].str.endswith(filter_["value"])]
                case "not_endswith":
                    df = df[~df[filter_["column"]].str.endswith(filter_["value"])]
                case "less_than_greater_than":
                    df = df
                case "contains":
                    df = df[df[filter_["column"]].str.contains(filter_["value"])]
                case "not_contains":
                    df = df[~df[filter_["column"]].str.contains(filter_["value"])]
                case "is_null":
                    df = df[df[filter_["column"]].isnull()]
                case "is_not_null":
                    df = df[~df[filter_["column"]].isnull()]
                case "is_true":
                    df = df
                case "is_false":
                    df = df
                case "in":
                    df = df[df[filter_["column"]].isin(filter_["value"])]
                case "not_in":
                    df = df[~df[filter_["column"]].isin(filter_["value"])]
                case "between":
                    df = df[df[filter_["column"]].between(filter_["value"][0], filter_["value"][1])]
                case _:
                    raise ValueError(f"Invalid operator: {filter_['operator']}")
        return df

    def apply_summarizations(self, df):
        """"""
        return df

    def del_filter(self, column, operator, value):
        """"""
        filter_ = {"operator": operator, "column": column, "value": value}
        self.add_change("filters", self.filters, filter_, "del")
        self.filters.remove(filter_)
        return self

    def del_summarization(self, column, formula, name=None):
        """"""
        summarization = {"column": column, "formula": formula, "name": name}
        self.add_change("summarizations", self.summarizations, summarization, "del")
        self.summarizations.remove(summarization)
        return self

    def get_data(self):
        """"""
        df = self.apply_filters(self.data)
        df = self.apply_summarizations(df)
        return df

    def load_document(self, document):
        """"""
        logma.info(f"Load Document {document}")
        if document is None:
            document = self.config.dikt.get("document", {})
            if document is None:
                document = {}
        super().load_document(document)
        self.set_columns(document.get("columns", []))
        self.set_data(document.get("data", {}))
        self.set_filters(document.get("filters", []))
        self.set_summarizations(document.get("summarizations", []))
        return self

    def set_columns(self, columns):
        """"""
        if columns != self.columns:
            self.add_change("columns", self.columns, columns)
        self.columns = columns
        return self

    def set_data(self, data):
        """"""
        cfg = {"data": data}
        data = PyfficeTable(cfg)
        if data != self.data:
            self.add_change("data", self.data, data)
            self.data = data
        return self

    def set_filters(self, filters):
        """"""
        filters = set(filters)
        if filters != self.filters:
            self.add_change("filters", self.filters, filters)
            self.filters = filters
        return self

    def set_summarizations(self, summarizations):
        """"""
        summarizations = set(summarizations)
        if summarizations != self.summarizations:
            self.add_change("summarizations", self.summarizations, summarizations)
            self.summarizations = summarizations
        return self

    def to_dict(self):
        """"""
        doc = super().to_dict()
        doc["document"] = {
            "filters": self.filters,
            "summarizations": self.summarizations,
            "columns": self.columns,
            "type": self.type,
            "data": self.data.to_dict(),
        }
        return doc


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||

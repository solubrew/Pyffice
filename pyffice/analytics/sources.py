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

from typing import Any, Dict, List, Optional, Tuple, Union, Set, FrozenSet

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "sources.yaml")


class PyfficeSource(PyfficeDocumentManager):
    """"""
    SERIALIZATION_VERSION = (1, 0, 0)

    def __init__(self, cfg):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeSource").override(cfg))
        self.data_sets = []
        self.data_views = []

    def add_data_set(self, data_set) -> "PyfficeSource":
        """Append a data set to self.data_sets."""
        self.data_sets.append(data_set)
        return self

    def add_data_view(self, data_set) -> "PyfficeSource":
        """Append a data view to self.data_views."""
        self.data_views.append(data_set)
        return self

    def edit_data_set(self, changes) -> "PyfficeSource":
        """Replace self.data_sets with changes (full snapshot)."""
        self.data_sets = list(changes)
        return self

    def edit_data_view(self, changes) -> "PyfficeSource":
        """Replace self.data_views with changes (full snapshot)."""
        self.data_views = list(changes)
        return self

    def load_document(self, document=None) -> "PyfficeSource":
        """Load document into this document.
        
        Args:
            document: Parameter.
        
        Returns:
            Self for chaining.
        """
        logma.info(f"Load Document {document}")
        document = document or self.config.dikt.get("document", {}) or {}
        super().load_document(document)
        return self

class PyfficeSourceManager(PyfficeDocumentManager):
    SERIALIZATION_VERSION = (1, 0, 0)
    """"""

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeSourceManager").override(cfg))
        self.sources = []

    def add_source(self, source, type_="file") -> Any:
        """Add a source reference.
        
        Args:
            source: Parameter.
            type_: Parameter.
        
        Returns:
            Self for chaining.
        """
        source = PyfficeSource({"name": source.name, "type": type_, "path": source.path})
        return self._add_to_collection("sources", source, "sources")

    def load_document(self, document=None) -> "PyfficeSourceManager":
        """Load document into this document.
        
        Args:
            document: Parameter.
        
        Returns:
            Self for chaining.
        """
        logma.info(f"Load Document {document}")
        document = document or self.config.dikt.get("document", {}) or {}
        super().load_document(document)
        self.set_sources(document.get("sources", []))
        return self

    def set_sources(self, sources) -> "PyfficeSourceManager":
        """Set the sources.
        
        Args:
            sources: Parameter.
        
        Returns:
            Self for chaining.
        """
        if sources is None:
            sources = []
        if self.sources != sources:
            self.add_change("sources", self.sources, sources)
            self.sources = sources
        return self

class PyfficeDataSet(PyfficeDocument):
    """"""
    SERIALIZATION_VERSION = (1, 0, 0)

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeDataSet").override(cfg))
        self.path = None
        self.sources = None
        self.relationships = None
        self.views = set()

    def add_relationship(self, left_view, right_view, relationship_type=None, relationship_name=None) -> "PyfficeDataSet":
        """Add a relationship.
        
        Args:
            left_view: Parameter.
            right_view: Parameter.
            relationship_type: Parameter.
            relationship_name: Parameter.
        
        Returns:
            Self for chaining.
        """
        if relationship_name is None:
            relationship_name = f"{left_view.name}-{right_view.name}"
        if relationship_type is None:
            relationship_type = "one_to_one"
        relationship = {"name": relationship_name, "left": left_view, "right": right_view, "type": relationship_type}
        self.add_change("relationships", self.relationships, relationship, "add")
        self.relationships.add(relationship)
        return self

    def add_view(self, datatable, name=None) -> Any:
        """Add a view.
        
        Args:
            datatable: Parameter.
            name: Parameter.
        
        Returns:
            Self for chaining.
        """
        cfg = {"table": datatable, "filters": {}, "name": name}
        view = PyfficeDataView(cfg)
        return self._add_to_collection("views", view, "views")

    def del_source(self, source) -> Any:
        """Remove the source.
        
        Args:
            source: Parameter.
        
        Returns:
            Self for chaining.
        """
        return self._del_from_collection("sources", source, "sources")

    def del_relationship(self, relationship) -> Any:
        """Remove the relationship.
        
        Args:
            relationship: Parameter.
        
        Returns:
            Self for chaining.
        """
        return self._del_from_collection("relationships", relationship, "relationships")

    def del_view(self, view) -> Any:
        """Remove the view.
        
        Args:
            view: Parameter.
        
        Returns:
            Self for chaining.
        """
        return self._del_from_collection("views", view, "views")

    def load_document(self, document=None) -> "PyfficeDataSet":
        """Load document into this document.
        
        Args:
            document: Parameter.
        
        Returns:
            Self for chaining.
        """
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

    def set_relationships(self, relationships) -> "PyfficeDataSet":
        """Set the relationships.
        
        Args:
            relationships: Parameter.
        
        Returns:
            Self for chaining.
        """
        relationships = set(relationships)
        if relationships != self.relationships:
            self.add_change("relationships", self.relationships, relationships)
            self.relationships = relationships
        return self

    def set_sources(self, sources) -> "PyfficeDataSet":
        """Set the sources.
        
        Args:
            sources: Parameter.
        
        Returns:
            Self for chaining.
        """
        sources = set(sources)
        if sources != self.sources:
            self.add_change("sources", self.sources, sources)
            self.sources = sources
        return self

    def set_views(self, views) -> "PyfficeDataSet":
        """Set the views.
        
        Args:
            views: Parameter.
        
        Returns:
            Self for chaining.
        """
        views = set(views)
        if views != self.views:
            self.add_change("views", self.views, views)
            self.views = views
        return self

class PyfficeDataView(PyfficeDocument):
    """"""
    SERIALIZATION_VERSION = (1, 0, 0)

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeDataView")).override(cfg)
        self.columns = None
        self.filters = None
        self.records = None
        self.summarizations = None
        self.type = None

    def add_filter(self, column, operator, value) -> Any:
        """Add a filter.
        
        Args:
            column: Parameter.
            operator: Parameter.
            value: Parameter.
        
        Returns:
            Self for chaining.
        """
        filter_ = {"operator": operator, "column": column, "value": value}
        return self._add_to_collection("filters", filter_, "filters")

    def add_summarization(self, column, formula, name=None) -> Any:
        """Add a summarization.
        
        Args:
            column: Parameter.
            formula: Parameter.
            name: Parameter.
        
        Returns:
            Self for chaining.
        """
        summarization = {"column": column, "formula": formula, "name": name}
        return self._add_to_collection("summarizations", summarization, "summarizations")

    def apply_filters(self, df) -> None:
        """Apply filters.
        
        Args:
            df: Parameter.
        
        Returns:
            Self for chaining.
        """
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

    def apply_summarizations(self, df) -> None:
        """Apply summarizations.
        
        Args:
            df: Parameter.
        
        Returns:
            Self for chaining.
        """
        return df

    def del_filter(self, column, operator, value) -> Any:
        """Remove the filter.
        
        Args:
            column: Parameter.
            operator: Parameter.
            value: Parameter.
        
        Returns:
            Self for chaining.
        """
        filter_ = {"operator": operator, "column": column, "value": value}
        return self._del_from_collection("filters", filter_, "filters")

    def del_summarization(self, column, formula, name=None) -> Any:
        """Remove the summarization.
        
        Args:
            column: Parameter.
            formula: Parameter.
            name: Parameter.
        
        Returns:
            Self for chaining.
        """
        summarization = {"column": column, "formula": formula, "name": name}
        return self._del_from_collection("summarizations", summarization, "summarizations")

    def get_data(self) -> None:
        """Return the data.
        
        Returns:
            Self for chaining.
        """
        df = self.apply_filters(self.data)
        df = self.apply_summarizations(df)
        return df

    def load_document(self, document) -> "PyfficeDataView":
        """Load document into this document.
        
        Args:
            document: Parameter.
        
        Returns:
            Self for chaining.
        """
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

    def set_columns(self, columns) -> "PyfficeDataView":
        """Set the columns.
        
        Args:
            columns: Parameter.
        
        Returns:
            Self for chaining.
        """
        if columns != self.columns:
            self.add_change("columns", self.columns, columns)
        self.columns = columns
        return self

    def set_data(self, data) -> "PyfficeDataView":
        """Set the data.
        
        Args:
            data: Parameter.
        
        Returns:
            Self for chaining.
        """
        cfg = {"data": data}
        data = PyfficeTable(cfg)
        if data != self.data:
            self.add_change("data", self.data, data)
            self.data = data
        return self

    def set_filters(self, filters) -> "PyfficeDataView":
        """Set the filters.
        
        Args:
            filters: Parameter.
        
        Returns:
            Self for chaining.
        """
        filters = set(filters)
        if filters != self.filters:
            self.add_change("filters", self.filters, filters)
            self.filters = filters
        return self

    def set_summarizations(self, summarizations) -> "PyfficeDataView":
        """Set the summarizations.
        
        Args:
            summarizations: Parameter.
        
        Returns:
            Self for chaining.
        """
        summarizations = set(summarizations)
        if summarizations != self.summarizations:
            self.add_change("summarizations", self.summarizations, summarizations)
            self.summarizations = summarizations
        return self

# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||

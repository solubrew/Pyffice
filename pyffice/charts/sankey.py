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
from floweaver import SankeyDefinition, ProcessGroup

# from floweaver import sankey_flow

import plotly.graph_objects as go

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma
from pyffice.document import PyfficeDocument, PyfficeDocumentManager

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")


class SankeyChart:
    """
    A class to create Sankey charts using Plotly.
    """

    VERSION = "0.0.1.0.1.0"

    def __init__(self, sources, targets, values, labels=None):
        """
        Initialize the Sankey chart data.

        Args:
            sources (list of int): List of source node indices.
            targets (list of int): List of target node indices.
            values (list of float): List of flow values corresponding to source->target.
            labels (list of str, optional): Optional labels for the nodes (default=None).
                If none, node indices will be displayed.
        """
        self.sources = sources
        self.targets = targets
        self.values = values
        self.labels = labels if labels else []

    def create_sankey_chart(self, title="Sankey Diagram"):
        """
        Create and render a Sankey diagram.

        Args:
            title (str): Title of the Sankey diagram.
        """
        # Define Sankey diagram data
        sankey_data = go.Sankey(
            node=dict(
                label=self.labels,
                pad=15,  # Padding between nodes
                thickness=20,  # Thickness of nodes
                color="blue",  # Node color
            ),
            link=dict(
                source=self.sources,
                target=self.targets,
                value=self.values,
                color="rgba(63,81,181,0.5)",  # Optional: link color
            ),
        )

        # Define layout for better visuals
        layout = go.Layout(
            title=title,
            font=dict(size=12),
        )

        # Create the figure and render it
        fig = go.Figure(data=[sankey_data], layout=layout)
        fig.show()

    def load_document(self, document):
        """"""
        super().load_document(document)
        return self

    def open_file(self, document):
        """Open a file."""
        if not document:
            return self
        return self

    def save_sankey_chart(self, filename="sankey_chart.html"):
        """
        Save the Sankey diagram to an HTML file.

        Args:
            filename (str): Name of the HTML file to save the chart (default="sankey_chart.html").
        """
        sankey_data = go.Sankey(
            node=dict(label=self.labels, pad=15, thickness=20, color="blue"),
            link=dict(
                source=self.sources,
                target=self.targets,
                value=self.values,
                color="rgba(63,81,181,0.5)",
            ),
        )

        fig = go.Figure(data=[sankey_data])
        fig.write_html(filename)
        logma.info(f"Sankey chart saved as '{filename}'.")


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||

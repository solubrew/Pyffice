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
from ganttlab import GanttChart
import gantt

import pandas as pd
import plotly.express as px

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from ogma.logma import Logma
from pyffice.document import PyfficeDocument, PyfficeDocumentManager

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")


class PyfficeGanttChart(object):
    """Initialize the Gantt chart parameters.

    Args:
        data (pd.DataFrame): A DataFrame containing task data.
        task_col (str): Column name for tasks.
        start_col (str): Column name for start dates/times.
        end_col (str): Column name for end dates/times.
        resource_col (str, optional): Column name for task categories or resources (default=None).
    """

    def __init__(self, data, task_col, start_col, end_col, resource_col=None, cfg=None):
        """"""
        self.config = condor.Instruct(pxcfg).select("").override(cfg)
        # Create Gantt chart data
        project = GanttChart(title="Project Timeline")
        project.add_task("Task A", "2023-10-01", "2023-10-10")
        project.add_task("Task B", "2023-10-11", "2023-10-20")

        # Show Gantt chart
        project.display()

        # Create a project
        project = gantt.Project(name="Demo Project")

        # Create tasks
        task1 = gantt.Task(name="Task 1", start="2023-07-01", duration=10)
        task2 = gantt.Task(name="Task 2", start="2023-07-11", duration=5)

        project.add_task(task1)
        project.add_task(task2)

        # Export to a .svg or .png
        project.make_svg_for_tasks(filename="gantt_chart.svg")

        self.data = data
        self.task_col = task_col
        self.start_col = start_col
        self.end_col = end_col
        self.resource_col = resource_col

    def create_gantt_chart(self, title="Gantt Chart", color_scheme="Viridis"):
        """
        Create and render an interactive Gantt chart.

        Args:
            title (str): Title of the chart (default="Gantt Chart").
            color_scheme (str): Color scheme for task coloring (default="Viridis").
                See options here: https://plotly.com/python/discrete-color/
        """
        # Plot Gantt chart using Plotly
        fig = px.timeline(
            self.data,
            x_start=self.start_col,
            x_end=self.end_col,
            y=self.task_col,
            color=self.resource_col,
            title=title,
            color_discrete_sequence=(
                px.colors.qualitative.__dict__[color_scheme]
                if color_scheme in px.colors.qualitative.__dict__
                else px.colors.qualitative.Viridis
            ),
            labels={self.task_col: "Task", self.resource_col: "Category"},
        )

        # Update layout for better visuals
        fig.update_layout(
            showlegend=True,
            xaxis_title="Time",
            yaxis_title="Tasks",
            yaxis=dict(autorange="reversed"),  # Reverse tasks for better readability
            title=dict(x=0.5),  # Center the title
        )

        # Render the chart
        fig.show()

    def load_document(self, document):
        """"""
        super().load_document(document)
        return self

    def open_file(self, document):
        """"""

    def save_gantt_chart(self, filename="gantt_chart.html"):
        """
        Save the Gantt chart as an HTML file.

        Args:
            filename (str): Name of the HTML file to save the chart (default="gantt_chart.html").
        """
        fig = px.timeline(
            self.data,
            x_start=self.start_col,
            x_end=self.end_col,
            y=self.task_col,
            color=self.resource_col,
            title="Gantt Chart",
            labels={self.task_col: "Task", self.resource_col: "Category"},
        )

        fig.update_layout(
            showlegend=True,
            xaxis_title="Time",
            yaxis_title="Tasks",
            yaxis=dict(autorange="reversed"),
            title=dict(x=0.5),
        )

        # Save the chart to an HTML file
        fig.write_html(filename)
        print(f"Gantt chart saved as '{filename}'.")


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||

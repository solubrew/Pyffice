# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
        docid:
        name: Pyffice Projects Module
        description: >
                Pyffice Gantt-style project management module.
                Implements MS Project compatible data model with tasks, resources,
                calendars, dependencies, and Gantt chart visualization.
                Supports export to Excel, YAML, and Markdown formats.
        version: 0.0.1.0.1.0
        authority: filesystem
        security: seclvl2
        <(WT)>: -32
"""

# -*- coding: utf-8 -*
# ======================================Project Management Module Exports==============================================||
from pyffice.projects.projects import (
    PyfficeProject,
    PyfficeProjectTask,
    PyfficeProjectResource,
    PyfficeProjectAssignment,
    # PyfficeProjectCalendar,
    # PyfficeProjectPort,
    # PyfficeProjectPortExcel,
    # PyfficeProjectPortYAML,
    # PyfficeProjectPortMarkdown,
    # PyfficeProjectGanttChart,
)

# from pyffice.projects.paxn import (
#     PyfficeProjectPortPAXN,
#     PyfficeProjectPortAXN,
# )

__all__ = [
    "PyfficeProject",
    "PyfficeProjectTask",
    "PyfficeProjectResource",
    "PyfficeProjectAssignment",
    "PyfficeProjectCalendar",
    "PyfficeProjectPort",
    "PyfficeProjectPortExcel",
    "PyfficeProjectPortYAML",
    "PyfficeProjectPortMarkdown",
    "PyfficeProjectGanttChart",
    "PyfficeProjectPortPAXN",
    "PyfficeProjectPortAXN",
]

# ====================================================================================================================||
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

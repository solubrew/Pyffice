# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
	docid:
	name: Pyffice PAXN/AXN Format Ports
	description: >
		Import/Export converters for PAXN (ProjectAXN) and AXN task formats.
		Enables bidirectional conversion between Pyffice Gantt projects and
		ProjectAXN/AXN task management formats.
	version: 0.0.1.0.1.0
	authority: filesystem
	security: seclvl2
	<(WT)>: -32
"""
# -*- coding: utf-8 -*
import os
import yaml
import datetime
from datetime import datetime as dt
from pathlib import Path
from typing import Dict, List, Optional, Any, Union

from pyffice.items.tasks import PyfficeProject, PyfficeTaskFrame, PyfficeTasksManager
from condor import condor


# ====================================================================================================================||
# Configuration
# ====================================================================================================================||
def _get_config():
    """Get Pyffice tasks configuration."""
    from os.path import dirname, join
    pxcfg = join(dirname(__file__), "_data_", "tasks.yaml")
    return condor.Instruct(pxcfg)


# ====================================================================================================================||
# PAXN Format Converter
# ====================================================================================================================||
class PyfficeProjectPortPAXN:
    """Port for PAXN (ProjectAXN) project format."""
    
    @staticmethod
    def load(paxn_path: str) -> 'PyfficeProject':
        """Load a PAXN project file and convert to PyfficeProject."""
        with open(paxn_path, 'r') as f:
            paxn_data = yaml.safe_load(f)
        
        project = PyfficeProject()
        project.document['verb_noun_txt'] = paxn_data.get('name', 'Unnamed Project')
        project.document['description'] = paxn_data.get('description', '')
        
        # Set status
        status_map = {
            'active': 'active',
            'planning': 'planning',
            'on_hold': 'suspended',
            'completed': 'completed',
            'cancelled': 'cancelled',
        }
        project.document['status'] = status_map.get(paxn_data.get('status', 'planning'), 'planning')
        
        # Load tasks from task_ids
        task_ids = paxn_data.get('task_ids', [])
        tasks_dir = Path(paxn_path).parent.parent / 'tasks'
        
        for task_id in task_ids:
            # Try different file patterns
            for pattern in [f"task_{task_id}.axn", f"task_{task_id}.yaml", 
                           f"axn_{task_id}.axn", f"axn_{task_id}.yaml"]:
                task_file = tasks_dir / pattern
                if task_file.exists():
                    task = PyfficeProjectPortAXN.load_task(str(task_file))
                    if task:
                        project.add_task(task)
                    break
        
        return project
    
    @staticmethod
    def save(project: PyfficeProject, paxn_path: str, tasks_dir: Optional[str] = None) -> None:
        """Save a PyfficeProject to PAXN format."""
        # Determine tasks directory
        if tasks_dir is None:
            tasks_dir = str(Path(paxn_path).parent.parent / 'tasks')
        
        os.makedirs(tasks_dir, exist_ok=True)
        
        # Extract project data
        name = project.document.get('verb_noun_txt', 'Unnamed Project')
        description = project.document.get('description', '')
        status = project.document.get('status', 'planning')
        
        # Build PAXN data structure
        paxn_data = {
            'name': name,
            'id': _generate_id(),
            'description': description or f'Project: {name}',
            'created': dt.now().isoformat(),
            'overall_progress': 0,
            'status': _map_pyffice_status_to_paxn(status),
            'tasks': {},
            'task_ids': [],
            'milestones': [],
            'dependencies': {},
            'metadata': {
                'source': 'pyffice',
                'exported': dt.now().isoformat(),
            }
        }
        
        # Export tasks
        documents = project.document.get('documents', {})
        if hasattr(documents, 'values'):
            task_docs = list(documents.values())
        else:
            task_docs = []
        
        for i, task_doc in enumerate(task_docs):
            task_id = task_doc.get('id') or _generate_id()
            paxn_data['task_ids'].append(task_id)
            
            # Save individual task file
            axn_data = PyfficeProjectPortAXN._task_to_axn(task_doc, task_id)
            task_file = Path(tasks_dir) / f"task_{task_id}.yaml"
            with open(task_file, 'w') as f:
                yaml.dump(axn_data, f, default_flow_style=False, sort_keys=False)
        
        # Save PAXN project file
        with open(paxn_path, 'w') as f:
            yaml.dump(paxn_data, f, default_flow_style=False, sort_keys=False)


# ====================================================================================================================||
# AXN Format Converter
# ====================================================================================================================||
class PyfficeProjectPortAXN:
    """Port for AXN (Task) format."""
    
    @staticmethod
    def load_task(axn_path: str) -> Optional[Dict]:
        """Load an AXN task file and return as dict."""
        with open(axn_path, 'r') as f:
            axn_data = yaml.safe_load(f)
        
        return PyfficeProjectPortAXN._axn_to_task_dict(axn_data)
    
    @staticmethod
    def _axn_to_task_dict(axn_data: Dict) -> Dict:
        """Convert AXN data to Pyffice task dict format."""
        # Map priority
        priority_map = {
            'critical': 1,
            'high': 2,
            'medium': 3,
            'low': 4,
            'minimal': 5,
        }
        priority = priority_map.get(
            axn_data.get('priority', 'medium').lower(), 
            3
        )
        
        # Map status
        status_map = {
            'pending': 'not_started',
            'in_progress': 'in_progress',
            'completed': 'completed',
            'blocked': 'blocked',
            'cancelled': 'cancelled',
        }
        status = status_map.get(
            axn_data.get('status', 'pending').lower(),
            'not_started'
        )
        
        # Parse depends_on
        depends_on = axn_data.get('depends_on', [])
        if isinstance(depends_on, str):
            depends_on = [depends_on]
        
        # Build description from AXN fields
        description = axn_data.get('description', '')
        scope = axn_data.get('scope', {})
        if scope:
            scope_text = _format_scope(scope)
            description = f"{description}\n\n{scope_text}" if description else scope_text
        
        # Create task dict (PyfficeTaskFrame document format)
        task_dict = {
            'verb_noun_txt': axn_data.get('name', 'Unnamed Task'),
            'description': description,
            'priority': priority,
            'status': status,
            'precedents': depends_on,
            'assignee': axn_data.get('assignee', '').lstrip('@'),
        }
        
        # Add dates
        if 'created' in axn_data:
            task_dict['created'] = _parse_date(axn_data['created'])
        if 'due_date' in axn_data:
            task_dict['due_dttm'] = _parse_date(axn_data['due_date'])
        if 'started' in axn_data:
            task_dict['start_dttm'] = _parse_date(axn_data['started'])
        if 'completed' in axn_data:
            task_dict['complete_dttm'] = _parse_date(axn_data['completed'])
        
        # Add progress
        progress = axn_data.get('progress', 0)
        if isinstance(progress, int):
            task_dict['progress'] = progress
        
        return task_dict
    
    @staticmethod
    def _task_to_axn(task_dict: Dict, task_id: Union[str, int]) -> Dict:
        """Convert Pyffice task dict to AXN format."""
        # Map priority
        priority_map = {
            1: 'critical',
            2: 'high', 
            3: 'medium',
            4: 'low',
            5: 'minimal',
        }
        
        # Map status
        status_map = {
            'not_started': 'pending',
            'in_progress': 'in_progress',
            'completed': 'completed',
            'blocked': 'blocked',
            'suspended': 'on_hold',
            'cancelled': 'cancelled',
        }
        
        # Get values from dict (handle both direct and nested document)
        name = task_dict.get('verb_noun_txt') or task_dict.get('name', 'Unnamed Task')
        description = task_dict.get('description', '')
        priority = task_dict.get('priority', 3)
        status = task_dict.get('status', 'not_started')
        
        axn_data = {
            'id': task_id,
            'name': name,
            'description': description,
            'priority': priority_map.get(priority, 'medium'),
            'status': status_map.get(status, 'pending'),
            'depends_on': task_dict.get('precedents', []) or task_dict.get('depends_on', []),
        }
        
        # Add dates
        if task_dict.get('start_dttm'):
            axn_data['started'] = _format_date(task_dict['start_dttm'])
        if task_dict.get('due_dttm'):
            axn_data['due_date'] = _format_date(task_dict['due_dttm'])
        if task_dict.get('complete_dttm'):
            axn_data['completed'] = _format_date(task_dict['complete_dttm'])
        
        # Add assignee
        assignee = task_dict.get('assignee', '')
        if assignee:
            axn_data['assignee'] = f"@{assignee}"
        
        # Add progress
        progress = task_dict.get('progress', 0)
        if progress:
            axn_data['progress'] = progress
        
        return axn_data


# ====================================================================================================================||
# Helper Functions
# ====================================================================================================================||
def _generate_id() -> str:
    """Generate a short ID."""
    import random
    return ''.join(random.choices('0123456789abcdef', k=8))


def _map_pyffice_status_to_paxn(status: str) -> str:
    """Map Pyffice status to PAXN status."""
    map_ = {
        'active': 'active',
        'planning': 'planning',
        'in_progress': 'active',
        'completed': 'completed',
        'suspended': 'on_hold',
        'cancelled': 'cancelled',
    }
    return map_.get(status, 'planning')


def _format_scope(scope: Dict) -> str:
    """Format scope dictionary as markdown text."""
    lines = []
    for key, value in scope.items():
        lines.append(f"**{key}:**")
        if isinstance(value, list):
            for item in value:
                lines.append(f"  - {item}")
        elif isinstance(value, dict):
            for subkey, subvalue in value.items():
                lines.append(f"  - {subkey}: {subvalue}")
        else:
            lines.append(f"  {value}")
    return '\n'.join(lines)


def _parse_date(date_str: Any) -> Optional[Any]:
    """Parse date string to date object."""
    if not date_str:
        return None
    if hasattr(date_str, 'date'):
        return date_str
    try:
        return datetime.date.fromisoformat(str(date_str).split('T')[0])
    except:
        return None


def _format_date(date_val: Any) -> Optional[str]:
    """Format date to ISO string."""
    if not date_val:
        return None
    if isinstance(date_val, str):
        return date_val
    if hasattr(date_val, 'isoformat'):
        return date_val.isoformat()
    return str(date_val)


# ====================================================================================================================||
# Exports
# ====================================================================================================================||
__all__ = [
    "PyfficeProjectPortPAXN",
    "PyfficeProjectPortAXN",
]

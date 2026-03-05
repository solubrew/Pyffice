"""
PAXN (ProjectAXN) Format Converter for Pyffice

PAXN is a YAML-based project format used by ProjectAXN/AXN task management.
This module provides converters to load/save PAXN projects as Pyffice projects.

PAXN Format:
- .paxn files: Project-level (contains multiple tasks)
- .axn files: Task-level (single task)

Author: Nchantrs Stack
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import yaml
import uuid


# PAXN Status Mapping
PAXN_STATUS_MAP = {
    'pending': 'pending',
    'in_progress': 'in_progress', 
    'completed': 'completed',
    'blocked': 'blocked',
    'cancelled': 'cancelled',
    'deferred': 'deferred',
}

# PAXN Priority Mapping (1=highest, 5=lowest in Pyffice)
PAXN_PRIORITY_MAP = {
    'critical': 1,
    'high': 2,
    'medium': 3,
    'low': 4,
    'trivial': 5,
}

REVERSE_PRIORITY_MAP = {v: k for k, v in PAXN_PRIORITY_MAP.items()}


@dataclass
class PAXNTask:
    """Represents a single task in PAXN format"""
    id: str
    title: str
    description: str = ""
    status: str = "pending"
    priority: str = "medium"
    project: Optional[str] = None
    assignee: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    created: Optional[str] = None
    updated: Optional[str] = None
    due: Optional[str] = None
    start: Optional[str] = None
    completed: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    subtasks: List[str] = field(default_factory=list)
    notes: str = ""
    effort_estimate: Optional[str] = None
    time_spent: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'project': self.project,
            'assignee': self.assignee,
            'tags': self.tags,
            'created': self.created,
            'updated': self.updated,
            'due': self.due,
            'start': self.start,
            'completed': self.completed,
            'dependencies': self.dependencies,
            'subtasks': self.subtasks,
            'notes': self.notes,
            'effort_estimate': self.effort_estimate,
            'time_spent': self.time_spent,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PAXNTask':
        """Create from dictionary"""
        return cls(
            id=data.get('id', str(uuid.uuid4())),
            title=data.get('title', ''),
            description=data.get('description', ''),
            status=data.get('status', 'pending'),
            priority=data.get('priority', 'medium'),
            project=data.get('project'),
            assignee=data.get('assignee'),
            tags=data.get('tags', []),
            created=data.get('created'),
            updated=data.get('updated'),
            due=data.get('due'),
            start=data.get('start'),
            completed=data.get('completed'),
            dependencies=data.get('dependencies', []),
            subtasks=data.get('subtasks', []),
            notes=data.get('notes', ''),
            effort_estimate=data.get('effort_estimate'),
            time_spent=data.get('time_spent'),
        )


@dataclass
class PAXNProject:
    """Represents a project in PAXN format"""
    id: str
    name: str
    description: str = ""
    status: str = "planning"
    priority: str = "medium"
    tasks: List[PAXNTask] = field(default_factory=list)
    created: Optional[str] = None
    updated: Optional[str] = None
    start: Optional[str] = None
    target: Optional[str] = None
    completed: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    members: List[str] = field(default_factory=list)
    owner: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'tasks': [t.to_dict() for t in self.tasks],
            'created': self.created,
            'updated': self.updated,
            'start': self.start,
            'target': self.target,
            'completed': self.completed,
            'tags': self.tags,
            'members': self.members,
            'owner': self.owner,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PAXNProject':
        """Create from dictionary"""
        tasks = [PAXNTask.from_dict(t) for t in data.get('tasks', [])]
        return cls(
            id=data.get('id', str(uuid.uuid4())),
            name=data.get('name', ''),
            description=data.get('description', ''),
            status=data.get('status', 'planning'),
            priority=data.get('priority', 'medium'),
            tasks=tasks,
            created=data.get('created'),
            updated=data.get('updated'),
            start=data.get('start'),
            target=data.get('target'),
            completed=data.get('completed'),
            tags=data.get('tags', []),
            members=data.get('members', []),
            owner=data.get('owner'),
        )


class PAXNConverter:
    """Converter between PAXN format and Pyffice format"""
    
    def __init__(self):
        self.status_map = PAXN_STATUS_MAP
        self.priority_map = PAXN_PRIORITY_MAP
    
    def load_paxn(self, path: str) -> PAXNProject:
        """Load a PAXN project from file"""
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
        return PAXNProject.from_dict(data)
    
    def save_paxn(self, project: PAXNProject, path: str):
        """Save a PAXN project to file"""
        with open(path, 'w') as f:
            yaml.dump(project.to_dict(), f, default_flow_style=False, sort_keys=False)
    
    def load_axn(self, path: str) -> PAXNTask:
        """Load an AXN task from file"""
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
        return PAXNTask.from_dict(data)
    
    def save_axn(self, task: PAXNTask, path: str):
        """Save an AXN task to file"""
        with open(path, 'w') as f:
            yaml.dump(task.to_dict(), f, default_flow_style=False, sort_keys=False)
    
    def convert_to_pyffice(self, paxn_project: PAXNProject) -> Dict[str, Any]:
        """Convert PAXN project to Pyffice project dict"""
        pyffice_project = {
            'id': paxn_project.id,
            'name': paxn_project.name,
            'description': paxn_project.description,
            'status': paxn_project.status,
            'priority': self.priority_map.get(paxn_project.priority, 3),
            'tags': paxn_project.tags,
            'created': paxn_project.created or datetime.now().isoformat(),
            'updated': datetime.now().isoformat(),
            'start_date': paxn_project.start,
            'target_date': paxn_project.target,
            'completed_date': paxn_project.completed,
            'owner': paxn_project.owner,
            'members': paxn_project.members,
            'items': [],
        }
        
        for task in paxn_project.tasks:
            pyffice_item = self.convert_task_to_pyffice(task)
            pyffice_project['items'].append(pyffice_item)
        
        return pyffice_project
    
    def convert_task_to_pyffice(self, task: PAXNTask) -> Dict[str, Any]:
        """Convert PAXN task to Pyffice item"""
        return {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'status': task.status,
            'priority': self.priority_map.get(task.priority, 3),
            'tags': task.tags,
            'assignee': task.assignee,
            'created': task.created or datetime.now().isoformat(),
            'updated': datetime.now().isoformat(),
            'due_date': task.due,
            'start_date': task.start,
            'completed_date': task.completed,
            'dependencies': task.dependencies,
            'notes': task.notes,
            'effort_estimate': task.effort_estimate,
            'time_spent': task.time_spent,
            'type': 'task',
        }
    
    def convert_from_pyffice(self, pyffice_dict: Dict[str, Any]) -> PAXNProject:
        """Convert Pyffice project dict to PAXN project"""
        tasks = []
        for item in pyffice_dict.get('items', []):
            if item.get('type') == 'task':
                tasks.append(self.convert_task_from_pyffice(item))
        
        priority = REVERSE_PRIORITY_MAP.get(pyffice_dict.get('priority', 3), 'medium')
        
        return PAXNProject(
            id=pyffice_dict.get('id', str(uuid.uuid4())),
            name=pyffice_dict.get('name', ''),
            description=pyffice_dict.get('description', ''),
            status=pyffice_dict.get('status', 'planning'),
            priority=priority,
            tasks=tasks,
            created=pyffice_dict.get('created'),
            updated=pyffice_dict.get('updated'),
            start=pyffice_dict.get('start_date'),
            target=pyffice_dict.get('target_date'),
            completed=pyffice_dict.get('completed_date'),
            tags=pyffice_dict.get('tags', []),
            members=pyffice_dict.get('members', []),
            owner=pyffice_dict.get('owner'),
        )
    
    def convert_task_from_pyffice(self, pyffice_item: Dict[str, Any]) -> PAXNTask:
        """Convert Pyffice item to PAXN task"""
        return PAXNTask(
            id=pyffice_item.get('id', str(uuid.uuid4())),
            title=pyffice_item.get('title', ''),
            description=pyffice_item.get('description', ''),
            status=pyffice_item.get('status', 'pending'),
            priority=REVERSE_PRIORITY_MAP.get(pyffice_item.get('priority', 3), 'medium'),
            assignee=pyffice_item.get('assignee'),
            tags=pyffice_item.get('tags', []),
            created=pyffice_item.get('created'),
            updated=pyffice_item.get('updated'),
            due=pyffice_item.get('due_date'),
            start=pyffice_item.get('start_date'),
            completed=pyffice_item.get('completed_date'),
            dependencies=pyffice_item.get('dependencies', []),
            notes=pyffice_item.get('notes', ''),
            effort_estimate=pyffice_item.get('effort_estimate'),
            time_spent=pyffice_item.get('time_spent'),
        )


# Convenience functions
def load_paxn(path: str) -> PAXNProject:
    """Load PAXN project from file"""
    return PAXNConverter().load_paxn(path)

def save_paxn(project: PAXNProject, path: str):
    """Save PAXN project to file"""
    return PAXNConverter().save_paxn(project, path)

def load_axn(path: str) -> PAXNTask:
    """Load AXN task from file"""
    return PAXNConverter().load_axn(path)

def save_axn(task: PAXNTask, path: str):
    """Save AXN task to file"""
    return PAXNConverter().save_axn(task, path)

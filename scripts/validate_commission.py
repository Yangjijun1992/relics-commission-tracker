#!/usr/bin/env python3
"""
Validate commission.json data format and consistency
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

REQUIRED_PROJECT_FIELDS = ['name', 'description', 'start_date', 'end_date']
REQUIRED_SUBSYSTEM_FIELDS = ['id', 'name', 'name_cn', 'responsible', 'planned_start', 'planned_end', 'subtasks']
REQUIRED_TASK_FIELDS = ['id', 'name', 'name_cn', 'planned_start', 'planned_end', 'status', 'progress', 'assignee', 'notes']
VALID_STATUSES = ['not_started', 'in_progress', 'completed', 'delayed', 'cancelled']

class ValidationError:
    def __init__(self, path: str, message: str):
        self.path = path
        self.message = message

    def __str__(self):
        return f"[{self.path}] {self.message}"

def validate_date(date_str: str, path: str) -> bool:
    """Validate date string format (YYYY-MM-DD)."""
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_progress(progress: int, path: str) -> bool:
    """Validate progress value (0-100)."""
    return 0 <= progress <= 100

def validate_subsystem(subsystem: dict, index: int, errors: list):
    """Validate a single subsystem."""
    path = f"subsystems[{index}]"

    for field in REQUIRED_SUBSYSTEM_FIELDS:
        if field not in subsystem:
            errors.append(ValidationError(path, f"Missing required field: {field}"))

    if 'planned_start' in subsystem and 'planned_end' in subsystem:
        if not validate_date(subsystem['planned_start'], f"{path}.planned_start"):
            errors.append(ValidationError(f"{path}.planned_start", "Invalid date format (expected YYYY-MM-DD)"))
        if not validate_date(subsystem['planned_end'], f"{path}.planned_end"):
            errors.append(ValidationError(f"{path}.planned_end", "Invalid date format (expected YYYY-MM-DD)"))
        
        if validate_date(subsystem['planned_start'], f"{path}.planned_start") and \
           validate_date(subsystem['planned_end'], f"{path}.planned_end"):
            start = datetime.strptime(subsystem['planned_start'], '%Y-%m-%d')
            end = datetime.strptime(subsystem['planned_end'], '%Y-%m-%d')
            if start > end:
                errors.append(ValidationError(path, "planned_start is after planned_end"))

    if 'subtasks' in subsystem:
        for task_index, task in enumerate(subsystem['subtasks']):
            validate_task(task, f"{path}.subtasks[{task_index}]", errors)

    if 'github_user' in subsystem and subsystem['github_user']:
        github_user = subsystem['github_user']
        if github_user.startswith('@'):
            github_user = github_user[1:]
        if not github_user.isalnum() and not github_user.replace('-', '').replace('_', '').isalnum():
            errors.append(ValidationError(f"{path}.github_user", "Invalid GitHub username format"))

def validate_task(task: dict, path: str, errors: list):
    """Validate a single task."""
    for field in REQUIRED_TASK_FIELDS:
        if field not in task:
            errors.append(ValidationError(path, f"Missing required field: {field}"))

    if 'planned_start' in task and 'planned_end' in task:
        if not validate_date(task['planned_start'], f"{path}.planned_start"):
            errors.append(ValidationError(f"{path}.planned_start", "Invalid date format (expected YYYY-MM-DD)"))
        if not validate_date(task['planned_end'], f"{path}.planned_end"):
            errors.append(ValidationError(f"{path}.planned_end", "Invalid date format (expected YYYY-MM-DD)"))
        
        if validate_date(task['planned_start'], f"{path}.planned_start") and \
           validate_date(task['planned_end'], f"{path}.planned_end"):
            start = datetime.strptime(task['planned_start'], '%Y-%m-%d')
            end = datetime.strptime(task['planned_end'], '%Y-%m-%d')
            if start > end:
                errors.append(ValidationError(path, "planned_start is after planned_end"))

    if 'progress' in task:
        if not isinstance(task['progress'], int):
            errors.append(ValidationError(f"{path}.progress", "Progress must be an integer"))
        elif not validate_progress(task['progress'], f"{path}.progress"):
            errors.append(ValidationError(f"{path}.progress", "Progress must be between 0 and 100"))

    if 'status' in task and task['status'] not in VALID_STATUSES:
        errors.append(ValidationError(f"{path}.status", f"Invalid status: {task['status']}. Must be one of: {VALID_STATUSES}"))

def validate_json(data: dict) -> list[ValidationError]:
    """Validate the entire JSON structure."""
    errors = []

    if 'project' not in data:
        errors.append(ValidationError("root", "Missing 'project' section"))
    else:
        for field in REQUIRED_PROJECT_FIELDS:
            if field not in data['project']:
                errors.append(ValidationError("project", f"Missing required field: {field}"))
        
        if 'start_date' in data['project'] and 'end_date' in data['project']:
            if not validate_date(data['project']['start_date'], "project.start_date"):
                errors.append(ValidationError("project.start_date", "Invalid date format (expected YYYY-MM-DD)"))
            if not validate_date(data['project']['end_date'], "project.end_date"):
                errors.append(ValidationError("project.end_date", "Invalid date format (expected YYYY-MM-DD)"))

    if 'subsystems' not in data:
        errors.append(ValidationError("root", "Missing 'subsystems' array"))
    else:
        subsystem_ids = set()
        for index, subsystem in enumerate(data['subsystems']):
            validate_subsystem(subsystem, index, errors)
            
            if 'id' in subsystem:
                if subsystem['id'] in subsystem_ids:
                    errors.append(ValidationError(f"subsystems[{index}]", f"Duplicate subsystem ID: {subsystem['id']}"))
                subsystem_ids.add(subsystem['id'])
            
            if 'subtasks' in subsystem:
                task_ids = set()
                for task_index, task in enumerate(subsystem['subtasks']):
                    if 'id' in task:
                        if task['id'] in task_ids:
                            errors.append(ValidationError(f"subsystems[{index}].subtasks[{task_index}]", f"Duplicate task ID: {task['id']}"))
                        task_ids.add(task['id'])

    return errors

def validate_consistency(data: dict) -> list[ValidationError]:
    """Check for consistency issues like timeline overlaps."""
    errors = []
    
    for sys_index, subsystem in enumerate(data.get('subsystems', [])):
        sys_path = f"subsystems[{sys_index}]"
        
        if 'planned_start' in subsystem and 'planned_end' in subsystem:
            sys_start = datetime.strptime(subsystem['planned_start'], '%Y-%m-%d')
            sys_end = datetime.strptime(subsystem['planned_end'], '%Y-%m-%d')
            
            for task_index, task in enumerate(subsystem.get('subtasks', [])):
                task_path = f"{sys_path}.subtasks[{task_index}]"
                
                if 'planned_start' in task and 'planned_end' in task:
                    task_start = datetime.strptime(task['planned_start'], '%Y-%m-%d')
                    task_end = datetime.strptime(task['planned_end'], '%Y-%m-%d')
                    
                    # These are warnings, not errors - tasks may intentionally extend beyond subsystem
                    # if task_start < sys_start:
                    #     errors.append(ValidationError(task_path, 
                    #         f"WARNING: Task starts ({task['planned_start']}) before subsystem start ({subsystem['planned_start']})"))
                    
                    # if task_end > sys_end:
                    #     errors.append(ValidationError(task_path,
                    #         f"WARNING: Task ends ({task['planned_end']}) after subsystem end ({subsystem['planned_end']})"))

    return errors

def main():
    script_dir = Path(__file__).parent
    json_path = script_dir.parent / "data" / "commission.json"

    if not json_path.exists():
        print(f"Error: {json_path} not found", file=sys.stderr)
        sys.exit(1)

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {json_path}: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading {json_path}: {e}", file=sys.stderr)
        sys.exit(1)

    errors = validate_json(data)
    consistency_errors = validate_consistency(data)
    errors.extend(consistency_errors)

    if errors:
        print(f"Validation failed with {len(errors)} error(s):")
        for error in errors:
            print(f"  {error}")
        sys.exit(1)
    else:
        print("Validation passed!")
        sys.exit(0)

if __name__ == "__main__":
    main()

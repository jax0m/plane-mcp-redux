"""
Setup Test Project and Items
=============================

This script creates a test project with work items and labels for feature testing.

Usage:
    python docs/makeplane_plane-python-sdk/workspace/TEST_SETUP_SCRIPT.py

Outputs:
    - Test project with work items
    - Labels assigned to items
    - Ready for feature testing (modules, cycles, etc.)
"""

import os
import sys

from dotenv import load_dotenv
from plane import PlaneClient
from plane.models.labels import CreateLabel
from plane.models.work_items import CreateWorkItem, UpdateWorkItem

sys.path.insert(0, "/workspaces/makeplane/plane-python-sdk")

load_dotenv("/workspaces/plane-mcp-redux/.env")

config = {
    "base_url": os.getenv("PLANE_BASE_URL", "https://api.plane.so"),
    "api_key": os.getenv("PLANE_API_KEY", ""),
    "workspace_slug": os.getenv("PLANE_WORKSPACE_SLUG", "workspace"),
}

client = PlaneClient(base_url=config["base_url"], api_key=config["api_key"])

projects = client.projects.list(workspace_slug=config["workspace_slug"])
project_uuid = projects.results[0].id
workspace_slug = config["workspace_slug"]

print("=" * 80)
print("SETUP TEST PROJECT")
print("=" * 80)

# 1. Create test project
print("\n1. Create test project")
try:
    project = client.projects.create(
        workspace_slug=workspace_slug,
        data={"name": "Feature Test Project", "identifier": "FEATURETEST123"},
    )
    print(f"Created project: {project.name} (ID: {project.id})")
    project_uuid = project.id
except Exception as e:
    print(f"Project create failed: {e}")
    print(f"Using existing project: {project_uuid}")

# 2. Create 3 work items
print("\n2. Create 3 work items")
item1 = client.work_items.create(
    workspace_slug=workspace_slug,
    project_id=project_uuid,
    data=CreateWorkItem(name="Work Item 1"),
)
item2 = client.work_items.create(
    workspace_slug=workspace_slug,
    project_id=project_uuid,
    data=CreateWorkItem(name="Work Item 2"),
)
item3 = client.work_items.create(
    workspace_slug=workspace_slug,
    project_id=project_uuid,
    data=CreateWorkItem(name="Work Item 3"),
)
print(f"Created items: {item1.id}, {item2.id}, {item3.id}")

# 3. Create 2 labels
print("\n3. Create 2 labels")
label1 = client.labels.create(
    workspace_slug=workspace_slug, project_id=project_uuid, data=CreateLabel(name="Bug")
)
label2 = client.labels.create(
    workspace_slug=workspace_slug,
    project_id=project_uuid,
    data=CreateLabel(name="Feature"),
)
print(f"Created labels: {label1.id} (Bug), {label2.id} (Feature)")

# 4. Assign labels
print("\n4. Assign labels to work items")
client.work_items.update(
    workspace_slug=workspace_slug,
    project_id=project_uuid,
    work_item_id=item1.id,
    data=UpdateWorkItem(labels=[label1.id]),
)
print("Item 1: Bug label assigned")

client.work_items.update(
    workspace_slug=workspace_slug,
    project_id=project_uuid,
    work_item_id=item2.id,
    data=UpdateWorkItem(labels=[label2.id]),
)
print("Item 2: Feature label assigned")

client.work_items.update(
    workspace_slug=workspace_slug,
    project_id=project_uuid,
    work_item_id=item3.id,
    data=UpdateWorkItem(labels=[label1.id, label2.id]),
)
print("Item 3: Both labels assigned")

print("\n5. Summary")
print(f"Project: {project_uuid}")
print(f"Items: {item1.id}, {item2.id}, {item3.id}")
print(f"Labels: {label1.id}, {label2.id}")
print("\nSetup complete! Ready for feature testing.")

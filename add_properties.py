"""
03 - Add Properties to Objects in a Speckle Model

This script demonstrates how to receive objects from Speckle,
add custom properties, and send them back as a new version.
"""

from main import get_client
from specklepy.transports.server import ServerTransport
from specklepy.api import operations
from specklepy.objects.base import Base
from specklepy.core.api.inputs.version_inputs import CreateVersionInput


PROJECT_ID = "128262a20c"
MODEL_ID = "e09d9dbeca"


# ----------------------------------
# Authenticate
# ----------------------------------
client = get_client()


# ----------------------------------
# Get the latest version
# ----------------------------------
latest_version = client.version.get_versions(
    MODEL_ID,
    PROJECT_ID,
    limit=1
).items[0]

print(f"✓ Fetching version: {latest_version.id}")


# ----------------------------------
# Receive the data
# ----------------------------------
transport = ServerTransport(
    client=client,
    stream_id=PROJECT_ID
)

data = operations.receive(
    latest_version.referenced_object,
    transport
)


# ----------------------------------
# Add root-level properties
# ----------------------------------
data["custom_property"] = "Team_02.1"
data["analysis_date"] = "2026-02-02"
data["processed_by"] = "Zeynep Sezen Dursun"


# ----------------------------------
# Find "Old modules" collection
# ----------------------------------
def find_collection(obj, name):
    elements = getattr(obj, "@elements", None) or getattr(obj, "elements", [])

    for el in elements or []:
        if getattr(el, "name", None) == name:
            return el

        found = find_collection(el, name)
        if found:
            return found

    return None


old_modules = find_collection(data, "Old modules")


# ----------------------------------
# Modify Designer names
# ----------------------------------
new_designers = [
    "Aditye Kossambe",
    "David Agudelo",
]

if old_modules:
    old_elements = getattr(old_modules, "@elements", None) or getattr(
        old_modules, "elements", []
    )

    for element, designer in zip(old_elements, new_designers):
        if isinstance(element, Base) and "properties" in element.get_member_names():
            element["properties"]["Designer"] = designer

    print("✓ Updated Designer names in 'Old modules' collection.")


# ----------------------------------
# Send the modified data back
# ----------------------------------
object_id = operations.send(data, [transport])
print(f"✓ Sent object: {object_id}")


# ----------------------------------
# Create a new version in Speckle
# ----------------------------------
version = client.version.create(
    CreateVersionInput(
        projectId=PROJECT_ID,
        modelId=MODEL_ID,
        objectId=object_id,
        message="Updated Designer names in Old modules",
    )
)

print(f"✓ Created new version: {version.id}")
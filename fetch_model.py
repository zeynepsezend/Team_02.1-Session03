from main import get_client

PROJECT_ID = "128262a20c"
SOURCE_MODEL_NAME = "a1014e4b32"
TARGET_MODEL_NAME = "96b3069344"

def main():
    client = get_client()

    # Tüm modelleri al
    models = client.model.get_models(PROJECT_ID)

    source = next(m for m in models.items if m.name == SOURCE_MODEL_NAME)

    # Latest version
    versions = client.version.get_versions(source.id, PROJECT_ID, limit=1)
    latest = versions.items[0]

    print("✓ Source model found")
    print("  Commit:", latest.id)
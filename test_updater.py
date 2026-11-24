import sys
sys.path.insert(0, r"C:\jarvis")

from core.updater import JarvisUpdater

updater = JarvisUpdater()
print("Checking for updates...")
result = updater.check()
if result:
    print(f"✅ Update available: {result['version']}")
    print(f"Files: {len(result['files'])}")
    print(f"Changelog: {len(result['changelog'])}")
    for f in result['files'][:5]:
        print(f"  {f}")
    if len(result['files']) > 5:
        print(f"  ... and {len(result['files']) - 5} more")
else:
    print("No updates (same version)")
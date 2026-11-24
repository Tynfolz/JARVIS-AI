#!/usr/bin/env python3
"""
Auto-generate update_manifest.py from git.
Run after committing: python gen_manifest.py
"""
import subprocess
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE)

def run(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=BASE)
    if result.returncode != 0:
        print(f"❌ {cmd}")
        print(result.stderr)
        return None
    return result.stdout.strip()

# Get current version from core/version.py
with open(os.path.join(BASE, "core", "version.py"), "r", encoding="utf-8") as f:
    exec(f.read())
version = VERSION

# Get changed files since last tag (or all files if no tags)
tags = run("git tag --sort=-v:refname")
last_tag = tags.split("\n")[0] if tags else None

if last_tag:
    changed = run(f"git diff --name-only {last_tag} HEAD")
else:
    changed = run("git ls-files")

if not changed:
    print("No files to include")
    sys.exit(1)

files = sorted([f.replace("\\", "/") for f in changed.split("\n") if f.strip()])

# Get commit messages for changelog
log = run(f"git log --oneline -20")
changelog = [line.split(" ", 1)[1] for line in log.split("\n") if line.strip()]

# Generate manifest
manifest = f'''VERSION = "{version}"

FILES = [
'''

for f in files:
    manifest += f'    "{f}",\n'

manifest += ''']

CHANGELOG = [
'''

for c in changelog:
    manifest += f'    "{c}",\n'

manifest += ''']

'''

with open(os.path.join(BASE, "update_manifest.py"), "w", encoding="utf-8") as f:
    f.write(manifest)

print(f"✅ Generated update_manifest.py")
print(f"Version: {version}")
print(f"Files: {len(files)}")
print(f"Changelog: {len(changelog)}")
#!/usr/bin/env python3
"""
Check GEMINI_API_KEY configuration and availability.

Checks in priority order:
1. Process environment variable
2. Skill directory .env file
3. Project root .env file
"""

import os
import sys
from pathlib import Path


def check_api_key():
    """Check for GEMINI_API_KEY in all possible locations"""

    print("Checking GEMINI_API_KEY configuration...\n")

    found = False

    # 1. Check process environment
    print("[1] Process Environment Variable")
    env_key = os.environ.get('GEMINI_API_KEY')
    if env_key:
        masked = env_key[:8] + '...' + env_key[-4:] if len(env_key) > 12 else '***'
        print(f"    ✓ Found: {masked}")
        found = True
    else:
        print("    ✗ Not found")

    # 2. Check skill directory .env
    print("\n[2] Skill Directory .env File")
    skill_dir = Path(__file__).parent.parent
    skill_env = skill_dir / '.env'
    print(f"    Path: {skill_env}")

    if skill_env.exists():
        skill_key = load_env_file(skill_env)
        if skill_key:
            masked = skill_key[:8] + '...' + skill_key[-4:] if len(skill_key) > 12 else '***'
            print(f"    ✓ Found: {masked}")
            if not found:
                found = True
        else:
            print("    ✗ File exists but GEMINI_API_KEY not found")
    else:
        print("    ✗ File does not exist")

    # 3. Check project root .env
    print("\n[3] Project Root .env File")
    current = Path.cwd()
    project_root = None

    # Find project root
    while current != current.parent:
        if (current / '.git').exists() or (current / '.claude').exists():
            project_root = current
            break
        current = current.parent

    if project_root:
        project_env = project_root / '.env'
        print(f"    Path: {project_env}")

        if project_env.exists():
            project_key = load_env_file(project_env)
            if project_key:
                masked = project_key[:8] + '...' + project_key[-4:] if len(project_key) > 12 else '***'
                print(f"    ✓ Found: {masked}")
                if not found:
                    found = True
            else:
                print("    ✗ File exists but GEMINI_API_KEY not found")
        else:
            print("    ✗ File does not exist")
    else:
        print("    ✗ Project root not found")

    # Summary
    print("\n" + "="*60)
    if found:
        print("✓ GEMINI_API_KEY is configured and available")
        print("\nYou can now use the gemini-video-understanding skill!")
        return 0
    else:
        print("✗ GEMINI_API_KEY not found")
        print("\nTo configure:")
        print("\n  Option 1 (Recommended): Environment Variable")
        print("    export GEMINI_API_KEY='your-api-key-here'")
        print("\n  Option 2: Skill Directory .env")
        print(f"    echo 'GEMINI_API_KEY=your-api-key-here' > {skill_env}")
        print("\n  Option 3: Project Root .env")
        if project_root:
            print(f"    echo 'GEMINI_API_KEY=your-api-key-here' > {project_root}/.env")
        else:
            print("    echo 'GEMINI_API_KEY=your-api-key-here' > .env")
        print("\nGet your API key at: https://aistudio.google.com/apikey")
        return 1


def load_env_file(env_path: Path) -> str:
    """Load GEMINI_API_KEY from .env file"""
    try:
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('GEMINI_API_KEY='):
                    value = line.split('=', 1)[1]
                    # Remove quotes if present
                    value = value.strip('"').strip("'")
                    return value if value else None
    except Exception as e:
        print(f"    ⚠ Error reading file: {e}")
    return None


if __name__ == '__main__':
    sys.exit(check_api_key())

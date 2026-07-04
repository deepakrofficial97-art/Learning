import subprocess
import sys
import os

os.environ.setdefault("FLASK_APP", "app.py")


def run(command):
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        sys.exit(result.returncode)


if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else None

    if action == "init":
        print("Initializing migrations folder...")
        run("flask db init")

    elif action == "migrate":
        message = sys.argv[2] if len(sys.argv) > 2 else "auto migration"
        print(f"Generating migration: '{message}'")
        run(f'flask db migrate -m "{message}"')

    elif action == "upgrade":
        print("Applying migrations to DB...")
        run("flask db upgrade")

    elif action == "downgrade":
        print("Rolling back last migration...")
        run("flask db downgrade")

    elif action == "history":
        run("flask db history")

    elif action == "current":
        run("flask db current")

    else:
        print("""
Usage:
  python migrate.py init                               # run once at project start
  python migrate.py migrate "add phone to employee"   # when model changes
  python migrate.py upgrade                            # apply to DB
  python migrate.py downgrade                          # rollback
  python migrate.py history                            # see all versions
  python migrate.py current                            # see current version
        """)
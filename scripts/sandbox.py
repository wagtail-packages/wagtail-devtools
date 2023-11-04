import subprocess

import click


@click.command()
def init_sandbox():
    """Initialize the sandbox by running migrations."""

    click.echo("Initializing sandbox...")
    subprocess.run(["./venv/bin/python", "sandboxmanage.py", "migrate"])


@click.command()
def reset_sandbox():
    """Reset the sandbox by deleting the database."""

    click.echo("Resetting sandbox...")
    subprocess.run(["rm", "sandbox.db"])
    click.echo("Sandbox reset.")


@click.command()
def create_superuser():
    """Create a superuser for the sandbox."""

    superuser = "from django.contrib.auth.models import User;(not User.objects.filter(username='admin').exists()) and User.objects.create_superuser('admin', 'admin@admin.com', 'admin')"

    subprocess.run(
        ["./venv/bin/python", "sandboxmanage.py", "shell", "-c", superuser],
        check=True,
    )
    click.echo(
        "Superuser created with Username: admin Password: admin Email: admin@admin.com"
    )

    click.echo(
        "Run the sandbox with ./venv/bin/python sandboxmanage.py runserver or activate your virtual environment with source venv/bin/activate and run the sandbox with python sandboxmanage.py runserver"
    )
    click.echo("Login at http://localhost:8000/admin/")


@click.command()
def run_sandbox():
    """Run the sandbox."""

    click.echo("Running sandbox...")
    subprocess.run(["./venv/bin/python", "sandboxmanage.py", "runserver"])

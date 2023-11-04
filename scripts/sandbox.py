import subprocess

import click


@click.command()
def init_sandbox():
    """Initialize the sandbox by running migrations."""

    click.echo("Initializing sandbox...")
    subprocess.run(["./venv/bin/python", "sandboxmanage.py", "migrate"])


@click.command()
@click.option(
    "--version", default=52, type=int, help="Wagtail version to load data for."
)
def sandbox_loaddata(version):
    """Load data into the sandbox."""

    dumpdata_files = {
        41: "sandbox/fixtures/data/wagtail_41_plus_data.json",
        52: "sandbox/fixtures/data/wagtail_52_plus_data.json",
    }

    click.echo("Loading data into sandbox...")
    delete_users = (
        "from django.contrib.auth.models import User; User.objects.all().delete()"
    )
    subprocess.run(
        ["./venv/bin/python", "sandboxmanage.py", "shell", "-c", delete_users],
        check=True,
    )
    if version not in dumpdata_files:
        raise Exception(f"No data for Wagtail version {version}")
    elif version == 41:
        subprocess.run(
            [
                "./venv/bin/python",
                "sandboxmanage.py",
                "loaddata",
                "sandbox/fixtures/data/wagtail_41_plus_data.json",
            ]
        )
    else:
        subprocess.run(
            [
                "./venv/bin/python",
                "sandboxmanage.py",
                "loaddata",
                "sandbox/fixtures/data/wagtail_52_plus_data.json",
            ]
        )


@click.command()
def sandbox_dumpdata():
    """Dump data from the sandbox."""

    click.echo("Dumping data from sandbox...")
    excludes_41_plus = [
        "contenttypes",
        "auth.Permission",
        "sessions",
        "admin.logentry",
        "auth.Group",
        # "auth.User",
        "wagtailimages.rendition",
        "wagtailsearch.sqliteftsindexentry",
        "wagtailsearch.indexentry",
        "wagtailcore.referenceindex",
        "wagtailcore.grouppagepermission",
        "wagtailcore.groupcollectionpermission",
        "wagtailcore.modellogentry",
        "wagtailcore.locale",
        "wagtailcore.collection",
        "wagtailcore.workflowpage",
        "wagtailcore.workflowtask",
        "wagtailcore.task",
        "wagtailcore.workflow",
        "wagtailcore.pagesubscription",
        "wagtailcore.groupapprovaltask",
        # "wagtailusers.userprofile",
    ]

    cmd = [
        "./venv/bin/python",
        "sandboxmanage.py",
        "dumpdata",
        "--natural-foreign",
        "--natural-primary",
    ]
    cmd += [f"--exclude={exclude}" for exclude in excludes_41_plus]
    cmd += [
        "--indent",
        "4",
        "--output",
        "sandbox/fixtures/data/wagtail_41_plus_data.json",
    ]

    excludes_52_plus = excludes_41_plus + [
        "home.testmodeladmin",
    ]
    cmd = [
        "./venv/bin/python",
        "sandboxmanage.py",
        "dumpdata",
        "--natural-foreign",
        "--natural-primary",
    ]
    cmd += [f"--exclude={exclude}" for exclude in excludes_52_plus]
    cmd += [
        "--indent",
        "4",
        "--output",
        "sandbox/fixtures/data/wagtail_52_plus_data.json",
    ]

    subprocess.run(cmd)


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

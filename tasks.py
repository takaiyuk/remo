from invoke import task


@task
def run(ctx):
    """Run the remo CLI"""
    ctx.run("poetry run python -m remo")


@task
def format(ctx):
    """Format the code"""
    ctx.run(
        """
        poetry run black .
        poetry run isort .
        """
    )

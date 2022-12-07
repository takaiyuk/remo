from invoke import task

from remo.utils import read_env


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


@task
def docker_build(ctx):
    """Build the Docker image"""
    ctx.run(
        """
        source .ecr-env

        docker build -f ./docker/lambda/Dockerfile -t $IMAGE:$TAG .
        """
    )


@task
def ecr_push(ctx):
    """Push the Docker image to ECR"""
    ctx.run(
        """
        source .ecr-env

        export ECR_URI=$ECR_URI_PREFIX/$IMAGE:$TAG
        aws ecr get-login-password | docker login --username AWS --password-stdin $ECR_URI_PREFIX
        docker tag $IMAGE:$TAG $ECR_URI
        docker push $ECR_URI
        """
    )

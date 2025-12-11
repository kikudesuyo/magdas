import os

from invoke.tasks import task


def get_env(extra_env: dict = {}) -> dict:
    path = os.path.abspath(os.path.dirname(__file__))
    env = {"PYTHONPATH": f"{os.environ.get('PYTHONPATH', '')}:{path}"}
    if extra_env:
        env.update(extra_env)
    return env


@task
def run(c, filename):
    c.run(f"python {filename}", env=get_env({"PYTHONUNBUFFERED": "1"}))


@task
def server(c):
    path = os.path.abspath(os.path.dirname(__file__))
    env = {"PYTHONPATH": f"{os.environ.get('PYTHONPATH', '')}:{path}"}
    c.run("uvicorn main:app --reload", env=env)


@task
def debug(c, filename):
    c.run(
        f"python -m debugpy --listen 5678 --wait-for-client {filename}", env=get_env()
    )


@task
def test(c, filename):
    c.run(f"python -m unittest {filename}", env=get_env())


@task
def test_all(c):
    """Run all tests
    Caution:
        Command `invoke test_all` is not available.
        Use `invoke test-all` instead.
    """
    c.run("python -m unittest", env=get_env())

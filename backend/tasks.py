import os

from invoke.tasks import task


@task
def run(c, filename):
    path = os.path.abspath(os.path.dirname(__file__))
    env = {"PYTHONPATH": f"{os.environ.get('PYTHONPATH', '')}:{path}"}
    c.run(f"python {filename}", env=env)


@task
def server(c):
    path = os.path.abspath(os.path.dirname(__file__))
    env = {"PYTHONPATH": f"{os.environ.get('PYTHONPATH', '')}:{path}"}
    c.run("uvicorn main:app --reload", env=env)


@task
def debug(c, filename):
    path = os.path.abspath(os.path.dirname(__file__))
    env = {"PYTHONPATH": f"{os.environ.get('PYTHONPATH', '')}:{path}"}
    c.run(f"python -m debugpy --listen 5678 --wait-for-client {filename}", env=env)


@task
def test(c, filename):
    path = os.path.abspath(os.path.dirname(__file__))
    env = {"PYTHONPATH": f"{os.environ.get('PYTHONPATH', '')}:{path}"}
    c.run(f"python -m unittest {filename}", env=env)


@task
def test_all(c):
    """Run all tests
    Caution:
        Command `invoke test_all` is not available.
        Use `invoke test-all` instead.
    """
    path = os.path.abspath(os.path.dirname(__file__))
    env = {"PYTHONPATH": f"{os.environ.get('PYTHONPATH', '')}:{path}"}
    c.run("python -m unittest", env=env)

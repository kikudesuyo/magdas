import os

from invoke.tasks import task


@task
def run(c, filename):
    path = os.path.abspath(os.path.dirname(__file__))
    # Windows環境用のコマンド
    if os.name == "nt":
        c.run(f'set "pythonpath=%PATH%;{path}" && python {filename}"')
    else:
        c.run(f'export PYTHONPATH="$PYTHONPATH:{path}" && python {filename}')


@task
def server(c):
    path = os.path.abspath(os.path.dirname(__file__))
    if os.name == "nt":
        c.run(f'set "pythonpath=%PATH%;{path}" && uvicorn main:app --relRoad')
    else:
        c.run(f'export PYTHONPATH="$PYTHONPATH:{path}" && uvicorn main:app --reload')


@task
def debug(c, filename):
    path = os.path.abspath(os.path.dirname(__file__))
    if os.name == "nt":
        c.run(
            f'set "pythonpath=%PATH%;{path}" && python -m debugpy --listen 5678 --wait-for-client {filename}'
        )
    else:
        c.run(
            f'export PYTHONPATH="$PYTHONPATH:{path}" && python -m debugpy --listen 5678 --wait-for-client {filename}'
        )


@task
def test(c, filename):
    path = os.path.abspath(os.path.dirname(__file__))
    if os.name == "nt":
        c.run(f'set "pythonpath=%PATH%;{path}" && python -m unittest {filename}"')
    else:
        c.run(
            f'export PYTHONPATH="$PYTHONPATH:{path}" && python -m unittest {filename}'
        )


@task
def test_all(c):
    """Run all tests
    Caution:
        Command `invoke test_all` is not available.
        Use `invoke test-all` instead.
    """
    path = os.path.abspath(os.path.dirname(__file__))
    if os.name == "nt":
        c.run(f'set "pythonpath=%PATH%;{path}" && python -m unittest')
    else:
        c.run(f'export PYTHONPATH="$PYTHONPATH:{path}" && python -m unittest')

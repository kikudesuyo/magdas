from pathlib import Path


def generate_abs_path(path):
    """絶対パスを生成

    Arg:
      path (str): ee-index/からの相対パス

    Return:
      str: 引数pathへの絶対パス
    """
    return str(Path(__file__).parents[1]) + path


def generate_parent_abs_path(path):
    """親ディレクトリの絶対パスを生成

    Description:
        ee-indexディレクトリよりも上のディレクトリを参照するための関数
        MAGDASデータを参照する際に使用
    Arg:
        path (str): ../ee-index/からの相対パス
    Return:
        str: 引数pathへの絶対パス
    """
    return str(Path(__file__).parents[2]) + path

from types import GeneratorType

import pytest


def sample_generator():
    print('code before yield "a"')
    yield "a"
    print('code before yield "b"')
    yield "b"
    print("code before last yield")
    yield


def test_generator_yield_basic(capsys):
    """
    ジェネレータ関数の基本

    ジェネレータ関数を呼び出すと、ジェネレータオブジェクトが返される。
    ジェネレータオブジェクトの__next__()メソッドが呼び出されると、
    関数内の次のyield命令までの処理が実行される。
    （__next__()メソッドはnext関数またはイテレート経由で呼び出す）
    処理はそこで一時停止し、呼び出し元に制御が戻される。
    その際に、呼び出し元にはyield命令で指定した値(省略した場合はNone)が返される。

    ジェネレータオブジェクトの__next__()メソッドを再度実行すると、
    一時停止箇所から次のyield命令までの処理が実行され、
    また呼び出し元に制御が戻される。

    尚、現在のジェネレータオブジェクトの状態から次のyield命令がない時に、
    __next__()メソッドを実行するとStopIteration例外が発生する。
    """
    gen = sample_generator()
    assert isinstance(gen, GeneratorType)
    assert next(gen) == "a"
    assert capsys.readouterr().out.rstrip() == 'code before yield "a"'
    assert next(gen) == "b"
    assert capsys.readouterr().out.rstrip() == 'code before yield "b"'
    assert next(gen) is None
    assert capsys.readouterr().out.rstrip() == "code before last yield"
    with pytest.raises(StopIteration):
        next(gen)


def test_generator_iterate():
    """
    ジェネレータオブジェクトをfor文でイテレートすることで、
    ジェネレータ関数内の各yield式の値を順次得ることができる
    """
    result = []
    for value in sample_generator():
        result.append(value)

    assert result == ["a", "b", None]

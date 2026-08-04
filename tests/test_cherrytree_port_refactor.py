"""Regression tests for the CherryTree port module split."""


def test_cherrytree_port_is_exported_from_noteports_and_public_ports_api():
    """The moved port remains importable from its canonical and public APIs."""
    from pyffice.ports.noteports import PyfficePortCherryTree as canonical
    from pyffice.ports import PyfficePortCherryTree as public

    assert public is canonical


def test_pyffice_codex_import_uses_moved_cherrytree_port():
    """The main PyfficeCodex consumer imports after the port module split."""
    from pyffice.pyffice import PyfficeCodex
    from pyffice.ports.noteports import PyfficePortCherryTree

    assert PyfficeCodex.import_cherrytree.__globals__["PyfficePortCherryTree"] is PyfficePortCherryTree

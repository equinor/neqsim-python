from scripts.generate_stubs import sanitize_python_local_references


def test_sanitize_python_local_references(tmp_path):
    stub = tmp_path / "example.pyi"
    stub.write_text(
        "from jneqsim.display import register.<locals>._StreamDisplay\n"
        "import typing\n\n"
        "class Stream(JavaBase, register.<locals>._StreamDisplay): ...\n"
        "class DisplayOnly(register.<locals>._StreamDisplay): ...   \n\n",
        encoding="utf-8",
    )

    sanitize_python_local_references(tmp_path)

    content = stub.read_text(encoding="utf-8")
    assert "<locals>" not in content
    assert "class Stream(JavaBase): ..." in content
    assert "class DisplayOnly(typing.Protocol): ..." in content
    assert content.endswith("...\n")
    compile(content, str(stub), "exec")

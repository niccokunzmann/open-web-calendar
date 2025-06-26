from pathlib import Path  # noqa: INP001

HERE = Path(__file__).parent


for po_file in HERE.glob("**/*.po"):
    content = po_file.read_text()
    print(po_file)  # noqa: T201
    if not any(line.startswith('"Content-Type:') for line in content.splitlines()):
        content = content.replace(
            'msgstr ""', 'msgstr ""\n"Content-Type: text/plain; charset=UTF-8\\n"', 1
        )
        po_file.write_text(content)
        print("\t added header")  # noqa: T201

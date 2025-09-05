from pr_reviewer.diff_parser import chunk_patch

def test_chunk_patch():
    sample = "\n".join([f"line {i}" for i in range(1000)])
    chunks = chunk_patch(sample, max_lines=100)
    assert len(chunks) == 10
    assert chunks[0].startswith("line 0")
    assert chunks[-1].endswith("line 999")

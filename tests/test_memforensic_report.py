import importlib.util
from pathlib import Path


MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "labs"
    / "memforensic"
    / "memforensic_toolkit.py"
)


def load_toolkit():
    spec = importlib.util.spec_from_file_location("memforensic_toolkit", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_build_html_report_preserves_css_and_escapes_output(tmp_path):
    toolkit = load_toolkit()
    (tmp_path / "sample.txt").write_text("<script>alert('x')</script>", encoding="utf-8")

    report_path = toolkit.build_html_report(tmp_path, "report.html")
    report = report_path.read_text(encoding="utf-8")

    assert "body { font-family:" in report
    assert "&lt;script&gt;alert(&#39;x&#39;)&lt;/script&gt;" in report
    assert "<script>alert('x')</script>" not in report
    assert report.rstrip().endswith("</html>")

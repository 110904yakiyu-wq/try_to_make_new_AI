import importlib.util,json
from pathlib import Path
here=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("audit",here/"run.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
assert m.assay()==json.loads((here/"results/default.json").read_text())
print("smoke: PASS")

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

MODULE = ROOT / "demo.py"
spec = importlib.util.spec_from_file_location("invernadero", MODULE)
demo = importlib.util.module_from_spec(spec)
sys.modules["invernadero"] = demo
spec.loader.exec_module(demo)

SETPOINT = demo.SETPOINT
cargar_clima = demo.cargar_clima
controlador_difuso = demo.controlador_difuso
simular = demo.simular
step_temperature = demo.step_temperature
triangular = demo.triangular


def test_triangular_limites():
    assert triangular(0.0, 0.0, 1.0, 2.0) == 0.0
    assert triangular(2.0, 0.0, 1.0, 2.0) == 0.0
    assert triangular(1.0, 0.0, 1.0, 2.0) == 1.0
    assert 0.0 < triangular(0.5, 0.0, 1.0, 2.0) < 1.0


def test_calefaccion_cuando_hace_frio():
    heater, vent = controlador_difuso(SETPOINT - 3.0)
    assert heater > 0.5
    assert vent == 0.0


def test_sin_calefaccion_cuando_hace_calor():
    heater, vent = controlador_difuso(SETPOINT + 3.0)
    assert heater == 0.0
    assert vent > 0.0


def test_zona_muerta():
    heater, vent = controlador_difuso(SETPOINT)
    assert heater == 0.0
    assert vent == 0.0


def test_calefaccion_sube_temperatura():
    frio = step_temperature(15.0, 5.0, 0.0, 0.0, 0.0)
    caliente = step_temperature(15.0, 5.0, 0.0, 1.0, 0.0)
    assert caliente > frio


def test_ventilacion_baja_temperatura():
    sin_vent = step_temperature(25.0, 15.0, 0.0, 0.0, 0.0)
    con_vent = step_temperature(25.0, 15.0, 0.0, 0.0, 1.0)
    assert con_vent < sin_vent


def test_simulacion_completa():
    clima = cargar_clima(ROOT / "data" / "clima_24h.csv")
    assert len(clima) == 24
    resultado = simular(clima)
    assert 0.0 <= resultado["pct_en_banda"] <= 100.0
    assert resultado["pct_en_banda"] >= 50.0
    assert resultado["t_int_min"] <= resultado["t_int_max"]
    assert len(resultado["pasos"]) == 24


def test_demo_escribe_evidencia(tmp_path):
    out = tmp_path / "report.md"
    js = tmp_path / "sim.json"
    clima = cargar_clima(ROOT / "data" / "clima_24h.csv")
    resultado = simular(clima)
    demo.escribir_informe(resultado, out)
    js.write_text(json.dumps(resultado), encoding="utf-8")
    assert out.exists() and "Invernadero EcoSmart" in out.read_text(encoding="utf-8")
    assert json.loads(js.read_text(encoding="utf-8"))["setpoint"] == SETPOINT

#!/usr/bin/env python3
"""Invernadero EcoSmart - gemelo digital (demo simplificada).

Capacidad 7 - Control climatico e IoT.

Reproduce el lazo de control del gemelo digital EcoSmart: un modelo termico
simplificado del invernadero mas un controlador difuso determinista que decide
la potencia de calefaccion y la apertura de ventilacion para mantener el
setpoint de temperatura. El proyecto real anade una regresion Ridge para estimar
el interior, un LLM local supervisor (Ollama) y datos de la estacion
MeteoGalicia; aqui se conserva la logica de control para que la demo corra con
solo la biblioteca estandar de Python 3.

Uso:
    python demo.py --demo
    python demo.py --input data/clima_24h.csv --report report.md

Solo biblioteca estandar de Python 3.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFAULT_INPUT = ROOT / "data" / "clima_24h.csv"
DEFAULT_REPORT = ROOT / "report.md"
DEFAULT_JSON = ROOT / "data" / "simulacion.json"

# --- Parametros del modelo termico simplificado ------------------------------
C_INERCIA = 0.9        # inercia termica (dC por unidad de flujo)
UA = 0.12              # perdida por envolvente (dC/h por dC de salto)
GANANCIA_SOLAR = 0.002  # aporte solar (dC/h por W/m2)
GANANCIA_CALOR = 3.0   # aporte de la calefaccion (dC/h por unidad de potencia)
GANANCIA_VENT = 0.5    # perdida por ventilacion (dC/h por unidad de apertura)
SETPOINT = 20.0        # consigna de temperatura interior (dC)
BANDA = 2.0            # banda de confort (dC)


def step_temperature(t_in: float, t_out: float, solar: float, heater: float,
                     vent: float) -> float:
    """Un paso de integracion del balance termico del invernadero."""
    perdida = UA * (t_in - t_out)
    aporte_solar = GANANCIA_SOLAR * solar
    aporte_calor = GANANCIA_CALOR * heater
    perdida_vent = GANANCIA_VENT * vent * max(0.0, t_in - t_out)
    return t_in + (aporte_solar + aporte_calor - perdida - perdida_vent) / C_INERCIA


# --- Controlador difuso determinista ----------------------------------------
def triangular(x: float, a: float, b: float, c: float) -> float:
    """Pertenencia triangular: 1 en b, 0 en a y c."""
    if x <= a or x >= c:
        return 0.0
    if x == b:
        return 1.0
    if x < b:
        return (x - a) / (b - a)
    return (c - x) / (c - b)


def controlador_difuso(t_in: float, setpoint: float = SETPOINT) -> tuple[float, float]:
    """Devuelve (calefaccion, ventilacion) en 0..1 a partir del error termico.

    Controlador difuso tipo Mamdani: cinco conjuntos triangulares sobre el error
    (consigna - temperatura interior) y salidas singleton ponderadas.
    """
    error = setpoint - t_in  # >0 -> hace frio, <0 -> hace calor

    reglas = (
        (triangular(error, 1.5, 3.0, 4.5), 1.00),    # frio fuerte
        (triangular(error, 0.2, 1.0, 1.8), 0.60),    # frio
        (triangular(error, -0.8, 0.0, 0.8), 0.00),   # zona de confort
        (triangular(error, -1.8, -1.0, -0.2), 0.00),  # calor
        (triangular(error, -4.5, -3.0, -1.5), 0.00),  # calor fuerte
    )
    numerador = sum(m * w for m, w in reglas)
    denominador = sum(m for m, _ in reglas)
    heater = numerador / denominador if denominador else 0.0

    exceso = max(0.0, t_in - setpoint)
    vent = min(1.0, exceso / 4.0)
    return round(heater, 4), round(vent, 4)


# --- Simulacion --------------------------------------------------------------
def cargar_clima(path: Path) -> list[dict]:
    filas: list[dict] = []
    with path.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            filas.append({
                "hora": int(row["hora"]),
                "t_ext": float(row["t_ext"]),
                "solar": float(row["solar"]),
            })
    if not filas:
        raise ValueError(f"sin datos de clima en {path}")
    return filas


def simular(clima: list[dict], t_inicial: float = 16.0) -> dict:
    t_in = t_inicial
    pasos: list[dict] = []
    en_banda = 0
    energia_calor = 0.0
    for f in clima:
        heater, vent = controlador_difuso(t_in)
        t_nueva = step_temperature(t_in, f["t_ext"], f["solar"], heater, vent)
        dentro = abs(t_nueva - SETPOINT) <= BANDA
        en_banda += int(dentro)
        energia_calor += heater
        pasos.append({
            "hora": f["hora"], "t_ext": f["t_ext"], "solar": f["solar"],
            "t_int": round(t_nueva, 2), "heater": heater, "vent": vent,
            "en_banda": dentro,
        })
        t_in = t_nueva
    n = len(pasos)
    return {
        "pasos": pasos,
        "t_int_final": round(t_in, 2),
        "t_int_min": round(min(p["t_int"] for p in pasos), 2),
        "t_int_max": round(max(p["t_int"] for p in pasos), 2),
        "pct_en_banda": round(100.0 * en_banda / n, 1),
        "horas_calefaccion": round(energia_calor, 2),
        "setpoint": SETPOINT,
        "banda": BANDA,
    }


def escribir_informe(resultado: dict, out: Path) -> None:
    lineas = [
        "# Invernadero EcoSmart — informe de simulación (demo)",
        "",
        "> Muestra generada por la demo del gemelo digital. El proyecto real usa",
        "> regresión Ridge, controlador difuso y un LLM local supervisor (Ollama)",
        "> sobre datos de MeteoGalicia; aquí se reproduce el lazo de control con",
        "> un modelo térmico simplificado.",
        "",
        f"- Setpoint: **{resultado['setpoint']} °C** (± {resultado['banda']} °C)",
        f"- Temperatura interior final: **{resultado['t_int_final']} °C**",
        f"- Rango interior: **{resultado['t_int_min']} – {resultado['t_int_max']} °C**",
        f"- Tiempo dentro de banda: **{resultado['pct_en_banda']} %**",
        f"- Calefacción acumulada (u): **{resultado['horas_calefaccion']}**",
        "",
        "| Hora | T ext (°C) | Solar (W/m²) | T int (°C) | Calef. | Vent. | En banda |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | :---: |",
    ]
    for p in resultado["pasos"]:
        lineas.append(
            f"| {p['hora']:02d} | {p['t_ext']} | {p['solar']} | {p['t_int']} | "
            f"{p['heater']} | {p['vent']} | {'sí' if p['en_banda'] else 'no'} |"
        )
    lineas += ["", "© 2026 Ronny L. Díaz López. Todos los derechos reservados.", ""]
    out.write_text("\n".join(lineas), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Gemelo digital de invernadero (demo)")
    ap.add_argument("--demo", action="store_true", help="corre la simulación de 24 h")
    ap.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    ap.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    ap.add_argument("--json", type=Path, default=DEFAULT_JSON)
    args = ap.parse_args()

    if not args.input.exists():
        print(f"[error] falta {args.input}")
        return 1

    resultado = simular(cargar_clima(args.input))
    escribir_informe(resultado, args.report)
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(resultado, ensure_ascii=False, indent=2),
                         encoding="utf-8")
    print(f"[ok] {args.report.name}: {resultado['pct_en_banda']}% en banda, "
          f"T final {resultado['t_int_final']} °C")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

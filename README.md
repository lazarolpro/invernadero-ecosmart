# Capa 7 — Control climático e IoT (gemelo digital)

[![CI](https://github.com/lazarolpro/invernadero-ecosmart/actions/workflows/ci.yml/badge.svg)](https://github.com/lazarolpro/invernadero-ecosmart/actions/workflows/ci.yml)
[`lazarolpro/invernadero-ecosmart`](https://github.com/lazarolpro/invernadero-ecosmart) · parte del [portafolio de 9 capacidades](https://github.com/lazarolpro/portafolio)

> © 2026 Ronny L. Díaz López. **Todos los derechos reservados.** Prohibida su
> venta o uso comercial sin autorización escrita. Ver [`LICENSE`](LICENSE).

**Capacidad demostrada:** mantener una variable de proceso (temperatura) dentro de
su banda de confort con un **controlador difuso** sobre un modelo térmico del
invernadero, decidiendo actuadores (calefacción y ventilación).

## Problema real

Un invernadero se enfría de noche y se sobrecalienta al mediodía. Sin control
automático hay que regular a mano y el cultivo sufre; con control mal ajustado se
gasta energía de más. La solución es un **gemelo digital**: un modelo del recinto
que permite probar el lazo de control antes de instalar un solo sensor.

## Qué hace la demo

- Integra un **modelo térmico** (inercia, pérdida por envolvente, aporte solar,
  calefacción y ventilación) a partir de un perfil horario de clima.
- Aplica un **controlador difuso tipo Mamdani** (cinco conjuntos triangulares
  sobre el error térmico) que decide la potencia de calefacción y la apertura de
  ventilación.
- Emite un informe con el porcentaje de tiempo dentro de banda y la energía de
  calefacción acumulada, más la traza completa en JSON.

> Alcance honesto: esta demo reproduce el **lazo de control** con un modelo
> simplificado. El proyecto EcoSmart real añade una regresión Ridge para estimar
> el interior, un LLM local supervisor (Ollama) y datos reales de la estación
> MeteoGalicia; aquí se conserva la lógica de control para que corra con solo la
> biblioteca estándar de Python 3.

## Cómo ejecutar

```bash
python demo.py --demo          # simulación de 24 h -> report.md + data/simulacion.json
python -m pytest -q
```

## Evidencia que produce

- [`report.md`](report.md) — informe de la simulación (banda, energía, traza).
- `data/clima_24h.csv` — perfil de clima de entrada (hora, temperatura, solar).
- `data/simulacion.json` — traza reproducible paso a paso.
- Pruebas del modelo y del controlador en verde.

## Stack

Python 3 (solo biblioteca estándar). Sin dependencias externas.

## Por qué le importa a la empresa

Cubre **control de procesos e IoT**: el mismo patrón (medir → modelar → decidir →
actuar) sirve para climatización, riego o cualquier lazo de control industrial.

**En mantenimiento:** permite ajustar y validar un lazo de control sin tocar el
equipo real, y detectar cuándo un actuador no responde como debería.

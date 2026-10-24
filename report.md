# Invernadero EcoSmart — informe de simulación (demo)

> Muestra generada por la demo del gemelo digital. El proyecto real usa
> regresión Ridge, controlador difuso y un LLM local supervisor (Ollama)
> sobre datos de MeteoGalicia; aquí se reproduce el lazo de control con
> un modelo térmico simplificado.

- Setpoint: **20.0 °C** (± 2.0 °C)
- Temperatura interior final: **19.2 °C**
- Rango interior: **18.03 – 21.01 °C**
- Tiempo dentro de banda: **100.0 %**
- Calefacción acumulada (u): **8.71**

| Hora | T ext (°C) | Solar (W/m²) | T int (°C) | Calef. | Vent. | En banda |
| ---: | ---: | ---: | ---: | ---: | ---: | :---: |
| 00 | 6.2 | 0.0 | 18.03 | 1.0 | 0.0 | sí |
| 01 | 5.8 | 0.0 | 19.73 | 1.0 | 0.0 | sí |
| 02 | 5.4 | 0.0 | 18.05 | 0.0702 | 0.0 | sí |
| 03 | 5.1 | 0.0 | 19.66 | 1.0 | 0.0 | sí |
| 04 | 4.9 | 0.0 | 18.16 | 0.1406 | 0.0 | sí |
| 05 | 5.0 | 10.0 | 19.76 | 1.0 | 0.0 | sí |
| 06 | 6.1 | 60.0 | 18.2 | 0.039 | 0.0 | sí |
| 07 | 7.8 | 150.0 | 20.46 | 0.9929 | 0.0 | sí |
| 08 | 9.6 | 280.0 | 18.94 | 0.0 | 0.1147 | sí |
| 09 | 11.5 | 430.0 | 20.9 | 0.6 | 0.0 | sí |
| 10 | 13.2 | 560.0 | 20.15 | 0.0 | 0.2262 | sí |
| 11 | 14.6 | 650.0 | 20.74 | 0.0 | 0.0384 | sí |
| 12 | 15.4 | 690.0 | 21.01 | 0.0 | 0.1848 | sí |
| 13 | 15.6 | 660.0 | 21.0 | 0.0 | 0.2531 | sí |
| 14 | 15.1 | 570.0 | 20.66 | 0.0 | 0.2491 | sí |
| 15 | 14.0 | 440.0 | 20.14 | 0.0 | 0.1652 | sí |
| 16 | 12.6 | 300.0 | 19.65 | 0.0 | 0.0348 | sí |
| 17 | 11.0 | 160.0 | 19.34 | 0.1451 | 0.0 | sí |
| 18 | 9.4 | 60.0 | 19.68 | 0.4599 | 0.0 | sí |
| 19 | 8.2 | 10.0 | 18.57 | 0.1189 | 0.0 | sí |
| 20 | 7.4 | 0.0 | 19.08 | 0.6 | 0.0 | sí |
| 21 | 6.9 | 0.0 | 19.46 | 0.6 | 0.0 | sí |
| 22 | 6.5 | 0.0 | 18.88 | 0.3443 | 0.0 | sí |
| 23 | 6.3 | 0.0 | 19.2 | 0.6 | 0.0 | sí |

© 2026 Ronny L. Díaz López. Todos los derechos reservados.

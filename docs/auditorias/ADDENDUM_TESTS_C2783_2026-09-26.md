# Cotejo independiente del ajuste de tests C-2783

UTC real: 2026-09-26T22:59:57Z. Revisor: `/root/verificacion_fuentes_nuevas`;
autor del ajuste: `/root`. Rama: `codex/cierre-plan-pendiente`.
Alcance exclusivo: actualización de las expectativas de tests después del
parche C-2783 ya revisado; no constituye revisión científica nueva.

Dictamen acotado: CONFORME. Leí el diff y ejecuté los cinco tests de
`tests.test_build_atomic_cell_claims`: todos pasan. El cambio no reduce las
expectativas anteriores: exige nominalmente las mismas 14 C corregidas,
añade C-2783 como decimoquinta corrección, fija los textos y SHA anterior y
nuevo, y comprueba que C-2783 no hereda C-2821/C-2822 posteriores.

Comprobación propia, independiente de las aserciones añadidas: leí las filas
de `correcciones_celdas_semanticas_v1.csv` y su versión HEAD; al excluir
C-2783, las 14 filas restantes coinciden celda por celda y en orden. Recalculé
ambas SHA del texto literal C-2783 más LF final, conforme al contrato de
`_digest`, y cotejé en el CSV vivo la atribución
`sintesis(C-1565, C-1566)` y Fuente `n/a; dependencias canónicas C-1565; C-1566`.
No aparecen C-2821/C-2822 dentro de esa fila. El código del constructor atómico
no tiene cambios frente a HEAD. No se editó ningún archivo revisado.

La primera comprobación propia de SHA omitió el LF del contrato y falló;
al leer `_digest` se corrigió únicamente el auditor temporal y ambas huellas
coincidieron. No fue un fallo del corpus ni se cambió su contenido para pasar.

| Objeto | SHA-256 |
|---|---|
| `tests/test_build_atomic_cell_claims.py` | `e0d0dd20edd6c2870bc482ea8333e4094e2d6ba0bd232f37e2e9049f9f36d55d` |
| `scripts/build_atomic_cell_claims.py` | `f3d8ff6b7a03552e500dc735a9ca169d628e86cc87799bddb7689bc74002b6aa` |
| `data/auditoria/correcciones_celdas_semanticas_v1.csv` | `5cfad5a16210d698f42d5a850e325ec9a441724ee8e9909741ec5928a180a270` |

Este addendum no altera el dictamen científico previo, no aprueba requisitos
completos ni cierra el censo semántico/global.

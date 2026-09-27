# Reinspección independiente del delta HGT

Revisor: `/root/revision_residuales/candidatos_editoriales`.
Rama: `codex/cierre-plan-pendiente`.
Inicio real:2026-09-27T01:30:43Z. Instantánea final:
2026-09-27T01:32:09.111165Z. Dictámenes:2026-09-27T01:33:21Z.

**Resultado: seis filas CONFORME en sus nuevas huellas**, tras lectura del
contenido modificado y pasajes primarios, no por tests del autor:
C-1186, C-1196, C-1197, C-1198, C-2832 y C-2838.
El CSV nuevo es `dictamenes_reinspeccion_independiente_delta_hgt_2026-09-27.csv`;
filas completas y hashes quedan en
`evidencia_reinspeccion_independiente_delta_hgt_2026-09-27.json`.

## Qué se volvió a comprobar

- **C-1186/C-2838:** releídos S290 Sec3, párrafo7, y Conclusion Sec8.
  La propuesta de barrera y el juicio de rareza/importancia quedaron separados.
  Se conservan ambos contenidos atribuidos, sin promoverlos a consenso.
- **C-2832:** la media aproximada de inventario sigue siendo la del
  [cuarto Highlight editorial](https://www.sciencedirect.com/science/article/pii/S0168952520302067),
  concordante con [Rutgers](https://scholarship.libraries.rutgers.edu/esploro/outputs/journalArticle/Horizontal-Gene-Transfer-in-Eukaryotes-Not/991031665538804646).
  La advertencia queda visible como cautela del estimador en Motivo y prosa.
  No se finge cuerpo completo ni PDF local de S291.
- **C-1196:** el nuevo localizador lleva al apartado correcto de la versión
  final S296. Su conclusión expresa tiene respaldo en los párrafos de
  contaminación/cobertura y cierre del apartado.
- **C-1197:** se cotejó el caso original en
  [S295, Significance/Abstract](https://pmc.ncbi.nlm.nih.gov/articles/PMC4702960/)
  y la crítica en el HTML final S296, *Claims of Extensive Functional Horizontal
  Gene Transfer into H. dujardini*. Ya no atribuye quimerismo ni convierte
  binning/cobertura en causa del falso positivo. La síntesis acota contaminación
  no detectada. No he adjudicado todo S295 ni sus inferencias de HGT real.
- **C-1198:** permanecen una síntesis y premisas nominadas; el nuevo Motivo
  distingue evidencia de aceptación. La etiqueta de consenso no acreditada
  desaparece. Las lecturas de S561, S211 y S296 apoyan la distinción entre
  casos positivos y falsos positivos, no una aprobación universal de cualquier
  candidato. Esto no firma separadamente todas las C padre.

El HTML final S296 inspeccionado tiene SHA256
`386809ac25942beaf0f8351ff6c3e2f3dc9de7b11b07210bc75908a915eb2136`.
El PDF local anterior sigue siendo el preprint2015: su NC de identificación
no se borra ni se transfiere al HTML nuevo.

## Conservación y alcance

Las seis filas corregidas coinciden íntegramente con la historia del autor
`correccion_hgt_tras_revision_2026-09-27.json`, SHA256
`97b88cd3186c16a4e377c8dea31455b776f32cc41482e38f18d5ea2e9974876f`.
Las cuatro filas antiguas con NC coinciden con las instantáneas independientes.
La historia de C-1196 preserva su proposición y cambia el localizador; C-2838
es nueva. Se inspeccionaron la prosa nominal y las etiquetas B vinculadas:
el nuevo contenido está sincronizado en esos destinos. Sus hashes completos
están en la evidencia, sin que ello equivalga a revisar todas sus demás filas.

El CSV inicial permanece intacto, SHA256
`c353f26334b07631dfc10db4ecfd90f35c10af2fc0075eca9c022400922d450d`.
Sus cuatro NC siguen siendo válidas para sus versiones antiguas; este
documento no las sobrescribe.

No redacté el parche, aunque identifiqué sus defectos y antes participé en
búsqueda/propuestas de los lotes S560/HGT. Esta es una reinspección de
implementación independiente del autor, no un investigador nuevo que
sustituya una segunda revisión independiente del conjunto.

Ninguna conformidad de estas seis filas aprueba los210 controles, los censos
globales C/S, la congelación, los derivados pendientes o `make verify`.
No se editaron canónicos ni se registraron fechas en nombre de otra persona.

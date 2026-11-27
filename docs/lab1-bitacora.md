# Laboratorio 1 — Bitácora de auditoría de la cadena de suministro

- **Autor/a:** ESCRIBE_AQUÍ_TU_NOMBRE_Y_APELLIDOS
- **Repositorio:** https://github.com/TU-USUARIO/reportaudit-lab
- **Sistema operativo y versión de Python usados:**

> Completa cada sección en el momento en que la guía te lo pide, no al final.
> Una bitácora escrita "de memoria" al terminar no sirve como evidencia.

---

## Parte B — Auditoría manual (antes de usar ninguna herramienta)

| # | Función | Línea | Qué sospechas | Dato de entrada (*source*) | Destino peligroso (*sink*) |
|---|---|---|---|---|---|
| 1 | reporte_auditoria.py | La línea de SMTP_PASSWORD | Contraseña hardcodeada | Credencial/contraseña | SMTP_PASSWORD |
| 2 | reporte_auditoria.py  | La línea de md5() | Uso de MD5 para hashing | Datos que se quieren proteger | md5() |
| 3 |  |  |  |  |  |
| 4 |  |  |  |  |  |
| 5 |  |  |  |  |  |

**Impacto en el negocio:** para cada sospecha, explica en una frase qué
consecuencia tendría para ReportAudit y sus clientes si fuera real (qué datos,
qué sistema o qué credencial quedarían expuestos).

---

## Matriz de detección (se completa a lo largo del laboratorio)

Marca ✓ (lo detectó, anota la regla) o ✗ (no lo detectó) en cada columna cuando
llegues a la parte correspondiente.

| Hallazgo | Manual (B) | SonarQube for IDE sin conexión (D) | SonarQube for IDE en Connected Mode (E) | SonarQube Cloud (F) | CodeQL (F) | Semgrep (G) | Trivy (K) |
|---|---|---|---|---|---|---|---|
| H1 Inyección SQL en `buscar_reportes_cliente` |  |  |  |  |  |  | n/a |
| H2 Inyección de comandos en `convertir_a_pdf` |  |  |  |  |  |  | n/a |
| H3 Deserialización YAML insegura en `cargar_configuracion` |  |  |  |  |  |  | n/a |
| H4 Hash MD5 en `hash_password_legacy` |  |  |  |  |  |  | n/a |
| H5 Clave de API escrita en el código |  |  |  |  |  |  |  |
| H6 Contraseña SMTP escrita en el código |  |  |  |  |  |  |  |

**Conclusión de la matriz** (Parte K): ¿alguna herramienta lo detectó todo? ¿Qué
te dice eso sobre depender de una sola herramienta?

---

## Parte J — SBOM: el iceberg medido

| Dato | Valor |
|---|---|
| Dependencias directas (`requirements.in`) |  |
| Componentes Python en el SBOM |  |
| Otros componentes que aparezcan en el SBOM (si los hay) y de dónde salen |  |
| Formato y versión de especificación del SBOM (`bomFormat`, `specVersion`) |  |

---

## Parte J — Triage de vulnerabilidades de dependencias (Grype)

| Paquete | Versión | ¿Directa o transitiva? (usa `# via`) | CVE / GHSA | Severidad | Corregida en | ¿Explotable en ReportAudit? ¿Por qué? | Decisión |
|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |

**Comparación con Dependabot** (Parte H): ¿las alertas coinciden con Grype? Explica
cualquier diferencia.

**Documento VEX:** copia `plantillas/reportaudit.openvex.json` a
`docs/evidencias/`, rellénalo, enlázalo aquí y resume en una frase la
justificación.

---

## Parte L y M — Antes y después

| Medida | Antes | Después |
|---|---|---|
| Hallazgos de Semgrep en `app/` |  |  |
| Alertas abiertas de CodeQL (Security → Code scanning) |  |  |
| Vulnerabilidades en SonarQube Cloud (rama main) |  |  |
| Security Hotspots por revisar en SonarQube Cloud |  |  |
| Vulnerabilidades de Grype sobre el SBOM |  |  |
| Alertas abiertas de Dependabot |  |  |

---
### Q. Divulgación coordinada (simulacro)

**Primera parte: compañero como investigador y yo como responsable del producto.**

- **Informe recibido de:** `juanmi2109`.
- **Identificador del borrador de aviso:** `GHSA-hch6-pqq8-wgqg`.
- **Título:** SQL injection in `/reportes` (cliente parameter) in versions before 1.0.0.
- **Estado:** Draft (borrador privado).
- **Severidad mostrada por GitHub:** Moderate.
- **Vector CVSS:** pendiente de verificar el vector definitivo del borrador.
- **CWE:** CWE-89 — SQL Injection.
- **Paquete:** `reportaudit` (ecosistema `pip`).
- **Versiones afectadas:** `< 1.0.0`.
- **Versión corregida:** `1.0.0`.
- **Créditos:** `juanmi2109`, con el rol Reporter.
- **Comentario:** se añadió un agradecimiento en inglés al investigador en la conversación privada del borrador.
- **Evidencias:** capturas del informe recibido, aceptación como borrador, configuración del advisory y comentario de agradecimiento.

**Segunda parte: pendiente.** Falta que yo informe de una vulnerabilidad en el repositorio de Juanmi y que él gestione el aviso como responsable del producto. Por tanto, el simulacro Q.3 todavía no está completado en su totalidad.

El advisory de este repositorio se mantiene como borrador privado. No se ha solicitado un CVE ni se ha publicado el aviso.

### R. Versión 1.0.0 verificable

**R.1 — Publicación automatizada**

- Workflow: `.github/workflows/publicar-version.yml`.
- Rama de publicación: `main`.
- Etiqueta Git: `v1.0.0`.
- Resultado: ejecución correcta del workflow `Publicar versión firmada`.
- Commit del workflow: `b4eb6c7`.
- Resultado: Release publicada correctamente en GitHub.

**R.2 — Release v1.0.0**

- Enlace: https://github.com/Samubrr/reportaudit-lab/releases/tag/v1.0.0
- Archivos publicados:
  - `reportaudit-1.0.0.tar.gz`
  - `reportaudit-provenance.sigstore.json`
  - `reportaudit-sbom.cdx.json`
  - `reportaudit-sbom.sigstore.json`
  - `SHA256SUMS`

**R.3 — Verificación como cliente**

- Descarga: se descargaron los archivos de la Release mediante `gh release download v1.0.0`.
- Integridad: `sha256sum -c SHA256SUMS` devolvió `OK` para el paquete y el SBOM.
- Procedencia SLSA: `gh attestation verify reportaudit-1.0.0.tar.gz --repo "$REPO"` devolvió `Verification succeeded!`.
- SBOM CycloneDX: la verificación con `--predicate-type https://cyclonedx.org/bom` también devolvió `Verification succeeded!`.
- Prueba de manipulación: se creó una copia del paquete llamada `alterado.tar.gz` y se añadió el texto `puerta trasera`. Su huella SHA-256 cambió:
  - Original: `ffdd5c346d3b199db2b169b2040767f0c34b668295c366100f06eb3fa329fddf`
  - Alterado: `912de56f8375df7423d02ea0c22c233942ed976d79569f361491b52e45e32325`
- Verificación del archivo alterado: GitHub devolvió `HTTP 404: Not Found` al buscar una atestación para la nueva huella. La prueba detectó correctamente que el archivo modificado no tenía una atestación asociada.

**Incidencia**

- Issue #11: `Release v1.0.0 with an SBOM and signed provenance`.
- Estado: cerrada.
- Se añadió un comentario indicando la publicación y los resultados de las verificaciones.

**Conclusión**

La versión v1.0.0 se ha publicado con SBOM, sumas SHA-256 y atestaciones Sigstore. Se ha comprobado la integridad y procedencia del paquete original y se ha demostrado que una modificación posterior impide encontrar una atestación válida para el archivo alterado.

## Preguntas de comprobación (Sección 7 de la guía)

1.
2.
3.
4.
5.
6.
7.
8.
9.
10.
11.
12.

## Backlog del laboratorio (Issues)

| Issue | Título | PR o evidencia de cierre |
|---|---|---|
| #1 | Adopt an international pull request template | |
| #2 | Run SAST (SonarQube Cloud and CodeQL) on every pull request | |
| #3 | Block insecure commits with a Semgrep pre-commit hook | |
| #4 | Enable Dependabot alerts and security updates | |
| #5 | Remediate the findings of the security audit | |
| #6 | Upgrade the vulnerable dependencies | |
| #7 | Publish the audit log and the before/after evidence | |
| #8 | Detect ReportAudit credentials in the whole Git history | |
| #9 | Make SCA and secret scanning required checks on main | |
| #10 | Publish a security policy and a private vulnerability reporting channel | |
| #11 | Release v1.0.0 with an SBOM and signed provenance | |
| #12 | Measure supply-chain maturity with OpenSSF Scorecard | |
| #13 | Build the CRA evidence index | |

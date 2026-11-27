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

### P. Puertas obligatorias en main

| Check | ¿Exigido en main? | Resultado en las pruebas |
|---|---|---|
| SAST - SonarQube Cloud | Sí | Correcto (verde) |
| SAST - CodeQL | Sí | Correcto (verde) |
| SCA - pip-audit | Sí | Fallido inicialmente (rojo); corregido localmente |
| Secretos - Gitleaks | Sí | Correcto (verde) |

**Configuración realizada**

Se añadieron los jobs `sca-pip-audit` y `secretos-gitleaks` al workflow `cadena-suministro.yml` en una rama de prueba.

En GitHub se configuró la protección de la rama `main` para exigir los cuatro checks de seguridad y mantener la aprobación de una Pull Request antes de fusionar cambios. También se comprobó que Push Protection estaba activada.

**Prueba de la puerta SCA**

En la primera prueba se utilizaron temporalmente Flask 3.0.0 y Werkzeug 3.0.1. `pip-audit` detectó 15 vulnerabilidades conocidas en ambos paquetes y terminó con código de salida 1, haciendo fallar el check.

Posteriormente, en una nueva Pull Request limpia, el análisis detectó 2 vulnerabilidades en Flask 3.0.0. Se identificó la vulnerabilidad `PYSEC-2026-2151`, cuya versión corregida es Flask 3.1.3.

Se actualizó Flask a la versión 3.1.3 en `requirements.in` y se regeneró `requirements.txt` mediante `pip-compile`. También se eliminaron las dependencias antiguas de Blinker e Itsdangerous.

La comprobación local posterior con `pip-audit -r requirements.txt` devolvió el resultado `No known vulnerabilities found`.

Además, se eliminó del workflow el parámetro `disable-pip`, que no estaba admitido por la versión utilizada de la acción.



**1. ¿Qué diferencia hay entre una alerta de Dependabot y el check SCA - pip-audit?**

Dependabot detecta vulnerabilidades en las dependencias y genera alertas, además de poder proponer actualizaciones mediante Pull Requests. Sin embargo, una alerta por sí sola no impide fusionar cambios.

Por el contrario, `pip-audit` analiza las dependencias del proyecto y, al configurarse como un check obligatorio, impide que se fusione una Pull Request cuando detecta vulnerabilidades conocidas.

**2. ¿Por qué no se exigió pip-audit desde la Parte G?**

Porque antes era necesario corregir las vulnerabilidades existentes en las dependencias durante la Parte M. Si se hubiera exigido desde la Parte G, los Pull Requests habrían quedado bloqueados mientras siguieran existiendo esas vulnerabilidades.

Se aplicó una estrategia progresiva denominada *ratchet* o trinquete: primero se corrigen los problemas existentes y después se establece la comprobación obligatoria para evitar que vuelvan a introducirse.

**Conclusión**

Se configuraron cuatro comprobaciones de seguridad obligatorias para `main`. Las pruebas permitieron comprobar que `pip-audit` detecta dependencias vulnerables y bloquea los cambios hasta que se corrigen. La actualización de Flask eliminó las vulnerabilidades detectadas en la comprobación local.

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

# Expediente de evidencias — ReportAudit 1.0.0

- Repositorio: https://github.com/Samubrr/reportaudit-lab
- Versión: v1.0.0
- Fecha: 2026-11-28
- Responsable: Samuel Bernabé Ortiz Ruiz

> Índice de evidencias frente a la Cyber Resilience Act (Reglamento (UE) 2024/2847).
> Este expediente es un índice de evidencias del laboratorio, no una declaración de conformidad ni una certificación CRA.

| # | Requisito | Referencia | Evidencia en ReportAudit | Enlace | Cómo lo verifica un tercero |
|---|---|---|---|---|---|
| 1 | Sin vulnerabilidades explotables conocidas al publicar | Anexo I, Parte I, 2.a | Análisis SAST y SCA en el pipeline; revisión y corrección de vulnerabilidades; VEX del simulacro | [PR #19](https://github.com/Samubrr/reportaudit-lab/pull/19) · [PR #28](https://github.com/Samubrr/reportaudit-lab/pull/28) ·| Abrir los PR y comprobar los checks y sus resultados. El VEX del simulacro es privado. |
| 2 | Configuración segura por defecto | Anexo I, Parte I, 2.b | Correcciones de seguridad: validación de YAML seguro, inyecciones y configuración | [PR #19](https://github.com/Samubrr/reportaudit-lab/pull/19) | Revisar los cambios del PR y el código integrado en main. |
| 3 | Protección frente a accesos no autorizados | Anexo I, Parte I, 2.d | Gestión de secretos, regla propia de Gitleaks y protección frente a filtraciones | [PR #25](https://github.com/Samubrr/reportaudit-lab/pull/25) · [PR #19](https://github.com/Samubrr/reportaudit-lab/pull/19) | Revisar la configuración de Gitleaks y los cambios de seguridad. Comprobar el check de secretos en el pipeline. |
| 4 | Identificar y documentar los componentes (SBOM) | Anexo I, Parte II, 1 | SBOM CycloneDX incluido en la Release v1.0.0 y atestado | [Release v1.0.0](https://github.com/Samubrr/reportaudit-lab/releases/tag/v1.0.0) | Descargar `reportaudit-sbom.cdx.json` y comprobar que existe. Verificar su atestación con GitHub CLI. |
| 5 | Corregir las vulnerabilidades sin demora | Anexo I, Parte II, 2 | Dependabot, actualización de dependencias y controles SCA mediante pip-audit | [PR #24](https://github.com/Samubrr/reportaudit-lab/pull/24) · [PR #28](https://github.com/Samubrr/reportaudit-lab/pull/28) | Revisar los PR de actualización y comprobar los resultados de pip-audit. |
| 6 | Pruebas y revisiones periódicas | Anexo I, Parte II, 3 | Pipeline de seguridad en PR y análisis periódico mediante OpenSSF Scorecard | [PR #15](https://github.com/Samubrr/reportaudit-lab/pull/15) · [PR #30](https://github.com/Samubrr/reportaudit-lab/pull/30) · [Ejecución Scorecard](https://github.com/Samubrr/reportaudit-lab/actions/runs/46043650135) | Consultar los workflows, sus ejecuciones y los resultados de los análisis. |
| 7 | Información sobre vulnerabilidades corregidas | Anexo I, Parte II, 4 | Simulacro de aviso privado de vulnerabilidad SQL Injection (CWE-89) | Evidencia privada: aviso GHSA del simulacro | Solo los colaboradores autorizados pueden consultar el borrador privado. No es un aviso público ni una vulnerabilidad publicada. |
| 8 | Política de divulgación coordinada | Anexo I, Parte II, 5 | Política de seguridad y procedimiento de comunicación de vulnerabilidades | [SECURITY.md](https://github.com/Samubrr/reportaudit-lab/blob/main/SECURITY.md) · [PR #26](https://github.com/Samubrr/reportaudit-lab/pull/26) | Abrir SECURITY.md y revisar el apartado de comunicación de vulnerabilidades. |
| 9 | Dirección de contacto para vulnerabilidades | Anexo I, Parte II, 6 | SECURITY.md incluye el procedimiento para reportar vulnerabilidades mediante el canal privado de GitHub | [SECURITY.md](https://github.com/Samubrr/reportaudit-lab/blob/main/SECURITY.md) · [PR #26](https://github.com/Samubrr/reportaudit-lab/pull/26) | Consultar el apartado Report a vulnerability y comprobar el canal privado habilitado. |
| 10 | Distribución segura de las actualizaciones | Anexo I, Parte II, 7 | Release v1.0.0 con SHA256SUMS y atestaciones Sigstore de procedencia y SBOM | [Release v1.0.0](https://github.com/Samubrr/reportaudit-lab/releases/tag/v1.0.0) · [PR #29](https://github.com/Samubrr/reportaudit-lab/pull/29) | Descargar los artefactos, verificar SHA-256 con `sha256sum -c SHA256SUMS` y consultar las atestaciones con GitHub CLI. |
| 11 | Período de soporte declarado | Art. 13.8 | SECURITY.md declara las versiones soportadas y la política de soporte | [SECURITY.md](https://github.com/Samubrr/reportaudit-lab/blob/main/SECURITY.md) · [PR #26](https://github.com/Samubrr/reportaudit-lab/pull/26) | Abrir SECURITY.md y revisar el apartado Supported versions. |
| 12 | Trazabilidad: cada cambio nace de un Issue y entra por un PR revisado | Buena práctica (no es un requisito literal) | Issues del laboratorio, Pull Requests revisados y cambios integrados en main | [Issues](https://github.com/Samubrr/reportaudit-lab/issues) · [Pull Requests](https://github.com/Samubrr/reportaudit-lab/pulls) · [PR #31](https://github.com/Samubrr/reportaudit-lab/pull/31) | Revisar la relación entre Issues y PR, las aprobaciones de revisión y los commits integrados en main. |

## Verificación técnica de la Release

La Release v1.0.0 contiene:

- `reportaudit-1.0.0.tar.gz`
- `reportaudit-sbom.cdx.json`
- `reportaudit-provenance.sigstore.json`
- `reportaudit-sbom.sigstore.json`
- `SHA256SUMS`

Comandos de referencia para verificar los artefactos:

```bash
gh release download v1.0.0
sha256sum -c SHA256SUMS
gh attestation verify reportaudit-1.0.0.tar.gz -R Samubrr/reportaudit-lab
```

## Limitaciones del expediente

Este documento no constituye una declaración de conformidad con la CRA.

No incluye la evaluación de riesgos documentada, la documentación técnica completa del Anexo VII, la declaración UE de conformidad ni el marcado CE. Estos elementos se estudian en la Práctica 2.

La evidencia del aviso de vulnerabilidad del simulacro es privada y solo está disponible para los colaboradores autorizados.

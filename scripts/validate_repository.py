from __future__ import annotations

import hashlib
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def tracked_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    return [item.decode("utf-8") for item in result.stdout.split(b"\0") if item]


def main() -> int:
    files = tracked_files()
    errors: list[str] = []

    forbidden = re.compile(r"(^|/)(node_modules|dist|__pycache__|\.deps)(/|$)|\.pyc$|(^|/)~\$")
    for path in files:
        if forbidden.search(path):
            errors.append(f"artefacto generado o temporal versionado: {path}")

    rules = {
        "01_Clase/Actividades/": re.compile(r"G6_ACT\d{2}_\d{2}-\d{2}\.(?:pdf|jpg|jpeg|png)$"),
        "01_Clase/Notas/": re.compile(r"G6_NC_[A-Z]{2,4}_(?:\d{2}-\d{2}|ACUM_(?:LUNES|MARTES|MIERCOLES|JUEVES|VIERNES))\.pdf$"),
        "03_Produccion_Propia/Ejercicios/": re.compile(r"G6_EJ_[A-Z]{2,4}_[A-Za-z0-9]+\.pdf$"),
        "03_Produccion_Propia/Resumenes/": re.compile(r"G6_RE_P[12](?:_PRACTICO)?_[A-Z]{2,4}\.pdf$"),
        "04_Trabajos_Practicos/No_Evaluables/": re.compile(r"G6_TPN\d{2}_[A-Z]{2,4}\.pdf$"),
    }
    for directory, pattern in rules.items():
        for path in files:
            if path.startswith(directory) and not path.endswith(".gitkeep"):
                name = Path(path).name
                if not pattern.fullmatch(name):
                    errors.append(f"nombre inválido en {directory}: {name}")

    hashes: dict[str, list[str]] = defaultdict(list)
    duplicate_extensions = {".pdf", ".docx", ".xlsx", ".pptx"}
    for path in files:
        file_path = ROOT / path
        if file_path.suffix.lower() not in duplicate_extensions or not file_path.is_file():
            continue
        digest = hashlib.sha256(file_path.read_bytes()).hexdigest()
        hashes[digest].append(path)
    for paths in hashes.values():
        if len(paths) > 1:
            errors.append("contenido binario duplicado: " + ", ".join(paths))

    required = [
        "00_Gestion_Configuracion/Inventario_IC/G6_INVENTARIO_IC.md",
        "00_Gestion_Configuracion/G6_CRITERIOS_LINEAS_BASE.md",
        "00_Gestion_Configuracion/Lineas_Base/Registros/G6_REGISTRO_LINEAS_BASE.md",
        "04_Trabajos_Practicos/Evaluables/TPE01/G6_TPE01.pdf",
        "04_Trabajos_Practicos/Evaluables/TPE02/G6_TPE02.pdf",
        "04_Trabajos_Practicos/Evaluables/TPE03/G6_TPE03_Documentacion_TDD.pdf",
    ]
    for path in required:
        if path not in files:
            errors.append(f"ítem obligatorio ausente: {path}")

    if errors:
        print("Validación del repositorio: FALLÓ", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Validación del repositorio: OK ({len(files)} archivos versionados)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Cross-platform local setup assistant for Odoo paths."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = REPO_ROOT / "config"
CONFIG_PATH = CONFIG_DIR / "local.paths.json"
EXAMPLE_PATH = CONFIG_DIR / "local.paths.example.json"


def _normalize(value: str) -> str:
    return str(Path(value).expanduser().resolve())


def _validate_community(path_str: str) -> tuple[bool, list[str]]:
    issues: list[str] = []
    path = Path(path_str)
    if not path.exists() or not path.is_dir():
        issues.append("La ruta no existe o no es directorio.")
        return False, issues
    if not (path / "odoo-bin").exists():
        issues.append("No se encontró 'odoo-bin' en la raíz indicada.")
    if not ((path / "odoo" / "addons").exists() or (path / "addons").exists()):
        issues.append(
            "No se encontró carpeta de addons esperada ('odoo/addons' o 'addons')."
        )
    return len(issues) == 0, issues


def _validate_enterprise(path_str: str) -> tuple[bool, list[str]]:
    issues: list[str] = []
    path = Path(path_str)
    if not path.exists() or not path.is_dir():
        issues.append("La ruta no existe o no es directorio.")
        return False, issues
    has_manifest = any(path.glob("*/__manifest__.py"))
    if not has_manifest:
        issues.append("No se detectaron addons enterprise (faltan */__manifest__.py).")
    return len(issues) == 0, issues


def _load_config() -> dict:
    if not CONFIG_PATH.exists():
        return {}
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def _save_config(data: dict) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def cmd_init(args: argparse.Namespace) -> int:
    if not EXAMPLE_PATH.exists():
        print(f"Falta plantilla: {EXAMPLE_PATH}")
        return 1

    if CONFIG_PATH.exists() and not args.reset:
        print(f"Ya existe configuración local: {CONFIG_PATH}")
        print("Use --reset para reconfigurar.")
        return 1

    community = args.community or input("Ruta Odoo Community (obligatoria): ").strip()
    if not community:
        print("Error: ODOO community es obligatoria.")
        return 1
    community = _normalize(community)
    ok_comm, issues_comm = _validate_community(community)
    if not ok_comm:
        print("Ruta community inválida:")
        for item in issues_comm:
            print(f"- {item}")
        return 1

    enterprise = args.enterprise
    if enterprise is None:
        enterprise = input(
            "Ruta Odoo Enterprise (opcional, Enter para omitir): "
        ).strip()
    enterprise = _normalize(enterprise) if enterprise else ""
    if enterprise:
        ok_ent, issues_ent = _validate_enterprise(enterprise)
        if not ok_ent:
            print("Ruta enterprise inválida:")
            for item in issues_ent:
                print(f"- {item}")
            return 1

    data = {
        "odoo_community_root": community,
        "odoo_enterprise_root": enterprise,
    }
    _save_config(data)
    print(f"Configuración guardada en: {CONFIG_PATH}")
    return 0


def cmd_check(_: argparse.Namespace) -> int:
    data = _load_config()
    comm = data.get("odoo_community_root", "")
    ent = data.get("odoo_enterprise_root", "")
    if not comm:
        hint = "python scripts/setup_assistant.py init"
        print(f"Falta 'odoo_community_root'. Ejecute: {hint}")
        return 1
    ok_comm, issues_comm = _validate_community(comm)
    if not ok_comm:
        print("Community inválida:")
        for item in issues_comm:
            print(f"- {item}")
        return 1
    print("Community: OK")

    if ent:
        ok_ent, issues_ent = _validate_enterprise(ent)
        if ok_ent:
            print("Enterprise: OK")
        else:
            print("Enterprise: WARNING")
            for item in issues_ent:
                print(f"- {item}")
    else:
        print("Enterprise: no configurada (opcional)")
    return 0


def cmd_show(_: argparse.Namespace) -> int:
    data = _load_config()
    if not data:
        hint = "python scripts/setup_assistant.py init"
        print(f"No hay configuración local. Ejecute: {hint}")
        return 1
    print(json.dumps(data, indent=2, ensure_ascii=False))
    return 0


def cmd_doctor(_: argparse.Namespace) -> int:
    rc = cmd_check(argparse.Namespace())
    if rc == 0:
        print("Diagnóstico: configuración utilizable.")
        return 0
    print("Diagnóstico: configuración incompleta o inválida.")
    print("Acción sugerida: python scripts/setup_assistant.py init --reset")
    return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Asistente de configuración local para Odoo paths."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    parser_init = subparsers.add_parser("init", help="Inicializa configuración local.")
    parser_init.add_argument("--community", help="Ruta absoluta de Odoo Community.")
    parser_init.add_argument(
        "--enterprise", help="Ruta absoluta de Odoo Enterprise (opcional)."
    )
    parser_init.add_argument(
        "--reset", action="store_true", help="Sobrescribir configuración existente."
    )
    parser_init.set_defaults(func=cmd_init)

    parser_check = subparsers.add_parser("check", help="Valida configuración actual.")
    parser_check.set_defaults(func=cmd_check)

    parser_show = subparsers.add_parser("show", help="Muestra configuración actual.")
    parser_show.set_defaults(func=cmd_show)

    parser_doctor = subparsers.add_parser(
        "doctor", help="Diagnóstico y siguiente acción."
    )
    parser_doctor.set_defaults(func=cmd_doctor)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
# pylint: disable=print-used

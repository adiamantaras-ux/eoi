from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from .import_athletes import import_athletes_from_xlsx
from .import_horses import import_horses_from_xlsx


def default_excel_dir() -> Path:
    """
    Θέλουμε: EOI-System/01_docs/03_excel_sources/
    Το project σου είναι: EOI-System/02_src/backend
    Άρα:
      BASE_DIR = .../EOI-System/02_src/backend
      EOI_ROOT = BASE_DIR.parent.parent = .../EOI-System
    """
    base_dir = Path(getattr(settings, "BASE_DIR", Path.cwd())).resolve()
    eoi_root = base_dir.parent.parent
    return eoi_root / "01_docs" / "03_excel_sources"


class Command(BaseCommand):
    help = "Imports athletes.xlsx and horses.xlsx into the database."

    def add_arguments(self, parser):
        parser.add_argument(
            "--excel-dir",
            default="",
            help="Folder that contains athletes.xlsx and horses.xlsx (optional).",
        )
        parser.add_argument(
            "--athletes",
            default="",
            help="Full path to athletes.xlsx (optional).",
        )
        parser.add_argument(
            "--horses",
            default="",
            help="Full path to horses.xlsx (optional).",
        )

    def handle(self, *args, **options):
        excel_dir = options["excel_dir"].strip()
        athletes_path = options["athletes"].strip()
        horses_path = options["horses"].strip()

        if excel_dir:
            base = Path(excel_dir).expanduser().resolve()
        else:
            base = default_excel_dir()

        if not athletes_path:
            athletes_file = base / "athletes.xlsx"
        else:
            athletes_file = Path(athletes_path).expanduser().resolve()

        if not horses_path:
            horses_file = base / "horses.xlsx"
        else:
            horses_file = Path(horses_path).expanduser().resolve()

        if not athletes_file.exists():
            raise CommandError(f"File not found: {athletes_file}")
        if not horses_file.exists():
            raise CommandError(f"File not found: {horses_file}")

        self.stdout.write(self.style.NOTICE(f"Importing: {athletes_file.name} + {horses_file.name}"))
        a = import_athletes_from_xlsx(athletes_file, stdout=self.stdout)
        h = import_horses_from_xlsx(horses_file, stdout=self.stdout)

        self.stdout.write(self.style.SUCCESS(f"OK. Athletes upserted: {a}, Horses upserted: {h}"))

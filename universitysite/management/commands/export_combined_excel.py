"""
Management command: export_combined_excel
=========================================
Tumia: python manage.py export_combined_excel
       python manage.py export_combined_excel --output /path/to/output.xlsx

Inaunganisha data yote kutoka vitabu vitatu na kuhifadhi Excel.
"""

import os
import sys
from pathlib import Path
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Unganisha data ya TCU, NACTE_1, NACTE_2 kwenye Excel moja (combined_data.xlsx)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--output",
            type=str,
            default=None,
            help="Njia ya kuhifadhi faili (default: combined_data.xlsx kwenye BASE_DIR)",
        )
        parser.add_argument(
            "--source",
            choices=["excel", "db"],
            default="excel",
            help="Chanzo cha data: 'excel' (kutoka .xlsx files) au 'db' (kutoka database)",
        )

    def handle(self, *args, **options):
        source = options["source"]
        output = options["output"]
        
        self.stdout.write(self.style.SUCCESS("=" * 55))
        self.stdout.write(self.style.SUCCESS("  KUUNGANISHA DATA KUTOKA VITABU VITATU"))
        self.stdout.write(self.style.SUCCESS("=" * 55))
        
        try:
            import pandas as pd
        except ImportError:
            self.stderr.write(self.style.ERROR("Pandas haijasanidiwa! Endesha: pip install pandas openpyxl"))
            return
        
        BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent

        if source == "excel":
            self._export_from_excel(pd, BASE_DIR, output)
        else:
            self._export_from_db(pd, BASE_DIR, output)

    def _export_from_excel(self, pd, BASE_DIR, output):
        """Chanzo: .xlsx files (TCU, NACTE1, NACTE2)"""
        # Ongeza script directory kwenye path
        sys.path.insert(0, str(BASE_DIR))
        
        try:
            from export_combined_excel import load_tcu, load_nacte, style_worksheet, HEADER_COLORS
            
            tcu_path   = BASE_DIR / "tcu" / "tcu_data.xlsx"
            nacte1_path = BASE_DIR / "nacte" / "nacte_data.xlsx"
            nacte2_path = BASE_DIR / "nacte" / "nacte_data2.xlsx"
            output_path = Path(output) if output else BASE_DIR / "combined_data.xlsx"
            
            self.stdout.write("\n[1/4] Kupakia TCU...")
            df_tcu = load_tcu(tcu_path)
            self.stdout.write(f"       Rekodi: {len(df_tcu):,}")
            
            self.stdout.write("[2/4] Kupakia NACTE_1...")
            df_nacte1 = load_nacte(nacte1_path, 1)
            self.stdout.write(f"       Rekodi: {len(df_nacte1):,}")
            
            self.stdout.write("[3/4] Kupakia NACTE_2...")
            df_nacte2 = load_nacte(nacte2_path, 2)
            self.stdout.write(f"       Rekodi: {len(df_nacte2):,}")
            
            self.stdout.write("[4/4] Kuandika Excel...")
            df_all = pd.concat([df_tcu, df_nacte1, df_nacte2], ignore_index=True, sort=False)
            df_all = df_all.fillna("")
            
            priority_cols = ["Source", "Category", "University", "Programme", "Requirements", "Duration"]
            other_cols = [c for c in df_all.columns if c not in priority_cols]
            df_all = df_all[priority_cols + other_cols]
            
            with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
                if len(df_tcu) > 0:
                    df_tcu.to_excel(writer, sheet_name="TCU", index=False)
                    style_worksheet(writer.sheets["TCU"], HEADER_COLORS["TCU"], df_tcu)
                if len(df_nacte1) > 0:
                    df_nacte1.to_excel(writer, sheet_name="NACTE_1", index=False)
                    style_worksheet(writer.sheets["NACTE_1"], HEADER_COLORS["NACTE_1"], df_nacte1)
                if len(df_nacte2) > 0:
                    df_nacte2.to_excel(writer, sheet_name="NACTE_2", index=False)
                    style_worksheet(writer.sheets["NACTE_2"], HEADER_COLORS["NACTE_2"], df_nacte2)
                df_all.to_excel(writer, sheet_name="ALL_DATA", index=False)
                style_worksheet(writer.sheets["ALL_DATA"], HEADER_COLORS["ALL_DATA"], df_all)
            
            self._print_summary(df_tcu, df_nacte1, df_nacte2, output_path)
            
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Kosa: {e}"))
            raise

    def _export_from_db(self, pd, BASE_DIR, output):
        """Chanzo: Database ya Django (UniversityCourse model)"""
        from universitysite.models import UniversityCourse, University, Course
        
        output_path = Path(output) if output else BASE_DIR / "combined_data_from_db.xlsx"
        
        self.stdout.write("\n[1/3] Kupakia data kutoka database...")
        
        qs = UniversityCourse.objects.select_related(
            "university", "course", "requirements", "university__region"
        ).all()
        
        rows = []
        for uc in qs:
            rows.append({
                "University": uc.university.name,
                "Region": uc.university.region.name if uc.university.region_id else "",
                "Ownership": uc.university.umiliki or "",
                "Programme": uc.course.name,
                "Level": uc.level,
                "Duration": uc.duration,
                "Requirements": uc.requirements.description if uc.requirements else "",
                "Fee": float(uc.fee) if uc.fee else "",
                "Application_Link": uc.application_link or "",
                "Is_Active": uc.is_active,
            })
        
        df_db = pd.DataFrame(rows)
        
        self.stdout.write(f"       Rekodi: {len(df_db):,}")
        self.stdout.write("[2/3] Kuandika Excel...")
        
        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            df_db.to_excel(writer, sheet_name="Database_Export", index=False)
            
            # Style header
            try:
                from openpyxl.styles import PatternFill, Font, Alignment
                from openpyxl.utils import get_column_letter
                ws = writer.sheets["Database_Export"]
                fill = PatternFill(start_color="2E4057", end_color="2E4057", fill_type="solid")
                for cell in ws[1]:
                    cell.fill = fill
                    cell.font = Font(bold=True, color="FFFFFF")
                    cell.alignment = Alignment(horizontal="center")
                ws.freeze_panes = "A2"
                ws.auto_filter.ref = ws.dimensions
                # Auto-fit columns
                for col_idx in range(1, len(df_db.columns) + 1):
                    ws.column_dimensions[get_column_letter(col_idx)].width = 25
            except ImportError:
                pass
        
        self.stdout.write(self.style.SUCCESS(f"\n  Faili: {output_path}"))
        self.stdout.write(self.style.SUCCESS(f"  Rekodi: {len(df_db):,}"))

    def _print_summary(self, df_tcu, df_nacte1, df_nacte2, output_path):
        total = len(df_tcu) + len(df_nacte1) + len(df_nacte2)
        self.stdout.write(self.style.SUCCESS("\n" + "=" * 55))
        self.stdout.write(self.style.SUCCESS("  IMEKAMILIKA!"))
        self.stdout.write(self.style.SUCCESS(f"  Faili:    {output_path}"))
        self.stdout.write(self.style.SUCCESS(f"  TCU:      {len(df_tcu):>6,} rekodi"))
        self.stdout.write(self.style.SUCCESS(f"  NACTE_1:  {len(df_nacte1):>6,} rekodi"))
        self.stdout.write(self.style.SUCCESS(f"  NACTE_2:  {len(df_nacte2):>6,} rekodi"))
        self.stdout.write(self.style.SUCCESS(f"  JUMLA:    {total:>6,} rekodi"))
        self.stdout.write(self.style.SUCCESS("=" * 55))

import csv
import json
import logging
import tempfile
from src.config import config

class DataManager:
    def _read_employees_from_csv(self):
        """Read employees from CSV file."""
        employees = []
        try:
            with open(config.employees_csv, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    employees.append(row)
            logging.info(f"Successfully read {len(employees)} employees from CSV")
            return employees
        except FileNotFoundError as e:
            logging.error(f"CSV file not found: {config.employees_csv}")
            raise
        except Exception as e:
            logging.error(f"Error reading CSV file: {e}")
            raise

    def _write_employees_to_json(self, employees):
        """Write employees to JSON file (persistent storage)."""
        try:
            with open(config.employees_json, "w", encoding="utf-8") as f:
                json.dump(employees, f, indent=4)
            logging.info(f"Successfully wrote {len(employees)} employees to JSON: {config.employees_json}")
            return config.employees_json
        except Exception as e:
            logging.error(f"Error writing to JSON file: {e}")
            raise

    def _create_temp_employees_file(self, employees):
        """Create a temporary JSON file with employee data."""
        try:
            with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".json", encoding="utf-8") as tmp:
                json.dump(employees, tmp, indent=4)
                temp_path = tmp.name
            logging.info(f"Created temporary file: {temp_path}")
            return temp_path
        except Exception as e:
            logging.error(f"Error creating temporary file: {e}")
            raise

    def ingest_bulk_employees(self):
        """Orchestrate the ingestion process: read CSV, write to JSON, create temp file."""
        try:
            # Step 1: Read employees from CSV
            employees = self._read_employees_from_csv()

            # Step 2: Write to JSON (persistent storage)
            json_path = self._write_employees_to_json(employees)

            # Step 3: Create temporary file with the same data
            temp_path = self._create_temp_employees_file(employees)

            logging.info(f"Ingestion completed: {len(employees)} employees processed")
            return {
                "message": f"{len(employees)} employees ingested",
                "json_file": str(json_path),
                "temp_file": temp_path
            }

        except Exception as e:
            logging.error(f"Error during bulk employee ingestion: {e}")
            raise

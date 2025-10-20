"""
automatizacion_ventas.py

Script para la prueba técnica - Automatización de Ventas RPA
Genera la estructura Output/YYYY/MM_NombreMes/, mueve los archivos originales allí,
consolida ventas por mes y genera un Excel por mes con dos hojas:
 - Datos_Consolidados
 - Ranking_Productos

Dependencias: pandas, openpyxl
Instalación: pip install pandas openpyxl

Uso: python automatizacion_ventas.py --input "./Input" --output "./Output"

"""

from pathlib import Path
import re
import shutil
import argparse
import pandas as pd
import logging
from datetime import datetime

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Mapeo de meses (soporta nombres en inglés y en español)
MONTH_MAP = {
    # English
    'january': (1, '01_Enero'), 'february': (2, '02_Febrero'), 'march': (3, '03_Marzo'),
    'april': (4, '04_Abril'), 'may': (5, '05_Mayo'), 'june': (6, '06_Junio'),
    'july': (7, '07_Julio'), 'august': (8, '08_Agosto'), 'september': (9, '09_Septiembre'),
    'october': (10, '10_Octubre'), 'november': (11, '11_Noviembre'), 'december': (12, '12_Diciembre'),
    # Español
    'enero': (1, '01_Enero'), 'febrero': (2, '02_Febrero'), 'marzo': (3, '03_Marzo'),
    'abril': (4, '04_Abril'), 'mayo': (5, '05_Mayo'), 'junio': (6, '06_Junio'),
    'julio': (7, '07_Julio'), 'agosto': (8, '08_Agosto'), 'septiembre': (9, '09_Septiembre'),
    'octubre': (10, '10_Octubre'), 'noviembre': (11, '11_Noviembre'), 'diciembre': (12, '12_Diciembre')
}

FILENAME_REGEX = re.compile(r"sales[_\-]?(?P<region>[a-zA-Z]+)[_\-]?(?P<month>[a-zA-Z]+)[_\-]?(?P<year>\d{4})", re.IGNORECASE)

REQUIRED_COLUMNS = {'Date', 'Region', 'Salesperson', 'Product', 'Quantity', 'UnitPrice'}


def parse_filename(fname: str):
    """Extrae region, month, year desde el nombre del archivo.
    Retorna (region, month_number, month_foldername, year) o None si no coincide.
    """
    m = FILENAME_REGEX.search(fname)
    if not m:
        return None
    region = m.group('region').lower()
    month_raw = m.group('month').lower()
    year = int(m.group('year'))
    if month_raw not in MONTH_MAP:
        logging.warning(f"Mes '{month_raw}' en el fichero '{fname}' no reconocido.")
        return None
    month_num, month_folder = MONTH_MAP[month_raw]
    return region, month_num, month_folder, year


def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)
    return path


def read_and_validate_excel(path: Path):
    """Lee un excel y valida columnas. Devuelve DataFrame o lanza ValueError."""
    try:
        df = pd.read_excel(path)
    except Exception as e:
        raise ValueError(f"Error leyendo {path}: {e}")
    cols = set(df.columns.str.replace('\ufeff', '').str.strip())
    if not REQUIRED_COLUMNS.issubset(cols):
        raise ValueError(f"Archivo {path.name} falta columnas requeridas. Encontradas: {sorted(cols)}")

    # Normalizar nombres de columnas (permitir variaciones de mayúsculas/espacios)
    df = df.rename(columns={c: c.strip() for c in df.columns})

    # Converciones
    # Date -> datetime
    if not pd.api.types.is_datetime64_any_dtype(df['Date']):
        try:
            df['Date'] = pd.to_datetime(df['Date'])
        except Exception:
            logging.warning(f"No se pudieron convertir todas las fechas en {path.name}; algunas filas pueden eliminarse.")
    # Quantity -> numeric
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
    df['UnitPrice'] = pd.to_numeric(df['UnitPrice'], errors='coerce')

    # Eliminar filas sin datos críticos
    before = len(df)
    df = df.dropna(subset=['Date', 'Product', 'Quantity', 'UnitPrice'])
    after = len(df)
    if after < before:
        logging.info(f"Se eliminaron {before-after} filas con datos críticos faltantes en {path.name}")

    return df


def consolidate_month(files: list, output_month_dir: Path, year: int, month_num: int):
    """Consolida una lista de archivos (Path) correspondientes al mismo mes/año.
    Guarda Ventas_Consolidadas_YYYY_MM.xlsx en output_month_dir.
    """
    dfs = []
    details = []
    for f in files:
        parsed = parse_filename(f.name)
        if parsed is None:
            logging.warning(f"Nombre de archivo no parseable: {f.name}. Se omite.")
            continue
        region, _, _, _ = parsed
        try:
            df = read_and_validate_excel(f)
        except ValueError as e:
            logging.error(e)
            continue
        # Añadir columnas necesarias
        df['Region_Archivo'] = df['Region'].fillna(region).str.strip().str.capitalize()

        df['Archivo_Origen'] = f.name   
        # Calcular Total         
        df['Total'] = df['Quantity'] * df['UnitPrice']

        dfs.append(df)
        details.append((f.name, len(df)))

    if not dfs:
        logging.info(f"No hay datos válidos para {year}-{month_num:02d}")
        return None

    full = pd.concat(dfs, ignore_index=True)

    # Reordenar columnas para que Total esté al final
    cols = [c for c in full.columns if c != 'Total'] + ['Total']
    full = full[cols]

    # Crear ranking de productos (por cantidad total vendida y por ventas totales)
    ranking = (
    full.groupby('Product', dropna=False)
        .agg(
            Cantidad_Total=('Quantity', 'sum'),
            Valor_Total=('Total', 'sum'),
            Precio_Promedio=('UnitPrice', 'mean'),
            Num_Transacciones=('Quantity', 'count'),
            Regiones=('Region_Archivo', lambda x: ', '.join(sorted(x.unique())))
        )
        .reset_index()
        .sort_values(['Cantidad_Total', 'Valor_Total'], ascending=False)
    )
    # Añadir columna de ranking
    ranking.insert(0, 'Ranking', range(1, len(ranking)+1))


    # Guardar excel con dos hojas
    output_file = output_month_dir / f"Ventas_Consolidadas_{year}_{month_num:02d}.xlsx"
    try:
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            full.to_excel(writer, sheet_name='Datos_Consolidados', index=False)
            ranking.to_excel(writer, sheet_name='Ranking_Productos', index=False)
        logging.info(f"Guardado reporte: {output_file}")
    except Exception as e:
        logging.error(f"Error guardando {output_file}: {e}")
        return None

    return output_file


def organize_and_process(input_dir: Path, output_dir: Path):
    """Punto de entrada: organiza archivos por fecha y procesa cada mes."""
    input_dir = input_dir.resolve()
    output_dir = output_dir.resolve()

    if not input_dir.exists():
        raise FileNotFoundError(f"Input directory {input_dir} no existe")

    # Listar archivos excel en input_dir (no recursivo)
    excel_files = [p for p in input_dir.iterdir() if p.is_file() and p.suffix.lower() in ('.xlsx', '.xls')]
    logging.info(f"Encontrados {len(excel_files)} archivos en {input_dir}")

    # Agrupar por (year, month_num, month_folder)
    groups = {}
    for f in excel_files:
        parsed = parse_filename(f.name)
        if parsed is None:
            logging.warning(f"No se pudo parsear: {f.name}; se omite")
            continue
        region, month_num, month_folder, year = parsed
        key = (year, month_num, month_folder)
        groups.setdefault(key, []).append((f, region))

    if not groups:
        logging.info("No hay archivos válidos para procesar.")
        return

    # Procesar cada grupo
    for (year, month_num, month_folder), files_info in groups.items():
        month_output_dir = output_dir / str(year) / month_folder
        ensure_dir(month_output_dir)

        # Mover archivos originales a la carpeta correspondiente (si ya existe, renombrar para evitar error)
        moved_files = []
        for f, region in files_info:
            dest = month_output_dir / f.name
            if dest.exists():
                # crear sufijo para evitar sobreescritura
                stamp = datetime.now().strftime('%Y%m%d%H%M%S')
                dest = month_output_dir / f"{f.stem}_{stamp}{f.suffix}"
            try:
                shutil.copy2(str(f), dest)
                moved_files.append(dest)
                logging.info(f"Movido {f.name} -> {dest}")
            except Exception as e:
                logging.error(f"Error moviendo {f.name} a {dest}: {e}")

        # Consolidar los archivos movidos de ese mes
        consolidated = consolidate_month(moved_files, month_output_dir, year, month_num)
        if consolidated is None:
            logging.info(f"No se generó reporte para {year}-{month_num:02d}")
        else:
            logging.info(f"Reporte generado en {consolidated}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Automatización de ventas - consolida archivos por mes y genera reportes')
    parser.add_argument('--input', '-i', type=str, default='./Input', help='Directorio de entrada con archivos Excel')
    parser.add_argument('--output', '-o', type=str, default='./Output', help='Directorio donde se crearán las carpetas y reportes')
    args = parser.parse_args()

    try:
        organize_and_process(Path(args.input), Path(args.output))
        logging.info('Proceso finalizado')
    except Exception as e:
        logging.exception(f'Error en la ejecución: {e}')

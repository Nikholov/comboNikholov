import os
import sys
from colorama import Fore, Style, init

# Inicializar colorama para compatibilidad multiplataforma
init(autoreset=True)

APP_TITLE = "COMBOMULTInikholov"

# Configurar el título de la consola
if sys.platform.startswith("win"):
    import ctypes
    ctypes.windll.kernel32.SetConsoleTitleW(APP_TITLE)
else:
    sys.stdout.write(f"\x1b]2{APP_TITLE}\x07")

# Rutas predeterminadas
DEFAULT_INPUT_SPLIT_REMOVE = "/sdcard/combo/"
DEFAULT_INPUT_JOIN = "/sdcard/Combo/"
DEFAULT_OUTPUT = "/sdcard/Multi-Combo/"

# Asegurar que la carpeta de salida exista
os.makedirs(DEFAULT_OUTPUT, exist_ok=True)


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def banner():
    clear_screen()
    print(
        f"""{Fore.YELLOW}*************************************************
*                                               *
*     🇪🇨   {Fore.RED}N{Fore.YELLOW} {Fore.GREEN}i{Fore.YELLOW} {Fore.CYAN}K{Fore.YELLOW} {Fore.MAGENTA}h{Fore.YELLOW} {Fore.BLUE}O{Fore.YELLOW} {Fore.LIGHTGREEN_EX}l{Fore.YELLOW} {Fore.LIGHTCYAN_EX}O{Fore.YELLOW} {Fore.LIGHTRED_EX}v{Fore.YELLOW}   🇪🇨   *
*                                               *
*************************************************
    {Style.RESET_ALL}{Fore.YELLOW}    COMBOMULTI | NIKHOLOV   {Style.RESET_ALL}
    {Fore.CYAN}by:Nikholov 🇪🇨{Style.RESET_ALL}\n"""
    )


def count_lines(filepath):
    """Cuenta de forma eficiente las líneas de un archivo."""
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        return sum(1 for _ in f)


def load_unique_lines(filepath):
    """Carga líneas únicas eliminando espacios y saltos de línea."""
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        return {line.replace(" ", "").strip() for line in f if line.strip()}


def get_combo_files(path):
    """Obtiene la lista de archivos disponibles en la ruta."""
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    return sorted(
        [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    )


def select_single_combo(input_path):
    """Muestra un menú interactivo para seleccionar un solo combo."""
    files = get_combo_files(input_path)
    if not files:
        print(
            f"{Fore.RED}No se encontró ningún combo en la carpeta: {input_path}{Style.RESET_ALL}"
        )
        return None

    print(f"{Fore.CYAN} ESCOGE UN COMBO DE LA LISTA DE ABAJO:{Style.RESET_ALL}\n")
    for idx, file in enumerate(files, 1):
        print(f"{Fore.GREEN}{idx}={Style.RESET_ALL} {file}")

    print(
        f"\n{Fore.YELLOW}Se encontraron {len(files)} combos! Elige uno.{Style.RESET_ALL}"
    )

    try:
        choice = int(input(f" {Fore.GREEN}Combo N°: {Style.RESET_ALL}"))
        if 1 <= choice <= len(files):
            return files[choice - 1]
    except ValueError:
        pass

    print(f"{Fore.RED}Opción inválida.{Style.RESET_ALL}")
    return None


def split_combo_action():
    """Opción 1: Dividir un combo en partes iguales sin duplicados."""
    filename = select_single_combo(DEFAULT_INPUT_SPLIT_REMOVE)
    if not filename:
        return

    filepath = os.path.join(DEFAULT_INPUT_SPLIT_REMOVE, filename)
    total_lines = count_lines(filepath)

    banner()
    print(f"{Fore.CYAN}{filepath}{Style.RESET_ALL}")
    print(
        f"\n{Fore.YELLOW}Este combo contiene {total_lines} líneas.{Style.RESET_ALL}\n"
    )

    unique_lines = list(load_unique_lines(filepath))

    try:
        num_parts = int(
            input(
                f" {Fore.CYAN}Digite el número de partes para dividir el combo: {Style.RESET_ALL}"
            )
        )
        if num_parts <= 0:
            raise ValueError
    except ValueError:
        print(f"{Fore.RED}Número de partes inválido.{Style.RESET_ALL}")
        return

    chunk_size = len(unique_lines) // num_parts
    for i in range(num_parts):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i < num_parts - 1 else len(unique_lines)
        part_lines = unique_lines[start:end]

        out_name = f"{filename}_part{i + 1}.txt"
        out_path = os.path.join(DEFAULT_OUTPUT, out_name)

        with open(out_path, "w", encoding="utf-8") as f:
            f.write("\n".join(part_lines) + "\n")

        print(
            f"\n{Fore.GREEN}Parte {i + 1} guardada en '{out_path}'.{Style.RESET_ALL}"
        )


def join_combos_action():
    """Opción 2: Unir múltiples combos seleccionados eliminando duplicados."""
    files = get_combo_files(DEFAULT_INPUT_JOIN)
    if not files:
        print(
            f"{Fore.RED}No se encontró ningún combo en la carpeta: {DEFAULT_INPUT_JOIN}{Style.RESET_ALL}"
        )
        return

    print(
        f"{Fore.CYAN} ESCOGE COMBOS DE LA LISTA DE ABAJO PARA UNIR:{Style.RESET_ALL}\n"
    )
    for idx, file in enumerate(files, 1):
        print(f"{Fore.GREEN}{idx}={Style.RESET_ALL} {file}")

    print(
        f"\n{Fore.YELLOW}Se encontraron {len(files)} combos!\nElige uno o más (separados por espacio).{Style.RESET_ALL}"
    )

    choices = input(
        f" {Fore.GREEN}Combos N° (separados por espacio): {Style.RESET_ALL}"
    ).split()
    selected_files = []

    try:
        for c in choices:
            idx = int(c)
            if 1 <= idx <= len(files):
                selected_files.append(files[idx - 1])
    except ValueError:
        print(f"{Fore.RED}Entrada inválida.{Style.RESET_ALL}")
        return

    if not selected_files:
        print(f"{Fore.RED}No se seleccionó ningún archivo válido.{Style.RESET_ALL}")
        return

    banner()
    combined_lines = set()
    for sf in selected_files:
        fpath = os.path.join(DEFAULT_INPUT_JOIN, sf)
        print(fpath)
        combined_lines.update(load_unique_lines(fpath))

    out_filename = input(
        f" {Fore.CYAN}Digite el nombre del archivo \n para salvar (sin la extensión .txt): {Style.RESET_ALL}"
    ).strip()
    if not out_filename:
        out_filename = "combo_unido"
    if not out_filename.endswith(".txt"):
        out_filename += ".txt"

    out_path = os.path.join(DEFAULT_OUTPUT, out_filename)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(combined_lines) + "\n")

    print(
        f"\n{Fore.GREEN}¡Listo! Los combos han sido unidos.\nResultado guardado en \n'{out_path}'.{Style.RESET_ALL}"
    )


def remove_duplicates_action():
    """Opción 3: Limpiar duplicados de un combo seleccionado."""
    filename = select_single_combo(DEFAULT_INPUT_SPLIT_REMOVE)
    if not filename:
        return

    filepath = os.path.join(DEFAULT_INPUT_SPLIT_REMOVE, filename)
    total_lines = count_lines(filepath)

    banner()
    print(f"{Fore.CYAN}{filepath}{Style.RESET_ALL}")
    print(
        f"\n{Fore.YELLOW}Este combo contiene {total_lines} líneas.{Style.RESET_ALL}\n"
    )

    unique_lines = load_unique_lines(filepath)

    out_filename = input(
        f" {Fore.CYAN}Digite el nombre del archivo \n para salvar (con extensión .txt): {Style.RESET_ALL}"
    ).strip()
    if not out_filename:
        out_filename = "combo_limpio.txt"
    if not out_filename.endswith(".txt"):
        out_filename += ".txt"

    out_path = os.path.join(DEFAULT_OUTPUT, out_filename)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(unique_lines) + "\n")

    removed_count = total_lines - len(unique_lines)
    print(
        f"\n{Fore.GREEN}¡Listo! Se eliminaron {Fore.YELLOW}{removed_count}{Style.RESET_ALL}{Fore.GREEN} duplicados.\nQuedan {Fore.YELLOW}{len(unique_lines)}{Style.RESET_ALL}{Fore.GREEN} líneas.\n\nLos resultados fueron guardados en \n'{out_path}'.{Style.RESET_ALL}"
    )


def main():
    while True:
        banner()
        print(f"\n\33[0;30;103m〓〓〓〓〓 𝗠𝗘𝗡𝗨 - NIKHOLOVS 〓〓〓〓〓\033[0m")
        print(f"{Fore.CYAN}Seleccione una opción:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}1.{Style.RESET_ALL} Dividir combos")
        print(f"{Fore.GREEN}2.{Style.RESET_ALL} Unir combos")
        print(f"{Fore.GREEN}3.{Style.RESET_ALL} Remover duplicados")
        print(f"{Fore.GREEN}4.{Style.RESET_ALL} Salir")

        choice = input(f"\n{Fore.YELLOW}Opción: {Style.RESET_ALL}").strip()

        if choice == "1":
            split_combo_action()
        elif choice == "2":
            join_combos_action()
        elif choice == "3":
            remove_duplicates_action()
        elif choice == "4":
            print(f"{Fore.CYAN}¡Hasta luego! - Nikholov 🇪🇨{Style.RESET_ALL}")
            sys.exit(0)
        else:
            print(
                f"\n{Fore.RED}Opción inválida. Intente nuevamente.{Style.RESET_ALL}"
            )

        input(f"\n{Fore.YELLOW}Presione Enter para continuar...{Style.RESET_ALL}")


if __name__ == "__main__":
    main()

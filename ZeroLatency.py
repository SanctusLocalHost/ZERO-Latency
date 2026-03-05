#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import platform
import shutil
import re
import tty
import termios

# ==========================================
# CONFIGURAÇÕES DE UI, CORES E HYPERLINKS
# ==========================================
C_GREEN = '\033[92m'
C_RED = '\033[91m'
C_CYAN = '\033[96m'
C_YELLOW = '\033[93m'
C_RESET = '\033[0m'
C_BOLD = '\033[1m'
C_GRAY = '\033[90m'

# Hyperlink no Padrão OSC 8 (Visual Limpo e Clicável)
LINK_URL = "https://t.me/Sanctus_Localhost"
LINK_TEXT = "@Sanctus_LocalHost"
CLICKABLE_LINK = f"\033]8;;{LINK_URL}\033\\{LINK_TEXT}\033]8;;\033\\"

FILE_PATH = "/usr/share/X11/xkb/symbols/capslock"
BACKUP_PATH = "/usr/share/X11/xkb/symbols/capslock.bak"

# Arte ANSI e Divisórias Organizadas (101 caracteres)
ASCII_ART = f"""
{C_GREEN}====================================================================================================={C_RESET}
{C_GREEN}{C_BOLD}███████╗███████╗██████╗  ██████╗       ██╗      █████╗ ████████╗███████╗███╗   ██╗██████╗ ██╗   ██╗
╚══███╔╝██╔════╝██╔══██╗██╔═══██╗ ██╗  ██║     ██╔══██╗╚══██╔══╝██╔════╝████╗  ██║██╔════╝╚██╗ ██╔╝
  ███╔╝ █████╗  ██████╔╝██║   ██║ ╚═╝  ██║     ███████║   ██║   █████╗  ██╔██╗ ██║██║      ╚████╔╝ 
 ███╔╝  ██╔══╝  ██╔══██╗██║   ██║ ██╗  ██║     ██╔══██║   ██║   ██╔══╝  ██║╚██╗██║██║       ╚██╔╝  
███████╗███████╗██║  ██║╚██████╔╝ ╚═╝  ███████╗██║  ██║   ██║   ███████╗██║ ╚████║╚██████╗   ██║   
╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝       ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝ ╚═════╝   ╚═╝{C_RESET}
                                     {C_GREEN}{C_BOLD}[ WAYLAND / X11 DELAY FIX ]{C_RESET}
{C_GREEN}====================================================================================================={C_RESET}"""

# ==========================================
# TEXTOS CONTEÚDO E REGEX
# ==========================================
REGEX_FIND_BLOCK = re.compile(
    r'hidden partial modifier_keys\s+xkb_symbols "ctrl_modifier" \{\s+replace key <CAPS> \{\s+type\[Group1\] = "ONE_LEVEL",\s+symbols\[Group1\] = \[ Caps_Lock \],\s+actions\[Group1\] = \[ SetMods\(modifiers=Control\) \]\s+\};\s+modifier_map Control \{ <CAPS> \};\s+\};',
    re.DOTALL
)

REPLACEMENT_BLOCK = """// This changes the <CAPS> key to become a Control modifier,
// but it will still produce the Caps_Lock keysym.
hidden partial modifier_keys
xkb_symbols "ctrl_modifier" {
\tkey <CAPS> {
\t\ttype="ALPHABETIC",
\t\trepeat=No,
\t\tsymbols[Group1]=[ Caps_Lock, Caps_Lock ],
\t\tactions[Group1]=[ LockMods(modifiers=Lock),
\t\tLockMods(modifiers=Shift+Lock,affect=unlock) ]
\t};
};"""

REGEX_CHECK_ALREADY_FIXED = re.compile(r'type="ALPHABETIC".*?repeat=No.*?LockMods\(modifiers=Shift\+Lock,affect=unlock\)', re.DOTALL)

# ==========================================
# DICIONÁRIO DE IDIOMAS (i18n)
# ==========================================
LANG_DICT = {
    'pt': {
        'menu_1': "1 - Fazer Backup Original",
        'menu_2': "2 - Corrigir Bug do CapsLock (FIX)",
        'menu_3': "3 - Sair",
        'menu_0': "0 - Mudar Idioma",
        'opt_prompt': "Escolha uma opção: ",
        'invalid': "Opção inválida! Tente novamente.",
        'prog_backup': "Criando backup seguro...",
        'prog_fix': "Injetando correção no sistema...",
        'bkp_ok': "Backup concluído com sucesso em:",
        'bkp_err': "Erro ao criar backup:",
        'file_miss': "ARQUIVO NÃO ENCONTRADO:",
        'fix_ok': "SUCESSO! Bug corrigido.\n[!] Lembre-se: Vá até 'Gnome Tweaks' e ative 'make Caps Lock an additional Ctrl'.",
        'fix_already': "AVISO: O arquivo já parece conter a correção do Bug!",
        'fix_no_match': "ERRO: As linhas originais não foram encontradas no arquivo.",
        'press_any': "[ Pressione QUALQUER TECLA para continuar... ]"
    },
    'en': {
        'menu_1': "1 - Backup original file",
        'menu_2': "2 - Fix CapsLock Bug",
        'menu_3': "3 - Exit",
        'menu_0': "0 - Change Language",
        'opt_prompt': "Select an option: ",
        'invalid': "Invalid option! Try again.",
        'prog_backup': "Creating secure backup...",
        'prog_fix': "Injecting fix into system...",
        'bkp_ok': "Backup successfully created at:",
        'bkp_err': "Error creating backup:",
        'file_miss': "FILE NOT FOUND:",
        'fix_ok': "SUCCESS! Bug fixed.\n[!] Remember: Go to 'Gnome Tweaks' and activate 'make Caps Lock an additional Ctrl'.",
        'fix_already': "WARNING: The file appears to be already fixed with the Bug correction!",
        'fix_no_match': "ERROR: Original lines not found in the file.",
        'press_any': "[ Press ANY KEY to continue... ]"
    },
    'es': {
        'menu_1': "1 - Copia de seguridad",
        'menu_2': "2 - Corregir Bug CapsLock (FIX)",
        'menu_3': "3 - Salir",
        'menu_0': "0 - Cambiar Idioma",
        'opt_prompt': "Seleccione una opción: ",
        'invalid': "¡Opción inválida! Intente nuevamente.",
        'prog_backup': "Creando copia de seguridad...",
        'prog_fix': "Inyectando corrección...",
        'bkp_ok': "Copia de seguridad exitosa en:",
        'bkp_err': "Error al crear copia:",
        'file_miss': "ARCHIVO NO ENCONTRADO:",
        'fix_ok': "¡ÉXITO! Bug corregido.\n[!] Recuerda: Ve a 'Gnome Tweaks' y activa 'make Caps Lock an additional Ctrl'.",
        'fix_already': "AVISO: ¡El archivo ya parece incluir la corrección del Bug!",
        'fix_no_match': "ERROR: No se encontraron las líneas originales.",
        'press_any': "[ Presione CUALQUIER TECLA para continuar... ]"
    },
    'ru': {
        'menu_1': "1 - Резервное копирование",
        'menu_2': "2 - Исправить Баг CapsLock (FIX)",
        'menu_3': "3 - Выход",
        'menu_0': "0 - Выбор языка",
        'opt_prompt': "Выберите опцию: ",
        'invalid': "Неверная опция! Попробуйте снова.",
        'prog_backup': "Создание резервной копии...",
        'prog_fix': "Внедрение исправления...",
        'bkp_ok': "Копия успешно создана:",
        'bkp_err': "Ошибка копирования:",
        'file_miss': "ФАЙЛ НЕ НАЙДЕН:",
        'fix_ok': "УСПЕШНО! Баг исправлен.\n[!] Напоминание: перейдите в 'Gnome Tweaks' и включите 'make Caps Lock...'.",
        'fix_already': "ПРЕДУПРЕЖДЕНИЕ: Файл уже содержит исправление Бага!",
        'fix_no_match': "ОШИБКА: Исходные строки не найдены.",
        'press_any': "[ Нажмите ЛЮБУЮ КЛАВИШУ для продолжения... ]"
    }
}

CURRENT_LANG = 'en'

# ==========================================
# FUNÇÕES DE UX (CLI EFFECTS & GETCH)
# ==========================================
def t(key):
    return LANG_DICT[CURRENT_LANG][key]

def clear_screen():
    os.system('clear')

def getch():
    """Lê um caractere imediatamente após ser pressionado (Desativa buffer de ENTER)."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    
    if ch == '\x03':  # Tratamento para CTRL+C
        raise KeyboardInterrupt
    return ch

ANSI_ESCAPE = re.compile(r'(\033\[[0-9;]*[a-zA-Z]|\033\]8;;.*?\033\\|\033\\)')

def typer(text, speed=0.012, end='\n'):
    """Typewriter Effect respeitando as Formatações ANSI Invisíveis (Cores/Hyperlinks)."""
    parts = ANSI_ESCAPE.split(text)
    for part in parts:
        if part.replace('\033', '').endswith('m') or ('\033]8;;' in part) or part == '\033\\':
            sys.stdout.write(part)
        else:
            for char in part:
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(speed)
    sys.stdout.write(end)
    sys.stdout.flush()

def animate_progress(task_text):
    """Animação Hacker de Processamento em barra."""
    typer(f"\n{C_CYAN}[+]{C_RESET} {task_text}", speed=0.02)
    bar_length = 40
    for i in range(101):
        time.sleep(0.012)
        filled = int(bar_length * i // 100)
        bar = '█' * filled + '-' * (bar_length - filled)
        sys.stdout.write(f"\r{C_GREEN}[{bar}] {i}%{C_RESET}")
        sys.stdout.flush()
    print("\n")

# ==========================================
# FUNÇÕES CORE SISTÊMICAS
# ==========================================
def check_os():
    current_os = platform.system()
    if current_os != "Linux":
        clear_screen()
        typer(f"{C_RED}{C_BOLD}====================================================================================================={C_RESET}")
        typer(f"{C_RED}FATAL ERROR: This software is built strictly for Linux.{C_RESET}")
        typer(f"{C_YELLOW}It fixes the latency Bug on the CapsLock key.{C_RESET}\n{C_GRAY}Unsupported OS: [{current_os}]{C_RESET}\n")
        typer(f"{C_RED}ERRO FATAL: Este software foi desenvolvido APENAS para Linux.{C_RESET}")
        typer(f"{C_YELLOW}Ele corrige o Bug/delay na digitação da tecla CapsLock.{C_RESET}\n{C_GRAY}Ambiente não suportado: [{current_os}]{C_RESET}")
        typer(f"{C_RED}{C_BOLD}====================================================================================================={C_RESET}\n")
        sys.exit(1)

def ensure_root():
    """Auto-Elevação com Explicação Educativa e Breve para Criar Confiança."""
    if os.geteuid() != 0:
        clear_screen()
        print(ASCII_ART)
        print(f"                                  {C_CYAN}Development By {CLICKABLE_LINK}{C_RESET}\n")
        
        typer(f"{C_YELLOW}[!] Solicitando permissão de Superusuário (ROOT)...{C_RESET}", speed=0.015)
        
        trust_text = f"""
{C_RED}🛡️_SEGURANÇA / SECURITY:{C_RESET}
{C_GRAY}PT:{C_RESET} Este script requer permissão de administrador para ler e editar o arquivo 
    protegido do sistema: {C_BOLD}(/usr/share/X11/xkb/symbols/capslock){C_RESET}.

{C_GRAY}EN:{C_RESET} This script requires admin privileges to read and edit the protected 
    system file: {C_BOLD}(/usr/share/X11/xkb/symbols/capslock){C_RESET}.
"""
        typer(trust_text, speed=0.005)
        
        try:
            # O Sudo pedirá a senha logo abaixo dessa explicação
            os.execvp('sudo',['sudo', sys.executable] + sys.argv)
        except Exception as e:
            typer(f"{C_RED}[✘] Falha ao solicitar permissão root: {e}{C_RESET}")
            sys.exit(1)

def backup_file():
    if not os.path.exists(FILE_PATH):
        typer(f"{C_RED}[!] {t('file_miss')} {FILE_PATH}{C_RESET}")
        return

    animate_progress(t('prog_backup'))
    try:
        shutil.copy2(FILE_PATH, BACKUP_PATH)
        typer(f"{C_GREEN}[✔] {t('bkp_ok')} {BACKUP_PATH}{C_RESET}")
    except Exception as e:
        typer(f"{C_RED}[✘] {t('bkp_err')} {e}{C_RESET}")

def fix_bug():
    if not os.path.exists(FILE_PATH):
        typer(f"{C_RED}[!] {t('file_miss')} {FILE_PATH}{C_RESET}")
        return

    animate_progress(t('prog_fix'))
    
    try:
        with open(FILE_PATH, 'r', encoding='utf-8') as file:
            content = file.read()

        if REGEX_CHECK_ALREADY_FIXED.search(content):
            typer(f"{C_YELLOW}[!] {t('fix_already')}{C_RESET}")
            return

        if not REGEX_FIND_BLOCK.search(content):
            typer(f"{C_RED}[✘] {t('fix_no_match')}{C_RESET}")
            return

        new_content = REGEX_FIND_BLOCK.sub(REPLACEMENT_BLOCK, content)

        with open(FILE_PATH, 'w', encoding='utf-8') as file:
            file.write(new_content)
        
        typer(f"\n{C_GREEN}[✔] {t('fix_ok')}{C_RESET}")
        
    except Exception as e:
        typer(f"{C_RED}[✘] ERROR: {e}{C_RESET}")

def select_language():
    global CURRENT_LANG
    clear_screen()
    print(ASCII_ART)
    print(f"                                  {C_CYAN}Development By {CLICKABLE_LINK}{C_RESET}\n")
    typer(f"{C_GRAY}====================================================================================================={C_RESET}\n")
    typer(f"{C_CYAN}Select Language / Selecione o Idioma:{C_RESET}\n\n")
    print("1 - English\n")
    print("2 - Português\n")
    print("3 - Español\n")
    print("4 - Русский\n")
    
    while True:
        typer(f"{C_YELLOW}> {C_RESET}", end='')
        opt = getch()
        print(opt) 
        if opt == '1': 
            CURRENT_LANG = 'en'; break
        elif opt == '2': 
            CURRENT_LANG = 'pt'; break
        elif opt == '3': 
            CURRENT_LANG = 'es'; break
        elif opt == '4': 
            CURRENT_LANG = 'ru'; break
        else: 
            typer(f"{C_RED}Inválido. Press again!{C_RESET}")

# ==========================================
# LIFECYCLE E MENU PRINCIPAL
# ==========================================
def main():
    check_os()       
    ensure_root()    
    
    select_language()
    
    while True:
        clear_screen()
        print(ASCII_ART)
        print(f"                                  {C_CYAN}Development By {CLICKABLE_LINK}{C_RESET}\n")
        
        typer(f"{C_GREEN}====================================================================================================={C_RESET}\n")
        typer(f"{C_CYAN}  {t('menu_1')}\n\n")
        typer(f"  {t('menu_2')}\n\n")
        typer(f"  {t('menu_3')}\n\n\n")
        typer(f"  {t('menu_0')}{C_RESET}\n")
        typer(f"{C_GREEN}====================================================================================================={C_RESET}\n\n")
        
        typer(f"{C_YELLOW}root@linux:~# {C_RESET}{t('opt_prompt')}", end='')
        choice = getch() 
        print(choice)
        
        if choice == '1':
            backup_file()
            typer(f"\n{C_CYAN}{t('press_any')}{C_RESET}")
            getch()
        elif choice == '2':
            fix_bug()
            typer(f"\n{C_CYAN}{t('press_any')}{C_RESET}")
            getch()
        elif choice == '0':
            select_language()
        elif choice == '3':
            typer(f"\n{C_GREEN}Connection closed... Happy hacking!{C_RESET}\n", speed=0.04)
            sys.exit(0)
        else:
            typer(f"\n{C_RED}[!] {t('invalid')}{C_RESET}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        typer(f"\n\n{C_RED}[!] Operation aborted by user (CTRL+C).{C_RESET}\n")
        sys.exit(0)

#!/usr/bin/env python3
"""
Kali Linux Security Configuration Script
Automatiza configurações de segurança e privacidade
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import time
import threading

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_banner():
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
  ██████ ▓█████▄▄▄█████▓ █    ██  ██▓███
▒██    ▒ ▓█   ▀▓  ██▒ ▓▒ ██  ▓██▒▓██░  ██▒
░ ▓██▄   ▒███  ▒ ▓██░ ▒░▓██  ▒██░▓██░ ██▓▒
  ▒   ██▒▒▓█  ▄░ ▓██▓ ░ ▓▓█  ░██░▒██▄█▓▒ ▒
▒██████▒▒░▒████▒ ▒██▒ ░ ▒▒█████▓ ▒██▒ ░  ░
▒ ▒▓▒ ▒ ░░░ ▒░ ░ ▒ ░░   ░▒▓▒ ▒ ▒ ▒▓▒░ ░  ░
░ ░▒  ░ ░ ░ ░  ░   ░    ░░▒░ ░ ░ ░▒ ░
░  ░  ░     ░    ░       ░░░ ░ ░ ░░
      ░     ░  ░           ░

{Colors.END}
    """
    print(banner)

def check_root():
    if os.geteuid() != 0:
        print(f"{Colors.RED}[!] Este script precisa ser executado como root (sudo){Colors.END}")
        sys.exit(1)

def run_command(cmd, shell=True, check=True):
    try:
        result = subprocess.run(cmd, shell=shell, check=check,
                              capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return False, e.stdout, e.stderr

def file_contains(filepath, search_string):
    try:
        with open(filepath, 'r') as f:
            return search_string in f.read()
    except FileNotFoundError:
        return False

def show_progress_bar(duration, label="Processando"):
    bar_length = 50
    for i in range(101):
        filled = int(bar_length * i / 100)
        bar = '█' * filled + '░' * (bar_length - filled)
        print(f"\r{Colors.CYAN}{label}: [{bar}] {i}%{Colors.END}", end='', flush=True)
        time.sleep(duration / 100)
    print()

def system_update():
    print(f"\n{Colors.BLUE}[*] Atualizando lista de pacotes...{Colors.END}")

    success, output, error = run_command("apt update", check=False)
    if not success:
        print(f"{Colors.RED}[!] Erro ao atualizar lista de pacotes{Colors.END}")
        if error:
            print(f"{Colors.YELLOW}{error}{Colors.END}")
        return

    print(f"{Colors.GREEN}[✓] Lista de pacotes atualizada{Colors.END}")

    print(f"\n{Colors.BLUE}[*] Verificando pacotes disponíveis...{Colors.END}")
    success, output, _ = run_command("apt list --upgradable 2>/dev/null | wc -l", check=False)
    upgradable = int(output.strip()) - 1

    if upgradable <= 0:
        print(f"{Colors.GREEN}[✓] Sistema já está atualizado!{Colors.END}")
        return

    print(f"{Colors.YELLOW}[!] {upgradable} pacote(s) disponível(is) para atualização{Colors.END}")
    print(f"{Colors.CYAN}[*] Atualizando sistema... (isso pode levar alguns minutos){Colors.END}\n")

    print(f"{Colors.CYAN}[*] Executando apt upgrade...{Colors.END}")
    success, output, error = run_command("DEBIAN_FRONTEND=noninteractive apt upgrade -y", check=False)
    if not success:
        print(f"{Colors.YELLOW}[!] Aviso durante apt upgrade{Colors.END}")
    else:
        print(f"{Colors.GREEN}[✓] apt upgrade concluído{Colors.END}")

    print(f"\n{Colors.CYAN}[*] Executando apt full-upgrade...{Colors.END}")
    success, output, error = run_command("DEBIAN_FRONTEND=noninteractive apt full-upgrade -y", check=False)
    if not success:
        print(f"{Colors.YELLOW}[!] Aviso durante apt full-upgrade{Colors.END}")
    else:
        print(f"{Colors.GREEN}[✓] apt full-upgrade concluído{Colors.END}")

    print(f"\n{Colors.CYAN}[*] Removendo pacotes desnecessários...{Colors.END}")
    run_command("apt autoremove -y", check=False)
    print(f"{Colors.GREEN}[✓] Limpeza concluída{Colors.END}")

    print(f"\n{Colors.GREEN}{Colors.BOLD}[✓] Sistema atualizado com sucesso!{Colors.END}")

def is_installed(package_name):
    success, output, _ = run_command(f"which {package_name}", check=False)
    if success:
        return True
    success, output, _ = run_command(f"dpkg -l | grep -w {package_name}", check=False)
    return success and output.strip() != ""

def install_brave():
    print(f"{Colors.CYAN}[*] Instalando Brave Browser...{Colors.END}")
    if is_installed("brave-browser"):
        print(f"{Colors.YELLOW}[!] Brave Browser já está instalado{Colors.END}")
        return True

    def install():
        run_command("apt install -y -qq curl", check=False)
        run_command("curl -fsSL https://dl.brave.com/install.sh | sh", check=False)

    thread = threading.Thread(target=install)
    thread.start()
    show_progress_bar(3, "Instalando Brave")
    thread.join()

    if is_installed("brave-browser"):
        print(f"{Colors.GREEN}[✓] Brave Browser instalado com sucesso!{Colors.END}")
        return True
    else:
        print(f"{Colors.RED}[!] Erro ao instalar Brave Browser{Colors.END}")
        return False

def install_discord():
    print(f"{Colors.CYAN}[*] Instalando Discord...{Colors.END}")
    if is_installed("discord"):
        print(f"{Colors.YELLOW}[!] Discord já está instalado{Colors.END}")
        return True

    def install():
        run_command("wget -q -O /tmp/discord.deb 'https://discord.com/api/download?platform=linux&format=deb'", check=False)
        run_command("apt install -y -qq /tmp/discord.deb", check=False)
        run_command("rm -f /tmp/discord.deb", check=False)

    thread = threading.Thread(target=install)
    thread.start()
    show_progress_bar(3, "Instalando Discord")
    thread.join()

    if is_installed("discord"):
        print(f"{Colors.GREEN}[✓] Discord instalado com sucesso!{Colors.END}")
        return True
    else:
        print(f"{Colors.RED}[!] Erro ao instalar Discord{Colors.END}")
        return False

def install_mullvad():
    print(f"{Colors.CYAN}[*] Instalando Mullvad VPN...{Colors.END}")
    if is_installed("mullvad-vpn"):
        print(f"{Colors.YELLOW}[!] Mullvad VPN já está instalado{Colors.END}")
        return True

    def install():
        run_command("wget -q -O /tmp/mullvad.deb https://mullvad.net/download/app/deb/latest", check=False)
        run_command("apt install -y -qq /tmp/mullvad.deb", check=False)
        run_command("rm -f /tmp/mullvad.deb", check=False)

    thread = threading.Thread(target=install)
    thread.start()
    show_progress_bar(3, "Instalando Mullvad VPN")
    thread.join()

    if is_installed("mullvad-vpn"):
        print(f"{Colors.GREEN}[✓] Mullvad VPN instalado com sucesso!{Colors.END}")
        return True
    else:
        print(f"{Colors.RED}[!] Erro ao instalar Mullvad VPN{Colors.END}")
        return False

def install_protonmail():
    print(f"{Colors.CYAN}[*] Instalando ProtonMail Bridge...{Colors.END}")
    if is_installed("protonmail-bridge"):
        print(f"{Colors.YELLOW}[!] ProtonMail Bridge já está instalado{Colors.END}")
        return True

    def install():
        run_command("apt install -y -qq debsig-verify debian-keyring", check=False)
        run_command("wget -q -O /tmp/bridge_pubkey.gpg https://proton.me/download/bridge/bridge_pubkey.gpg", check=False)
        run_command("gpg --dearmor --output /tmp/debsig.gpg /tmp/bridge_pubkey.gpg", check=False)
        run_command("mkdir -p /usr/share/debsig/keyrings/E2C75D68E6234B07", check=False)
        run_command("mv /tmp/debsig.gpg /usr/share/debsig/keyrings/E2C75D68E6234B07/", check=False)
        run_command("wget -q -O /tmp/bridge.pol https://proton.me/download/bridge/bridge.pol", check=False)
        run_command("mkdir -p /etc/debsig/policies/E2C75D68E6234B07", check=False)
        run_command("cp /tmp/bridge.pol /etc/debsig/policies/E2C75D68E6234B07/", check=False)
        run_command("wget -q -O /tmp/protonmail-bridge.deb https://proton.me/download/bridge/protonmail-bridge_3.13.0-1_amd64.deb", check=False)
        run_command("apt install -y -qq /tmp/protonmail-bridge.deb", check=False)
        run_command("rm -f /tmp/protonmail-bridge.deb /tmp/bridge_pubkey.gpg /tmp/bridge.pol", check=False)

    thread = threading.Thread(target=install)
    thread.start()
    show_progress_bar(4, "Instalando ProtonMail Bridge")
    thread.join()

    if is_installed("protonmail-bridge"):
        print(f"{Colors.GREEN}[✓] ProtonMail Bridge instalado com sucesso!{Colors.END}")
        return True
    else:
        print(f"{Colors.RED}[!] Erro ao instalar ProtonMail Bridge{Colors.END}")
        return False

def install_protonvpn():
    print(f"{Colors.CYAN}[*] Instalando Proton VPN...{Colors.END}")
    if is_installed("protonvpn-app") or is_installed("proton-vpn-gnome-desktop"):
        print(f"{Colors.YELLOW}[!] Proton VPN já está instalado{Colors.END}")
        return True

    def install():
        run_command("wget -q -O /tmp/protonvpn-stable-release.deb https://repo.protonvpn.com/debian/dists/stable/main/binary-all/protonvpn-stable-release_1.0.8_all.deb", check=False)
        run_command("dpkg -i /tmp/protonvpn-stable-release.deb", check=False)
        run_command("apt update -qq", check=False)
        run_command("apt install -y -qq proton-vpn-gnome-desktop", check=False)
        run_command("apt install -y -qq libayatana-appindicator3-1 gir1.2-ayatanaappindicator3-0.1 gnome-shell-extension-appindicator", check=False)
        run_command("rm -f /tmp/protonvpn-stable-release.deb", check=False)

    thread = threading.Thread(target=install)
    thread.start()
    show_progress_bar(4, "Instalando Proton VPN")
    thread.join()

    if is_installed("proton-vpn-gnome-desktop") or is_installed("protonvpn-app"):
        print(f"{Colors.GREEN}[✓] Proton VPN instalado com sucesso!{Colors.END}")
        print(f"{Colors.CYAN}[i] Abra o app Extensions e ative 'Ubuntu AppIndicators'{Colors.END}")
        return True
    else:
        print(f"{Colors.RED}[!] Erro ao instalar Proton VPN{Colors.END}")
        return False

def install_telegram():
    print(f"{Colors.CYAN}[*] Instalando Telegram...{Colors.END}")
    if is_installed("telegram-desktop") or os.path.exists("/opt/Telegram/Telegram"):
        print(f"{Colors.YELLOW}[!] Telegram já está instalado{Colors.END}")
        return True

    def install():
        run_command("wget -q -O /tmp/telegram.tar.xz https://telegram.org/dl/desktop/linux", check=False)
        run_command("mkdir -p /opt/Telegram", check=False)
        run_command("tar -xf /tmp/telegram.tar.xz -C /opt/", check=False)
        run_command("ln -sf /opt/Telegram/Telegram /usr/local/bin/telegram-desktop", check=False)
        run_command("rm -f /tmp/telegram.tar.xz", check=False)

        desktop_entry = """[Desktop Entry]
Version=1.0
Name=Telegram Desktop
Comment=Official desktop application for the Telegram messaging service
TryExec=/opt/Telegram/Telegram
Exec=/opt/Telegram/Telegram -- %u
Icon=/opt/Telegram/Telegram
Terminal=false
StartupWMClass=TelegramDesktop
Type=Application
Categories=Network;InstantMessaging;Qt;
MimeType=x-scheme-handler/tg;
Keywords=tg;chat;im;messaging;messenger;sms;tdesktop;
X-GNOME-UsesNotifications=true"""

        with open("/usr/share/applications/telegram-desktop.desktop", "w") as f:
            f.write(desktop_entry)

    thread = threading.Thread(target=install)
    thread.start()
    show_progress_bar(3, "Instalando Telegram")
    thread.join()

    if os.path.exists("/opt/Telegram/Telegram"):
        print(f"{Colors.GREEN}[✓] Telegram instalado com sucesso!{Colors.END}")
        return True
    else:
        print(f"{Colors.RED}[!] Erro ao instalar Telegram{Colors.END}")
        return False

def install_tor():
    print(f"{Colors.CYAN}[*] Instalando Tor Browser...{Colors.END}")
    if os.path.exists("/opt/tor-browser") or is_installed("torbrowser-launcher"):
        print(f"{Colors.YELLOW}[!] Tor Browser já está instalado{Colors.END}")
        return True

    def install():
        run_command("apt install -y -qq torbrowser-launcher", check=False)

    thread = threading.Thread(target=install)
    thread.start()
    show_progress_bar(3, "Instalando Tor Browser Launcher")
    thread.join()

    if is_installed("torbrowser-launcher"):
        print(f"{Colors.GREEN}[✓] Tor Browser Launcher instalado com sucesso!{Colors.END}")
        print(f"{Colors.CYAN}[i] Execute 'torbrowser-launcher' para baixar e iniciar o Tor Browser{Colors.END}")
        return True
    else:
        print(f"{Colors.RED}[!] Erro ao instalar Tor Browser{Colors.END}")
        return False

def install_virtualbox():
    print(f"{Colors.CYAN}[*] Instalando VirtualBox...{Colors.END}")
    if is_installed("virtualbox"):
        print(f"{Colors.YELLOW}[!] VirtualBox já está instalado{Colors.END}")
        return True

    def install():
        run_command("apt update -qq", check=False)
        run_command("apt install -y -qq virtualbox virtualbox-ext-pack virtualbox-guest-additions-iso", check=False)

    thread = threading.Thread(target=install)
    thread.start()
    show_progress_bar(4, "Instalando VirtualBox")
    thread.join()

    if is_installed("virtualbox"):
        print(f"{Colors.GREEN}[✓] VirtualBox instalado com sucesso!{Colors.END}")
        run_command("usermod -aG vboxusers $SUDO_USER", check=False)
        print(f"{Colors.CYAN}[i] Usuário adicionado ao grupo vboxusers (reinicie a sessão){Colors.END}")
        return True
    else:
        print(f"{Colors.RED}[!] Erro ao instalar VirtualBox{Colors.END}")
        return False

def install_genymotion():
    print(f"{Colors.CYAN}[*] Instalando Genymotion...{Colors.END}")
    if os.path.exists("/opt/genymobile/genymotion"):
        print(f"{Colors.YELLOW}[!] Genymotion já está instalado{Colors.END}")
        return True

    def install():
        run_command("apt install -y -qq virtualbox virtualbox-ext-pack", check=False)
        run_command("wget -q -O /tmp/genymotion.bin https://dl.genymotion.com/releases/genymotion-3.9.0/genymotion-3.9.0-linux_x64.bin", check=False)
        run_command("chmod +x /tmp/genymotion.bin", check=False)
        run_command("yes | /tmp/genymotion.bin -d /opt/genymobile/genymotion", check=False)
        run_command("rm -f /tmp/genymotion.bin", check=False)
        run_command("ln -sf /opt/genymobile/genymotion/genymotion /usr/local/bin/genymotion", check=False)

        desktop_entry = """[Desktop Entry]
Name=Genymotion
Comment=Android Emulator
Exec=/opt/genymobile/genymotion/genymotion
Icon=/opt/genymobile/genymotion/icons/genymotion-logo.png
Terminal=false
Type=Application
Categories=Development;Emulator;"""

        with open("/usr/share/applications/genymotion.desktop", "w") as f:
            f.write(desktop_entry)

        run_command("update-desktop-database", check=False)

    thread = threading.Thread(target=install)
    thread.start()
    show_progress_bar(4, "Instalando Genymotion")
    thread.join()

    if os.path.exists("/opt/genymobile/genymotion"):
        print(f"{Colors.GREEN}[✓] Genymotion instalado com sucesso!{Colors.END}")
        print(f"{Colors.CYAN}[i] Execute 'genymotion' ou encontre no menu de aplicativos{Colors.END}")
        return True
    else:
        print(f"{Colors.RED}[!] Erro ao instalar Genymotion{Colors.END}")
        return False

def applications_menu():
    while True:
        menu = f"""
{Colors.BOLD}{Colors.CYAN}╔════════════════════════════════════════╗
║      INSTALADOR DE APLICATIVOS         ║
╚════════════════════════════════════════╝{Colors.END}

{Colors.GREEN}1.{Colors.END} Brave Browser
{Colors.GREEN}2.{Colors.END} Discord
{Colors.GREEN}3.{Colors.END} Mullvad VPN
{Colors.GREEN}4.{Colors.END} ProtonMail Bridge
{Colors.GREEN}5.{Colors.END} Proton VPN
{Colors.GREEN}6.{Colors.END} Telegram
{Colors.GREEN}7.{Colors.END} Tor Browser
{Colors.GREEN}8.{Colors.END} VirtualBox
{Colors.GREEN}9.{Colors.END} Genymotion
{Colors.GREEN}10.{Colors.END} {Colors.BOLD}Instalar TODOS{Colors.END}
{Colors.RED}0.{Colors.END} Voltar

{Colors.CYAN}Escolha uma opção:{Colors.END} """

        choice = input(menu).strip()

        if choice == '1':
            install_brave()
        elif choice == '2':
            install_discord()
        elif choice == '3':
            install_mullvad()
        elif choice == '4':
            install_protonmail()
        elif choice == '5':
            install_protonvpn()
        elif choice == '6':
            install_telegram()
        elif choice == '7':
            install_tor()
        elif choice == '8':
            install_virtualbox()
        elif choice == '9':
            install_genymotion()
        elif choice == '10':
            print(f"\n{Colors.BOLD}{Colors.YELLOW}[*] Instalando todos os aplicativos...{Colors.END}\n")
            install_brave()
            install_discord()
            install_mullvad()
            install_protonmail()
            install_protonvpn()
            install_telegram()
            install_tor()
            install_virtualbox()
            install_genymotion()
            print(f"\n{Colors.GREEN}{Colors.BOLD}[✓] Todos os aplicativos foram processados!{Colors.END}")
        elif choice == '0':
            break
        else:
            print(f"\n{Colors.RED}[!] Opção inválida. Tente novamente.{Colors.END}")

        if choice != '0':
            input(f"\n{Colors.YELLOW}Pressione ENTER para continuar...{Colors.END}")

def configure_random_mac():
    print(f"\n{Colors.BLUE}[*] Configurando MAC Address Aleatório...{Colors.END}")

    conf_dir = "/etc/NetworkManager/conf.d"
    conf_file = f"{conf_dir}/00-macrandomize.conf"

    config_content = """[device]
wifi.scan-rand-mac-address=yes

[connection]
wifi.cloned-mac-address=random
ethernet.cloned-mac-address=random
connection.stable-id=${CONNECTION}/${BOOT}
"""

    if os.path.exists(conf_file):
        with open(conf_file, 'r') as f:
            current = f.read()
            if "wifi.cloned-mac-address=random" in current and "ethernet.cloned-mac-address=random" in current:
                print(f"{Colors.YELLOW}[!] MAC aleatório já está configurado{Colors.END}")
                return

    os.makedirs(conf_dir, exist_ok=True)

    try:
        with open(conf_file, 'w') as f:
            f.write(config_content)
        print(f"{Colors.GREEN}[✓] Arquivo de configuração criado: {conf_file}{Colors.END}")

        success, _, _ = run_command("systemctl restart NetworkManager")
        if success:
            print(f"{Colors.GREEN}[✓] NetworkManager reiniciado{Colors.END}")
            print(f"{Colors.GREEN}[✓] MAC aleatório configurado com sucesso!{Colors.END}")

            success, output, _ = run_command("ip link show | grep -A 1 'wlan0\\|eth0'", check=False)
            if success:
                print(f"\n{Colors.CYAN}MACs atuais:{Colors.END}")
                print(output)
        else:
            print(f"{Colors.RED}[!] Erro ao reiniciar NetworkManager{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}[!] Erro ao configurar MAC aleatório: {e}{Colors.END}")

def configure_ram_logs():
    print(f"\n{Colors.BLUE}[*] Configurando Logs em RAM (volatile)...{Colors.END}")

    journald_conf = "/etc/systemd/journald.conf"

    if file_contains(journald_conf, "Storage=volatile"):
        with open(journald_conf, 'r') as f:
            for line in f:
                if line.strip() == "Storage=volatile":
                    print(f"{Colors.YELLOW}[!] Logs em RAM já estão configurados{Colors.END}")
                    return

    try:
        if not os.path.exists(f"{journald_conf}.bak"):
            shutil.copy(journald_conf, f"{journald_conf}.bak")
            print(f"{Colors.GREEN}[✓] Backup criado: {journald_conf}.bak{Colors.END}")

        with open(journald_conf, 'r') as f:
            lines = f.readlines()

        modified = False
        journal_section_found = False

        for i, line in enumerate(lines):
            if line.strip() == "[Journal]":
                journal_section_found = True
            if journal_section_found and line.strip().startswith("Storage="):
                lines[i] = "Storage=volatile\n"
                modified = True
                break
            if journal_section_found and line.strip().startswith("#Storage="):
                lines[i] = "Storage=volatile\n"
                modified = True
                break

        if not modified:
            if journal_section_found:
                for i, line in enumerate(lines):
                    if line.strip() == "[Journal]":
                        lines.insert(i + 1, "Storage=volatile\n")
                        modified = True
                        break
            else:
                lines.insert(0, "[Journal]\n")
                lines.insert(1, "Storage=volatile\n")
                modified = True

        with open(journald_conf, 'w') as f:
            f.writelines(lines)

        print(f"{Colors.GREEN}[✓] Configuração de logs modificada{Colors.END}")

        success, _, _ = run_command("systemctl restart systemd-journald")
        if success:
            print(f"{Colors.GREEN}[✓] systemd-journald reiniciado{Colors.END}")
            print(f"{Colors.GREEN}[✓] Logs configurados para RAM com sucesso!{Colors.END}")
            print(f"{Colors.CYAN}[i] Os logs agora são armazenados em /run/log/journal (RAM){Colors.END}")
        else:
            print(f"{Colors.RED}[!] Erro ao reiniciar systemd-journald{Colors.END}")

    except Exception as e:
        print(f"{Colors.RED}[!] Erro ao configurar logs em RAM: {e}{Colors.END}")

def configure_lid_switch():
    print(f"\n{Colors.BLUE}[*] Configurando Ação da Tampa (Poweroff)...{Colors.END}")

    logind_conf = "/etc/systemd/logind.conf"

    required_settings = [
        "HandleLidSwitch=poweroff",
        "HandleLidSwitchExternalPower=poweroff",
        "HandleLidSwitchDocked=poweroff"
    ]

    all_configured = True
    with open(logind_conf, 'r') as f:
        content = f.read()
        for setting in required_settings:
            if setting not in content or f"#{setting}" in content:
                all_configured = False
                break

    if all_configured:
        print(f"{Colors.YELLOW}[!] Ação da tampa já está configurada{Colors.END}")
        return

    try:
        if not os.path.exists(f"{logind_conf}.bak"):
            shutil.copy(logind_conf, f"{logind_conf}.bak")
            print(f"{Colors.GREEN}[✓] Backup criado: {logind_conf}.bak{Colors.END}")

        with open(logind_conf, 'r') as f:
            lines = f.readlines()

        login_section_found = False
        settings_added = []

        for i, line in enumerate(lines):
            if line.strip() == "[Login]":
                login_section_found = True

            if login_section_found:
                for setting in required_settings:
                    key = setting.split('=')[0]
                    if line.strip().startswith(f"{key}=") or line.strip().startswith(f"#{key}="):
                        lines[i] = f"{setting}\n"
                        settings_added.append(setting)

        for setting in required_settings:
            if setting not in settings_added:
                if not login_section_found:
                    lines.insert(0, "[Login]\n")
                    login_section_found = True

                for i, line in enumerate(lines):
                    if line.strip() == "[Login]":
                        lines.insert(i + 1, f"{setting}\n")
                        break

        with open(logind_conf, 'w') as f:
            f.writelines(lines)

        print(f"{Colors.GREEN}[✓] Configuração da tampa modificada{Colors.END}")

        success, _, _ = run_command("systemctl restart systemd-logind")
        if success:
            print(f"{Colors.GREEN}[✓] systemd-logind reiniciado{Colors.END}")
            print(f"{Colors.GREEN}[✓] Tampa configurada para desligar o sistema!{Colors.END}")
        else:
            print(f"{Colors.RED}[!] Erro ao reiniciar systemd-logind{Colors.END}")

    except Exception as e:
        print(f"{Colors.RED}[!] Erro ao configurar tampa: {e}{Colors.END}")

def configure_firewall():
    print(f"\n{Colors.BLUE}[*] Configurando Firewall (UFW)...{Colors.END}")

    success, _, _ = run_command("which ufw", check=False)
    if not success:
        print(f"{Colors.YELLOW}[!] UFW não está instalado. Instalando...{Colors.END}")
        success, _, _ = run_command("apt update && apt install -y ufw")
        if success:
            print(f"{Colors.GREEN}[✓] UFW instalado com sucesso{Colors.END}")
        else:
            print(f"{Colors.RED}[!] Erro ao instalar UFW{Colors.END}")
            return

    success, output, _ = run_command("ufw status", check=False)
    if success and "Status: active" in output:
        if "default deny incoming" in output.lower() and "default allow outgoing" in output.lower():
            print(f"{Colors.YELLOW}[!] Firewall já está configurado e ativo{Colors.END}")

            success, output, _ = run_command("sysctl net.ipv4.icmp_echo_ignore_all net.ipv6.icmp.echo_ignore_all", check=False)
            if "net.ipv4.icmp_echo_ignore_all = 1" in output and "net.ipv6.icmp.echo_ignore_all = 1" in output:
                print(f"{Colors.YELLOW}[!] ICMP já está bloqueado{Colors.END}")
                return

    try:
        print(f"{Colors.CYAN}[*] Configurando regras do firewall...{Colors.END}")

        run_command("ufw --force reset", check=False)
        run_command("ufw default deny incoming")
        run_command("ufw default allow outgoing")

        success, _, _ = run_command("ufw --force enable")
        if success:
            print(f"{Colors.GREEN}[✓] UFW ativado{Colors.END}")

        print(f"{Colors.CYAN}[*] Bloqueando ICMP (ping)...{Colors.END}")
        run_command("sysctl -w net.ipv4.icmp_echo_ignore_all=1")
        run_command("sysctl -w net.ipv6.icmp.echo_ignore_all=1")

        sysctl_conf = "/etc/sysctl.conf"
        with open(sysctl_conf, 'a') as f:
            f.write("\n# Bloquear ICMP (ping)\n")
            f.write("net.ipv4.icmp_echo_ignore_all=1\n")
            f.write("net.ipv6.icmp.echo_ignore_all=1\n")

        print(f"{Colors.GREEN}[✓] Firewall configurado com sucesso!{Colors.END}")
        print(f"{Colors.GREEN}[✓] ICMP (ping) bloqueado{Colors.END}")

        success, output, _ = run_command("ufw status verbose")
        if success:
            print(f"\n{Colors.CYAN}Status do Firewall:{Colors.END}")
            print(output)

    except Exception as e:
        print(f"{Colors.RED}[!] Erro ao configurar firewall: {e}{Colors.END}")

def configure_login_wallpaper():
    print(f"\n{Colors.BLUE}[*] Configurando Wallpaper de Login...{Colors.END}")

    background_path = "/usr/share/desktop-base/kali-theme/login/background"

    print(f"\n{Colors.CYAN}Cole o caminho completo da imagem que deseja usar:{Colors.END}")
    print(f"{Colors.YELLOW}Exemplo: /home/user/Downloads/minha_imagem.jpg{Colors.END}")
    image_path = input(f"{Colors.GREEN}Caminho: {Colors.END}").strip()

    image_path = image_path.strip('"').strip("'")

    if not image_path:
        print(f"{Colors.RED}[!] Nenhum caminho fornecido. Cancelando...{Colors.END}")
        return

    image_path = os.path.expanduser(image_path)

    if not os.path.exists(image_path):
        print(f"{Colors.RED}[!] Arquivo não encontrado: {image_path}{Colors.END}")
        return

    valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
    if not any(image_path.lower().endswith(ext) for ext in valid_extensions):
        print(f"{Colors.YELLOW}[!] Aviso: O arquivo pode não ser uma imagem válida{Colors.END}")

    try:
        if os.path.exists(background_path) and not os.path.exists(f"{background_path}.bak"):
            shutil.copy(background_path, f"{background_path}.bak")
            print(f"{Colors.GREEN}[✓] Backup criado: {background_path}.bak{Colors.END}")

        dest_dir = "/usr/share/desktop-base/kali-theme/login/"
        filename = os.path.basename(image_path)
        dest_path = os.path.join(dest_dir, filename)

        shutil.copy(image_path, dest_path)
        print(f"{Colors.GREEN}[✓] Imagem copiada para: {dest_path}{Colors.END}")

        os.chmod(dest_path, 0o644)
        os.chown(dest_path, 0, 0)
        print(f"{Colors.GREEN}[✓] Permissões configuradas (644, root:root){Colors.END}")

        shutil.copy(dest_path, background_path)
        os.chmod(background_path, 0o644)
        os.chown(background_path, 0, 0)

        print(f"{Colors.GREEN}[✓] Wallpaper de login configurado com sucesso!{Colors.END}")
        print(f"{Colors.CYAN}[i] Faça logout para ver o novo wallpaper{Colors.END}")

    except PermissionError:
        print(f"{Colors.RED}[!] Erro de permissão. Certifique-se de executar como root{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}[!] Erro ao configurar wallpaper: {e}{Colors.END}")

def get_directory_size(path):
    total = 0
    try:
        for entry in os.scandir(path):
            if entry.is_file(follow_symlinks=False):
                total += entry.stat().st_size
            elif entry.is_dir(follow_symlinks=False):
                total += get_directory_size(entry.path)
    except (PermissionError, FileNotFoundError):
        pass
    return total

def format_bytes(bytes_size):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} TB"

def deep_clean_system():
    print(f"\n{Colors.BLUE}[*] Iniciando Limpeza Profunda do Sistema...{Colors.END}")
    print(f"{Colors.YELLOW}[!] Esta operação pode levar alguns minutos{Colors.END}\n")

    total_freed = 0

    print(f"{Colors.CYAN}[1/12] Limpando cache do APT...{Colors.END}")
    try:
        cache_size = get_directory_size("/var/cache/apt/archives")
        run_command("apt-get clean", check=False)
        run_command("apt-get autoclean", check=False)
        freed = cache_size - get_directory_size("/var/cache/apt/archives")
        total_freed += freed
        print(f"{Colors.GREEN}[✓] Cache do APT limpo - Liberado: {format_bytes(freed)}{Colors.END}")
    except Exception as e:
        print(f"{Colors.YELLOW}[!] Erro ao limpar cache APT: {e}{Colors.END}")

    print(f"\n{Colors.CYAN}[2/12] Removendo pacotes órfãos e dependências não utilizadas...{Colors.END}")
    try:
        success, output, _ = run_command("apt-get autoremove --purge -y", check=False)
        if success:
            print(f"{Colors.GREEN}[✓] Pacotes órfãos removidos{Colors.END}")
        else:
            print(f"{Colors.YELLOW}[!] Nenhum pacote órfão encontrado{Colors.END}")
    except Exception as e:
        print(f"{Colors.YELLOW}[!] Erro ao remover pacotes órfãos: {e}{Colors.END}")

    print(f"\n{Colors.CYAN}[3/12] Removendo arquivos de configuração residuais...{Colors.END}")
    try:
        success, output, _ = run_command("dpkg -l | grep '^rc' | awk '{print $2}'", check=False)
        if output.strip():
            run_command(f"dpkg --purge {output.strip().replace(chr(10), ' ')}", check=False)
            print(f"{Colors.GREEN}[✓] Configurações residuais removidas{Colors.END}")
        else:
            print(f"{Colors.YELLOW}[!] Nenhuma configuração residual encontrada{Colors.END}")
    except Exception as e:
        print(f"{Colors.YELLOW}[!] Erro ao remover configurações residuais: {e}{Colors.END}")

    print(f"\n{Colors.CYAN}[4/12] Limpando logs do journald...{Colors.END}")
    try:
        journal_size = get_directory_size("/var/log/journal")
        run_command("journalctl --vacuum-time=3d", check=False)
        run_command("journalctl --vacuum-size=50M", check=False)
        freed = journal_size - get_directory_size("/var/log/journal")
        total_freed += freed
        print(f"{Colors.GREEN}[✓] Logs do journald limpos - Liberado: {format_bytes(freed)}{Colors.END}")
    except Exception as e:
        print(f"{Colors.YELLOW}[!] Erro ao limpar journald: {e}{Colors.END}")

    print(f"\n{Colors.CYAN}[5/12] Limpando logs antigos do sistema...{Colors.END}")
    try:
        log_size = get_directory_size("/var/log")
        run_command("find /var/log -type f -name '*.log' -mtime +7 -delete", check=False)
        run_command("find /var/log -type f -name '*.gz' -delete", check=False)
        run_command("find /var/log -type f -name '*.old' -delete", check=False)
        run_command("find /var/log -type f -name '*.1' -delete", check=False)
        freed = log_size - get_directory_size("/var/log")
        total_freed += freed
        print(f"{Colors.GREEN}[✓] Logs antigos removidos - Liberado: {format_bytes(freed)}{Colors.END}")
    except Exception as e:
        print(f"{Colors.YELLOW}[!] Erro ao limpar logs: {e}{Colors.END}")

    print(f"\n{Colors.CYAN}[6/12] Limpando arquivos temporários...{Colors.END}")
    try:
        tmp_size = get_directory_size("/tmp") + get_directory_size("/var/tmp")
        run_command("rm -rf /tmp/*", check=False)
        run_command("rm -rf /var/tmp/*", check=False)
        freed = tmp_size
        total_freed += freed
        print(f"{Colors.GREEN}[✓] Arquivos temporários removidos - Liberado: {format_bytes(freed)}{Colors.END}")
    except Exception as e:
        print(f"{Colors.YELLOW}[!] Erro ao limpar temporários: {e}{Colors.END}")

    print(f"\n{Colors.CYAN}[7/12] Limpando cache de thumbnails...{Colors.END}")
    try:
        freed_thumb = 0
        for user_home in Path("/home").iterdir():
            if user_home.is_dir():
                thumb_path = user_home / ".cache" / "thumbnails"
                if thumb_path.exists():
                    size = get_directory_size(str(thumb_path))
                    run_command(f"rm -rf {thumb_path}/*", check=False)
                    freed_thumb += size
        total_freed += freed_thumb
        print(f"{Colors.GREEN}[✓] Thumbnails removidos - Liberado: {format_bytes(freed_thumb)}{Colors.END}")
    except Exception as e:
        print(f"{Colors.YELLOW}[!] Erro ao limpar thumbnails: {e}{Colors.END}")

    print(f"\n{Colors.CYAN}[8/12] Esvaziando lixeiras de todos os usuários...{Colors.END}")
    try:
        freed_trash = 0
        for user_home in Path("/home").iterdir():
            if user_home.is_dir():
                trash_path = user_home / ".local" / "share" / "Trash"
                if trash_path.exists():
                    size = get_directory_size(str(trash_path))
                    run_command(f"rm -rf {trash_path}/*", check=False)
                    freed_trash += size

        root_trash = Path("/root/.local/share/Trash")
        if root_trash.exists():
            size = get_directory_size(str(root_trash))
            run_command(f"rm -rf {root_trash}/*", check=False)
            freed_trash += size

        total_freed += freed_trash
        print(f"{Colors.GREEN}[✓] Lixeiras esvaziadas - Liberado: {format_bytes(freed_trash)}{Colors.END}")
    except Exception as e:
        print(f"{Colors.YELLOW}[!] Erro ao esvaziar lixeiras: {e}{Colors.END}")

    print(f"\n{Colors.CYAN}[9/12] Limpando cache de navegadores...{Colors.END}")
    try:
        freed_browser = 0
        for user_home in Path("/home").iterdir():
            if user_home.is_dir():
                firefox_cache = user_home / ".cache" / "mozilla"
                if firefox_cache.exists():
                    size = get_directory_size(str(firefox_cache))
                    run_command(f"rm -rf {firefox_cache}/*", check=False)
                    freed_browser += size

                chrome_cache = user_home / ".cache" / "google-chrome"
                chromium_cache = user_home / ".cache" / "chromium"
                for cache in [chrome_cache, chromium_cache]:
                    if cache.exists():
                        size = get_directory_size(str(cache))
                        run_command(f"rm -rf {cache}/*", check=False)
                        freed_browser += size

        total_freed += freed_browser
        print(f"{Colors.GREEN}[✓] Cache de navegadores limpo - Liberado: {format_bytes(freed_browser)}{Colors.END}")
    except Exception as e:
        print(f"{Colors.YELLOW}[!] Erro ao limpar cache de navegadores: {e}{Colors.END}")

    print(f"\n{Colors.CYAN}[10/12] Limpando cache DNS...{Colors.END}")
    try:
        success, _, _ = run_command("systemctl is-active systemd-resolved", check=False)
        if success:
            run_command("systemd-resolve --flush-caches", check=False)
            print(f"{Colors.GREEN}[✓] Cache DNS do systemd-resolved limpo{Colors.END}")

        success, _, _ = run_command("systemctl is-active nscd", check=False)
        if success:
            run_command("nscd -i hosts", check=False)
            run_command("nscd -i services", check=False)
            print(f"{Colors.GREEN}[✓] Cache DNS do nscd limpo{Colors.END}")

        run_command("systemctl restart NetworkManager", check=False)
        print(f"{Colors.GREEN}[✓] NetworkManager reiniciado (cache DNS limpo){Colors.END}")

    except Exception as e:
        print(f"{Colors.YELLOW}[!] Erro ao limpar cache DNS: {e}{Colors.END}")

    print(f"\n{Colors.CYAN}[11/12] Limpando cache do Python...{Colors.END}")
    try:
        run_command("find /home -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null", check=False)
        run_command("find /root -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null", check=False)
        run_command("find /home -type f -name '*.pyc' -delete 2>/dev/null", check=False)
        run_command("find /root -type f -name '*.pyc' -delete 2>/dev/null", check=False)
        print(f"{Colors.GREEN}[✓] Cache do Python limpo{Colors.END}")
    except Exception as e:
        print(f"{Colors.YELLOW}[!] Erro ao limpar cache Python: {e}{Colors.END}")

    print(f"\n{Colors.CYAN}[12/12] Limpar histórico de comandos bash? (s/N):{Colors.END} ", end='')
    if input().strip().lower() == 's':
        try:
            for user_home in Path("/home").iterdir():
                if user_home.is_dir():
                    bash_history = user_home / ".bash_history"
                    zsh_history = user_home / ".zsh_history"
                    for hist in [bash_history, zsh_history]:
                        if hist.exists():
                            hist.unlink()

            for hist in [Path("/root/.bash_history"), Path("/root/.zsh_history")]:
                if hist.exists():
                    hist.unlink()

            print(f"{Colors.GREEN}[✓] Histórico de comandos limpo{Colors.END}")
        except Exception as e:
            print(f"{Colors.YELLOW}[!] Erro ao limpar histórico: {e}{Colors.END}")
    else:
        print(f"{Colors.YELLOW}[!] Histórico de comandos preservado{Colors.END}")

    print(f"\n{Colors.GREEN}{Colors.BOLD}╔════════════════════════════════════════╗")
    print(f"║     LIMPEZA CONCLUÍDA COM SUCESSO!     ║")
    print(f"╚════════════════════════════════════════╝{Colors.END}")
    print(f"\n{Colors.CYAN}Espaço total liberado: {Colors.BOLD}{format_bytes(total_freed)}{Colors.END}")
    print(f"{Colors.CYAN}Privacidade: Cache DNS, logs e temporários limpos{Colors.END}")
    print(f"{Colors.CYAN}Lixeiras, thumbnails e cache de navegador removidos{Colors.END}\n")

def show_menu():
    menu = f"""
{Colors.BOLD}   8           8        w               8
.d88 .d88 8d8b 8.dP    w8ww .d8b. .d8b. 8 d88b
8  8 8  8 8P   88b      8   8' .8 8' .8 8 `Yb.
`Y88 `Y88 8    8 Yb     Y8P `Y8P' `Y8P' 8 Y88P
                                               {Colors.END}

{Colors.GREEN}1.{Colors.END} Atualizar Sistema
{Colors.GREEN}2.{Colors.END} Configurar MAC Address Aleatório
{Colors.GREEN}3.{Colors.END} Configurar Logs em RAM (volatile)
{Colors.GREEN}4.{Colors.END} Configurar Tampa para Desligar
{Colors.GREEN}5.{Colors.END} Configurar Firewall (UFW + Bloquear ICMP)
{Colors.GREEN}6.{Colors.END} Configurar Wallpaper de Login
{Colors.GREEN}7.{Colors.END} Instalar Aplicativos Essenciais
{Colors.GREEN}8.{Colors.END} Limpeza Profunda (Cache, Logs, Temp, DNS)
{Colors.GREEN}9.{Colors.END} {Colors.BOLD}Configurar TUDO de uma vez{Colors.END}
{Colors.RED}0.{Colors.END} Sair

{Colors.CYAN}Escolha uma opção:{Colors.END} """
    return input(menu).strip()

def configure_all():
    print(f"\n{Colors.BOLD}{Colors.YELLOW}[*] Configurando todas as opções...{Colors.END}\n")
    configure_random_mac()
    configure_ram_logs()
    configure_lid_switch()
    configure_firewall()

    print(f"\n{Colors.CYAN}[?] Deseja configurar o wallpaper de login também? (s/N):{Colors.END} ", end='')
    if input().strip().lower() == 's':
        configure_login_wallpaper()

    print(f"\n{Colors.GREEN}{Colors.BOLD}[✓] Todas as configurações foram concluídas!{Colors.END}")

def main():
    print_banner()
    check_root()

    while True:
        choice = show_menu()

        if choice == '1':
            system_update()
        elif choice == '2':
            configure_random_mac()
        elif choice == '3':
            configure_ram_logs()
        elif choice == '4':
            configure_lid_switch()
        elif choice == '5':
            configure_firewall()
        elif choice == '6':
            configure_login_wallpaper()
        elif choice == '7':
            applications_menu()
        elif choice == '8':
            deep_clean_system()
        elif choice == '9':
            configure_all()
        elif choice == '0':
            print(f"\n{Colors.CYAN}Saindo... Até logo!{Colors.END}\n")
            sys.exit(0)
        else:
            print(f"\n{Colors.RED}[!] Opção inválida. Tente novamente.{Colors.END}")

        input(f"\n{Colors.YELLOW}Pressione ENTER para continuar...{Colors.END}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}[!] Interrompido pelo usuário{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}[!] Erro inesperado: {e}{Colors.END}")
        sys.exit(1)

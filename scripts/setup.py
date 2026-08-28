#!/usr/bin/env python3
"""
Cross-Platform GSC & GA4 MCP Setup Script
Supports macOS, Windows, and Linux.
Configures mcp-search-console and analytics-mcp for OpenCode / Claude Code / AI Agents.
"""

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

def is_windows():
    return platform.system() == "Windows"

def is_macos():
    return platform.system() == "Darwin"

def get_opencode_config_path(custom_path=None):
    if custom_path:
        p = Path(custom_path).expanduser().resolve()
        return p

    home = Path.home()
    if is_windows():
        candidates = [
            home / ".config" / "opencode" / "opencode.json",
            Path(os.environ.get("APPDATA", str(home / "AppData" / "Roaming"))) / "opencode" / "opencode.json"
        ]
    else:
        candidates = [
            home / ".config" / "opencode" / "opencode.json"
        ]

    for c in candidates:
        if c.exists():
            return c
    return candidates[0]

def find_uv_or_uvx():
    """Find uv and uvx binaries in system PATH and standard install locations."""
    uv_bin = shutil.which("uv")
    uvx_bin = shutil.which("uvx")

    if uv_bin and uvx_bin:
        return uv_bin, uvx_bin

    home = Path.home()
    extra_paths = []
    if is_windows():
        extra_paths = [
            home / ".local" / "bin",
            home / "AppData" / "Local" / "Programs" / "uv",
            Path("C:/Program Files/uv")
        ]
    elif is_macos():
        extra_paths = [
            Path("/opt/homebrew/bin"),
            Path("/usr/local/bin"),
            home / ".local" / "bin",
            home / ".cargo" / "bin"
        ]
    else:
        extra_paths = [
            home / ".local" / "bin",
            Path("/usr/local/bin"),
            Path("/usr/bin"),
            home / ".cargo" / "bin"
        ]

    for p in extra_paths:
        test_uv = p / ("uv.exe" if is_windows() else "uv")
        test_uvx = p / ("uvx.exe" if is_windows() else "uvx")
        if not uv_bin and test_uv.exists():
            uv_bin = str(test_uv)
        if not uvx_bin and test_uvx.exists():
            uvx_bin = str(test_uvx)

    return uv_bin, uvx_bin

def install_uv():
    """Attempt automatic installation of uv on macOS / Windows / Linux."""
    print("📦 uv not found. Installing astral-sh/uv...")
    try:
        if is_windows():
            cmd = 'powershell -ExecutionPolicy ByPass -Command "irm https://astral.sh/uv/install.ps1 | iex"'
            subprocess.run(cmd, shell=True, check=True)
        elif is_macos():
            brew = shutil.which("brew") or "/opt/homebrew/bin/brew"
            if os.path.exists(brew):
                subprocess.run([brew, "install", "uv"], check=True)
            else:
                cmd = "curl -LsSf https://astral.sh/uv/install.sh | sh"
                subprocess.run(cmd, shell=True, check=True)
        else:
            cmd = "curl -LsSf https://astral.sh/uv/install.sh | sh"
            subprocess.run(cmd, shell=True, check=True)
        print("✅ uv installation succeeded.")
    except Exception as e:
        print(f"⚠️ Automatic uv installation failed: {e}")
        print("👉 Please install uv manually: https://docs.astral.sh/uv/getting-started/installation/")

def get_system_path_env():
    """Return a standard PATH string for MCP configuration."""
    if is_windows():
        paths = [
            str(Path.home() / ".local" / "bin"),
            "C:\\Windows\\system32",
            "C:\\Windows",
            "C:\\Windows\\System32\\Wbem",
            "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\"
        ]
        current = os.environ.get("PATH", "")
        return f"{paths[0]};{current}"
    elif is_macos():
        return "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:" + str(Path.home() / ".local" / "bin")
    else:
        return str(Path.home() / ".local" / "bin") + ":/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

def validate_service_account(sa_path):
    p = Path(sa_path).expanduser().resolve()
    if not p.exists():
        raise FileNotFoundError(f"Service Account key file not found: {p}")
    try:
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
        if data.get("type") != "service_account" or "client_email" not in data:
            print("⚠️ Warning: JSON does not appear to be a standard Google Service Account key.")
        else:
            print(f"🔑 Detected Service Account Email: {data.get('client_email')}")
        return str(p), data.get("client_email")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON file: {p}")

def configure_opencode_json(config_path, uvx_path, sa_path=None, remove=False):
    config_path = Path(config_path)
    config_path.parent.mkdir(parents=True, exist_ok=True)

    config_data = {}
    if config_path.exists():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config_data = json.load(f)
        except Exception as e:
            print(f"⚠️ Could not parse existing {config_path}: {e}. Creating new.")
            config_data = {}

    if "mcp" not in config_data:
        config_data["mcp"] = {}

    # Clean legacy duplicate search-console if present
    if "search-console" in config_data["mcp"]:
        print("🧹 Removing deprecated search-console (search-console-mcp)...")
        del config_data["mcp"]["search-console"]

    if remove:
        if "mcp-gsc" in config_data["mcp"]:
            del config_data["mcp"]["mcp-gsc"]
        if "analytics-mcp" in config_data["mcp"]:
            del config_data["mcp"]["analytics-mcp"]
        print("🗑️ Removed mcp-gsc and analytics-mcp from configuration.")
    else:
        path_env = get_system_path_env()

        # 1. Configure GSC (mcp-search-console)
        gsc_env = {"PATH": path_env}
        if sa_path:
            gsc_env["GSC_CREDENTIALS_PATH"] = sa_path
            gsc_env["GSC_SKIP_OAUTH"] = "true"

        config_data["mcp"]["mcp-gsc"] = {
            "command": [uvx_path, "mcp-search-console"],
            "enabled": True,
            "type": "local",
            "environment": gsc_env
        }

        # 2. Configure GA4 (analytics-mcp)
        ga4_env = {"PATH": path_env}
        if sa_path:
            ga4_env["GOOGLE_APPLICATION_CREDENTIALS"] = sa_path

        config_data["mcp"]["analytics-mcp"] = {
            "command": [uvx_path, "analytics-mcp"],
            "enabled": True,
            "type": "local",
            "environment": ga4_env
        }

        mode_str = f"Service Account ({sa_path})" if sa_path else "Personal OAuth 2.0"
        print(f"⚙️ Configured mcp-gsc & analytics-mcp in mode: {mode_str}")

    # Backup existing config before writing
    if config_path.exists():
        backup_path = config_path.with_suffix(".json.bak")
        shutil.copyfile(config_path, backup_path)
        print(f"💾 Backed up previous configuration to {backup_path}")

    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config_data, f, indent=2, ensure_ascii=False)
    print(f"✅ Configuration successfully saved to: {config_path}")

def main():
    parser = argparse.ArgumentParser(description="Install and configure Google Search Console & GA4 MCP servers.")
    parser.add_argument("--service-account", "-s", type=str, help="Path to Google Service Account JSON key file.")
    parser.add_argument("--oauth", "-o", action="store_true", help="Force Personal OAuth 2.0 authentication mode.")
    parser.add_argument("--config", "-c", type=str, help="Custom path to opencode.json config file.")
    parser.add_argument("--uninstall", "-u", action="store_true", help="Remove GSC and GA4 MCP servers from config.")
    parser.add_argument("--non-interactive", "-n", action="store_true", help="Run without interactive prompts.")

    args = parser.parse_args()

    print("=" * 60)
    print(" Google Search Console (GSC) & GA4 MCP Setup")
    print(f" Operating System: {platform.system()} ({platform.machine()})")
    print("=" * 60)

    # 1. Check or install uv / uvx
    uv_bin, uvx_bin = find_uv_or_uvx()
    if not uvx_bin:
        install_uv()
        uv_bin, uvx_bin = find_uv_or_uvx()

    if not uvx_bin:
        print("❌ Error: uvx command is not available. Please install uv first.")
        sys.exit(1)
    else:
        print(f"✅ Found uvx at: {uvx_bin}")

    config_path = get_opencode_config_path(args.config)
    print(f"📁 Target Config File: {config_path}")

    if args.uninstall:
        configure_opencode_json(config_path, uvx_bin, remove=True)
        print("🎉 Uninstallation complete.")
        return

    sa_path = None
    client_email = None

    if args.service_account:
        sa_path, client_email = validate_service_account(args.service_account)
    elif args.oauth:
        sa_path = None
        print("🔐 Selected mode: Personal Account OAuth 2.0")
    elif not args.non-interactive:
        print("\nChoose Authentication Mode:")
        print("1. Service Account (.json key file) [Recommended for background / server use]")
        print("2. Personal Google Account (OAuth 2.0 browser login)")
        choice = input("Enter choice (1/2, default 1): ").strip() or "1"

        if choice == "1":
            raw_path = input("Enter full path to Service Account JSON key: ").strip()
            # remove surrounding quotes if dragged & dropped in terminal
            raw_path = raw_path.strip("'\"")
            if raw_path:
                try:
                    sa_path, client_email = validate_service_account(raw_path)
                except Exception as e:
                    print(f"❌ Error validating key file: {e}")
                    sys.exit(1)
            else:
                print("⚠️ No path entered. Defaulting to OAuth 2.0 mode.")
                sa_path = None
        else:
            sa_path = None
            print("🔐 Selected mode: Personal Account OAuth 2.0")
    else:
        sa_path = None

    configure_opencode_json(config_path, uvx_bin, sa_path=sa_path)

    print("\n" + "=" * 60)
    print(" Next Steps:")
    print("=" * 60)
    if sa_path and client_email:
        print(f"1. GSC: Add Service Account email as User/Owner in Google Search Console:")
        print(f"   👉 {client_email}")
        print(f"2. GA4: Add Service Account email to your GA4 Property (Viewer or Analyst):")
        print(f"   👉 {client_email}")
    else:
        print("1. GSC OAuth: When you run a GSC tool (or call mcp-gsc_reauthenticate), a browser window will open.")
        print("   Follow the Google OAuth prompt to authorize your personal account.")
        print("2. GA4 OAuth: Run the following command in terminal to authorize Google ADC:")
        print("   👉 gcloud auth application-default login")

    print("\n✨ Setup complete! Restart or reload OpenCode to start using GSC & GA4 tools.")

if __name__ == "__main__":
    main()

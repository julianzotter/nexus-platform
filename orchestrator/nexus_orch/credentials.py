"""Read existing local credentials; never migrate or persist secret values."""
from __future__ import annotations
import json
import os
import stat
import subprocess
from pathlib import Path

class CredentialError(RuntimeError):
    pass

def _check_permissions(path: Path) -> None:
    if path.is_symlink() or path.parent.is_symlink():
        raise CredentialError('DSH_STORE_SYMLINK_REJECTED')
    info = path.stat()
    parent = path.parent.stat()
    if not stat.S_ISREG(info.st_mode) or info.st_size > 65536:
        raise CredentialError('DSH_STORE_INVALID_TYPE_OR_SIZE')
    if os.name != 'nt':
        if info.st_uid != os.getuid() or stat.S_IMODE(info.st_mode) & 0o077 or parent.st_uid != os.getuid() or stat.S_IMODE(parent.st_mode) & 0o077:
            raise CredentialError('DSH_STORE_OWNER_OR_MODE_UNSAFE')
        return
    script = r'''$ErrorActionPreference='Stop'; $a=Get-Acl -LiteralPath $env:NEXUS_DSH_ACL_PATH;
$me=[System.Security.Principal.WindowsIdentity]::GetCurrent().User.Value;
$allowed=@($me,'S-1-5-18','S-1-5-32-544'); $ok=$a.GetOwner([System.Security.Principal.SecurityIdentifier]).Value -eq $me;
foreach($r in $a.Access){if($r.AccessControlType -eq 'Allow'){$sid=$r.IdentityReference.Translate([System.Security.Principal.SecurityIdentifier]).Value;if($sid -notin $allowed){$ok=$false}}};
@{secure=$ok}|ConvertTo-Json -Compress'''
    try:
        result = subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',script],
            env={**os.environ,'NEXUS_DSH_ACL_PATH':str(path)},capture_output=True,text=True,timeout=10,check=True)
        if json.loads(result.stdout).get('secure') is not True:
            raise CredentialError('DSH_WINDOWS_ACL_UNSAFE')
    except (OSError,ValueError,subprocess.SubprocessError):
        raise CredentialError('DSH_WINDOWS_ACL_NOT_VERIFIED') from None

def resolve_key(env_name: str, store: str | None = None, path: Path | None = None) -> str:
    key = os.environ.get(env_name)
    if key:
        return key
    if store != 'dsh' or env_name != 'DEEPSEEK_API_KEY':
        raise CredentialError('CREDENTIAL_BINDING_MISSING')
    target = path or Path(os.environ.get('DSH_HOME',str(Path.home()/'.dsh'))) / '.credentials.yaml'
    try:
        _check_permissions(target)
        import yaml
        data = yaml.safe_load(target.read_text(encoding='utf-8'))
    except FileNotFoundError:
        raise CredentialError('DSH_STORE_NOT_AVAILABLE_ON_THIS_HOST') from None
    except (OSError,ImportError):
        raise CredentialError('DSH_STORE_UNREADABLE_OR_SAFE_YAML_UNAVAILABLE') from None
    except CredentialError:
        raise
    except Exception:
        raise CredentialError('DSH_STORE_INVALID_YAML') from None
    key = data.get(env_name) if isinstance(data,dict) else None
    if not isinstance(key,str) or not key.strip() or len(key)>4096 or '\n' in key or '\r' in key:
        raise CredentialError('DSH_RECORD_MISSING_OR_UNSUPPORTED_SCHEMA')
    return key.strip()

"""Windows-only RFEM5 COM ROT attachment probe; never requests model lock."""
import json
import platform


def probe() -> dict[str, object]:
    if platform.system() != "Windows":
        return {"status": "BLOCKED_NOT_WINDOWS"}
    try:
        from comtypes.client import GetActiveObject
    except ImportError:
        return {"status": "BLOCKED_COMTYPES_NOT_INSTALLED"}
    try:
        app = GetActiveObject("RFEM5.Application")
    except Exception as exc:
        return {"status": "BLOCKED_COM_ATTACHMENT", "error_class": type(exc).__name__}
    # COM model data requires validated license lock and adapter version.
    # Stop after attaching to ROT. No LockLicense or mutable model calls.
    return {"status": "COM_APPLICATION_ATTACHED", "model_readback": "NOT_RUN",
            "writes": "NONE", "solver": "NOT_RUN"}


if __name__ == "__main__":
    print(json.dumps(probe(), indent=2))

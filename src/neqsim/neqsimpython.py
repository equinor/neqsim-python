"""
JVM bootstrap for NeqSim.

Importing this module starts the Java Virtual Machine (JVM) used by NeqSim,
unless automatic startup has been disabled via the ``NEQSIM_JVM_AUTOSTART``
environment variable (set it to "0" to disable). When autostart is disabled,
call :func:`init_jvm` explicitly before using ``jneqsim``.
"""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import jpype


class NeqSimJVMError(Exception):
    """Exception raised when JVM initialization fails."""


def _get_jvm_error_message() -> str:
    """Return helpful error message for JVM issues."""
    return (
        "Failed to start Java Virtual Machine (JVM).\n\n"
        "Common solutions:\n"
        "1. Install Java JDK 11+ from https://adoptium.net/\n"
        "2. Ensure JAVA_HOME environment variable is set\n"
        "3. Ensure 64-bit Python matches 64-bit Java (or 32-bit with 32-bit)\n\n"
        "See: https://github.com/equinor/neqsim-python#prerequisites"
    )


def _default_jvm_args() -> List[str]:
    """
    Build the default JVM startup arguments.

    "-Xrs" reduces the JVM's use of OS signals. Without this, the JVM
    installs signal handlers (SIGINT/SIGTERM/SIGSEGV) that can crash
    embedded Python kernels in IDEs such as Spyder 6 and some Jupyter
    setups, producing "The kernel died, restarting..." errors immediately
    on `import neqsim`. "-Xrs" is safe for normal use.

    Extra arguments can be supplied via the ``NEQSIM_JVM_ARGS`` environment
    variable (space separated), and a max heap size via
    ``NEQSIM_JVM_MAX_HEAP`` (e.g. "2g").

    Returns:
        The list of JVM startup argument strings.
    """
    args = ["-Xrs"]
    extra = os.environ.get("NEQSIM_JVM_ARGS", "").strip()
    if extra:
        args.extend(extra.split())
    max_heap = os.environ.get("NEQSIM_JVM_MAX_HEAP", "").strip()
    if max_heap:
        args.append(f"-Xmx{max_heap}")
    return args


def is_jvm_started() -> bool:
    """
    Check whether the Java Virtual Machine has already been started.

    Returns:
        True if the JVM is running, False otherwise.
    """
    return jpype.isJVMStarted()


def init_jvm(jvm_args: Optional[List[str]] = None, interrupt: bool = False) -> None:
    """
    Start the JVM used by NeqSim, if it is not already running.

    Safe to call multiple times: if the JVM is already started this is a
    no-op. Call this explicitly when automatic startup has been disabled via
    ``NEQSIM_JVM_AUTOSTART=0``, e.g. to control JVM startup arguments before
    any NeqSim classes are used.

    Args:
        jvm_args: Optional list of JVM startup arguments. Defaults to
            :func:`_default_jvm_args` when not provided.
        interrupt: Passed to ``jpype.startJVM`` (JPype >= 1.5). When False,
            JPype leaves SIGINT handling to the host process, which avoids
            "kernel died, restarting" errors in some embedded kernels.

    Raises:
        NeqSimJVMError: If the JVM fails to start, or the detected Java
            version is older than 11.
    """
    if jpype.isJVMStarted():
        return

    try:
        args = jvm_args if jvm_args is not None else _default_jvm_args()
        start_kwargs: Dict[str, Any] = {"convertStrings": False}
        try:
            # `interrupt` kwarg was added in JPype 1.5.0. Guard with a
            # fallback for older versions just in case.
            jpype.startJVM(*args, interrupt=interrupt, **start_kwargs)
        except TypeError:
            jpype.startJVM(*args, **start_kwargs)
    except Exception as e:
        raise NeqSimJVMError(_get_jvm_error_message()) from e

    jvm_version = jpype.getJVMVersion()[0]
    if jvm_version < 11:
        raise NeqSimJVMError(
            "Detected Java version below 11. Please upgrade to Java version "
            "11 or higher.\n"
            "See: https://github.com/equinor/neqsim-python#prerequisites"
        )

    module_dir = Path(__file__).resolve().parent
    jpype.addClassPath(str(module_dir / "lib" / "java11" / "*"))


def _autostart_enabled() -> bool:
    """
    Check whether automatic JVM startup on import is enabled.

    Returns:
        True unless ``NEQSIM_JVM_AUTOSTART`` is set to "0", "false", or "no".
    """
    return os.environ.get("NEQSIM_JVM_AUTOSTART", "1").strip().lower() not in (
        "0",
        "false",
        "no",
    )


if _autostart_enabled():
    init_jvm()

jneqsim = jpype.JPackage("neqsim")

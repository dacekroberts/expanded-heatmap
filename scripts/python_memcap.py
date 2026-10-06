"""Cap the memory of every Python process this user runs on this machine.

On 2026-09-28 a scratch PDF decoder grew one python.exe to 47 GB on a 16 GB
machine (commit limit 29 GB). Windows ran out of commit and closed the Claude
app, twice (DECISIONS, 2026-09-28). Installed as `usercustomize.py` in the
user site-packages, this file puts each Python process into a Windows job
object at start-up: no process may commit more than PROCESS_GB, and no
process with all the children it starts more than TREE_GB. A runaway script
then gets a MemoryError of its own, and the machine keeps running.

The numbers are the owner's. Never raise them to get past a MemoryError: a
step that needs more is a step to fix. HEATMAP_MEMCAP_TEST_GB can only LOWER
the cap, for the self-test.

    python scripts/python_memcap.py --install    # copy to this Python's user site
    python scripts/python_memcap.py --check      # installed copy current, cap live
    python scripts/python_memcap.py --selftest   # a child over a test cap fails

`--install` covers only the Python that runs it; run it with each Python the
sessions use. A virtualenv (`.venv-lean`) skips the user site and is not
covered.
"""
import os
import sys

PROCESS_GB = 8
# 12 until 2026-10-05; 16 since the machine went from 16 GB to 32 GB (owner),
# so drift_check.py can run three cities at once: the Japan sweep's heaviest
# city measured 4.74 GB, so three like it would need about 14 GB (Tokyo, Osaka
# and Kobe together measured 0.72 GB, 2026-10-05). The per-process cap stays 8:
# no step has needed more than 5.4 GB (Oslo's step 2, now 2.38 GB).
TREE_GB = 16
_GB = 1 << 30
_JOB = None  # the job handle, held for the life of the process


def _limits():
    per, tree = PROCESS_GB, TREE_GB
    test = os.environ.get("HEATMAP_MEMCAP_TEST_GB")
    if test:
        try:
            value = float(test)
        except ValueError:
            value = 0
        if 0 < value < per:  # lower only
            per, tree = value, min(tree, value)
    return int(per * _GB), int(tree * _GB)


def _api():
    import ctypes
    from ctypes import wintypes

    class Basic(ctypes.Structure):
        _fields_ = [("PerProcessUserTimeLimit", ctypes.c_int64),
                    ("PerJobUserTimeLimit", ctypes.c_int64),
                    ("LimitFlags", wintypes.DWORD),
                    ("MinimumWorkingSetSize", ctypes.c_size_t),
                    ("MaximumWorkingSetSize", ctypes.c_size_t),
                    ("ActiveProcessLimit", wintypes.DWORD),
                    ("Affinity", ctypes.c_size_t),
                    ("PriorityClass", wintypes.DWORD),
                    ("SchedulingClass", wintypes.DWORD)]

    class Io(ctypes.Structure):
        _fields_ = [(name, ctypes.c_uint64) for name in (
            "ReadOperationCount", "WriteOperationCount", "OtherOperationCount",
            "ReadTransferCount", "WriteTransferCount", "OtherTransferCount")]

    class Extended(ctypes.Structure):
        _fields_ = [("BasicLimitInformation", Basic),
                    ("IoInfo", Io),
                    ("ProcessMemoryLimit", ctypes.c_size_t),
                    ("JobMemoryLimit", ctypes.c_size_t),
                    ("PeakProcessMemoryUsed", ctypes.c_size_t),
                    ("PeakJobMemoryUsed", ctypes.c_size_t)]

    k32 = ctypes.WinDLL("kernel32", use_last_error=True)
    k32.CreateJobObjectW.restype = wintypes.HANDLE
    k32.CreateJobObjectW.argtypes = [ctypes.c_void_p, ctypes.c_wchar_p]
    k32.GetCurrentProcess.restype = wintypes.HANDLE
    k32.SetInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int,
                                            ctypes.c_void_p, wintypes.DWORD]
    k32.QueryInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int,
                                              ctypes.c_void_p, wintypes.DWORD,
                                              ctypes.c_void_p]
    k32.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
    return ctypes, k32, Extended


EXTENDED_LIMITS = 9           # JobObjectExtendedLimitInformation
LIMIT_PROCESS_MEMORY = 0x100  # JOB_OBJECT_LIMIT_PROCESS_MEMORY
LIMIT_JOB_MEMORY = 0x200      # JOB_OBJECT_LIMIT_JOB_MEMORY


def apply():
    """Put this process in a capped job. Never raises: start-up must not break."""
    global _JOB
    if sys.platform != "win32":
        return False
    try:
        ctypes, k32, Extended = _api()
        info = Extended()
        info.BasicLimitInformation.LimitFlags = LIMIT_PROCESS_MEMORY | LIMIT_JOB_MEMORY
        info.ProcessMemoryLimit, info.JobMemoryLimit = _limits()
        job = k32.CreateJobObjectW(None, None)
        if not job:
            return False
        if not k32.SetInformationJobObject(job, EXTENDED_LIMITS, ctypes.byref(info),
                                           ctypes.sizeof(info)):
            return False
        if not k32.AssignProcessToJobObject(job, k32.GetCurrentProcess()):
            return False
        _JOB = job  # no KILL_ON_JOB_CLOSE: children outlive this process as before
        return True
    except Exception:
        return False


def current():
    """(process limit, tree limit) of the job this process is in, in bytes."""
    ctypes, k32, Extended = _api()
    info = Extended()
    if not k32.QueryInformationJobObject(None, EXTENDED_LIMITS, ctypes.byref(info),
                                         ctypes.sizeof(info), None):
        return None
    flags = info.BasicLimitInformation.LimitFlags
    return (info.ProcessMemoryLimit if flags & LIMIT_PROCESS_MEMORY else 0,
            info.JobMemoryLimit if flags & LIMIT_JOB_MEMORY else 0)


if __name__ == "usercustomize":
    apply()


def _installed_path():
    import site
    return os.path.join(site.getusersitepackages(), "usercustomize.py")


def _child(code, env_extra=None):
    import subprocess
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    env.pop("HEATMAP_MEMCAP_TEST_GB", None)
    env.update(env_extra or {})
    run = subprocess.run([sys.executable, "-c", code], capture_output=True,
                         text=True, env=env, timeout=120)
    return run.returncode, (run.stdout + run.stderr).strip()


REPORT = ("import usercustomize as u; r = u.current() or (0, 0); "
          "print('limits', format(r[0] / 2**30, 'g'), format(r[1] / 2**30, 'g'))")


def main():
    import site
    mode = sys.argv[1] if len(sys.argv) > 1 else "--check"
    here = os.path.abspath(__file__)
    target = _installed_path()
    if sys.platform != "win32":
        print("OK - not Windows; the cap is a Windows job object and does not apply")
        return 0
    if mode == "--install":
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(here, "rb") as src, open(target, "wb") as dst:
            dst.write(src.read())
        print(f"installed {target}")
        mode = "--check"
    if mode == "--check":
        if not site.ENABLE_USER_SITE:
            print(f"FAIL - {sys.executable} has the user site turned off; the cap cannot load")
            return 1
        if not os.path.exists(target):
            print(f"FAIL - no {target}; run: python scripts/python_memcap.py --install")
            return 1
        with open(here, "rb") as a, open(target, "rb") as b:
            if a.read() != b.read():
                print(f"FAIL - {target} differs from scripts/python_memcap.py; re-run --install")
                return 1
        code, out = _child(REPORT)
        want = f"limits {PROCESS_GB:g} {TREE_GB:g}"
        if code != 0 or out != want:
            print(f"FAIL - a fresh Python reports '{out}', expected '{want}'")
            return 1
        print(f"OK - every new {os.path.basename(sys.executable)} {sys.version.split()[0]} "
              f"is capped at {PROCESS_GB} GB a process, {TREE_GB} GB with its children")
        return 0
    if mode == "--selftest":
        cases = [
            # (what, env, code, expected text in output, expected exit is zero)
            ("cap live at the owner's numbers", None, REPORT,
             f"limits {PROCESS_GB:g} {TREE_GB:g}", True),
            ("a test cap lowers it", {"HEATMAP_MEMCAP_TEST_GB": "0.5"}, REPORT,
             "limits 0.5 0.5", True),
            ("a test cap cannot raise it", {"HEATMAP_MEMCAP_TEST_GB": "64"}, REPORT,
             f"limits {PROCESS_GB:g} {TREE_GB:g}", True),
            ("under the cap allocates", {"HEATMAP_MEMCAP_TEST_GB": "0.5"},
             "b = bytearray(100 * 2**20); print('allocated', len(b) >> 20, 'MB')",
             "allocated 100 MB", True),
            ("over the cap is a MemoryError", {"HEATMAP_MEMCAP_TEST_GB": "0.5"},
             "b = bytearray(2**30); print('allocated')", "MemoryError", False),
        ]
        bad = 0
        for what, env, code, expect, zero in cases:
            rc, out = _child(code, env)
            ok = expect in out and (rc == 0) == zero
            bad += not ok
            print(f"{'ok  ' if ok else 'FAIL'} {what}: exit {rc}, {out.splitlines()[-1] if out else ''}")
        print(f"{len(cases) - bad} of {len(cases)} cases behaved as intended.")
        return 1 if bad else 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())

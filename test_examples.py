"""Test all example scripts and report results."""
import subprocess
import sys
import os

examples_dir = 'examples'
skip = ['testspark.py', 'processBuilderGUI.py', 'asterix.py', 'processBuilderConfig.py', 'process_api.py']
py_files = sorted([f for f in os.listdir(examples_dir) if f.endswith('.py') and f not in skip])

results = {}
for f in py_files:
    path = os.path.join(examples_dir, f)
    try:
        r = subprocess.run([sys.executable, path], capture_output=True, text=True, timeout=60, encoding='utf-8', errors='replace')
        if r.returncode == 0:
            results[f] = 'OK'
        else:
            err = r.stderr.strip().split('\n')[-1][:200]
            results[f] = 'FAIL: ' + err
    except subprocess.TimeoutExpired:
        results[f] = 'TIMEOUT'
    except Exception as e:
        results[f] = f'ERROR: {e}'

print('=== RESULTS ===')
ok = 0
fail = 0
timeout = 0
for f, status in results.items():
    print(f'{f}: {status}')
    if status == 'OK':
        ok += 1
    elif status == 'TIMEOUT':
        timeout += 1
    else:
        fail += 1

print(f'\nTotal: {len(results)}, OK: {ok}, FAIL: {fail}, TIMEOUT: {timeout}')

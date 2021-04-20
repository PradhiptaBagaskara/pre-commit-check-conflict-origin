
import argparse
import os.path
import subprocess
import re

from typing import Sequence
from typing import Any
from typing import List
from typing import Optional
from typing import Set


class CalledProcessError(RuntimeError):
    pass


def added_files() -> Set[str]:
    cmd = ('git', 'diff', '--staged', '--name-only', '--diff-filter=A')
    return set(cmd_output(*cmd).splitlines())


def cmd_output(*cmd: str, retcode: Optional[int] = 0, **kwargs: Any) -> str:
    kwargs.setdefault('stdout', subprocess.PIPE)
    kwargs.setdefault('stderr', subprocess.PIPE)
    proc = subprocess.Popen(cmd, **kwargs)
    stdout, stderr = proc.communicate()
    stdout = stdout.decode()
    if retcode is not None and proc.returncode != retcode:
        raise CalledProcessError(cmd, retcode, proc.returncode, stdout, stderr)
    return stdout


def zsplit(s: str) -> List[str]:
    s = s.strip('\0')
    if s:
        return s.split('\0')
    else:
        return []

def pre_check(target_branch):
    cmd = ['git', 'fetch', 'origin', target_branch]
    stdout = cmd_output(*cmd, retcode=None, **kwargs)

def check_origin():
    cmd = ['git', 'config', '--get', 'remote.origin.url']
    try:
        stdout = cmd_output(*cmd, retcode=0)
        return True
    except CalledProcessError as e:
        print("origin not set yet.")
        return
    
def current_branch():
    cmd = ['git', 'rev-parse', '--abbrev-ref', 'HEAD']
    branch = re.sub(r"[^a-zA-z0-9]+", "", cmd_output(*cmd, env={"GIT_DIR": ".git"}))
    return branch
            
        
    
    
current_repo = "git rev-parse --abbrev-ref HEAD"
def main(argv: str) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--target_branch', action='store_true')
    args = parser.parse_args(argv)
    print(args)
    if not check_origin():
        return 0

if __name__ == '__main__':
    main('--target_branch=dev')
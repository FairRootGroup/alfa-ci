import logging
from asyncio import run
from asyncio.subprocess import create_subprocess_exec, PIPE, STDOUT

from alfaci import Error

log = logging.getLogger(__name__)


class CalledProcessError(Error):
    def __init__(self, cmd, pid, rc):
        super().__init__(
            "Executed '%s' with PID %s with non-zero return code: %s" %
            (cmd, pid, rc))


async def _call(program, *args, logger=log):
    args = list(map(str, args))
    cmd = ' '.join([program] + args)
    proc = await create_subprocess_exec(program,
                                        *args,
                                        stdout=PIPE,
                                        stderr=STDOUT)
    pid = proc.pid
    logger.debug("[%s] Executing '%s':", pid, cmd)

    while not proc.stdout.at_eof():
        line = await proc.stdout.readline()
        if line != b'':
            logger.debug('[%s] %s', pid, line.decode().rstrip())

    rc = await proc.wait()
    logger.debug('[%s] Process exited with code: %s', pid, rc)
    return (cmd, pid, rc)


def call(program, *args, logger=log):
    """Helper to call external CLIs"""
    cmd, pid, rc = run(_call(program, *args, logger=logger))
    if rc != 0:
        raise CalledProcessError(cmd, pid, rc)

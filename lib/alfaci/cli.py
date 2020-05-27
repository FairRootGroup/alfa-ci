# PYTHON_ARGCOMPLETE_OK
"""Command line interface 'alfa-ci'"""

import argparse
from subprocess import check_call
import sys
from pathlib import Path
import shutil
import argcomplete

from alfaci.version import PKG_VERSION
from alfaci.repo import init_repo, Repo


class ArgumentParser(argparse.ArgumentParser):
    """Specialized arg parser with custom error handling"""
    def error(self, message):
        self.print_help(sys.stderr)
        self.exit(2, '%s: error: %s\n' % (self.prog, message))


def do_shell_setup(_args):
    """Print the argcomplete bash hook to be eval'ed by the user"""
    for reg in ('register-python-argcomplete3',
                'register-python-argcomplete'):  # pragma: no cover
        if shutil.which(reg) is not None:
            break
    check_call([reg, 'alfa-ci'])


def do_version(_args):
    """Print the package version defined in the setup.py metadata"""
    print(PKG_VERSION)


def do_init(_args):
    """Initialize the current working directory as environment repo"""
    repo = init_repo(Path.cwd())
    print('Initialized empty alfa-ci repository in %s' % repo.location)


def do_list(_args):
    """Print the list of installed environments"""
    repo = Repo(Path.cwd())
    for env in repo.envs:
        print(env)


def do_install(_args):
    """Install environments"""
    repo = Repo(Path.cwd())
    for env in repo.envs:
        env.install()


def main():
    """Main entry function called from the CLI"""
    parser = ArgumentParser(description='Manage alfa-ci environments.')
    subparsers = parser.add_subparsers(title='COMMANDS')

    shell_setup_parser = subparsers.add_parser(
        'shell-setup',
        add_help=False,
        help='run \'eval "$(alfa-ci shell-setup)"\' to enable shell completion'
        ', e.g. from your ~/.bashrc')
    shell_setup_parser.set_defaults(func=do_shell_setup)

    version_parser = subparsers.add_parser('version',
                                           add_help=False,
                                           help='show version number and exit')
    version_parser.set_defaults(func=do_version)

    init_parser = subparsers.add_parser('init',
                                        add_help=False,
                                        help='initialize environment repo')
    init_parser.set_defaults(func=do_init)

    list_parser = subparsers.add_parser('list',
                                        add_help=False,
                                        help='list environments')
    list_parser.set_defaults(func=do_list)

    install_parser = subparsers.add_parser('install',
                                           add_help=False,
                                           help='install environments')
    install_parser.set_defaults(func=do_install)

    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
        sys.exit(0)
    else:
        parser.print_help()
        sys.exit(2)


if __name__ == '__main__':
    main()

import logging
from textwrap import indent

log = logging.getLogger(__name__)

_COMMON_PKGS = [
    'autoconf', 'automake', 'bison', 'binutils', 'bzip2', 'ca-certificates',
    'cmake', 'cmake-data', 'curl', 'elfutils', 'flex', 'hostname', 'git',
    'gzip', 'libtool', 'make', 'patch', 'sed', 'subversion', 'tar', 'unzip',
    'wget'
]

_COMMON_PKGS_RPM = [
    'gcc', 'gcc-c++', 'gcc-gfortran', 'glibc-devel', 'python2-devel',
    'pkgconf', 'procps', 'which', 'xz'
]

_COMMON_PKGS_DEB = [
    'build-essential', 'debianutils', 'g++', 'gcc', 'gfortran', 'libc6-dev',
    'lsb-release', 'python-dev', 'xz-utils'
]

_INSTALL_YUM = """\
yum -y update
yum -y install {packages}
yum -y clean all
"""

_INSTALL_APT = """\
apt-get update
apt-get -y upgrade
apt-get -y install {packages}
apt-get -y clean
"""

_INSTALL_DNF = """\
dnf -y update
dnf -y install {packages}
dnf -y clean all
"""

_INSTALL_ZYPPER = """\
zypper refresh
zypper update -y
zypper install -y --no-recommends {packages}
zypper clean
"""

CONTAINER_DATA = {
    'centos7': {
        'from': 'centos:7',
        'packages': _COMMON_PKGS + _COMMON_PKGS_RPM + ['redhat-lsb-core'],
        'install': _INSTALL_YUM
    },
    'debian10': {
        'from': 'debian:10',
        'packages': _COMMON_PKGS + _COMMON_PKGS_DEB,
        'install': _INSTALL_APT
    },
    'fedora31': {
        'from': 'fedora:31',
        'packages': _COMMON_PKGS + _COMMON_PKGS_RPM + ['redhat-lsb-core'],
        'install': _INSTALL_DNF
    },
    'opensuse15.2': {
        'from': 'opensuse/leap:15.2',
        'packages': _COMMON_PKGS + _COMMON_PKGS_RPM + ['lsb-release'],
        'install': _INSTALL_ZYPPER
    },
    'ubuntu18.04': {
        'from': 'ubuntu:18.04',
        'packages': _COMMON_PKGS + _COMMON_PKGS_DEB,
        'install': _INSTALL_APT
    }
}

CONTAINER_DEF = """\
Bootstrap: docker
From: {from}

%post
{install}
"""


def get_singularity_definition(name):
    """Generate a singularity container definition"""
    data = CONTAINER_DATA[name]
    data['packages'] = ' '.join(data['packages'])
    data['install'] = indent(data['install'].format(**data), '    ').rstrip()
    sdef = CONTAINER_DEF.format(**data)
    log.debug(">>> Generated singularity definition for '%s':\n%s\n<<<", name,
              sdef.rstrip())
    return sdef

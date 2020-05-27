"""repo module"""

from pathlib import Path
import sys
import yaml

from alfaci.envs.fairroot import FairRootEnv


class Error(Exception):
    """Basic repo error"""


class NotInitializedError(Error):
    """Repo is not initialized"""
    def __init__(self):
        super().__init__('Repo is not initialized')


class AlreadyExistsError(Error):
    """Repo already exists"""
    def __init__(self, location):
        super().__init__('Repository already exists in %s' % location)


class Repo:
    """A repo contains a sub-directory .alfa-ci in the given location storing
       all environments and metadata. Additionally, a repo provides a
       convenient filesystem representation for the user,
       the so-called working tree, in the given location."""

    repo_dir = '.alfa-ci'
    config_file = 'config.yaml'

    def __init__(self, path):
        self._location = path / Repo.repo_dir

        if not (self.location.exists() or
                (self.location / Repo.config_file).exists()):
            raise NotInitializedError()

        with (self.location / Repo.config_file).open() as file:
            yaml.safe_load(file)

        if sys.platform.startswith('linux'):  # pragma: no cover
            self._envs = [
                FairRootEnv(self, 'debian10'),
                FairRootEnv(self, 'fedora31')
            ]
        else:  # pragma: no cover
            self._envs = []

    @property
    def location(self):
        """getter"""
        return self._location

    @property
    def envs(self):
        """getter"""
        return self._envs


def init_repo(path):
    """Initializes an empty repo in the given path and
       returns a Repo object for it"""

    if not isinstance(path, Path):
        path = Path(path)

    try:
        repo = Repo(path)
        raise AlreadyExistsError(repo.location)
    except NotInitializedError:
        (path / Repo.repo_dir).mkdir(parents=False, exist_ok=False)
        (path / Repo.repo_dir / Repo.config_file).touch(exist_ok=False)

    return Repo(path)

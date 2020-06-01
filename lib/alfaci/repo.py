from pathlib import Path
import logging
import yaml

from alfaci import Error
from alfaci.envs.fairroot import get_envs as fairroot_envs
from alfaci.subprocess import call

log = logging.getLogger(__name__)


class NotInitializedError(Error):
    def __init__(self):
        super().__init__('Repo is not initialized')


class AlreadyExistsError(Error):
    def __init__(self, location):
        super().__init__('Repository already exists in %s' % location)


class Repo:
    """A repo contains a sub-directory .alfa-ci in the given location storing
       all environments and metadata. Additionally, a repo provides a
       convenient filesystem representation for the user,
       the so-called working tree, in the given location."""

    repo_dir = '.alfa-ci'
    config_file = 'config.yaml'
    fairsoft_dir = 'fairsoft'

    def __init__(self, path):
        self._envs = None
        self._location = path / Repo.repo_dir

        if not (self.location.exists() or
                (self.location / Repo.config_file).exists()):
            raise NotInitializedError()

        with (self.location / Repo.config_file).open() as file:
            yaml.safe_load(file)

    @property
    def location(self):
        return self._location

    @property
    def envs(self):
        if self._envs is None:
            self._envs = fairroot_envs(self)
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
        call('git',
             *[
                 'clone', '-b', 'dev',
                 'https://github.com/FairRootGroup/FairSoft',
                 (path / Repo.repo_dir / Repo.fairsoft_dir)
             ],
             logger=log)

    return Repo(path)

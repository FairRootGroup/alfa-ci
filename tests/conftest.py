"""shared fixtures for tests module"""
# pylint: disable=redefined-outer-name, unused-argument

import pytest
import alfaci.cli
from alfaci.repo import Repo
from alfaci.env import Env
from alfaci.envs.fairroot import FairRootEnv


class CliMockEnv:
    """Mock-up for alfaci.env"""
    def install(self):
        """install"""

    @property
    def definition(self):
        """prop"""
        return ''


class CliMockRepo:
    """Mock-up for alfaci.repo.Repo"""
    def __init__(self, path):
        self._location = path / '.alfa-ci'
        self._envs = [CliMockEnv(), CliMockEnv()]

    @property
    def location(self):
        """prop"""
        return self._location

    @property
    def envs(self):
        """prop"""
        return self._envs


@pytest.fixture
def mock_subprocess_call(monkeypatch):
    monkeypatch.setattr(
        alfaci.repo, "call", lambda *_args, **_kwargs:
        ('<mocked git clone>', 42, 0))


@pytest.fixture
def mock_init_repo(monkeypatch, mock_subprocess_call):
    """alfaci.repo.init_repo() mocked to return MockRepo"""
    monkeypatch.setattr(alfaci.cli, "init_repo", CliMockRepo)


@pytest.fixture
def mock_repo(monkeypatch):
    """alfaci.repo.Repo mocked by MockRepo"""
    monkeypatch.setattr(alfaci.cli, "Repo", CliMockRepo)


@pytest.fixture
def mock_cwd(tmp_path, monkeypatch):
    """cwd mocked to tmp dir"""
    monkeypatch.chdir(tmp_path)
    return tmp_path


@pytest.fixture
def empty_initialized_repo(tmp_path, mock_subprocess_call):
    """Create empty repo"""
    (tmp_path / Repo.repo_dir).mkdir(parents=False, exist_ok=False)
    (tmp_path / Repo.repo_dir / Repo.config_file).touch(exist_ok=False)
    return tmp_path


@pytest.fixture
def mock_env(empty_initialized_repo):
    """Create mocked env"""
    return Env(empty_initialized_repo)


@pytest.fixture
def mock_fairroot_env(empty_initialized_repo):
    """Create mocked fairroot env"""
    return FairRootEnv(empty_initialized_repo, 'fedora31')

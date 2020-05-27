"""alfaci.repo test module"""

import sys
import pytest
from alfaci.repo import init_repo, Repo, Error


def test_load(empty_initialized_repo):
    """Test loading empty initialized repo"""
    Repo(empty_initialized_repo)


def test_load_unitialized(tmp_path):
    """Test loading unitialized repo"""
    with pytest.raises(Error):
        Repo(tmp_path)


def test_init_repo(tmp_path):
    """Test initalizing empty folder"""
    init_repo(tmp_path)


def test_init_repo_existing(empty_initialized_repo):
    """Test initializing existing repo"""
    with pytest.raises(Error):
        init_repo(empty_initialized_repo)


def test_location(empty_initialized_repo):
    """Test location getter"""
    assert Repo(empty_initialized_repo).location == (empty_initialized_repo /
                                                     Repo.repo_dir)


def test_envs(empty_initialized_repo):
    """Test environments getter"""
    if sys.platform.startswith('linux'):
        assert len(Repo(empty_initialized_repo).envs) == 2
    else:
        assert Repo(empty_initialized_repo).envs == []

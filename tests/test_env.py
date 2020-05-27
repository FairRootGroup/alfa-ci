"""alfaci.env test module"""


def test_env(mock_env):
    """Check the default implementation"""
    assert not mock_env.installed
    assert mock_env.repo


def test_fairroot_env(mock_fairroot_env):
    """Test FairRootEnv"""
    assert mock_fairroot_env.name == 'foo'

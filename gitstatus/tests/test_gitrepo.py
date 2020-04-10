import textwrap
from unittest import mock

import pytest

from gitstatus.git.repo import GitRepo


###############################################################################
# FIXTURES ####################################################################
###############################################################################
@pytest.fixture
def gitrepo_instance():
    with mock.patch("gitstatus.git.os.path.exists") as mock_exists, \
         mock.patch("gitstatus.git.os.path.isdir") as mock_isdir, \
         mock.patch("gitstatus.git.os.path.isfile") as mock_isfile:
        g = GitRepo("fake_path", mock.Mock())
    return g

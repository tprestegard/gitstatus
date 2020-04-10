import textwrap
from unittest import mock

import pytest

from gitstatus.git.config import GitConfig, _parse_gitconfig


###############################################################################
# FIXTURES ####################################################################
###############################################################################
@pytest.fixture
def config():
    return textwrap.dedent("""
        [core]
                repositoryformatversion = 0
                filemode = true
                bare = false
                logallrefupdates = true
        [remote "origin"]
                url = git@github.com:me/repo.git
                fetch = +refs/heads/*:refs/remotes/origin/*
        [branch "master"]
                remote = origin
                merge = refs/heads/master
        [user]
                email = user@email.com
                signingkey = 41391Q731V9VS020
        [remote "upstream"]
                url = git@github.com:upstream/repo.git
                fetch = +refs/heads/*:refs/remotes/upstream/*
        [branch "docker"]
                remote = origin
                merge = refs/heads/docker
        [branch "localdev"]
                remote = origin
                merge = refs/heads/localdev
        [branch "python3"]
                remote = origin
                merge = refs/heads/python3
    """).strip()


###############################################################################
# TESTS #######################################################################
###############################################################################
def test_remove_config_comments(gitrepo_instance):
    # Setup
    str_with_comments = textwrap.dedent("""
        ; ok test
        [core]
            key = val ; test
            key2 = val;test
        [other]
            key1 = val2
            ; test2
        [third]
        ; yup
            ok = yeah
            zz = yepyep   ;    ok  what
    """).strip()
    str_without_comments = textwrap.dedent("""
        [core]
            key = val
            key2 = val
        [other]
            key1 = val2
        [third]
            ok = yeah
            zz = yepyep
    """).strip()

    # Run
    gc = GitConfig("fake_path")
    gc._str = str_with_comments

    # Check
    assert gc._remove_comments() == str_without_comments
    

def test_parse_gitconfig(config):
    out = _parse_gitconfig(config)
    import ipdb; ipdb.set_trace()
    x = 1

from __future__ import (absolute_import, division, print_function)

import pytest


@pytest.fixture
def always_true():
    return True


def test_dummy():
    assert always_true

"""
Tests of printing functionality
"""
import logging
import sys
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from unittest.mock import patch

import pytest

import aesara
from aesara.link.c.cmodule import default_blas_ldflags
from aesara.printing import (
    PatternPrinter,
    PPrinter,
    debugprint,
    default_printer,
    get_node_by_id,
    min_informative_str,
    pp,
    pydot_imported,
    pydotprint,
)
from aesara.tensor.type import dmatrix, dvector, matrix
from tests.graph.utils import MyInnerGraphOp, MyOp, MyVariable


def mocked_blas_opt(*args, **kwargs):
    print("This line will be re-printed to stdout", file=sys.stdout)
    print("This line will be re-printed to stderr", file=sys.stderr)
    print(
        "Could not locate executable g77: this line will be caught and filtered",
        file=sys.stdout,
    )
    print(
        "Could not locate executable g77: this line will be caught and filtered",
        file=sys.stderr,
    )
    print(
        "Could not locate executable foo: this line will be re-printed to stdout",
        file=sys.stdout,
    )
    print(
        "Could not locate executable foo: this line will be re-printed to stderr",
        file=sys.stderr,
    )
    return {
        "libraries": [],
        "library_dirs": [],
        "define_macros": [],
        "include_dirs": [],
    }


@patch("numpy.distutils.system_info.get_info", new=mocked_blas_opt)
def test_blas_opt_warnings():
    sio_out = StringIO()
    sio_err = StringIO()
    with redirect_stdout(sio_out):
        with redirect_stderr(sio_err):
            default_blas_ldflags()
    stdout_lines = sio_out.getvalue().splitlines()
    stderr_lines = sio_err.getvalue().splitlines()
    assert stdout_lines == [
        "This line will be re-printed to stdout",
        "Could not locate executable foo: this line will be re-printed to stdout",
    ]
    assert stderr_lines == [
        "This line will be re-printed to stderr",
        "Could not locate executable foo: this line will be re-printed to stderr",
    ]

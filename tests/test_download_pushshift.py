
import pytest
from download_pushshift import *


def test_get_months_list():
    output = get_months_list("2021-01", "2021-05")
    expected_output = ["2021-01", "2021-02", "2021-03", "2021-04", "2021-05"]
    assert output == expected_output
    output = get_months_list("2022-10", "2023-01")
    expected_output = ["2022-10", "2022-11", "2022-12", "2023-01"]
    assert output == expected_output

    with pytest.raises(AssertionError):
        get_months_list("2021-02", "2020-01")

    with pytest.raises(AssertionError):
        get_months_list("2021-02", "2021-02")

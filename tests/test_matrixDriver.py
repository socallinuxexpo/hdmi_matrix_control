# pylint: disable=invalid-name, no-self-use, missing-docstring, too-few-public-methods

import hdmi_matrix_controller.hw


class TestMatrixDriver:
    def test_assign(self):
        driver = hdmi_matrix_controller.hw.MatrixDriver()
        driver.assign(0, 0)
        assert driver.pending == [(0, 0)]

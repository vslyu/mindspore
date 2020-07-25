# Copyright 2019 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================

import numpy as np
import pytest

import mindspore.context as context
import mindspore.nn as nn
from mindspore import Tensor
from mindspore.ops import operations as P
from mindspore.ops import composite as C

context.set_context(mode=context.GRAPH_MODE, device_target='GPU')


class StridedSliceNet(nn.Cell):
    def __init__(self, begin, end, stride, begin_mask=0, end_mask=0, ellipsis_mask=0):
        super(StridedSliceNet, self).__init__()
        self.begin = begin
        self.end = end
        self.strides = stride
        self.slice = P.StridedSlice(begin_mask, end_mask, ellipsis_mask)

    def construct(self, x):
        return self.slice(x, self.begin, self.end, self.strides)

class GradData(nn.Cell):
    def __init__(self, network):
        super(GradData, self).__init__()
        self.grad = C.GradOperation(name="get_all", get_all=True, sens_param=False)
        self.network = network

    def construct(self, x):
        return self.grad(self.network)(x)

@pytest.mark.level0
@pytest.mark.platform_x86_gpu_training
@pytest.mark.env_onecard
def test_strided_slice_grad():
    x = Tensor(np.arange(0, 2*3*4*5).reshape(2, 3, 4, 5).astype(np.float32))
    net = StridedSliceNet((1, 0, 0, 2), (2, 2, 2, 4), (1, 1, 1, 1))
    dx = GradData(net)(x)
    expect = np.array([[[[0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.]],

                        [[0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.]],

                        [[0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.]]],


                       [[[0., 0., 1., 1., 0.],
                         [0., 0., 1., 1., 0.],
                         [0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.]],

                        [[0., 0., 1., 1., 0.],
                         [0., 0., 1., 1., 0.],
                         [0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.]],

                        [[0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.]]]])
    assert np.allclose(dx[0].asnumpy(), expect)

    net = StridedSliceNet((1, 0, 0, 5), (2, 2, 2, 1), (1, 1, 1, -2))
    dx = GradData(net)(x)
    expect = np.array([[[[0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.]],

                        [[0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.]],

                        [[0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.]]],


                       [[[0., 0., 1., 0., 1.],
                         [0., 0., 1., 0., 1.],
                         [0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.]],

                        [[0., 0., 1., 0., 1.],
                         [0., 0., 1., 0., 1.],
                         [0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.]],

                        [[0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.]]]])
    assert np.allclose(dx[0].asnumpy(), expect)


    net = StridedSliceNet((1, 0, 0, -1), (2, 2, 2, 1), (1, 1, 1, -1))
    dx = GradData(net)(x)
    expect = np.array([[[[0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.]],

                        [[0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.]],

                        [[0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.]]],


                       [[[0., 0., 1., 1., 1.],
                         [0., 0., 1., 1., 1.],
                         [0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.]],

                        [[0., 0., 1., 1., 1.],
                         [0., 0., 1., 1., 1.],
                         [0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.]],

                        [[0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.]]]])
    assert np.allclose(dx[0].asnumpy(), expect)

    # ME infer fault
    # y = GradData()(x, (1, 0, -1, -2), (2, 2, 0, -5), (1, 1, -1, -2))
    # expect = np.array([[[[0., 0., 0., 0., 0.],
    #                      [0., 0., 0., 0., 0.],
    #                      [0., 0., 0., 0., 0.],
    #                      [0., 0., 0., 0., 0.]],

    #                     [[0., 0., 0., 0., 0.],
    #                      [0., 0., 0., 0., 0.],
    #                      [0., 0., 0., 0., 0.],
    #                      [0., 0., 0., 0., 0.]],

    #                     [[0., 0., 0., 0., 0.],
    #                      [0., 0., 0., 0., 0.],
    #                      [0., 0., 0., 0., 0.],
    #                      [0., 0., 0., 0., 0.]]],


    #                    [[[0., 0., 0., 0., 0.],
    #                      [0., 1., 0., 1., 0.],
    #                      [0., 1., 0., 1., 0.],
    #                      [0., 1., 0., 1., 0.]],

    #                     [[0., 0., 0., 0., 0.],
    #                      [0., 1., 0., 1., 0.],
    #                      [0., 1., 0., 1., 0.],
    #                      [0., 1., 0., 1., 0.]],begin_mask=0b1000, end_mask=0b0010, ellipsis_mask=0b0100

    #                     [[0., 0., 0., 0., 0.],
    #                      [0., 0., 0., 0., 0.],
    #                      [0., 0., 0., 0., 0.],
    #                      [0., 0., 0., 0., 0.]]]])
    # assert np.allclose(y.asnumpy(), expect)

    # y = Grad(begin_mask=0b1000, end_mask=0b0010)(x, (1, 0, 0, 2), (2, 2, 2, 4), (1, 1, 1, 1))
    # expect = np.array([[[[0., 0., 0., 0., 0.],
    #                      [0., 0., 0., 0., 0.],
    #                      [0., 0., 0., 0., 0.],
    #                      [0., 0., 0., 0., 0.]],

    #                     [[0., 0., 0., 0., 0.],
    #                      [0., 0., 0., 0., 0.],
    #                      [0., 0., 0., 0., 0.],
    #                      [0., 0., 0., 0., 0.]],

    #                     [[0., 0., 0., 0., 0.],
    #                      [0., 0., 0., 0., 0.],
    #                      [0., 0., 0., 0., 0.],
    #                      [0., 0., 0., 0., 0.]]],


    #                    [[[0., 0., 1., 1., 0.],
    #                      [0., 0., 1., 1., 0.],
    #                      [0., 0., 0., 0., 0.],
    #                      [0., 0., 0., 0., 0.]],

    #                     [[0., 0., 1., 1., 0.],
    #                      [0., 0., 1., 1., 0.],
    #                      [0., 0., 0., 0., 0.],
    #                      [0., 0., 0., 0., 0.]],

    #                     [[0., 0., 0., 0., 0.],
    #                      [0., 0., 0., 0., 0.],
    #                      [0., 0., 0., 0., 0.],
    #                      [0., 0., 0., 0., 0.]]]])
    # assert np.allclose(y.asnumpy(), expect)


    net = StridedSliceNet((1, 0, 0, 2), (2, 2, 2, 4), (1, 1, 1, 1),
                          begin_mask=0b1000, end_mask=0b0010, ellipsis_mask=0b0100)
    dx = GradData(net)(x)
    expect = np.array([[[[0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.]],

                        [[0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.]],

                        [[0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0.]]],


                       [[[1., 1., 1., 1., 0.],
                         [1., 1., 1., 1., 0.],
                         [1., 1., 1., 1., 0.],
                         [1., 1., 1., 1., 0.]],

                        [[1., 1., 1., 1., 0.],
                         [1., 1., 1., 1., 0.],
                         [1., 1., 1., 1., 0.],
                         [1., 1., 1., 1., 0.]],

                        [[1., 1., 1., 1., 0.],
                         [1., 1., 1., 1., 0.],
                         [1., 1., 1., 1., 0.],
                         [1., 1., 1., 1., 0.]]]])
    assert np.allclose(dx[0].asnumpy(), expect)

    x = Tensor(np.arange(0, 3*4*5).reshape(3, 4, 5).astype(np.float32))
    net = StridedSliceNet((1, 0, 0), (2, -3, 3), (1, 1, 3))
    dx = GradData(net)(x)
    expect = np.array([[[0., 0., 0., 0., 0.],
                        [0., 0., 0., 0., 0.],
                        [0., 0., 0., 0., 0.],
                        [0., 0., 0., 0., 0.]],

                       [[1., 0., 0., 0., 0.],
                        [0., 0., 0., 0., 0.],
                        [0., 0., 0., 0., 0.],
                        [0., 0., 0., 0., 0.]],

                       [[0., 0., 0., 0., 0.],
                        [0., 0., 0., 0., 0.],
                        [0., 0., 0., 0., 0.],
                        [0., 0., 0., 0., 0.]]])
    assert np.allclose(dx[0].asnumpy(), expect)

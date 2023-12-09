# SPDX-FileCopyrightText: 2023 Efabless Corporation

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#      http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# SPDX-License-Identifier: Apache-2.0

from caravel_cocotb.caravel_interfaces import *
import cocotb

async def set_byte(env, select1, select2, value):
    env.drive_gpio_in(28, 1)
    env.drive_gpio_in(27, select1)
    env.drive_gpio_in(26, select2)
    env.drive_gpio_in(25, ((value & 0x80) >> 7))
    env.drive_gpio_in(24, ((value & 0x40) >> 6))
    env.drive_gpio_in(23, ((value & 0x20) >> 5))
    env.drive_gpio_in(22, ((value & 0x10) >> 4))
    env.drive_gpio_in(21, ((value & 0x08) >> 3))
    env.drive_gpio_in(20, ((value & 0x04) >> 2))
    env.drive_gpio_in(19, ((value & 0x02) >> 1))
    env.drive_gpio_in(18, ((value & 0x01) >> 0))
    await cocotb.triggers.ClockCycles(env.clk, 2)

async def expect_byte(env, select1, select2, expected):
    env.drive_gpio_in(28, 0)
    env.drive_gpio_in(27, select1)
    env.drive_gpio_in(26, select2)
    await cocotb.triggers.ClockCycles(env.clk, 2)
    bits = env.monitor_gpio(12,5)
    bits_string = bits.binstr
    value = bits.integer
    cocotb.log.info(f"gonsolo: {bits_string} {hex(value)}")
    if (value == expected):
        cocotb.log.info (f"[TEST] Pass the value is '{hex(value)}'")
    else:
        cocotb.log.error (f"[TEST] Fail the value is :'{hex(value)}' expected {hex(expected)}")

async def set_or_expect_byte(env, input_set, select1, select2, byte):
    match input_set:
        case 1:
            await set_byte(env, select1, select2, byte)
        case 0:
            await expect_byte(env, select1, select2, byte)

async def set_or_expect_uint32(env, input_set, value):
    await set_or_expect_byte(env, input_set, 1, 1, (value & 0xFF000000) >> 24)
    await set_or_expect_byte(env, input_set, 1, 0, (value & 0x00FF0000) >> 16)
    await set_or_expect_byte(env, input_set, 0, 1, (value & 0x0000FF00) >> 8)
    await set_or_expect_byte(env, input_set, 0, 0, (value & 0x000000FF) >> 0)

async def pepe_test(env, value, expected):

    await set_or_expect_uint32(env, 1, value)
    await set_or_expect_uint32(env, 0, expected)

@cocotb.test()
@report_test
async def pepe(dut):
    caravelEnv = await test_configure(dut)
    await caravelEnv.wait_mgmt_gpio(1)

    test_pairs = [
        # Input: -33.f, output: -33.f / pi
        [0xC2040000, 0xC128114F],
        # Input: 0.3f, output: 0.3f / pi
        [0x3e99999a, 0x3dc391d1],
        # Input: 0.f, output: 0.f / pi == 0.f
        [0x0, 0x0]
    ]

    for pair in test_pairs:
        await pepe_test(caravelEnv, pair[0], pair[1])


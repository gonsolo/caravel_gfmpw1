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

# Keep in sync with rtl/user_proj_example.v
# 1: Write data, 0: Read data.
WRITE = 28
# Select which channel to write (r, g, b)
CHANNEL_SELECT0 = 27
CHANNEL_SELECT1 = 26
# Select which of four bytes for a 32 bit float to write (0-3)
BYTE_SELECT0 = 25
BYTE_SELECT1 = 24
# The 8 bits of a byte mapped to input pins
INPUT7 = 23
INPUT6 = INPUT7 - 1
INPUT5 = INPUT7 - 2
INPUT4 = INPUT7 - 3
INPUT3 = INPUT7 - 4
INPUT2 = INPUT7 - 5
INPUT1 = INPUT7 - 6
INPUT0 = INPUT7 - 7

# The output bits of a byte
OUTPUT7 = 12
OUTPUT0 = OUTPUT7 - 7

async def set_byte(env, channel_select0, channel_select1, byte_select0, byte_select1, value):
    env.drive_gpio_in(WRITE, 1)
    env.drive_gpio_in(CHANNEL_SELECT0, channel_select0)
    env.drive_gpio_in(CHANNEL_SELECT1, channel_select1)
    env.drive_gpio_in(BYTE_SELECT0, byte_select0)
    env.drive_gpio_in(BYTE_SELECT1, byte_select1)
    env.drive_gpio_in(INPUT7, ((value & 0x80) >> 7))
    env.drive_gpio_in(INPUT6, ((value & 0x40) >> 6))
    env.drive_gpio_in(INPUT5, ((value & 0x20) >> 5))
    env.drive_gpio_in(INPUT4, ((value & 0x10) >> 4))
    env.drive_gpio_in(INPUT3, ((value & 0x08) >> 3))
    env.drive_gpio_in(INPUT2, ((value & 0x04) >> 2))
    env.drive_gpio_in(INPUT1, ((value & 0x02) >> 1))
    env.drive_gpio_in(INPUT0, ((value & 0x01) >> 0))
    await cocotb.triggers.ClockCycles(env.clk, 2)

async def expect_byte(env, channel_select0, channel_select1, byte_select0, byte_select1, expected):
    env.drive_gpio_in(WRITE, 0)
    env.drive_gpio_in(CHANNEL_SELECT0, channel_select0)
    env.drive_gpio_in(CHANNEL_SELECT1, channel_select1)
    env.drive_gpio_in(BYTE_SELECT0, byte_select0)
    env.drive_gpio_in(BYTE_SELECT1, byte_select1)
    await cocotb.triggers.ClockCycles(env.clk, 2)
    bits = env.monitor_gpio(OUTPUT7, OUTPUT0)
    bits_string = bits.binstr
    value = bits.integer
    cocotb.log.info(f"gonsolo: {bits_string} {hex(value)}")
    if (value == expected):
        cocotb.log.info (f"[TEST] Pass the value is '{hex(value)}'")
    else:
        cocotb.log.error (f"[TEST] Fail the value is :'{hex(value)}' expected {hex(expected)}")

async def set_or_expect_byte(env, input_set, channel_select0, channel_select1, byte_select0, byte_select1, byte):
    match input_set:
        case 1:
            await set_byte(env, channel_select0, channel_select1, byte_select0, byte_select1, byte)
        case 0:
            await expect_byte(env, channel_select0, channel_select1, byte_select0, byte_select1, byte)

async def set_or_expect_uint32(env, input_set, channel_select0, channel_select1, value):
    await set_or_expect_byte(env, input_set, channel_select0, channel_select1, 1, 1, (value & 0xFF000000) >> 24)
    await set_or_expect_byte(env, input_set, channel_select0, channel_select1, 1, 0, (value & 0x00FF0000) >> 16)
    await set_or_expect_byte(env, input_set, channel_select0, channel_select1, 0, 1, (value & 0x0000FF00) >> 8)
    await set_or_expect_byte(env, input_set, channel_select0, channel_select1, 0, 0, (value & 0x000000FF) >> 0)

async def pepe_test_channel(env, channel_select0, channel_select1, value, expected):
    await set_or_expect_uint32(env, 1, channel_select0, channel_select1, value)
    await set_or_expect_uint32(env, 0, channel_select0, channel_select1, expected)

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
        await pepe_test_channel(caravelEnv, 0, 0, pair[0], pair[1])
        await pepe_test_channel(caravelEnv, 0, 1, pair[0], pair[1])
        await pepe_test_channel(caravelEnv, 1, 0, pair[0], pair[1])


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
# Select which channel to write (r, g, b)
CHANNEL1 =  37
CHANNEL0 =  36 
SELECT3 =   35
SELECT2 =   34
SELECT1 =   33
SELECT0 =   32
INPUT1 =    31
INPUT0 =    30
OUTPUT1 =    7
OUTPUT0 =    6
WRITE =      5

async def set_bits(env, channel1, channel0, select3, select2, select1, select0, value):
    env.drive_gpio_in(WRITE, 1)
    env.drive_gpio_in(CHANNEL1, channel1)
    env.drive_gpio_in(CHANNEL0, channel0)
    env.drive_gpio_in(SELECT3, select3)
    env.drive_gpio_in(SELECT2, select2)
    env.drive_gpio_in(SELECT1, select1)
    env.drive_gpio_in(SELECT0, select0)
    env.drive_gpio_in(INPUT1, ((value & 0b10) >> 1))
    env.drive_gpio_in(INPUT0, ((value & 0b01) >> 0))
    await cocotb.triggers.ClockCycles(env.clk, 2)

async def expect_bits(env, channel1, channel0, select3, select2, select1, select0, expected):
    env.drive_gpio_in(WRITE, 0)
    env.drive_gpio_in(CHANNEL1, channel1)
    env.drive_gpio_in(CHANNEL0, channel0)
    env.drive_gpio_in(SELECT3, select3)
    env.drive_gpio_in(SELECT2, select2)
    env.drive_gpio_in(SELECT1, select1)
    env.drive_gpio_in(SELECT0, select0)
    await cocotb.triggers.ClockCycles(env.clk, 2)
    bits = env.monitor_gpio(OUTPUT1, OUTPUT0)
    bits_string = bits.binstr
    value = bits.integer
    cocotb.log.info(f"gonsolo: {bits_string} {hex(value)}")
    if (value == expected):
        cocotb.log.info (f"[TEST] Pass the value is '{hex(value)}'")
    else:
        cocotb.log.error (f"[TEST] Fail the value is :'{hex(value)}' expected {hex(expected)}")

async def set_or_expect_bits(env, input_set, channel1, channel0, select3, select2, select1, select0, value):
    match input_set:
        case 1:
            await set_bits(env, channel1, channel0, select3, select2, select1, select0, value)
        case 0:
            await expect_bits(env, channel1, channel0, select3, select2, select1, select0, value)

async def set_or_expect_uint32(env, input_set, channel1, channel0, value):
    await set_or_expect_bits(env, input_set, channel1, channel0, 1, 1, 1, 1, (value & 0b11000000_00000000_00000000_00000000) >> 30)
    await set_or_expect_bits(env, input_set, channel1, channel0, 1, 1, 1, 0, (value & 0b00110000_00000000_00000000_00000000) >> 28)
    await set_or_expect_bits(env, input_set, channel1, channel0, 1, 1, 0, 1, (value & 0b00001100_00000000_00000000_00000000) >> 26)
    await set_or_expect_bits(env, input_set, channel1, channel0, 1, 1, 0, 0, (value & 0b00000011_00000000_00000000_00000000) >> 24)

    await set_or_expect_bits(env, input_set, channel1, channel0, 1, 0, 1, 1, (value & 0b00000000_11000000_00000000_00000000) >> 22)
    await set_or_expect_bits(env, input_set, channel1, channel0, 1, 0, 1, 0, (value & 0b00000000_00110000_00000000_00000000) >> 20)
    await set_or_expect_bits(env, input_set, channel1, channel0, 1, 0, 0, 1, (value & 0b00000000_00001100_00000000_00000000) >> 18)
    await set_or_expect_bits(env, input_set, channel1, channel0, 1, 0, 0, 0, (value & 0b00000000_00000011_00000000_00000000) >> 16)

    await set_or_expect_bits(env, input_set, channel1, channel0, 0, 1, 1, 1, (value & 0b00000000_00000000_11000000_00000000) >> 14)
    await set_or_expect_bits(env, input_set, channel1, channel0, 0, 1, 1, 0, (value & 0b00000000_00000000_00110000_00000000) >> 12)
    await set_or_expect_bits(env, input_set, channel1, channel0, 0, 1, 0, 1, (value & 0b00000000_00000000_00001100_00000000) >> 10)
    await set_or_expect_bits(env, input_set, channel1, channel0, 0, 1, 0, 0, (value & 0b00000000_00000000_00000011_00000000) >>  8)

    await set_or_expect_bits(env, input_set, channel1, channel0, 0, 0, 1, 1, (value & 0b00000000_00000000_00000000_11000000) >>  6)
    await set_or_expect_bits(env, input_set, channel1, channel0, 0, 0, 1, 0, (value & 0b00000000_00000000_00000000_00110000) >>  4)
    await set_or_expect_bits(env, input_set, channel1, channel0, 0, 0, 0, 1, (value & 0b00000000_00000000_00000000_00001100) >>  2)
    await set_or_expect_bits(env, input_set, channel1, channel0, 0, 0, 0, 0, (value & 0b00000000_00000000_00000000_00000011) >>  0)

async def pepe_test_channel(env, channel_select0, channel_select1, value, expected):
    await set_or_expect_uint32(env, 1, channel_select0, channel_select1, value)
    await cocotb.triggers.ClockCycles(env.clk, 20)
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
        #await pepe_test_channel(caravelEnv, 0, 1, pair[0], pair[1])
        #await pepe_test_channel(caravelEnv, 1, 0, pair[0], pair[1])


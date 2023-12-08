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

async def set_byte(env, input_set, select1, select2, value):
    env.drive_gpio_in(28, input_set)
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

async def expect_byte(env, input_set, select1, select2, expected):
    env.drive_gpio_in(28, input_set)
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

async def pepe_test(env):

    # 32 bit float -33.f as hex bits: C2040000
    await set_byte(env, 1, 1, 1, 0xC2) # C2
    await set_byte(env, 1, 1, 0, 0x04) # 04
    await set_byte(env, 1, 0, 1, 0x00) # 00
    await set_byte(env, 1, 0, 0, 0x00) # 00

    # Result in hex: C128114F
    await expect_byte(env, 0, 1, 1, 0xC1) # C1
    await expect_byte(env, 0, 1, 0, 0x28) # 28
    await expect_byte(env, 0, 0, 1, 0x11) # 11
    await expect_byte(env, 0, 0, 0, 0x4f) # 4f

@cocotb.test()
@report_test
async def pepe(dut):
    caravelEnv = await test_configure(dut)
    await caravelEnv.wait_mgmt_gpio(1)
    await pepe_test(caravelEnv)


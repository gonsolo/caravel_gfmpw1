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

async def set_byte(env, input_set, select1, select2, bit0, bit1, bit2, bit3, bit4, bit5, bit6, bit7):
    env.drive_gpio_in(28, input_set)
    env.drive_gpio_in(27, select1)
    env.drive_gpio_in(26, select2)
    env.drive_gpio_in(25, bit0)
    env.drive_gpio_in(24, bit1)
    env.drive_gpio_in(23, bit2)
    env.drive_gpio_in(22, bit3)
    env.drive_gpio_in(21, bit4)
    env.drive_gpio_in(20, bit5)
    env.drive_gpio_in(19, bit6)
    env.drive_gpio_in(18, bit7)
    await cocotb.triggers.ClockCycles(env.clk, 2)

async def pepe_test(env):

    # 32 bit float -33.f as hex bits: C2040000
    await set_byte(env, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0) # C2
    await set_byte(env, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0) # 04
    await set_byte(env, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0) # 00
    await set_byte(env, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0) # 00

    # Result in hex: c128114f
    env.drive_gpio_in(28, 0)
    env.drive_gpio_in(27, 1)
    env.drive_gpio_in(26, 1)
    await cocotb.triggers.ClockCycles(env.clk, 2)
    expected = 0xC1
    bits = env.monitor_gpio(12,5)
    bits_string = bits.binstr
    value = bits.integer
    cocotb.log.info(f"gonsolo: {bits_string} {hex(value)}")
    if (value == expected):
        cocotb.log.info (f"[TEST] Pass the value is '{hex(value)}'")
    else:
        cocotb.log.error (f"[TEST] Fail the value is :'{hex(value)}' expected {hex(expected)}")

    env.drive_gpio_in(28, 0)
    env.drive_gpio_in(27, 1)
    env.drive_gpio_in(26, 0)
    await cocotb.triggers.ClockCycles(env.clk, 2)
    expected = 0x28
    bits = env.monitor_gpio(12,5)
    bits_string = bits.binstr
    value = bits.integer
    cocotb.log.info(f"gonsolo: {bits_string} {hex(value)}")
    if (value == expected):
        cocotb.log.info (f"[TEST] Pass the value is '{hex(value)}'")
    else:
        cocotb.log.error (f"[TEST] Fail the value is :'{hex(value)}' expected {hex(expected)}")

    env.drive_gpio_in(28, 0)
    env.drive_gpio_in(27, 0)
    env.drive_gpio_in(26, 1)
    await cocotb.triggers.ClockCycles(env.clk, 2)
    expected = 0x11
    bits = env.monitor_gpio(12,5)
    bits_string = bits.binstr
    value = bits.integer
    cocotb.log.info(f"gonsolo: {bits_string} {hex(value)}")
    if (value == expected):
        cocotb.log.info (f"[TEST] Pass the value is '{hex(value)}'")
    else:
        cocotb.log.error (f"[TEST] Fail the value is :'{hex(value)}' expected {hex(expected)}")

    env.drive_gpio_in(28, 0)
    env.drive_gpio_in(27, 0)
    env.drive_gpio_in(26, 0)
    await cocotb.triggers.ClockCycles(env.clk, 2)
    expected = 0x4f
    bits = env.monitor_gpio(12,5)
    bits_string = bits.binstr
    value = bits.integer
    cocotb.log.info(f"gonsolo: {bits_string} {hex(value)}")
    if (value == expected):
        cocotb.log.info (f"[TEST] Pass the value is '{hex(value)}'")
    else:
        cocotb.log.error (f"[TEST] Fail the value is :'{hex(value)}' expected {hex(expected)}")

@cocotb.test()
@report_test
async def pepe(dut):
    caravelEnv = await test_configure(dut)
    await caravelEnv.wait_mgmt_gpio(1)
    await pepe_test(caravelEnv)


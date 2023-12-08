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

from caravel_cocotb.caravel_interfaces import * # import python APIs
import cocotb

async def pepe_test(env, drive, expected):
    env.drive_gpio_in(28, drive)
    await cocotb.triggers.ClockCycles(env.clk, 1)

    bits = env.monitor_gpio(12,5).binstr
    cocotb.log.info(f"gonsolo: {bits}")

    value = env.monitor_gpio(12,5).integer
    cocotb.log.info(f"gonsolo: {value} {hex(value)}")
    if (value == expected):
        cocotb.log.info (f"[TEST] Pass the value is '{hex(value)}'")
    else:
        cocotb.log.error (f"[TEST] Fail the value is :'{hex(value)}' expected {hex(expected)}")

async def pepe_set(env):

    # 32 bit float -33.f as hex bits: C2040000

    # Set first byte: C2
    env.drive_gpio_in(28, 1)
    # 27-26 select one of four bytes
    env.drive_gpio_in(27, 1)
    env.drive_gpio_in(26, 1)
    # 25-18: byte to set: C2
    env.drive_gpio_in(25, 1)
    env.drive_gpio_in(24, 1)
    env.drive_gpio_in(23, 0)
    env.drive_gpio_in(22, 0)
    env.drive_gpio_in(21, 0)
    env.drive_gpio_in(20, 0)
    env.drive_gpio_in(19, 1)
    env.drive_gpio_in(18, 0)
    await cocotb.triggers.ClockCycles(env.clk, 2)

    # Set second byte: 04
    env.drive_gpio_in(28, 1)
    # 27-26 select one of four bytes
    env.drive_gpio_in(27, 1)
    env.drive_gpio_in(26, 0)
    # 25-18: byte to set: C2
    env.drive_gpio_in(25, 0)
    env.drive_gpio_in(24, 0)
    env.drive_gpio_in(23, 0)
    env.drive_gpio_in(22, 0)
    env.drive_gpio_in(21, 0)
    env.drive_gpio_in(20, 1)
    env.drive_gpio_in(19, 0)
    env.drive_gpio_in(18, 0)
    await cocotb.triggers.ClockCycles(env.clk, 2)

    # Set third byte: 00
    env.drive_gpio_in(28, 1)
    # 27-26 select one of four bytes
    env.drive_gpio_in(27, 0)
    env.drive_gpio_in(26, 1)
    # 25-18: byte to set: C2
    env.drive_gpio_in(25, 0)
    env.drive_gpio_in(24, 0)
    env.drive_gpio_in(23, 0)
    env.drive_gpio_in(22, 0)
    env.drive_gpio_in(21, 0)
    env.drive_gpio_in(20, 0)
    env.drive_gpio_in(19, 0)
    env.drive_gpio_in(18, 0)
    await cocotb.triggers.ClockCycles(env.clk, 2)

    # Set forth byte: 00
    env.drive_gpio_in(28, 1)
    # 27-26 select one of four bytes
    env.drive_gpio_in(27, 0)
    env.drive_gpio_in(26, 0)
    # 25-18: byte to set: C2
    env.drive_gpio_in(25, 0)
    env.drive_gpio_in(24, 0)
    env.drive_gpio_in(23, 0)
    env.drive_gpio_in(22, 0)
    env.drive_gpio_in(21, 0)
    env.drive_gpio_in(20, 0)
    env.drive_gpio_in(19, 0)
    env.drive_gpio_in(18, 0)
    await cocotb.triggers.ClockCycles(env.clk, 2)

    # Read first byte:
    #env.drive_gpio_in(28, 0)
    # 27-26 select one of four bytes
    #env.drive_gpio_in(27, 1)
    #env.drive_gpio_in(26, 1)
    await cocotb.triggers.ClockCycles(env.clk, 2)
    expected = 0x4F
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

    #await pepe_test(caravelEnv, 1, 0x4F)
    #await pepe_test(caravelEnv, 0, 0x00)

    await pepe_set(caravelEnv)


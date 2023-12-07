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

@cocotb.test()
@report_test
async def pepe(dut):
    caravelEnv = await test_configure(dut)
    await caravelEnv.wait_mgmt_gpio(1)

    await pepe_test(caravelEnv, 1, 0xFF)
    await pepe_test(caravelEnv, 0, 0x00)

    #caravelEnv.drive_gpio_in(28, 1)


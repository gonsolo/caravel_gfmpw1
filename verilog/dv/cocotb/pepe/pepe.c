// SPDX-FileCopyrightText: 2023 Efabless Corporation

// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at

//      http://www.apache.org/licenses/LICENSE-2.0

// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include <firmware_apis.h>

int main(){
	ManagmentGpio_outputEnable();
	ManagmentGpio_write(0);
	enableHkSpi(0);

	for (int i = 0; i < 8; i++) {
		GPIOs_configure(i, GPIO_MODE_USER_STD_OUTPUT);
	}

	GPIOs_configure(37, GPIO_MODE_MGMT_STD_INPUT_PULLDOWN);
	GPIOs_configure(36, GPIO_MODE_MGMT_STD_INPUT_PULLDOWN);
	GPIOs_configure(35, GPIO_MODE_MGMT_STD_INPUT_PULLDOWN);
	GPIOs_configure(34, GPIO_MODE_MGMT_STD_INPUT_PULLDOWN);

	GPIOs_loadConfigs();
	ManagmentGpio_write(1);
}

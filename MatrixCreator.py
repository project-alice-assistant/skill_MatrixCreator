#  Copyright (c) 2021
#
#  This file, MatrixCreator.py, is part of Project Alice.
#
#  Project Alice is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>
#
#  Last modified: 2021.08.20 at 18:39:56 CEST
import time
from typing import Any, Dict

from matrix_lite import sensors

from core.base.model.AliceSkill import AliceSkill
from core.util.model.TelemetryType import TelemetryType


class MatrixCreator(AliceSkill):
	"""
	Author: Psychokiller1888
	Description: Access Matrix Creator sensors
	"""

	def __init__(self):
		super().__init__()


	def onBooted(self):
		super().onBooted()

		if self.getConfig('enableTemperatureSensor'):
			self.ThreadManager.newThread(name='matrix_sensor_temperature', target=self.temperatureSensorThread)

		if self.getConfig('enableAltitudeSensor'):
			self.ThreadManager.newThread(name='matrix_sensor_altitude', target=self.altitudeSensorThread)

		if self.getConfig('enableUVSensor'):
			self.ThreadManager.newThread(name='matrix_sensor_uv', target=self.uvSensorThread)


	def temperatureSensorThread(self):
		while True:
			data = sensors.humidity.read()
			if data:
				self.store(data={
					TelemetryType.TEMPERATURE: data.temperature,
					TelemetryType.HUMIDITY   : data.humidity
				})
			else:
				self.logWarning('Failed retrieving temperature/humidity data')

			time.sleep(self.getConfig('sensorReportInterval') * 60)


	def altitudeSensorThread(self):
		while True:
			data = sensors.pressure.read()
			if data:
				self.store(data={
					TelemetryType.TEMPERATURE: data.temperature,
					TelemetryType.PRESSURE   : data.pressure,
					TelemetryType.ALTITUDE   : data.altitude
				})
			else:
				self.logWarning('Failed retrieving temperature/pressure/altitude data')

			time.sleep(self.getConfig('sensorReportInterval') * 60)


	def uvSensorThread(self):
		while True:
			data = sensors.uv.read()
			if data:
				self.store(data={TelemetryType.UV_INDEX: data.uv})
			else:
				self.logWarning('Failed retrieving uv data')

			time.sleep(self.getConfig('sensorReportInterval') * 60)


	def store(self, data: Dict[TelemetryType, Any]):
		for ttype, item in data.items():
			self.TelemetryManager.storeData(ttype=ttype, value=item, service=self.name, deviceId=self.DeviceManager.getMainDevice().id, locationId=self.DeviceManager.getMainDevice().parentLocation)

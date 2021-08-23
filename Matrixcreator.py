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

from core.base.model.AliceSkill import AliceSkill
from matrix_lite import sensors

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
		elif self.getConfig('enableAltitudeSensor'):
			self.ThreadManager.newThread(name='matrix_sensor_altitude', target=self.altitudeSensorThread)
		elif self.getConfig('enableUVSensor'):
			self.ThreadManager.newThread(name='matrix_sensor_uv', target=self.uvSensorThread)


	def temperatureSensorThread(self):
		while True:
			data = sensors.humidity.read()
			if data:
				self.TelemetryManager.storeData(ttype=TelemetryType.TEMPERATURE, value=data.get('temperature', 999), service=self.name, deviceId=self.DeviceManager.getMainDevice().id, locationId=self.DeviceManager.getMainDevice().parentLocation)
				self.TelemetryManager.storeData(ttype=TelemetryType.HUMIDITY, value=data.get('humidity', -1), service=self.name, deviceId=self.DeviceManager.getMainDevice().id, locationId=self.DeviceManager.getMainDevice().parentLocation)
			else:
				self.logWarning('Failed retrieving temperature/humidity data')

			time.sleep(self.getConfig('sensorReportInterval') * 60)


	def altitudeSensorThread(self):
		while True:
			data = sensors.pressure.read()
			if data:
				self.TelemetryManager.storeData(ttype=TelemetryType.TEMPERATURE, value=data.get('temperature', 999), service=self.name, deviceId=self.DeviceManager.getMainDevice().id, locationId=self.DeviceManager.getMainDevice().parentLocation)
				self.TelemetryManager.storeData(ttype=TelemetryType.PRESSURE, value=data.get('pressure', -1), service=self.name, deviceId=self.DeviceManager.getMainDevice().id, locationId=self.DeviceManager.getMainDevice().parentLocation)
				self.TelemetryManager.storeData(ttype=TelemetryType.ALTITUDE, value=data.get('altitude', -999), service=self.name, deviceId=self.DeviceManager.getMainDevice().id, locationId=self.DeviceManager.getMainDevice().parentLocation)
			else:
				self.logWarning('Failed retrieving temperature/pressure/altitude data')

			time.sleep(self.getConfig('sensorReportInterval') * 60)


	def uvSensorThread(self):
		while True:
			data = sensors.uv.read()
			if data:
				self.TelemetryManager.storeData(ttype=TelemetryType.UV_INDEX, value=data.get('uv', 999), service=self.name, deviceId=self.DeviceManager.getMainDevice().id, locationId=self.DeviceManager.getMainDevice().parentLocation)
			else:
				self.logWarning('Failed retrieving uv data')

			time.sleep(self.getConfig('sensorReportInterval') * 60)

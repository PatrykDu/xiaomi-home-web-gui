from miio.integrations.light.yeelight.yeelight import Yeelight
from miio.miot_device import MiotDevice
from dataclasses import dataclass
from typing import List, Dict
import json


DEVICES_JSON_PATH = 'D:\Programs\Mi Home\dist\devices.json'


@dataclass
class Device:
    name: str
    ip: str
    token: str
    device_type: str
    remote_object: Yeelight = None


class DeviceResource:

    def create_device(device_item: Dict[str, str]) -> Device:
        return Device(
            name=device_item[0],
            ip=device_item[1]["ip"],
            token=device_item[1]["token"],
            device_type=None
        )

    def create_list_of_devices(data, type_of_device) -> List[Device]:
        devices_data = data[type_of_device]
        devices_list = []
        for device in devices_data.items():
            device_object = DeviceResource.create_device(device)
            devices_list.append(device_object)
        for device in devices_list:
            device.device_type = type_of_device
        return devices_list

    def change_json_to_devices(devices_json_path: str) -> List[Device]:
        with open(devices_json_path, 'r') as file:
            data = json.load(file)

        all_devices_list = []
        for type in data.keys():
            device_list = DeviceResource.create_list_of_devices(data, type)
            all_devices_list += device_list

        return all_devices_list


# Yeelight lights handling

def create_device_yeelight(device: Device) -> (Yeelight):
    return Yeelight(device.ip,
                    device.token)


def power_status_yeelight(device: Yeelight):
    device_status = Yeelight.status(device)
    if device_status.data['power'] == 'on':
        return True
    else:
        return False


def toggle_yeelight_device(device: Yeelight):
    device.toggle()


# Cuco lights handing

def create_cuco_light_s14_group(cuco_devices_list: List[Device]) -> List[MiotDevice]:
    cuco_group_list = []
    for device in cuco_devices_list:
        device_object = MiotDevice(device.ip, device.token)
        cuco_group_list.append(device_object)
    return cuco_group_list


def power_status_cuco_light_s14_group(cuco_group_list: List[MiotDevice]):
    """ Works only with Model: cuco.light.sl4 documentation about properties can be found here:
    https://miot-spec.org/miot-spec-v2/instance?type=urn:miot-spec-v2:device:light:0000A001:cuco-sl4:1"""

    status1 = cuco_group_list[0].get_property_by(2, 1)[0]['value']
    status2 = cuco_group_list[1].get_property_by(2, 1)[0]['value']
    if status1 and status2:
        return True
    else:
        return False


def on_cuco_light_s14(cuco_group_list: List[MiotDevice]) -> None:
    for cuco in cuco_group_list:
        cuco.set_property_by(2, 1, True)


def off_cuco_light_s14(cuco_group_list: List[MiotDevice]) -> None:
    for cuco in cuco_group_list:
        cuco.set_property_by(2, 1, False)


# Turn on and off yeelight lights and check power status
# toggle_yeelight_device(yeelight_devices_list[0])
# print(power_status_yeelight(yeelight_devices_list[0]))


# Turn on and off celling cuco lights and check power status
# on_cuco_light_s14(cuco_group_list)
# off_cuco_light_s14(cuco_group_list)
# print(power_status_cuco_light_s14_group(cuco_group_list))

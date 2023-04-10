from actions import DeviceResource, create_cuco_light_s14_group, create_yeelight_device, power_status_yeelight, DEVICES_JSON_PATH
from miio.integrations.light.yeelight.yeelight import Yeelight
import tkinter as tk

window = tk.Tk()
label = window.title("Mi Home")


def refresh():
    window.destroy()


# Create list of all devices
devices_list = DeviceResource.change_json_to_devices(DEVICES_JSON_PATH)

# Create group of cuco devices in one group (connected lights in one room)
cuco_devices_list = [
    device for device in devices_list if device.device_type == "MiotDevice"]
cuco_group_list = create_cuco_light_s14_group(cuco_devices_list)

yeelight_remotes_list = [
    create_yeelight_device(device) for device in devices_list if device.device_type == "yeelight"]

yeelight_devices_dict = {}
for remote in yeelight_remotes_list:
    for device in devices_list:
        if remote.token == device.token:
            yeelight_devices_dict[device.name] = remote


def button_color(device):
    if power_status_yeelight(device):
        return "green"
    else:
        return "red"


def toggle_yeelight_device(device: Yeelight, button):
    if power_status_yeelight(device):
        device.toggle()
        button.config(background='red')
    else:
        device.toggle()
        button.config(background='green')


bed_device = yeelight_devices_dict["Bed LED"]
button_bed = tk.Button(window, text="Bed LED")
button_bed.config(command=lambda: toggle_yeelight_device(bed_device, button_bed))
button_bed.configure(bg=button_color(bed_device))
button_bed.grid(row=2, column=0)

edroom_lamp_device = yeelight_devices_dict["Bedroom Lamp"]
button_bedroom_lamp = tk.Button(window, text="Bedroom Lamp")
button_bedroom_lamp.config(command=lambda: toggle_yeelight_device(edroom_lamp_device, button_bedroom_lamp))
button_bedroom_lamp.configure(bg=button_color(edroom_lamp_device))
button_bedroom_lamp.grid(row=2, column=1)

island_device = yeelight_devices_dict["Island"]
button_island = tk.Button(window, text="Island")
button_island.config(command=lambda: toggle_yeelight_device(island_device, button_island))
button_island.configure(bg=button_color(island_device))
button_island.grid(row=2, column=2)

livingroom_lamp_device = yeelight_devices_dict["Livingroom Lamp"]
button_livingroom_lamp = tk.Button(window, text="Livingroom Lamp")
button_livingroom_lamp.config(command=lambda: toggle_yeelight_device(livingroom_lamp_device, button_livingroom_lamp))
button_livingroom_lamp.configure(bg=button_color(livingroom_lamp_device))
button_livingroom_lamp.grid(row=2, column=3)

kitchen_device = yeelight_devices_dict["Kitchen"]
button_kitchen = tk.Button(window, text="Kitchen")
button_kitchen.config(command=lambda: toggle_yeelight_device(kitchen_device, button_kitchen))
button_kitchen.configure(bg=button_color(kitchen_device))
button_kitchen.grid(row=2, column=4)


window.mainloop()

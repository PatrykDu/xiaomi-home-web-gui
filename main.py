from actions import DeviceResource, create_cuco_light_s14_group, create_device_yeelight, power_status_yeelight, power_status_cuco_light_s14_group, off_cuco_light_s14, on_cuco_light_s14, DEVICES_JSON_PATH
from miio.integrations.light.yeelight.yeelight import Yeelight
from miio.miot_device import MiotDevice
import pystray
from PIL import Image
import tkinter as tk
from typing import List

PHOTO_PATH = 'D:\Programs\Mi Home\dist\mi.png'


window = tk.Tk()
label = window.title("Mi Home")

icon_photo = tk.PhotoImage(file=PHOTO_PATH)
window.iconphoto(False, icon_photo)


# Define a function for quit the window
def quit_window(icon, item):
    icon.stop()
    window.destroy()


# Define a function to show the window again
def show_window(icon, item):
    icon.stop()
    window.after(0, window.deiconify())


# Hide the window and show on the system taskbar
def hide_window():
    window.withdraw()
    image = Image.open("mi.ico")
    icon = pystray.Icon(name="Mi Home", icon=image, title="Mi Home", menu=pystray.Menu(
        pystray.MenuItem(text="Open", action=show_window, default=True),
        pystray.MenuItem(text="Exit", action=quit_window)
    ))
    icon.run()


# Buttons logic
def button_initial_color_yeelight(device):
    if power_status_yeelight(device):
        return "green"
    else:
        return "red"


def button_initial_color_cuco(cuco_group_list):
    if power_status_cuco_light_s14_group(cuco_group_list):
        return "green"
    else:
        return "red"


def toggle_device_yeelight(device: Yeelight, button):
    if power_status_yeelight(device):
        device.toggle()
        button.config(background='red')
    else:
        device.toggle()
        button.config(background='green')


def toggle_device_cuco_group(cuco_group_list: List[MiotDevice], button):
    if power_status_cuco_light_s14_group(cuco_group_list):
        off_cuco_light_s14(cuco_group_list)
        button.config(background='red')
    else:
        on_cuco_light_s14(cuco_group_list)
        button.config(background='green')


# Create list of all devices
devices_list = DeviceResource.change_json_to_devices(DEVICES_JSON_PATH)

yeelight_remotes_list = [
    create_device_yeelight(device) for device in devices_list if device.device_type == "yeelight"]

yeelight_devices_dict = {}
for remote in yeelight_remotes_list:
    for device in devices_list:
        if remote.token == device.token:
            yeelight_devices_dict[device.name] = remote


bed_device = yeelight_devices_dict["Bed LED"]
button_bed = tk.Button(window, text="Bed LED", height=5, width=25)
button_bed.config(
    command=lambda: toggle_device_yeelight(bed_device, button_bed))
button_bed.configure(bg=button_initial_color_yeelight(bed_device))
button_bed.grid(row=2, column=0)

edroom_lamp_device = yeelight_devices_dict["Bedroom Lamp"]
button_bedroom_lamp = tk.Button(
    window, text="Bedroom Lamp", height=5, width=25)
button_bedroom_lamp.config(command=lambda: toggle_device_yeelight(
    edroom_lamp_device, button_bedroom_lamp))
button_bedroom_lamp.configure(
    bg=button_initial_color_yeelight(edroom_lamp_device))
button_bedroom_lamp.grid(row=2, column=1)

island_device = yeelight_devices_dict["Island"]
button_island = tk.Button(window, text="Island", height=5, width=25)
button_island.config(command=lambda: toggle_device_yeelight(
    island_device, button_island))
button_island.configure(bg=button_initial_color_yeelight(island_device))
button_island.grid(row=2, column=2)

livingroom_lamp_device = yeelight_devices_dict["Livingroom Lamp"]
button_livingroom_lamp = tk.Button(
    window, text="Livingroom Lamp", height=5, width=25)
button_livingroom_lamp.config(command=lambda: toggle_device_yeelight(
    livingroom_lamp_device, button_livingroom_lamp))
button_livingroom_lamp.configure(
    bg=button_initial_color_yeelight(livingroom_lamp_device))
button_livingroom_lamp.grid(row=2, column=3)

kitchen_device = yeelight_devices_dict["Kitchen"]
button_kitchen = tk.Button(window, text="Kitchen", height=5, width=25)
button_kitchen.config(command=lambda: toggle_device_yeelight(
    kitchen_device, button_kitchen))
button_kitchen.configure(bg=button_initial_color_yeelight(kitchen_device))
button_kitchen.grid(row=2, column=4)


# Create group of cuco devices in one group (connected lights in one room)
cuco_devices_list = [
    device for device in devices_list if device.device_type == "MiotDevice"]
cuco_group_list = create_cuco_light_s14_group(cuco_devices_list)

button_sufit = tk.Button(window, text="Sufit", height=5, width=25)
button_sufit.config(command=lambda: toggle_device_cuco_group(
    cuco_group_list, button_sufit))
button_sufit.configure(bg=button_initial_color_cuco(cuco_group_list))
button_sufit.grid(row=2, column=5)

# Start minimalized
start_flag = True
if start_flag:
    start_flag = False
    hide_window()

window.protocol('WM_DELETE_WINDOW', hide_window)
window.mainloop()

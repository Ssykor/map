import tkinter as tk
import customtkinter
import tkintermapview
from geopy.distance import geodesic as GD
import geocoder as gc
from datetime import datetime as dt
import json
from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo
import re

# customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
# customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

root = customtkinter.CTk()
root.title("Pfadfinder")
# root.iconbitmap("gui.ico")
# root.geometry("1000x800")

color0 = "#333" # _darkgrey
color1 = "#073330" # _darkgreen
color2 ="#00bbff" #_lihtblue
m_color = "#5533ff"

switch_var = customtkinter.StringVar(value="off")

marker_count_path = 0
marker_count_poi = 0

marker_list_path = []
dist_list_path = []
path_marker_list = []
path_marker_dist_list = []
new_marker_json_list = []
search_results_json_list = []
search_results = []

search_frame = tk.Frame(root, width=1000, height=60, relief='groove', background=color1)
main_frame = tk.Frame(root, width=1000, height=740, relief='groove', background=color0)
infoFrame = tk.Frame(root, width=270, height=810, bg=color0, pady=0)
btnFrame = tk.Frame(infoFrame, width=270, height=80, bg=color0, pady=10)

# =================================================================================

searchfield = tk.Entry(search_frame)
searchfield.config(width=40)
searchfield.config(font=30)

# ==============================================================================
# Info Frame and Switch

def info_switch_event():
    if switch_var.get() == "show data panel":
        main_frame.configure(width=1260)
        search_frame.configure(width=1260)
        infoSwitch.configure(text="hide data panel")
        infoFrame.place(relx=1, rely=0, anchor=tk.NE)
        searchfield.place(relx=0.143, rely=0.5, anchor=tk.W)
        btn_marker_poi.place(relx=0.4988, rely=0.51, anchor=tk.W)
        infoSwitch.place(relx=0.682, rely=0.51, anchor=tk.W)
    else: 
        search_frame.configure(width=1000)
        main_frame.configure(width=1000)
        infoSwitch.configure(text="show data panel")
        infoFrame.place(relx=1, rely=0, anchor=tk.NW)
        searchfield.place(relx=0.18, rely=0.5, anchor=tk.W)
        btn_marker_poi.place(relx=0.628, rely=0.51, anchor=tk.W)
        infoSwitch.place(relx=0.85, rely=0.51, anchor=tk.W)

    # print("switch toggled, current value:", switch_var.get())

infoSwitch = customtkinter.CTkSwitch(master=search_frame, text="show data panel", command=info_switch_event,
                                   variable=switch_var, onvalue="show data panel", offvalue="hide data panel", fg_color=("#fff", "#000"), text_color="#fff")

info_label_poi = tk.Label(infoFrame, width=28, text="POIs (Places Of Interests)", font = ("Helvetica", 13), bg=color1, fg=color2, pady=19)
listbox_marker_poi = tk.Listbox(infoFrame, selectmode=tk.MULTIPLE, height = 17, width=42, bd=None, borderwidth=0, relief=None,  bg=color0, font = ("Helvetica", 8), fg=color2)

info_label_path = tk.Label(infoFrame, width=28, text="MARKERs on PATH", font=("Helvetica", 13), bg="#5533ff", fg="#fff", pady=19)
marker_pos_label_path = tk.Label(infoFrame, width=36, text="Longitude, Latitude", bg="#fff", fg="#5533ff", pady=4)
marker_dist_label_path = tk.Label(infoFrame, width=36, text="Distances", bg="#fff", fg="#5533ff", pady=4)

listbox_marker_path = tk.Listbox(infoFrame, height=10, width=42, bd=0, bg=color0, font=("Helvetica", 8), fg="#fff")
listbox_dist_path = tk.Listbox(infoFrame, height=10, width=42, bd=0, bg=color0, font=("Helvetica", 8), fg="#fff")

# ==============================================================================
# Button Functions

def convert_coordinates_to_address(deg_x: float, deg_y: float) -> gc.osm_reverse.OsmReverse:
    """ returns address object with the following attributes:
        street, housenumber, postal, city, state, country, latlng
        Geocoder docs: https://geocoder.readthedocs.io/api.html#reverse-geocoding """
    result = gc.osm([deg_x, deg_y], method="reverse")

    if result.ok:
        return result.json


def feed_map_poi_marker():
    global marker_count_poi
    marker_count_poi+=1

    x = re.findall("[a-z]", searchfield.get())

    try:
        if len(x) > 0:
            print(len(x))
            search_results.append(searchfield.get())
            search_results_json_list.append(searchfield.get())
            listbox_marker_poi.insert(len(search_results)+1, "  P"+str(len(search_results))+": "+searchfield.get())
        else:
            print(len(x))
            search_results.append(searchfield.get().replace(",", ""))
            new_search_result_json = convert_coordinates_to_address((searchfield.get().replace(",", "").split(" ")[0]), (searchfield.get().replace(",", "").split(" ")[1]))
            search_results_json_list.append(new_search_result_json)
            listbox_marker_poi.insert(len(search_results)+1, "  P"+str(len(search_results))+": "+searchfield.get().replace(",", ""))

        map_widget.set_address(searchfield.get(), text="P"+str(len(search_results)), marker=True, 
                                marker_color_circle=color2, marker_color_outside=color1, text_color=color1)
        print(search_results_json_list)
    except:
        print("not a valid entry")


def feed_map_poi_marker_right_click(coords):
    global marker_count_poi
    marker_count_poi+=1

    search_results.append(str(coords[0])+","+str(coords[1]))
    new_search_result_json = convert_coordinates_to_address(str(coords[0]), str(coords[1]))
    search_results_json_list.append(new_search_result_json)
    listbox_marker_poi.insert(len(search_results)+1, "  P"+str(len(search_results))+": "+"{0:.7f}".format(coords[0])+" "+"{0:.7f}".format(coords[1]))

    map_widget.set_marker(coords[0],coords[1], text="P"+str(marker_count_poi), 
                                            marker_color_circle=color2, marker_color_outside=color1, text_color=color1)
    print(search_results_json_list)

# =============================================================================
# save & clear

def save_all():
    name = askstring('project name', 'name your project: ')
    # showinfo('Hello!', 'Hi {}'.format(name))

    dt_now = dt.now().strftime("%Y%m%d%H%M")

    if len(name) == 0:
        name = "noname"

    poi_json_object = json.dumps(search_results_json_list, indent=4)
    with open("C:/_data/__github/map/pois/pois_"+name+"_"+dt_now+".json", "w") as outfile:
            outfile.write(poi_json_object)

    path_marker_json_object = json.dumps(new_marker_json_list, indent=4)
    with open("C:/_data/__github/map/path/path_"+name+"_"+dt_now+".json", "w") as outfile:
            outfile.write(path_marker_json_object)


def clear_all():
    global marker_count_path
    global marker_count_poi
    
    map_widget.delete_all_marker()
    map_widget.delete_all_path()
    listbox_marker_poi.delete(0, marker_count_poi)
    listbox_marker_path.delete(0, marker_count_path)
    listbox_dist_path.delete(0, marker_count_path)
    marker_count_poi = 0
    marker_count_path = 0
    search_results.clear()
    search_results_json_list.clear()
    marker_list_path.clear()
    dist_list_path.clear()
    new_marker_json_list.clear()

# =============================================================================

def add_marker(coords):
    global marker_count_path
    marker_count_path+=1
    new_marker_path = map_widget.set_marker(coords[0], coords[1], text="M"+str(marker_count_path), 
                                            marker_color_circle=None, marker_color_outside=m_color, text_color=m_color)

    marker_list_path.append(new_marker_path.position)
    listbox_marker_path.insert(len(marker_list_path)+1, "   M"+str(len(marker_list_path))+": "+str(new_marker_path.position[0])+", "+str(new_marker_path.position[1]))
    path_marker_list.append((coords[0], coords[1]))
    new_marker_json = convert_coordinates_to_address(coords[0], coords[1])
    new_marker_json_list.append(new_marker_json)
    print(new_marker_json_list)

    if len(marker_list_path) >= 2:
       penult =  marker_list_path[-2]
       latter = marker_list_path[-1]
       map_widget.set_path([penult, latter], width=6, color=m_color)
       single_dist_path = GD(penult,latter).km
       dist_list_path.append(single_dist_path)

       sum=0
       for dist in dist_list_path:
           sum += dist

       listbox_dist_path.insert(len(marker_list_path)+1, "   M"+str(marker_count_path-1)+"->"+"M"+str(marker_count_path)+": "+"{0:.3f}".format(single_dist_path)+" km"+"       "+"M1->M"+str(marker_count_path)+": "+"{0:.3f}".format(sum)+" km")
       path_marker_dist_list.append("   M"+str(marker_count_path-1)+"->"+"M"+str(marker_count_path)+": "+"{0:.3f}".format(single_dist_path)+" km"+"       "+"M1->M"+str(marker_count_path)+": "+"{0:.3f}".format(sum)+" km")

# =============================================================================

def print_path_lists():
    print('-'*100)
    print(path_marker_list)
    print('-'*100)
    print(path_marker_dist_list)
    print('-'*100)


def func_help():
    tk.messagebox.showinfo("pathfinder usage info", 'By clicking the Right Button\nyou can Add Markers with Paths between.')

# ==================================================================================================
# Buttons

btn_marker_poi = tk.Button(search_frame, text="SHOW POI", command=feed_map_poi_marker, bg=color2, fg=color1)
# btn_help = tk.Button(search_frame, text="  ?  ", bg="grey", fg="white", command=func_help)

btn_save_all = tk.Button(btnFrame, width=10, text="SAVE", command=save_all, bg="green", fg="white")
btn_clear_all = tk.Button(btnFrame, width=10, text="CLEAR", command=clear_all, bg="red", fg="white")

map_widget = tkintermapview.TkinterMapView(main_frame, width=1000, height=750, corner_radius=0)
map_widget.add_right_click_menu_command(label="Add PATH Marker", command=add_marker, pass_coords=True)
map_widget.add_right_click_menu_command(label="Add POI Marker", command=feed_map_poi_marker_right_click, pass_coords=True)

# ==================================================================================================
# place

searchfield.place(relx=0.18, rely=0.5, anchor=tk.W)
btn_marker_poi.place(relx=0.628, rely=0.51, anchor=tk.W)
infoSwitch.place(relx=0.85, rely=0.51, anchor=tk.W)
map_widget.place(relx=0, rely=0.5, anchor=tk.W)

info_label_poi.pack()
listbox_marker_poi.pack()
info_label_path.pack()
marker_pos_label_path.pack()
listbox_marker_path.pack()
marker_dist_label_path.pack()
listbox_dist_path.pack()
btnFrame.pack()

btn_save_all.grid(row=0, column=0)
btn_clear_all.grid(row=0, column=1)

search_frame.grid(row=0, column=0)
main_frame.grid(row=1, column=0)

# ==================================================================================================
# play as long as you can (infinitly)

root.mainloop()

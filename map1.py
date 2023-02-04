import tkinter as tk
import customtkinter
import tkintermapview
from geopy.distance import geodesic as GD

# customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
# customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

root = customtkinter.CTk() # tk.Tk()
root.title("Pfadfinder")
# root.iconbitmap("gui.ico")
# root.geometry("1000x800")

marker_count_path = 0
marker_count_poi = 0

color0 = "#333" # _darkgrey
color1 = "#073330" # _darkgreen
color2 ="#00bbff" #_lihtblue
m_color = "#5533ff"

search_frame = tk.Frame(root, width=1000, height=60, relief='groove', background=color1)
main_frame = tk.Frame(root, width=1000, height=740, relief='groove', background=color0)

# =================================================================================
# search option menu and entry field
options_poi = ["Search by Address", "Search by Coordinates"]

def get_search_option_poi(*args):
    print(f"search option has changed to '{option_clicked_poi.get()}'")

option_clicked_poi = tk.StringVar(value='Search by Address')
option_clicked_poi.set(options_poi[0])
option_clicked_poi.trace('w', get_search_option_poi)

drop_poi = tk.OptionMenu(search_frame, option_clicked_poi, *options_poi)
drop_poi.config(bg=color1)
drop_poi.config(width=20)
drop_poi.config(height=1)
drop_poi.config(fg=color2)

searchfield = tk.Entry(search_frame)
searchfield.config(width=40)
searchfield.config(font=30)

# ==============================================================================
# Info Frame and Switch

infoFrame = tk.Frame(root, width=270, height=810, bg=color0, pady=0)

switch_var = customtkinter.StringVar(value="off")

def info_switch_event():
    if switch_var.get() == "show data panel":
        main_frame.configure(width=1260)
        search_frame.configure(width=1260)
        infoSwitch.configure(text="hide data panel")
        infoFrame.place(relx=1, rely=0, anchor=tk.NE)
        
        # drop_poi.place(relx=0.009, rely=0.5, anchor=tk.W)
        searchfield.place(relx=0.143, rely=0.5, anchor=tk.W)
        btn_marker_poi.place(relx=0.4988, rely=0.51, anchor=tk.W)
        infoSwitch.place(relx=0.682, rely=0.51, anchor=tk.W)
    else: 
        search_frame.configure(width=1000)
        main_frame.configure(width=1000)
        infoSwitch.configure(text="show data panel")
        infoFrame.place(relx=1, rely=0, anchor=tk.NW)
        
        # drop_poi.place(relx=0.0108, rely=0.5, anchor=tk.W)
        searchfield.place(relx=0.18, rely=0.5, anchor=tk.W)
        btn_marker_poi.place(relx=0.628, rely=0.51, anchor=tk.W)
        infoSwitch.place(relx=0.85, rely=0.51, anchor=tk.W)

    # print("switch toggled, current value:", switch_var.get())

infoSwitch = customtkinter.CTkSwitch(master=search_frame, text="show data panel", command=info_switch_event,
                                   variable=switch_var, onvalue="show data panel", offvalue="hide data panel", fg_color=("#fff", "#000"), text_color="#fff")

# info_label_hello = tk.Label(infoFrame, width=25, height=1, text="", bg=color0, fg="#fff")

info_label_poi = tk.Label(infoFrame, width=28, text="Places Of Interests", font = ("Helvetica", 12), bg=color1, fg=color2, pady=19)
listbox_marker_poi = tk.Listbox(infoFrame, height = 17, width=42, bd=0, bg=color0, font = ("Helvetica", 8), fg=color2)

info_label_path = tk.Label(infoFrame, width=28, text="Path", font=("Helvetica", 12), bg="#5533ff", fg="#fff", pady=19)
marker_pos_label_path = tk.Label(infoFrame, width=36, text="Longitude, Latitude", bg="#fff", fg="#5533ff", pady=4)
marker_dist_label_path = tk.Label(infoFrame, width=36, text="Distances", bg="#fff", fg="#5533ff", pady=4)

listbox_marker_path = tk.Listbox(infoFrame, height=10, width=42, bd=0, bg=color0, font=("Helvetica", 8), fg="#fff")
listbox_dist_path = tk.Listbox(infoFrame, height=10, width=42, bd=0, bg=color0, font=("Helvetica", 8), fg="#fff")

# ==============================================================================
# Button Functions

search_results = []

def change_search_map():
    global marker_count_poi
    marker_count_poi+=1
    search_results.append(searchfield.get())
    try:
        listbox_marker_poi.insert(len(search_results)+1, "  POI "+str(len(search_results))+": "+searchfield.get())
        map_widget.set_address(searchfield.get(), text="POI "+str(len(search_results)), marker=True, 
                                marker_color_circle=color2, marker_color_outside=color1, text_color=color1)
    except:
        print("not a valid entry")

# =============================================================================
# Markers and Path
def clear_map():
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
    marker_list_path.clear()
    dist_list_path.clear()
    print(search_results, marker_list_path, dist_list_path)

marker_list_path = []
dist_list_path = []

def add_marker(coords):
    global marker_count_path
    marker_count_path+=1
    new_marker_path = map_widget.set_marker(coords[0], coords[1], text="M"+str(marker_count_path), 
                                            marker_color_circle=None, marker_color_outside=m_color, text_color=m_color)

    marker_list_path.append(new_marker_path.position)
    listbox_marker_path.insert(len(marker_list_path)+1, "   M"+str(len(marker_list_path))+": "+str(new_marker_path.position[0])+", "+str(new_marker_path.position[1]))

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


def func_help():
    tk.messagebox.showinfo("pathfinder usage info", 'By clicking the Right Button\nyou can Add Markers with Paths between.')

# ==================================================================================================
# Buttons
btn_marker_poi = tk.Button(search_frame, text="SET POI", command=change_search_map, bg=color2, fg=color1)
# btn_help = tk.Button(search_frame, text="  ?  ", bg="grey", fg="white", command=func_help)

btn_clear = tk.Button(infoFrame, text="CLEAR", command=clear_map, bg="red", fg="white")

map_widget = tkintermapview.TkinterMapView(main_frame, width=1000, height=750, corner_radius=0)
map_widget.add_right_click_menu_command(label="Add Marker", command=add_marker, pass_coords=True)

# ==================================================================================================
# place all stuff

# drop_poi.place(relx=0.0108, rely=0.5, anchor=tk.W)
searchfield.place(relx=0.18, rely=0.5, anchor=tk.W)
btn_marker_poi.place(relx=0.628, rely=0.51, anchor=tk.W)
infoSwitch.place(relx=0.85, rely=0.51, anchor=tk.W)
# btn_help.place(relx=0.98, rely=0.5, anchor=tk.E)

map_widget.place(relx=0, rely=0.5, anchor=tk.W)

# info_label_hello.pack()
info_label_poi.pack()
listbox_marker_poi.pack()
info_label_path.pack()
marker_pos_label_path.pack()
listbox_marker_path.pack()
marker_dist_label_path.pack()
listbox_dist_path.pack()
btn_clear.pack() # place(relx=0.05, rely=0.05, anchor=tk.SE)

search_frame.grid(row=0, column=0)
main_frame.grid(row=1, column=0)

# ==================================================================================================
# play as long as you can (infinitly)
root.mainloop()

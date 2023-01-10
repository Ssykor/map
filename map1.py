import tkinter as tk
import customtkinter
import tkintermapview
from geopy.distance import geodesic as GD

# customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
# customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

root = customtkinter.CTk() # tk.Tk()
root.title("POI LEI e LUI e +++")
# root.iconbitmap("gui.ico")
root.geometry("1000x800")

marker_count_path = 0
marker_count_poi = 0

frame_0 = tk.Frame(root, width=1000, height=60, relief='raised', background="#333")
frame_1 = tk.Frame(root, width=1000, height=740, relief='raised')

# =================================================================================
# search option menu and entry field
options_poi = ["Search by Address", "Search by Coordinates"]

def get_search_option_poi(*args):
    print(f"search option has changed to '{option_clicked_poi.get()}'")

option_clicked_poi = tk.StringVar(value='Search by Address')
option_clicked_poi.set(options_poi[0])
option_clicked_poi.trace('w', get_search_option_poi)

drop_poi = tk.OptionMenu(frame_0, option_clicked_poi, *options_poi)
drop_poi.config(bg='#333')
drop_poi.config(width=20)
drop_poi.config(height=1)
drop_poi.config(fg="white")

searchfield = tk.Entry(frame_0)
searchfield.config(width=40)
searchfield.config(font=30)

# ==============================================================================
# Info Switch

switch_var = customtkinter.StringVar(value="off")

def info_switch_event():
    if switch_var.get() == "on":
        infoSwitch.configure(text="info ON")
        infoFrame.place(relx=1, rely=0.07, anchor=tk.NE)
    else: 
        infoSwitch.configure(text="info OFF")
        infoFrame.place(relx=1, rely=0.07, anchor=tk.NW)

    # print("switch toggled, current value:", switch_var.get())

infoSwitch = customtkinter.CTkSwitch(master=frame_0, text="info OFF", command=info_switch_event,
                                   variable=switch_var, onvalue="on", offvalue="off", fg_color=("#fff", "#000"), text_color="#ccc")

infoFrame = tk.Frame(root, width=270, height = 760, bg = "#333", pady=3)

info_label_hello = tk.Label(infoFrame, width=25, height=1, text="", bg="#333", fg="#fff")
spacer_label_info_frame = tk.Label(infoFrame, width=36, height=2, text="", bg="#333", fg="#fff")

info_label_poi = tk.Label(infoFrame, width=28, text="Places Of Interests", font = ("Helvetica", 12), bg="#00bbff", fg="#000", pady=8)
listbox_marker_poi = tk.Listbox(infoFrame, height = 17, width = 42, bd=0, bg = "#333", font = ("Helvetica", 8), fg = "#fff")

info_label_path = tk.Label(infoFrame, width=28, text="Path Marker", font = ("Helvetica", 12), bg="#5533ff", fg="#fff", pady=8)
marker_pos_label_path = tk.Label(infoFrame, width=36, text="Marker: Longitude, Latitude", bg="#fff", fg="#5533ff", pady=4)
marker_dist_label_path = tk.Label(infoFrame, width=36, text="Marker Distances", bg="#fff", fg="#5533ff", pady=4)

listbox_marker_path = tk.Listbox(infoFrame, height = 10, width = 42, bd=0, bg = "#333", font = ("Helvetica", 8), fg = "#fff")
listbox_dist_path = tk.Listbox(infoFrame, height = 10, width = 42, bd=0, bg = "#333", font = ("Helvetica", 8), fg = "#fff")

# ==============================================================================
# Button Functions

search_results = []

def change_search_map():
    global marker_count_poi
    marker_count_poi+=1
    search_results.append(searchfield.get())
    listbox_marker_poi.insert(len(search_results)+1, "  POI "+str(len(search_results))+": "+searchfield.get())

    if option_clicked_poi.get() == "Search by Address":
        map_widget.set_address(searchfield.get(), text="POI "+str(len(search_results)), marker=True, 
                                marker_color_circle=None, marker_color_outside="#00bbff", text_color="#333")
        # print("searchfield.get(), address:", searchfield.get())
    elif option_clicked_poi.get() == "Search by Coordinates":
        if option_clicked_poi.get().find(","):
            sep=","
        elif option_clicked_poi.get().find(" "):
            sep=" "
        x = float(searchfield.get().split(sep)[0])
        y = float(searchfield.get().split(sep)[1])

        # print("searchfield.get(), coordinates:", searchfield.get())

        map_widget.set_marker(x, y, text="POI "+str(len(search_results)), 
                                marker_color_circle=None, marker_color_outside="#00bbff", text_color="#333")
    else:
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
    print(search_results)
    search_results.clear()
    print(search_results)
    print(marker_list_path)
    marker_list_path.clear()
    dist_list_path.clear()
    print(marker_list_path, dist_list_path)

marker_list_path = []
dist_list_path = []

def add_marker(coords):
    global marker_count_path

    marker_count_path+=1

    new_marker_path = map_widget.set_marker(coords[0], coords[1], text="M"+str(marker_count_path), 
                                            marker_color_circle=None, marker_color_outside="#5533ff", text_color="#5533ff")

    marker_list_path.append(new_marker_path.position)
    listbox_marker_path.insert(len(marker_list_path)+1, "   M"+str(len(marker_list_path))+": "+str(new_marker_path.position[0])+", "+str(new_marker_path.position[1]))

    if len(marker_list_path) >= 2:
       penult =  marker_list_path[-2]
       latter = marker_list_path[-1]
       map_widget.set_path([penult, latter], width=6, color="#5533ff")
       single_dist_path = GD(penult,latter).km
       dist_list_path.append(single_dist_path)

       sum=0
       for dist in dist_list_path:
           sum += dist

       listbox_dist_path.insert(len(marker_list_path)+1, "   M"+str(marker_count_path-1)+"->"+"M"+str(marker_count_path)+": "+"{0:.3f}".format(single_dist_path)+" km"+"       "+"M1->M"+str(marker_count_path)+": "+"{0:.3f}".format(sum)+" km")


def func_help():
    tk.messagebox.showinfo("POI LEI e LUI e +++ Usage Info", 'By clicking the Right Button\nyou can Add Markers with Paths between.')

# ==================================================================================================
# Buttons
btn_marker_poi = tk.Button(frame_0, text="SET POI", command=change_search_map, bg="#00bbff", fg="#333")
btn_clear = tk.Button(frame_0, text="CLEAR", command=clear_map, bg="red", fg="white")
btn_help = tk.Button(frame_0, text="  ?  ", bg="grey", fg="white", command=func_help)

map_widget = tkintermapview.TkinterMapView(frame_1, width=1000, height=750, corner_radius=0)
map_widget.add_right_click_menu_command(label="Add Marker", command=add_marker, pass_coords=True)

# ==================================================================================================
# place all stuff
searchfield.place(relx=0.206, rely=0.5, anchor=tk.W)
drop_poi.place(relx=0.0108, rely=0.5, anchor=tk.W)
btn_marker_poi.place(relx=0.605, rely=0.5, anchor=tk.CENTER)
infoSwitch.place(relx=0.8, rely=0.5, anchor=tk.CENTER)

info_label_hello.pack()
info_label_poi.pack()
listbox_marker_poi.pack()
info_label_path.pack()
marker_pos_label_path.pack()
listbox_marker_path.pack()
marker_dist_label_path.pack()
listbox_dist_path.pack()
spacer_label_info_frame.pack()

btn_clear.place(relx=0.94, rely=0.5, anchor=tk.E)
btn_help.place(relx=0.98, rely=0.5, anchor=tk.E)
map_widget.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

frame_0.grid(row=0, column=0)
frame_1.grid(row=1, column=0)

# ==================================================================================================
# play as long as you can (infinitly)
root.mainloop()

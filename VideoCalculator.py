import tkinter as tk

video_width = 1920.
video_height = 1080.

def clear_settings(event):
    output_window.delete(1.0, tk.END)

def clear_anchor(event):
    anchor_window.delete(1.0, tk.END)

def calculate_settings(event):
    try:
        border = float(gap_entry.get())
        num_row_videos = int(x_videos_entry.get())
        row_size = float(x_size_entry.get())
        num_col_videos = int(y_videos_entry.get())
        col_size = float(y_size_entry.get())
        
        row_gap = border * (num_row_videos + 1)
        col_gap = border * (num_col_videos + 1)
        total_row_gap = border * ((num_row_videos - row_size)+2)
        total_col_gap = border * ((num_col_videos - col_size)+2)
        
        new_video_width = row_size * (video_width-total_row_gap)/num_row_videos
        new_video_height = col_size * (video_height-total_col_gap)/num_col_videos
        one_video_width = row_size * (video_width-row_gap)/num_row_videos
        one_video_height = col_size * (video_height-col_gap)/num_col_videos

        settings = {}
        preserve_setting1 = 0. if p1_entry.get() == '' else float(p1_entry.get())
        preserve_setting2 = 0. if p2_entry.get() == '' else float(p2_entry.get())
        if (preserve.get() == 0):
            cur_video_height = video_height * (1 - preserve_setting1/100. - preserve_setting2/100.)
            full_scale = new_video_height/cur_video_height
            cur_video_width = video_width * full_scale
            
            settings['Left Crop'] = str(round(50 * ((cur_video_width - new_video_width)/full_scale)/video_width, 2)) + '%'
            settings['Top Crop'] = str(round(preserve_setting1, 2)) + '%'
            settings['Right Crop'] = str(round(50 * ((cur_video_width - new_video_width)/full_scale)/video_width, 2)) + '%'
            settings['Bot Crop'] = str(round(preserve_setting2, 2)) + '%'
            
            settings['Scale'] = str(round(1000 * full_scale)/10.) + '%'
        else:
            cur_video_width = video_width * (1 - preserve_setting1/100. - preserve_setting2/100.)
            full_scale = new_video_width/cur_video_width
            print(full_scale)
            cur_video_height = video_height * full_scale
            
            settings['Left Crop'] = str(round(preserve_setting2, 2)) + '%'
            settings['Top Crop'] = str(round(50 * ((cur_video_height - new_video_height)/full_scale)/video_height, 2)) + '%'
            settings['Right Crop'] = str(round(preserve_setting1, 2)) + '%'
            settings['Bot Crop'] = str(round(50 * ((cur_video_height - new_video_height)/full_scale)/video_height, 2)) + '%'

            settings['Scale'] = str(round(1000 * full_scale)/10.) + '%'
        
        x_positions = []
        if (row_size % 2 != 0):
            for i in range(num_row_videos):
                x_positions.append(border*(i+1) + ((one_video_width/row_size)/2.) + (one_video_width/row_size)*i)
        else:
            for i in range(num_row_videos-1):
                x_positions.append(border*(i+1) + (one_video_width/row_size)*(i+1) + border/2.)

        y_positions = []
        if (col_size % 2 != 0):
            for i in range(num_col_videos):
                y_positions.append(border*(i+1) + ((one_video_height/col_size)/2.) + (one_video_height/col_size)*i)
        else:
            for i in range(num_col_videos-1):
                y_positions.append(border*(i+1) + (one_video_height/col_size)*(i+1) + border/2.)

        positions_str = ''
        for y in y_positions:
            for x in x_positions:
                positions_str += '(' + str(int(x)) + ', ' + str(int(y)) + '), '
            positions_str = positions_str[:-2] + '\n'
        
        output_str = 'Image Settings\n'
        for key in settings.keys():
            output_str += key + ": " + str(settings[key]) + '\n'
        output_str += positions_str + '\n'
        output_window.insert(tk.INSERT, output_str)
    except ValueError:
        output_window.insert(tk.INSERT, 'Error: Make sure that the first five value fields have integer values.')

def calculate_anchor(event):
    try:
        top_pix = 0. if top_entry.get() == '' else float(top_entry.get())/100. * video_height
        bot_pix = 0. if bot_entry.get() == '' else float(bot_entry.get())/100. * video_height
        lef_pix = 0. if lef_entry.get() == '' else float(lef_entry.get())/100. * video_width
        rig_pix = 0. if rig_entry.get() == '' else float(rig_entry.get())/100. * video_width

        anchor_x = ((video_width - rig_pix) - lef_pix)/2. + lef_pix
        anchor_y = ((video_height - bot_pix) - top_pix)/2. + top_pix

        output_str = 'Image Anchor Point\n'
        output_str += 'x: ' + str(round(anchor_x,2)) + ' y: ' + str(round(anchor_y,2)) + '\n\n'
        anchor_window.insert(tk.INSERT, output_str)
    except ValueError:
        anchor_window.insert(tk.INSERT, 'Error: Make sure that all value fields have real number values 0 <= n <= 100.')

def switch_preserve():
    if (preserve.get() == 0):
        p1_label['text'] = preserve_top_text
        p2_label['text'] = preserve_bottom_text
    else:
        p1_label['text'] = preserve_left_text
        p2_label['text'] = preserve_right_text

# Initialize the window
window = tk.Tk()
label = window.title("Adobe Video Calculator")

# Number of videos in a row
x_videos_label = tk.Label(text="# of videos in a row")
x_videos_label.grid(row=1, column=1)
x_videos_entry = tk.Entry()
x_videos_entry.grid(row=1, column=2)
x_size_label = tk.Label(text="# of videos long")
x_size_label.grid(row=2, column=1)
x_size_entry = tk.Entry()
x_size_entry.grid(row=2, column=2)

# Numbers of videos in a column
y_videos_label = tk.Label(text="# of videos in a column")
y_videos_label.grid(row=3, column=1)
y_videos_entry = tk.Entry()
y_videos_entry.grid(row=3, column=2)
y_size_label = tk.Label(text="# of videos tall")
y_size_label.grid(row=4, column=1)
y_size_entry = tk.Entry()
y_size_entry.grid(row=4, column=2)

# Size of the gap between each video
gap_label = tk.Label(text="Size of the gap (in pixels) between videos")
gap_label.grid(row=5, column=1)
gap_entry = tk.Entry()
gap_entry.insert(0, '10') # default to 10 pixels
gap_entry.grid(row=5, column=2)

# Whether or not the height or width is preserved
preserve = tk.IntVar()
preserve.set(0)
tk.Radiobutton(text="Preserve Height",
               padx = 10,
               variable=preserve,
               command=switch_preserve,
               value=0).grid(row=6, column=1)
tk.Radiobutton(text="Preserve Width",
               padx = 10,
               variable=preserve,
               command=switch_preserve,
               value=1).grid(row=6, column=2)

preserve_top_text = "% taken off the top"
preserve_bottom_text = "% taken off the bottom"
preserve_left_text = "% taken off the left"
preserve_right_text = "% taken off the right"

# The preserve labels and entries
p1_label = tk.Label(text=preserve_top_text)
p1_label.grid(row=7, column=1)
p1_entry = tk.Entry()
p1_entry.grid(row=7, column=2)
p2_label = tk.Label(text=preserve_bottom_text)
p2_label.grid(row=8, column=1)
p2_entry = tk.Entry()
p2_entry.grid(row=8, column=2)

# Calculate the result
button = tk.Button(text="Calculate!")
button.bind("<Button-1>", calculate_settings)
button.grid(row=9,column=2)

button = tk.Button(text="Clear Output")
button.bind("<Button-1>", clear_settings)
button.grid(row=9,column=3)

# Output Window
output_window = tk.Text(height=20)
output_window.grid(row=9, column=1)
output_window.bind("<Key>", lambda e: "break")

lef_label = tk.Label(text=preserve_left_text)
lef_label.grid(row=10, column=1)
lef_entry = tk.Entry()
lef_entry.grid(row=10, column=2)
top_label = tk.Label(text=preserve_top_text)
top_label.grid(row=11, column=1)
top_entry = tk.Entry()
top_entry.grid(row=11, column=2)
rig_label = tk.Label(text=preserve_right_text)
rig_label.grid(row=12, column=1)
rig_entry = tk.Entry()
rig_entry.grid(row=12, column=2)
bot_label = tk.Label(text=preserve_bottom_text)
bot_label.grid(row=13, column=1)
bot_entry = tk.Entry()
bot_entry.grid(row=13, column=2)

# Calculate the result
button = tk.Button(text="Calculate anchor!")
button.bind("<Button-1>", calculate_anchor)
button.grid(row=14,column=2)

button = tk.Button(text="Clear Output")
button.bind("<Button-1>", clear_anchor)
button.grid(row=14,column=3)

# Output Window
anchor_window = tk.Text(height=16)
anchor_window.grid(row=14, column=1)
anchor_window.bind("<Key>", lambda e: "break")

window.mainloop()

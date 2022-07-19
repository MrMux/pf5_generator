import os
from tkinter import *
from tkinter import filedialog
import xml.etree.ElementTree as ET
from global_ import BG_COLOR, DEFAULT_DIR

class Parameter:
    def __init__(self, number, name, val, multiplier=1, divider = 1, display = 1):
        """Parameter and Display data"""
        self.number = number
        self.name = name
        self.value = val
        self.multiplier = multiplier
        self.divider = divider
        self.display = display
        self.dict = {self.number : {'Name': self.name, 'Value' : self.value, 'Multiplier' : self.multiplier, 'Divider' : self.divider, 'Display' : self.display}}

def writepf5(directory, parameters, entry, firmware_major, firmware_minor, vfd_name):
    """Generate xml and write to file"""
    for prams in parameters:
        parameters[prams]['Display'] = float(entry[prams].get())
        updateparameter(parameters, prams)
    xml_node = ET.Element('Node')
    xml_drive = ET.SubElement(xml_node, 'Drive')
    xml_drive.set('Brand', "1")
    xml_drive.set('Family', "9")
    xml_drive.set('Config', "212")
    xml_drive.set('Major Rev', firmware_major)
    xml_drive.set('Minor Rev', firmware_minor)
    xml_parameters = ET.SubElement(xml_drive, "Parameters")

    isdir = os.path.isdir(directory)
    if isdir is False:
        directory = DEFAULT_DIR

    vfd_name = vfd_name.replace('-','_')

    for val in parameters:
        xml_parameters.append(ET.Element('Parameter', {'Instance': f'{val}'}))
        xml_parameters[-1].text = f'{parameters[val]["Value"]}'
    tree = ET.ElementTree(xml_node)
    ET.indent(tree, space="  ", level=0)
    tree.write(directory + '\\' + vfd_name + '.pf5', encoding= "utf-8", method="xml", xml_declaration = True)

def updateparameter(parameters, number):
    """Easy Calculate value"""
    parameters[number]['Value'] = int(parameters[number]['Display'] * parameters[number]['Divider'] / parameters[number]['Multiplier'])

def dis_pram(parameters, number):
    """Easy Calculate Display"""
    parameters[number]['Display'] = parameters[number]['Value'] * parameters[number]['Multiplier'] / parameters[number]['Divider']

def browse_folder():
    global folder_path
    filename = filedialog.askdirectory(
    initialdir = r'\\',
    title = "Select Location for PF525 Files"
    )
    folder_path.set(filename)

PF525 = [Parameter(33,'Motor OL Current', 16, 1, 10).dict,
Parameter(34, 'FLA', 16, 1,10).dict,
Parameter(41, 'Accel Time', 300,1, 100).dict,
Parameter(42, 'Decel Time', 300,1, 100).dict,
Parameter(43, 'Min Freq', 0, 100).dict,
Parameter(44, 'Max Freq', 10000, 1, 100).dict,
Parameter(45, 'Stop Mode', 1).dict,
Parameter(46, 'Start Mode', 5).dict,
Parameter(47, 'Speed Reference', 15).dict,
Parameter(76, 'Relay 1', 2).dict,
Parameter(105, 'Safety Open En', 1).dict,
Parameter(128, 'EN Addr Select', 1).dict,
Parameter(129, 'IP Addr Cfg 1', 10).dict,
Parameter(130, 'IP Addr Cfg 2', 208).dict,
Parameter(131, 'IP Addr Cfg 3', 1).dict,
Parameter(132, 'IP Addr Cfg 4', 100).dict,
Parameter(133, 'Subnet Cfg 1', 255).dict,
Parameter(134, 'Subnet Cfg 2', 255).dict,
Parameter(135, 'Subnet Cfg 3', 255).dict,
Parameter(136, 'Subnet Cfg 4', 0).dict,
Parameter(143, 'Comm Flt Actn', 1).dict,
Parameter(144, 'Idle Flt Actn', 1).dict,
Parameter(440, 'PWM', 20,1,10).dict
]

if __name__ == "__main__":
    parameters = {}
    entry = {}
    label = {}
    for pram in PF525:
        parameters.update(pram)

    for pram in parameters:
        dis_pram(parameters, pram)
    ws = Tk()
    ws.title('Powerflex USB Tool')
    ws.geometry("300x650")
    ws.pack_propagate(0)
    ws.config(background = BG_COLOR)

    drive_name = StringVar(ws, value = 'VFD-TTF-101')
    drive_name_Tf = Entry(ws, textvariable = drive_name)
    drive_name_Tf.grid(column = 1, row = 1)
    drive_text = Text(ws, height = 1, width = 18, bg = BG_COLOR)
    drive_text.insert(INSERT, 'Drive Name')
    drive_text.grid(column = 0, row = 1)
    major_revision = StringVar(ws, value = '7')
    major_revision_Tf = Entry(ws, textvariable = major_revision)
    major_revision_Tf.grid(column = 1, row = 2)
    maj_rev_text = Text(ws, height = 1, width = 18, bg = BG_COLOR)
    maj_rev_text.insert(INSERT, 'Major Revision')
    maj_rev_text.grid(column = 0, row = 2)
    minor_revision = StringVar(ws, value = '1')
    minor_revision_Tf = Entry(ws, textvariable = minor_revision)
    minor_revision_Tf.grid(column = 1, row = 3)
    minor_rev_text = Text(ws, height = 1, width = 18, bg = BG_COLOR)
    minor_rev_text.insert(INSERT, 'Minor Revision')
    minor_rev_text.grid(column = 0, row = 3)
    i = 4

    for prams in parameters:
        e = Entry(ws,textvariable = StringVar(ws, '%g'%parameters[prams]['Display']))
        e.grid(row = i, column = 1)
        entry[prams] = e
        lb = Label(ws, text = parameters[prams]['Name'], bg = BG_COLOR, anchor = 'e', justify = LEFT)
        lb.grid(row = i, column = 0)
        label[prams] = lb
        i += 1

    button_exit = Button(ws,text = "Exit", command = exit )
    button_exit.pack(side = BOTTOM)

    button_gen = Button(ws, text = "Generate", command = lambda: writepf5(folder_path.get(), parameters, entry, major_revision.get(), minor_revision.get(), drive_name.get()))
    button_gen.pack(side = BOTTOM)

    folder_path = StringVar(ws, value = DEFAULT_DIR)
    label_browse = Label(master = ws, textvariable = folder_path)
    label_browse.pack(side = BOTTOM)

    button_browse = Button(text ="Browse", command = browse_folder)
    button_browse.pack(side = BOTTOM)

    ws.mainloop()

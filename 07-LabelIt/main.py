import io
import os
import pyperclip as pyc
import PySimpleGUI as sg

from PIL import Image, ImageDraw, ImageFont

import jsonHelper as jsh

file_types = [("JPEG (*.jpg)", "*.jpg"),
              ("PNG (*.png)", "*.png")]

BLACK_COLOR = (0, 0, 0)

# UI Picture View size
Wd1 = 550
Ht1 = 450
Wd2 = 500
Ht2 = 350
image1Ready = False
image2Ready = False
window = None
iRowCnt = 0 # Number of rows which are current in UI
iRowIndx = 0 # Number of rows (Visible in UI + Hiddend/Deleted)

def translate_coord(iTotalWdHt, val):
    if val.find('.') >= 0:
        return int(iTotalWdHt * float(val))
    return int(val)

def render_txts1(inputVals):
    img = Image.open(inputVals["-FILE-"])
    img = img.convert("RGB", colors=255)
    imgW, imgH = img.size
    i = 0
    while ('-txtName-', i) in window.AllKeysDict: # inputVals[('-txtName-', i)]:
        if len(inputVals[('-txtName-', i)]) > 0:
            strTxt = inputVals[('-txtName-', i)]
            iXAbs = translate_coord(imgW, inputVals[('-txtX-', i)])
            iY = translate_coord(imgH, inputVals[('-txtY-', i)])
            iZ = translate_coord(imgH, inputVals[('-txtZ-', i)])
            iR = int(inputVals[('-txtR-', i)])
            iG = int(inputVals[('-txtG-', i)])
            iB = int(inputVals[('-txtB-', i)])
            iMaxWd = translate_coord(imgW, inputVals[('-txtMaxW-', i)])
            strAlign = inputVals[('-cboAlign-', i)]
            text_draw = ImageDraw.Draw(img)            
            _, _, tmpW, _ = text_draw.textbbox((0, 0), strTxt, font=ImageFont.truetype("/arial.ttf", iZ, encoding='unic'))
            if strAlign == 'Center':
                iX = translate_coord(imgW, inputVals[('-txtX-', i)]) - (tmpW/2)
                text_draw.text((iX, iY), strTxt, fill=(iR, iG, iB, 255), font=ImageFont.truetype("/arial.ttf", iZ, encoding='unic'))
                text_draw.line([(iXAbs - (iMaxWd/2), iY), (iXAbs + (iMaxWd/2), iY)], fill=(iR, iG, iB, 255), width=5)
            else:
                iX = translate_coord(imgW, inputVals[('-txtX-', i)])
                text_draw.text((iX, iY), strTxt, fill=(iR, iG, iB, 255), font=ImageFont.truetype("/arial.ttf", iZ, encoding='unic'))
                text_draw.line([(iXAbs, iY), (iXAbs + iMaxWd, iY)], fill=(iR, iG, iB, 255), width=5)
        i = i + 1
    img.thumbnail((Wd1, Ht1))
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    window["-IMAGE-"].update(data=bio.getvalue())
    return

def render_txts2(inputVals):
    img = Image.open(inputVals["-TFILE-"])
    img = img.convert("RGB", colors=255)
    imgW, imgH = img.size
    strTxt = inputVals[('-txtTName-', 0)]
    if len(strTxt) > 0:
        iX = translate_coord(imgW, inputVals[('-txtTX-', 0)])
        iY = translate_coord(imgH, inputVals[('-txtTY-', 0)])
        iZ = translate_coord(imgH, inputVals[('-txtTZ-', 0)])
        iR = int(inputVals[('-txtTR-', 0)])
        iG = int(inputVals[('-txtTG-', 0)])
        iB = int(inputVals[('-txtTB-', 0)])
        text_draw = ImageDraw.Draw(img)            
        text_draw.text((iX, iY), strTxt, fill=(iR, iG, iB, 255), font=ImageFont.truetype("/arial.ttf", iZ, encoding='unic'))
    img.thumbnail((Wd2, Ht2))
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    window["-TIMAGE-"].update(data=bio.getvalue())
    return

def hide_row(i):
    global iRowCnt
    if iRowCnt > 1:
        iRowCnt = iRowCnt - 1
        tmpCtrl = window[('-RemoveTxt-', i)]
        tmpCtrl.hide_row()
    else:
        window[('-txtName-', i)].Update('')
        window[('-txtX-', i)].Update('')
        window[('-txtY-', i)].Update('')
        window[('-txtZ-', i)].Update('')
        window[('-cboAlign-', i)].Update(value='Left')
    
def add_row(i):
    return [
        [
            sg.Button("-",enable_events=True, key=("-RemoveTxt-", i)),
            sg.T("Name: ", key=("-lblName-", i)), 
            sg.InputText(size=(25,1),key=("-txtName-", i)), 
            sg.T("X", key=("-lblX-", i)), 
            sg.InputText(size=(10,1),key=("-txtX-", i), default_text = "0.5"),
            sg.T("Y", key=("-lblY-", i)), 
            sg.InputText(size=(10,1),key=("-txtY-", i), default_text = "0.5"),
            sg.T("Size", key=("-lblZ-", i)), 
            sg.InputText(size=(5,1),key=("-txtZ-", i), default_text = "20"),
            sg.T("Horizontal Align", key=("-lblAlign-", i)), 
            sg.Combo(['Left', 'Center'], default_value='Left',key=("-cboAlign-", i)),
            sg.T("R", key=("-lblR-", i)), 
            sg.InputText(size=(5,1),key=("-txtR-", i), default_text = "0"),
            sg.T("G", key=("-lblG-", 0)), 
            sg.InputText(size=(5,1),key=("-txtG-", i), default_text = "0"),
            sg.T("B", key=("-lblB-", 0)), 
            sg.InputText(size=(5,1),key=("-txtB-", i), default_text = "0"),
            sg.T("Max Width", key=("-lblMaxW-", i)), 
            sg.InputText(size=(5,1),key=("-txtMaxW-", i), default_text = "0.5")
        ]
    ]

def main():
    global window
    global iRowCnt
    global image1Ready
    global image2Ready
    iRowCnt = 1
    iRowIndx = 1
    layout = [ 
    [
        [
            sg.Text("Image File 1"),
            sg.Input(size=(25, 1), enable_events=True, key="-FILE-"),
            sg.FileBrowse(file_types=file_types),
            sg.Button("+",enable_events=True, key=("-AddTxt-")),
            sg.Button("Render",enable_events=True, key=("-Render-")),
            sg.Button("Copy settings",enable_events=True, key=("-Copy1-")),
            sg.Column([[
                sg.Text("Image File 2"),
                sg.Input(size=(25, 1), enable_events=True, key="-TFILE-"),
                sg.FileBrowse(file_types=file_types),
                sg.Button("Render",enable_events=True, key=("-TRender-"))
            ]])
        ],
        [
            sg.Image(key="-IMAGE-"),
            sg.Column([[
                sg.Image(key="-TIMAGE-")
            ]])
        ],
        [
            sg.Text("Labels for Image 1")
        ],
        [
            sg.Column(
                [[
                    sg.Button("-",enable_events=True, key=("-RemoveTxt-", 0)),
                    sg.T("Name: ", key=("-lblName-", 0)), 
                    sg.InputText(size=(25,1),key=("-txtName-", 0)), 
                    sg.T("X", key=("-lblX-", 0)), 
                    sg.InputText(size=(10,1),key=("-txtX-", 0), default_text = "0.5"),
                    sg.T("Y", key=("-lblY-", 0)), 
                    sg.InputText(size=(10,1),key=("-txtY-", 0), default_text = "0.5"),
                    sg.T("Size", key=("-lblZ-", 0)), 
                    sg.InputText(size=(5,1),key=("-txtZ-", 0), default_text = "20"),
                    sg.T("Horizontal Align", key=("-lblAlign-", 0)), 
                    sg.Combo(['Left', 'Center'], default_value='Left',key=("-cboAlign-", 0)),
                    sg.T("R", key=("-lblR-", 0)), 
                    sg.InputText(size=(5,1),key=("-txtR-", 0), default_text = "0"),
                    sg.T("G", key=("-lblG-", 0)), 
                    sg.InputText(size=(5,1),key=("-txtG-", 0), default_text = "0"),
                    sg.T("B", key=("-lblB-", 0)), 
                    sg.InputText(size=(5,1),key=("-txtB-", 0), default_text = "0"),
                    sg.T("Max Width", key=("-lblMaxW-", 0)), 
                    sg.InputText(size=(5,1),key=("-txtMaxW-", 0), default_text = "0.5")
                ]], key ="-txtToRender-")
            ]
        ],
        [
            sg.Text("Label for Image 2")
        ],
        [
            [
                sg.T("Name: "), 
                sg.InputText(size=(25,1),key=("-txtTName-", 0)), 
                sg.T("X"), 
                sg.InputText(size=(10,1),key=("-txtTX-", 0), default_text = "0.5"),
                sg.T("Y"), 
                sg.InputText(size=(10,1),key=("-txtTY-", 0), default_text = "0.5"),
                sg.T("Size"), 
                sg.InputText(size=(5,1),key=("-txtTZ-", 0), default_text = "20"),
                sg.T("R"), 
                sg.InputText(size=(10,1),key=("-txtTR-", 0), default_text = "0"),
                sg.T("G"), 
                sg.InputText(size=(10,1),key=("-txtTG-", 0), default_text = "0"),
                sg.T("B"), 
                sg.InputText(size=(5,1),key=("-txtTB-", 0), default_text = "0")
            ]
        ]
    ]
    window = sg.Window("Image Viewer", layout)
    evtDetail1 = ""
    evtDetail2 = ""
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "-FILE-":
            filename = values["-FILE-"]
            if os.path.exists(filename):
                image = Image.open(values["-FILE-"])
                image.thumbnail((Wd1, Ht1))
                bio = io.BytesIO()
                image.save(bio, format="PNG")
                window["-IMAGE-"].update(data=bio.getvalue())
                image1Ready = True
        if event == "-TFILE-":
            filename = values["-TFILE-"]
            if os.path.exists(filename):
                image = Image.open(values["-TFILE-"])
                image.thumbnail((Wd2, Ht2))
                bio = io.BytesIO()
                image.save(bio, format="PNG")
                window["-TIMAGE-"].update(data=bio.getvalue())
                image2Ready = True
        if event == "-Render-":
            if image1Ready == False:
                sg.Popup("First load Image 1")
            else:
                render_txts1(values)
        if event == "-TRender-":
            if image2Ready == False:
                sg.Popup("First load Image 2")
            else:
                render_txts2(values)
        if event == "-Copy1-":
            pyc.copy(jsh.getJson(values))
        if event == "-AddTxt-":
            window.extend_layout(window['-txtToRender-'], add_row(iRowIndx))
            iRowCnt = iRowCnt + 1
            iRowIndx = iRowIndx + 1
        if type(event) is tuple:
            evtDetail1, evtDetail2 = event
            if evtDetail1 == "-RemoveTxt-":
                hide_row(evtDetail2)          
    window.close()

if __name__ == "__main__":
    main()
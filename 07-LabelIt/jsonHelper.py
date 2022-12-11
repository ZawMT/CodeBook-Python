import copy
import json
import numpy as np

jsoTemplate = {
	"template_img": "",
	"template_img_n": "",
	"template_mail": "",
	"template_mail_d": "",
	"cc_email": [],
	"cc_email_d": [],
	"additional_template_info": {
		"campaign_email": "",
		"program_website_url": "",
		"program_facebook_url": ""
	},
	"draw_info_n": {"x": "", "y": "", "z": "", "r": "0", "g": "0", "b": "0"},
	"draw_info": []
}

jsoDrawInfoTemplate = {
        "info": "", "x": "", "y": "", "z": "", "ha": "",
        "maxW": "", "minSz": "9", "crop": "y", "r": "0", "g": "0", "b": "0"
    }

jsoObj = {}
drawInfo = []
bTicketType = False

valueMap1 = [
    ["-txtEmailTmpl-", "template_mail", "", True, "Email Template"],
    ["-txtVoidTmpl-", "template_mail_d", "", True, "Void Email Template"],
    ["-txtEmailCampaign-", ["additional_template_info","campaign_email"], "", True, "Campaign Email"],
    ["-txtFbUrl-", ["additional_template_info","program_facebook_url"], "no_fb_url", False, ""],
    ["-txtWebUrl-", ["additional_template_info","program_website_url"], "no_web_url", False, ""]
]

valueMap2 = [    
    ["-txtTX-", ["draw_info_n","x"], "", True, "Ticket Text X"],
    ["-txtTY-", ["draw_info_n","y"], "", True, "Ticket Text Y"],
    ["-txtTZ-", ["draw_info_n","z"], "", True, "Ticket Text Size"],
    ["-txtTR-", ["draw_info_n","r"], "", True, "Ticket Text Red"],
    ["-txtTG-", ["draw_info_n","g"], "", True, "Ticket Text Green"],
    ["-txtTB-", ["draw_info_n","b"], "", True, "Ticket Text Blue"]
]

valueMap3 = [
    ["-txtName-", "info", "Name"], 
    ["-txtX-", "x", "X"], 
    ["-txtY-", "y", "Y"], 
    ["-txtZ-", "z", "Size"],
    ["-txtZ-", "r", "Red"],
    ["-txtZ-", "g", "Green"],
    ["-txtZ-", "b", "Blue"],
    ["-txtMaxW-", "maxW", "Max Width"],
    ["-cboAlign-", "ha", "Horizontal Align"]
]

def createErr(valName):
    return "ERROR: Missing " + valName

def getBasicInfo(inputVals, tagName, jsonTag, defaultVal, bCompulsory):
    global jsoObj
    if len(inputVals[tagName]) > 0: 
        if np.isscalar(jsonTag):
            jsoObj[jsonTag] = inputVals[tagName]
        else:
            jsoObj[jsonTag[0]][jsonTag[1]] = inputVals[tagName]
        return True
    if bCompulsory is True:
        return False
    if np.isscalar(jsonTag):
        jsoObj[jsonTag] = defaultVal
    else:
        jsoObj[jsonTag[0]][jsonTag[1]] = defaultVal
    return True

def getDrawInfo(inputVals, tagName, jsonTag, jsoTmp):   
    if len(inputVals[tagName]) > 0: 
        jsoTmp[jsonTag] = inputVals[tagName]
        return True
    return False

def getCCEmails(inputVals):
    global jsoObj
    tmpCC = inputVals["-txtCC-"]
    tmpCC1s = []
    tmpCC2s = []
    if len(tmpCC) > 0:
        tmpCC1s = tmpCC.split(";")
    tmpCC = inputVals["-cboCC-"]
    iCC = tmpCC.find("CC")
    iPri = tmpCC.find("Primary")
    iAdd = tmpCC.find("Additional")
    for i in range(40):
        if i == iCC:
            tmpCC2s.append("FrCC")
        elif i == iPri:
            tmpCC2s.append("FrPrimary")
        elif i == iAdd:
            tmpCC2s.append("FrAdditional")
        if len(tmpCC2s) == 3:
            break
    tmpCC1s.extend(tmpCC2s)
    jsoObj["cc_email"] = tmpCC1s

def getCCVoidEmails(inputVals):
    global jsoObj
    tmpCCVs = []
    tmpCCV = inputVals["-txtCCVoid-"]
    if len(tmpCCV) > 0:
        tmpCCVs = tmpCCV.split(";")
    if inputVals["-chkVFrCC-"]:
        tmpCCVs.append("FrCC")
    if inputVals["-chkVFrCC-"]:
        tmpCCVs.append("FrCC")
    if inputVals["-chkVFrCC-"]:
        tmpCCVs.append("FrCC")
    jsoObj["cc_email_d"] = tmpCCVs

def getJson(inputVals, allKeys):
    global jsoObj
    global drawInfo
    global bTicketType
    jsoObj = {}
    drawInfo = []
    bTicketType = False
    certImg = inputVals["-FILE-"]
    if len(certImg) == 0:
        return "ERROR: Certificate image is missing"
    else:
        jsoObj = copy.deepcopy(jsoTemplate)
        iLastSlash = certImg.rfind("/")
        jsoObj["template_img"] = certImg[iLastSlash:]
    tktImg = inputVals["-TFILE-"]
    if len(tktImg) > 0:
        bTicketType = True
        iLastSlash = certImg.rfind("/")
        jsoObj["template_img_n"] = tktImg[iLastSlash:]
    for ent in valueMap1:
        if getBasicInfo(inputVals, ent[0], ent[1], ent[2], ent[3]) == False:
            return createErr(ent[4])
    if bTicketType == True:
        for ent in valueMap2:
            if getBasicInfo(inputVals, ent[0], ent[1], ent[2], ent[3]) == False:
                return createErr(ent[4])
    iIndx = 0
    bDone = False
    while not bDone:
        jsoTmp = copy.deepcopy(jsoDrawInfoTemplate)
        for ent in valueMap3:
            if (ent[0], iIndx) in allKeys:
                if  getDrawInfo(inputVals, (ent[0], iIndx), ent[1], jsoTmp) == False:
                    return createErr(ent[2] + " info in row " + str(iIndx))
            else:
                bDone = True     
                break
        if not bDone:    
            if jsoTmp["ha"] == "Center":
                jsoTmp["ha"] = "c"
            else:
                jsoTmp["ha"] = "l"  
            drawInfo.append(jsoTmp)
        iIndx = iIndx + 1
    jsoObj["draw_info"] = drawInfo
    getCCEmails(inputVals)
    getCCVoidEmails(inputVals)
    return json.dumps(jsoObj, separators=(',', ':'))
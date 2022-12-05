import copy
import json

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
	"draw_info_n": {"x": "", "y": "", "z": "", "r": "", "g": "", "b": ""},
	"draw_info": []
}

jsoDrawInfoTemplate = {
        "info": "", "x": "", "y": "", "z": "", "ha": "",
        "maxW": "", "minSz": "", "crop": "", "r": "", "g": "", "b": ""
    }

def getJson(inputVals):
    jsoTmp = copy.deepcopy(jsoTemplate)
    jsoTmp["template_img"] = inputVals["-FILE-"]    
    return json.dumps(jsoTmp, separators=(',', ':'))
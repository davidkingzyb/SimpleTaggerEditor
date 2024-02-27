# 2024/2/25 by DKZ

import modules.scripts as scripts
import gradio as gr
import os
import re

from modules import script_callbacks

def on_ui_tabs():
    with gr.Blocks(analytics_enabled=False) as ui_component:
        with gr.Row():
            dir_tb=gr.Textbox(label="Input directory")
            load_btn=gr.Button(value="Load",variant="primary")
        with gr.Row():
            with gr.Column():
                gallery=gr.Gallery().style(columns=3)
            with gr.Column():
                add_tb=gr.Textbox(label="Additional tags")
                remove_tb=gr.Textbox(label="Exclude tags (split by comma)")
                tagger_tb=gr.Textbox(label="Tagger")
                save_btn=gr.Button(value="Save",variant="primary")
        load_btn.click(fn=loadBtnClick,inputs=dir_tb,outputs=gallery)
        gallery.select(gallerySelect,None,tagger_tb)
        save_btn.click(fn=saveClick,inputs=tagger_tb)
        add_tb.blur(fn=addBlur,inputs=add_tb)
        remove_tb.blur(fn=removeBlur,inputs=remove_tb)
        return [(ui_component, "Tagger Editor", "taggers_editor_tab")]

script_callbacks.on_ui_tabs(on_ui_tabs)

add=''
def addBlur(i):
    global add
    add=i

removes=[]
def removeBlur(i):
    global removes
    removes=i.split(',')

pngs=[]
dir=''
def loadBtnClick(dir_tb):
    global pngs
    global dir
    dir=dir_tb
    files=os.listdir(dir_tb)
    for f in files:
        if 'txt' not in f:
            pngs.append(f)
    result=[os.path.join(dir_tb,l) for l in pngs]
    return result
    
file_name=''   
def gallerySelect(evt:gr.SelectData):
    global pngs
    global dir
    global file_name
    global add
    global removes
    file_name=pngs[evt.index].split('.')[0]
    print('select',file_name)
    with open(os.path.join(dir,file_name+'.txt')) as f:
        t=f.read()
    result=t
    for s in removes:
        result=result.replace(s,'')
    if add not in result:
        result=result+','+add
    result=re.sub(r',\s+,',',',result)
    result=re.sub(r',\s+,',',',result)# cause by prev line
    result=re.sub(r',,',',',result)
    result=re.sub(r',,',',',result)
    if result!=t:
        with open(os.path.join(dir,file_name+'.txt'),'w') as ff:
            ff.write(result)
    return result

def saveClick(tagger_tb):
    print('save',file_name)
    with open(os.path.join(dir,file_name+'.txt'),'w') as f:
        f.write(tagger_tb)

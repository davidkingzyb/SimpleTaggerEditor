# 2024/2/25 by DKZ

import modules.scripts as scripts
import gradio as gr
import os

from modules import script_callbacks


def on_ui_tabs():
    with gr.Blocks(analytics_enabled=False) as ui_component:
        with gr.Row():
            input_dir=gr.Textbox(label="Input directory")
            load_btn=gr.Button(value="Load")
        with gr.Row():
            with gr.Column():
                gallery=gr.Gallery().style(columns=3)
            with gr.Column():
                tagger=gr.Textbox(label="Tagger")
                save=gr.Button(value="Save")
        load_btn.click(fn=loadBtnClick,inputs=input_dir,outputs=gallery)
        gallery.select(gallerySelect,None,tagger)
        save.click(fn=saveClick,inputs=tagger)
        return [(ui_component, "Tagger Editor", "taggers_editor_tab")]

script_callbacks.on_ui_tabs(on_ui_tabs)

pngs=[]
pic_dir=''
def loadBtnClick(input_dir):
    global pngs
    global pic_dir
    pic_dir=input_dir
    files=os.listdir(input_dir)
    for f in files:
        if 'txt' not in f:
            pngs.append(f)
    result=[os.path.join(input_dir,l) for l in pngs]
    return result
    
file_name=''   
def gallerySelect(evt: gr.SelectData):
    global pngs
    global pic_dir
    global file_name
    file_name=pngs[evt.index].split('.')[0]
    print(evt.index,file_name,pic_dir)
    with open(os.path.join(pic_dir,file_name+'.txt')) as f:
        t=f.read()
    return t

def saveClick(tagger):
    with open(os.path.join(pic_dir,file_name+'.txt'),'w') as f:
        f.write(tagger)
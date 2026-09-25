
import gradio as gr
import os
import re
from tkinter import filedialog, Tk

try:
    from modules import script_callbacks
    script_callbacks.on_ui_tabs(on_ui_tabs)
except Exception as err:
    print("not in webui")

def on_ui_tabs():
    with gr.Blocks(analytics_enabled=False) as ui_component:
        with gr.Row():
            with gr.Column():
                dir_tb=gr.Textbox(label="Input directory")
            with gr.Row():
                folder_btn = gr.Button(
                    '📂'
                )
                folder_btn.click(
                    folderBtnClick,
                    outputs=dir_tb,
                    show_progress=False,
                )
                load_btn=gr.Button(value="Load",variant="primary")
                save_all_btn=gr.Button(value="Save All")
        with gr.Row():
            with gr.Column():
                # 优化：将 .style(columns=3) 改为直接传入参数，兼容新版 Gradio
                gallery=gr.Gallery(columns=3) 
            with gr.Column():
                add_tb=gr.Textbox(label="Additional tags (split by comma) (first letter is $ add at the end)")
                remove_tb=gr.Textbox(label="Exclude tags (split by comma) (regular expression support `(` escaped as `\(` )")
                tagger_tb=gr.Textbox(label="Tagger")
                save_btn=gr.Button(value="Save",variant="primary")
                
        load_btn.click(fn=loadBtnClick,inputs=dir_tb,outputs=gallery)
        gallery.select(gallerySelect,None,tagger_tb)
        save_btn.click(fn=saveClick,inputs=tagger_tb)
        save_all_btn.click(fn=saveAllClick)
        add_tb.blur(fn=addBlur,inputs=add_tb)
        remove_tb.blur(fn=removeBlur,inputs=remove_tb)
        return [(ui_component, "Tagger Editor", "taggers_editor_tab")]


def folderBtnClick():
    root = Tk()
    root.wm_attributes("-topmost", 1)
    root.withdraw()
    folder_path = filedialog.askdirectory()
    root.destroy()
    return folder_path


adds=[]
def addBlur(i):
    global adds
    adds=i.split(',')

removes=[]
def removeBlur(i):
    global removes
    removes=i.split(',')

pngs=[]
dir=''
def loadBtnClick(dir_tb):
    global pngs
    global dir
    pngs=[]
    dir=dir_tb
    files=os.listdir(dir_tb)
    for f in files:
        if 'txt' not in f and 'npz' not in f:
            pngs.append(f)
    result=[os.path.join(dir_tb,l) for l in pngs]
    return result

def saveAllClick():
    global pngs
    global dir
    for png in pngs:
        file_name=os.path.join(dir,png.split('.')[0]+'.txt')
        with open(file_name,'r') as f:
            t=f.read()
        result=_doRemove(t)
        result=_doAdd(result)
        result=_format(result)
        if result!=t:
            print('save all ',file_name)
            with open(file_name,'w') as ff:
                ff.write(result)

def _doAdd(tag):
    global adds
    result=tag
    front=''
    for a in adds:
        r=a.strip()
        if r and r[0]=='$' and r[1:] not in result:
            result=result+', '+r[1:]
        elif r and r[0]!='$' and r not in result:
            front=front+', '+r
    result=front[2:]+', '+result
    return result

def _doRemove(tag):
    global removes
    result=tag
    for s in removes:
        r=re.compile(s.strip())
        result=re.sub(r,'',result)#result.replace(r,'')
    return result

def _format(tag):
    tags=tag.split(',')
    result=[]
    for t in tags:
        if t.strip()!='':
            result.append(t.strip())
    return ', '.join(result)

    
    
file_name=''   
def gallerySelect(evt:gr.SelectData):
    global pngs
    global dir
    global file_name
    file_name=pngs[evt.index].split('.')[0]
    print('select',file_name)
    with open(os.path.join(dir,file_name+'.txt')) as f:
        t=f.read()

    result=_doRemove(t)
    result=_doAdd(result)
    result=_format(result)

    if result!=t:
        print('edit ',file_name)
        with open(os.path.join(dir,file_name+'.txt'),'w') as ff:
            ff.write(result)
    return result

def saveClick(tagger_tb):
    print('save',file_name)
    with open(os.path.join(dir,file_name+'.txt'),'w') as f:
        f.write(tagger_tb)


# ================= 新增部分：支持独立运行 =================
if __name__ == "__main__":
    # 调用 on_ui_tabs 获取构建好的 UI 组件
    ui_tabs = on_ui_tabs()
    
    if ui_tabs:
        # on_ui_tabs 返回的格式是 [(ui_component, "Title", "Tab_ID")]
        # 我们提取出第一个元素中的 ui_component (即 gr.Blocks 实例)
        app = ui_tabs[0][0]
        
        print("Starting standalone Tagger Editor...")
        # 启动独立的 Gradio Web 界面
        # share=False: 不生成公网链接
        # inbrowser=True: 启动后自动在浏览器中打开
        app.launch(share=False, inbrowser=True)
    else:
        print("Failed to create UI component.")
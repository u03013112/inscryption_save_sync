import json
import os
import requests
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox

config_file = "config.json"


def load_config():
    if not os.path.exists(config_file):
        return {"serverIP": "", "serverPort": 8888, "savePath": ""}

    with open(config_file, "r") as f:
        return json.load(f)


def save_config(config):
    with open(config_file, "w") as f:
        json.dump(config, f)


def sync():
    config = load_config()
    server_url = f"http://{config['serverIP']}:{config['serverPort']}"

    try:
        response = requests.get(f"{server_url}/download", timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to download save file: {e}")
        return

    server_save = json.loads(response.text)
    with open('%s.download'%(config["savePath"]), "w") as temp_file:
        temp_file.write(response.text)

    try:
        with open(config["savePath"], "r") as f:
            local_save = json.load(f)
    except FileNotFoundError:
        messagebox.showerror("Error", "Local save file not found")
        return

    server_play_time = server_save["playTime"]
    local_play_time = local_save["playTime"]

    if local_play_time > server_play_time:
        messagebox.showinfo("Info", "本地存档较新，需要上传")
    elif local_play_time < server_play_time:
        messagebox.showinfo("Info", "服务器存档较新，需要覆盖本地存档")
    else:
        messagebox.showinfo("Info", "无需任何操作")



def force_upload():
    config = load_config()
    server_url = f"http://{config['serverIP']}:{config['serverPort']}"

    if messagebox.askokcancel("Warning", "Are you sure you want to force upload? This will overwrite the server save file."):
        try:
            with open(config["savePath"], "rb") as f:
                response = requests.post(f"{server_url}/upload", files={"file": f})
                response.raise_for_status()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to upload save file: {e}")
            return

        messagebox.showinfo("Info", "Save file uploaded successfully")


def force_download():
    config = load_config()
    if messagebox.askokcancel("Warning", "确认要强制下载吗？这将覆盖本地存档。"):
        try:
            with open(config["savePath"], "r") as f:
                local_save = json.load(f)
                play_time = local_save["playTime"]
                backup_path = f"{config['savePath']}.%f" % play_time

            with open(backup_path, "w") as backup_file:
                json.dump(local_save, backup_file)

        except FileNotFoundError:
            messagebox.showerror("Error", "Local save file not found")
            return

        with open('%s.download'%(config["savePath"]), "r") as temp_file, open(config["savePath"], "w") as local_file:
            local_file.write(temp_file.read())

        messagebox.showinfo("Info", "本地存档已经同步至最新")



app = Tk()
app.title("Save Sync")

Label(app, text="Server IP:Port").grid(row=0, column=0)
Label(app, text="Save Path").grid(row=1, column=0)

server_ip_port = StringVar()
server_ip_port.set(f"{load_config()['serverIP']}:{load_config()['serverPort']}")
Entry(app, textvariable=server_ip_port).grid(row=0, column=1)

save_path = StringVar()
save_path.set(load_config()["savePath"])
Entry(app, textvariable=save_path).grid(row=1, column=1)

Button(app, text="Sync", command=sync).grid(row=2, column=0)
Button(app, text="Force Upload", command=force_upload).grid(row=2, column=1)
Button(app, text="Force Download", command=force_download).grid(row=2, column=2)

app.mainloop()

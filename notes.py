import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import json
root = tk.Tk()
root.title('Notes App')
root.geometry('270x340')
root.configure(bg='lightgreen')
notes_data = []

def addText():
    text = enteredText.get('1.0', tk.END).strip()
    if text == '':
        messagebox.showerror("Üres", "Írj be valamit!")
        return
    note = {
        "text": text,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "priority": priorityVar.get()
    }
    content.insert(tk.END, f"[{note['priority']}] {note['text']} ({note['time']})")
    notes_data.append(note)
    enteredText.delete('1.0', tk.END)
    autosave()
    
def delete():
    if content.size() == 0:
        messagebox.showerror("Hiba", "A lista üres!")
    else:
        content.delete(0, tk.END)
        notes_data.clear()
        autosave()

def choose(event):
    selected = content.curselection()
    if selected:
        text = content.get(selected)
        enteredText.delete('1.0', tk.END)
        enteredText.insert(tk.END, text)

def save():
    if len(notes_data) == 0:
        messagebox.showerror("Hiba", "Nincs mit menteni!")
        return
    with open('notes.json', 'w', encoding='utf-8') as f:
        json.dump(notes_data, f, indent=4)
    messagebox.showinfo("Mentés", "Sikeres mentés!")

def load():
    global notes_data
    try:
        with open('notes.json', 'r', encoding='utf-8') as f:
            notes_data = json.load(f)
        content.delete(0, tk.END)
        for note in notes_data:
            if isinstance(note, dict):
                content.insert(tk.END, f"[{note['priority']}] {note['text']} ({note['time']})")
    except FileNotFoundError:
        notes_data = []

def autosave():
    with open('notes.json', 'w', encoding='utf-8') as f:
        json.dump(notes_data, f, indent=4)

def search(event=None):
    query = searchVar.get().lower()
    content.delete(0, tk.END)
    if query == "":
        for note in notes_data:
            content.insert(tk.END, f"[{note['priority']}] {note['text']} ({note['time']})")
        return
    for note in notes_data:
        if query in note['text'].lower():
            content.insert(tk.END, f"[{note['priority']}] {note['text']} ({note['time']})")

def suggest(event=None):
    current = enteredText.get('1.0', tk.END).strip().lower()
    for note in notes_data:
        if note['text'].lower().startswith(current) and current != '':
            enteredText.delete('1.0', tk.END)
            enteredText.insert(tk.END, note['text'])
            break

enteredText = tk.Text(root, width='20', height='1')
enteredText.bind("<KeyRelease>", suggest)
addButton = tk.Button(root, text='Add', bg='lightblue', command=addText)
deleteButton = tk.Button(root, text='Delete', bg='red', command=delete)
content = tk.Listbox(root, width='40', height='10')
content.bind("<<ListboxSelect>>", choose)
saveButton = tk.Button(root, text='Save', bg='yellow', command=save)
loadButton = tk.Button(root, text='Load', bg='orange', command=load)
searchVar = tk.StringVar()
searchEntry = tk.Entry(root, textvariable=searchVar)
searchEntry.bind("<KeyRelease>", search)
priorityVar = tk.StringVar(value='Low')
priorityMenu = tk.OptionMenu(root, priorityVar, "Low", "Medium", "High")
enteredText.place(x=50, y=10)
addButton.place(x=20, y=40)
deleteButton.place(x=85, y=40)
content.place(x=10, y=80)
saveButton.place(x=80, y=260)
loadButton.place(x=130, y=260)
searchEntry.place(x=60, y=300)
priorityMenu.place(x=160, y=37)
root.mainloop()
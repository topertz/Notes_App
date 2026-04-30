import tkinter as tk
from tkinter import messagebox
import json
root = tk.Tk()
root.title('Notes App')
root.geometry('500x500')
root.configure(bg='lightgreen')

def addText():
    text = enteredText.get('1.0', tk.END).strip()
    if text != '':
        content.insert(tk.END, text)
        enteredText.delete('1.0', tk.END)
    else:
        messagebox.showerror("Üres", "Írj be valamit!")

def delete():
    if content.size() == 0:
        messagebox.showerror("Hiba", "A lista üres!")
    else:
        content.delete(0, tk.END)

def choose(event):
    selected = content.curselection()
    if selected:
        text = content.get(selected)
        enteredText.delete('1.0', tk.END)
        enteredText.insert(tk.END, text)

def save():
    notes = list(content.get(0, tk.END))
    if len(notes) == 0:
        messagebox.showerror("Hiba", "Nincs mit menteni!")
        return
    with open('notes.json', 'w', encoding='utf-8') as f:
        json.dump(notes, f, indent=4)
    messagebox.showinfo("Mentés", "Sikeres mentés!")

def load():
    try:
        with open('notes.json', 'r', encoding='utf-8') as f:
            notes = json.load(f)
        content.delete(0, tk.END)
        for note in notes:
            content.insert(tk.END, note)
    except FileNotFoundError:
        messagebox.showerror("Hiba", "Nincs mentett fájl!")
    except json.JSONDecodeError:
        messagebox.showerror("Hiba", "Sérült JSON fájl!")

enteredText = tk.Text(root, width='20', height='1')
addButton = tk.Button(root, text='Add', bg='lightblue', command=addText)
deleteButton = tk.Button(root, text='Delete', bg='red', command=delete)
content = tk.Listbox(root, width='25', height='10')
content.bind("<<ListboxSelect>>", choose)
saveButton = tk.Button(root, text='Save', bg='yellow', command=save)
loadButton = tk.Button(root, text='Load', bg='orange', command=load)
enteredText.place(x=10, y=10)
addButton.place(x=10, y=40)
deleteButton.place(x=60, y=40)
content.place(x=10, y=80)
saveButton.place(x=10, y=260)
loadButton.place(x=60, y=260)
root.mainloop()
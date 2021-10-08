import tkinter as tk
from tkinter import *
from PIL import Image
from PIL import ImageTk, Image
from tkinter import filedialog
from tkinter.filedialog import asksaveasfile
from tkinter import messagebox
from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo
from tkinter.messagebox import showwarning

win = tk.Tk()
win.geometry("1050x750+0+0")
win.config(bg="#074463")
win.title("stegonography")
win.resizable(width=True, height=True)
bg_color = "#074463"
fg_color = "white"
lbl_color = 'white'


def open_img():
    x = openfilename()
    print(x)

    img = Image.open(x)
    img = img.resize((460, 340), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel = Label(win, image=img)
    panel.image = img
    panel.place(x=30, y=150, width=450, height=340)


def openfilename():
    filename = filedialog.askopenfilename(title='"pen')
    return filename


def save():

    files = [('All Files', '*.*'),
             ('Python Files', '*.py'),
             ('Text Document', '*.txt'),
             ('png files','*.png')]
    file = asksaveasfile(filetypes = files, defaultextension = files)

    messagebox.showinfo("saved!!!", "Your image saved successfully!!!!!!!")


def genData(data):
    newd = []

    for i in data:
        newd.append(format(ord(i), '08b'))
    return newd


def modPix(pix, data):
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):
        pix = [value for value in imdata.__next__()[:3] +
               imdata.__next__()[:3] +
               imdata.__next__()[:3]]
        for j in range(0, 8):
            if (datalist[i][j] == '0') and (pix[j] % 2 != 0):
                if (pix[j] % 2 != 0):
                    pix[j] -= 1
                elif (datalist[i][j] == '1') and (pix[j] % 2 == 0):
                    pix[j] -= 1
        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                pix[-1] -= 1
        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]

def encode_enc(newimg, data):
    w = newimg.size[0]

    (x, y) = (0, 0)

    for pixel in modPix(newimg.getdata(), data):

        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1


def encodeText():
    global data
    data = " "
    img = bl_en.get()
    print()

    image = Image.open(img, 'r')
    data = va_en.get()
    print()

    if (len(data) == 0):
        showwarning('WARNING', 'Data is empty')
        breakpoint()
    newimg = image.copy()
    encode_enc(newimg, data)
    new_img_name = ch_en.get()
    newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))
    print("Image stored: " + new_img_name)
    showinfo('saved', 'Image stored:{},'.format(new_img_name))


def decode():

    img = de_en.get()
    print()
    image = Image.open(img, 'r')

    dataa = ''

    imgdata = iter(image.getdata())

    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
                  imgdata.__next__()[:3] +
                  imgdata.__next__()[:3]]

        binstr = ''

        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'

        dataa += chr(int(binstr, 2))

        if (pixels[-1] % 2 != 0):
            return dataa

def high():
    dep = ""
    dep = ("" + decode())
    showinfo('DECODE', 'Your Decoded Text is, {}'.format(dep))


def gettext():
    test_str = data
    w = ""
    te = ""
    print("original : " + str(test_str))
    res = ''.join(format(ord(i), 'b') for i in test_str)
    print("binary : " + str(res))
    ye = (str(res)[::-1])
    print(str(ye))
    for i in str(ye):
        if i == '1':
            w += "0"
        elif i == '0':
            w += "1"
        elif i == "b":
            w += 'b'
        else:
            pass
    print(w)

    def BinaryToDecimal(binary):
        binary1 = binary
        decimal, i, n = 0, 0, 0
        while (binary != 0):
            dec = binary % 10
            decimal = decimal + dec * pow(2, i)
            binary = binary // 10
            i += 1
        return (decimal)

    bin_data = str(w)
    print("The binary value is:", bin_data)
    str_data = ' '
    for i in range(0, len(bin_data), 7):
        temp_data = int(bin_data[i:i + 7])
        decimal_data = BinaryToDecimal(temp_data)
        str_data = str_data + chr(decimal_data)
    print("The encoded string which is visible to others:",
          str_data)
    showinfo('DECODE', 'Your Decoded Text is, {}'.format(str_data))

    #####decoding
    def BinaryToDecimal(binary):
        binary1 = binary
        decimal, i, n = 0, 0, 0
        while (binary != 0):
            dec = binary % 10
            decimal = decimal + dec * pow(2, i)
            binary = binary // 10
            i += 1
        return (decimal)

    bin_data = str(res)
    print("The binary value is:", bin_data)
    str_data = ' '
    for i in range(0, len(bin_data), 7):
        temp_data = int(bin_data[i:i + 7])
        decimal_data = BinaryToDecimal(temp_data)
        str_data = str_data + chr(decimal_data)
    print("The Binary value for decoding is:",
          str_data)


# ========================================clear===============================================

def clear():
    bl_en.delete(0, "end")
    va_en.delete(0, "end")
    ch_en.delete(0, "end")
    de_en.delete(0, "end")


# ========== Frame==========#
F1 = tk.LabelFrame(win, font=("time new roman", 15, "bold"), fg="gold", bg=bg_color, relief=GROOVE, bd=10)
F1.place(x=20, y=20, width=1010, height=105)

clear_btn = Button(win, text="CLEAR", bg=lbl_color, bd=7, pady=25, font="arial 15 bold", command=clear)
clear_btn.place(x=690, y=40, width=150, height=60)

exit_btn = Button(win, text="EXIT", bg=lbl_color, bd=7, pady=25, font="arial 15 bold", command=win.destroy)
exit_btn.place(x=860, y=40, width=150, height=60)

# ===============label===========#
cname_lbl = Label(F1, text="ABHEDY", bd=12, bg=bg_color, fg=fg_color, relief=FLAT, font=("times new roman", 30, "bold"))
cname_lbl.grid(row=1, column=1, padx=20, pady=5)

# ========frame2======#
F2 = LabelFrame(win, text='Image', bd=10, relief=GROOVE, bg=bg_color, fg="gold", font=("times new roman", 15, "bold"))
F2.place(x=20, y=130, width=480, height=370)

F3 = LabelFrame(win, text="Encode", bd=10, relief=GROOVE, bg=bg_color, fg="gold", font=("times new roman", 15, "bold"))
F3.place(x=550, y=130, width=480, height=200)

F4 = LabelFrame(win, text="Decode", bd=10, relief=GROOVE, bg=bg_color, fg="gold", font=("times new roman", 15, "bold"))
F4.place(x=550, y=350, width=480, height=150)

bl_lbl = Label(F3,font = ("times new roman",16,"bold"),fg = "lightgreen",bg = bg_color,text = "Enter Image Name:")
bl_lbl.grid(row = 0,column = 0,padx = 10,pady = 10,sticky="w")
bl_en = Entry(F3,width=15,font=("times new roman",16,"bold"),bd=5,relief=SUNKEN)
bl_en.grid(row = 0,column = 1,pady = 10,padx = 10)

# ===============#
va_lbl = Label(F3, font=("times new roman", 16, "bold"), fg="lightgreen", bg=bg_color, text="Enter The Text :")
va_lbl.grid(row=1, column=0, padx=10, pady=10, sticky="w")
va_en = Entry(F3, width=15, font=("times new roman", 16, "bold"), bd=5, relief=SUNKEN)
va_en.grid(row=1, column=1, pady=10, padx=10)

# ====================#
ch_lbl = Label(F3, font=("times new roman", 16, "bold"), fg="lightgreen", bg=bg_color, text="Enter New Image:")
ch_lbl.grid(row=2, column=0, padx=20, pady=10, sticky="w")
ch_en = Entry(F3, width=15, font=("times new roman", 16, "bold"), bd=5, relief=SUNKEN)
ch_en.grid(row=2, column=1, pady=10, padx=10)

de_lbl = Label(F4, font=("times new roman", 16, "bold"), fg="lightgreen", bg=bg_color, text="Enter New Image:")
de_lbl.grid(row=0, column=0, padx=10, pady=10, sticky="w")
de_en = Entry(F4, width=15, font=("times new roman", 16, "bold"), bd=5, relief=SUNKEN)
de_en.grid(row=0, column=1, pady=10, padx=10)

# ==================frame left bottom=======================#
F6 = LabelFrame(text="Open,Save", bd=10, relief=GROOVE, bg=bg_color, fg="gold", font=("times new roman", 15, "bold"))
F6.place(x=20, y=550, width=480, height=100)

open_btn = Button(win, text="OPEN", bg=lbl_color, bd=7, pady=25, font="arial 15 bold", command=open_img)
open_btn.place(x=50, y=580, width=200, height=50)

save_btn = Button(win, text="SAVE", bg=lbl_color, bd=7, pady=25, font="arial 15 bold", command=lambda: save())
save_btn.place(x=270, y=580, width=200, height=50)

# ==============frame ryt bottom======================#
F6 = LabelFrame(text="Stego fun", bd=10, relief=GROOVE, bg=bg_color, fg="gold", font=("times new roman", 15, "bold"))
F6.place(x=550, y=550, width=480, height=100)

hide_btn = Button(win, text="HIDE TEXT", bg=lbl_color, bd=7, pady=25, font="arial 15 bold", command=encodeText)
hide_btn.place(x=580, y=580, width=200, height=50)

get_btn = Button(win, text="GET TEXT", bg=lbl_color, bd=7, pady=25, font="arial 15 bold", command=gettext)
get_btn.place(x=800, y=580, width=200, height=50)

# ==============frame at bottom==============#
F10 = LabelFrame(text="Message", bd=10, relief=GROOVE, bg=bg_color, fg="gold", font=("times new roman", 15, "bold"))
F10.place(x=20, y=650, width=1010, height=60)

# ==============frame on save open===========#
F11 = LabelFrame(F6, bd=10, relief=FLAT, bg=lbl_color)
F11.place(x=30, y=560, width=460, height=80)

btn11 = tk.Button(win, font="arial 10 bold", bd=7, command=high)
btn11.place(x=0, y=720, width=1050, height=30)
win.mainloop()

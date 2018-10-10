#!/usr/bin/env python
import Tkinter as tk
import tkFileDialog as tkfile
import xml.etree.ElementTree

root = tk.Tk()
root.title("svg sticker")

flist = []
def fileClick():
	global flist
	fnamez = tkfile.askopenfilenames(parent=root, title="select all svgs", defaultextension='svg', filetypes=[('svg files','.svg')])
	flist = list(root.tk.splitlist(fnamez))
	fileMsg.config(state=tk.NORMAL)
	fileMsg.delete(1.0, tk.END)
	fileMsg.insert(tk.END, '\n'.join(flist))
	fileMsg.config(state=tk.DISABLED)

svgHeader1 = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg"
   baseProfile="full"
   version="1.1"
'''   
svgFooter = '''</svg>
'''

def generate(flist, w, dx, dy, px=0, py=0, piled=''):
	n = len(flist)

	xml.etree.ElementTree.register_namespace('', "http://www.w3.org/2000/svg")
	
	if not piled:
		widthStr = '   width="{}"'.format((dx+2*px)*w)
		heightStr = '   height="{}"'.format((dy+2*py)*((n+w-1)//w))
	else:
		widthStr = '   width="{}"'.format((dx+2*px)*1)
		heightStr = '   height="{}"'.format((dy+2*py)*1)		
	ans = svgHeader1 + widthStr + "\n" + heightStr + ">" + "\n"
	#ans = svgHeader1 + ">"
	for i in range(n):
		e = xml.etree.ElementTree.parse(flist[i]).getroot()
		#print "..."+str(e.attrib)+"..."
		newAtt = e.attrib
		if not piled:
			newAtt['x'] = str(i%w*(dx+2*px)+px)
			newAtt['y'] = str(i//w*(dy+2*py)+py)
		else:
			newAtt['x'] = str(0*(dx+2*px)+px)
			newAtt['y'] = str(0*(dy+2*py)+py)
		newAtt['width'] = str(dx)
		newAtt['height'] = str(dy)
		e.attrib = newAtt
		ans = ans + xml.etree.ElementTree.tostring(e) + '\n'
	ans = ans + svgFooter
	fname = tkfile.asksaveasfilename(parent=root, title="save as...", defaultextension='svg', filetypes=[('svg files','.svg')])
	if fname!='':
		with open(fname, "w") as fd:
			fd.write(ans)

def genBtnClick():
	n = len(flist)
	print "# of svgs="+str(n)
	newFlist = []
	for i in range( int(dupBox.get()) ):
		newFlist = newFlist + flist
	generate( newFlist, int(widthBox.get()), int(dxBox.get()), int(dyBox.get()), int(pxBox.get()), int(pyBox.get()), piledVar.get() )

#generate(['C:/Users/wolfdigit/Downloads/Geometric_Low_Poly_Deer_Head/svg/deer_head_reshaped-v3.6.1_slices_SVG/deer_head_reshaped-v3.6.1_slice_4.svg'], 1, 30, 30)



fileMsg = tk.Text(root)
fileMsg.insert(tk.END, "no file selected")
fileMsg.config(state=tk.DISABLED)
fileMsg.grid(row=0, column=0, columnspan=4)
fileBtn = tk.Button(root, text="open svg's", command=fileClick)
fileBtn.grid(row=1, column=0)

dupLbl = tk.Label(root, text="duplicate svgs for # times:")
dupLbl.grid(row=1, column=2)
dupBox = tk.Spinbox(root, from_=1, to=99)
dupBox.grid(row=1, column=3)

dxLbl = tk.Label(root, text="width:")
dxLbl.grid(row=2, column=0)
dxBox = tk.Spinbox(root, from_=-999, to=999)
dxBox.delete(0, tk.END)
dxBox.insert(0, "200")
dxBox.grid(row=2, column=1)

dyLbl = tk.Label(root, text="height:")
dyLbl.grid(row=2, column=2)
dyBox = tk.Spinbox(root, from_=-999, to=999)
dyBox.delete(0, tk.END)
dyBox.insert(0, "200")
dyBox.grid(row=2, column=3)

pxLbl = tk.Label(root, text="padding-x:")
pxLbl.grid(row=3, column=0)
pxBox = tk.Spinbox(root, from_=-999, to=999)
pxBox.delete(0, tk.END)
pxBox.insert(0, "0")
pxBox.grid(row=3, column=1)

pyLbl = tk.Label(root, text="padding-y:")
pyLbl.grid(row=3, column=2)
pyBox = tk.Spinbox(root, from_=-999, to=999)
pyBox.delete(0, tk.END)
pyBox.insert(0, "0")
pyBox.grid(row=3, column=3)

widthLbl = tk.Label(root, text="# of svgs in a row:")
widthLbl.grid(row=4, column=0)
widthBox = tk.Spinbox(root, from_=1, to=99)
widthBox.delete(0, tk.END)
widthBox.insert(0, "4")
widthBox.grid(row=4, column=1)

piledVar = tk.BooleanVar()
piledBox = tk.Checkbutton(root, text='piled together', variable=piledVar)
piledBox.grid(row=4, column=2)

genBtn = tk.Button(root, text="generate!", command=genBtnClick)
genBtn.grid(row=4, column=3)

root.mainloop()

# !/usr/bin/python 
# -*- coding: utf-8 -*-

"""
    Script for the integration of the GNU GPLv3 translated to Spanish
    into tex or html in order to save time.
    Copyright (C) 2013  Borja Menendez Moreno

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

import sys, os, re
# reload(sys)
# sys.setdefaultencoding('utf-8')

def usage():
	print 'Method of use:'
	print sys.argv[0] + ' <directory> <format>'
	print 'Example of use of integration of "dir" directory to a ".tex" format:'
	print sys.argv[0] + ' dir tex'

def convertTex(text):
	encoded = text
	encoded = encoded.replace('Á', "\\'A")
	encoded = encoded.replace('É', "\\'E")
	encoded = encoded.replace('Í', "\\'I")
	encoded = encoded.replace('Ó', "\\'O")
	encoded = encoded.replace('Ú', "\\'U")
	encoded = encoded.replace('Ñ', "\\~N")
	encoded = encoded.replace('á', "\\'a")
	encoded = encoded.replace('é', "\\'e")
	encoded = encoded.replace('í', "\\'i")
	encoded = encoded.replace('ó', "\\'o")
	encoded = encoded.replace('ú', "\\'u")
	encoded = encoded.replace('ñ', "\\~n")
	return encoded

def convertHtml(text):
	encoded = text
	encoded = encoded.replace('Á', "&Aacute;")
	encoded = encoded.replace('É', "&Eacute;")
	encoded = encoded.replace('Í', "&Iacute;")
	encoded = encoded.replace('Ó', "&Oacute;")
	encoded = encoded.replace('Ú', "&Uacute;")
	encoded = encoded.replace('Ñ', "&Ntilde;")
	encoded = encoded.replace('á', "&aacute;")
	encoded = encoded.replace('é', "&eacute;")
	encoded = encoded.replace('í', "&iacute;")
	encoded = encoded.replace('ó', "&oacute;")
	encoded = encoded.replace('ú', "&uacute;")
	encoded = encoded.replace('ñ', "&ntilde;")
	return encoded

def changeToTex(route, files):
	out = open('integrated.tex', 'w')
	for f in files:
		op = open(route + '/' + f, 'r')

		# Convert written accents into tex words
		read = convertTex(op.read())

		# Convert the titles of each section into items
		lines = read.split('\n')
		for line in lines:
			if re.match('.*[0-9]+\..*[a-zA-Z]\.', line):
				li = '\item' + line.split('.')[1]
				read = read.replace(line, li)

		# Convert the double quotes when required
		conv = True
		final = ''
		for word in read:
			if word == '"':
				if conv:
					word = '``'
				conv = not conv
			final += word

		out.write(final)
		out.write('\r\n')
		op.close()

	out.close()

def changeToHtml(route, files):
	out = open('integrated.html', 'w')
	for f in files:
		op = open(route + '/' + f, 'r')

		# Convert written accents into html words
		read = convertHtml(op.read())

		# Convert the titles of each section into:
		# <h4><a name="section<number>"></a><section_name></h4>
		# as in the original GNU GPLv3 html document
		lines = read.split('\n')
		section = 0
		for line in lines:
			if re.match('.*[0-9]+\..*[a-zA-Z]\.', line):
				li = '<h4><a "name=section' + str(section) + '"></a>' + line + '</h4>'
				read = read.replace(line, li)
				section += 1

		# Convert each paragraph into <p><paragraph></p>
		paragraphs = read.split('\n\n')
		for paragraph in paragraphs:
			par = '<p>' + paragraph + '</p>'
			read = read.replace(paragraph, par)

		# Convert the double quotes when required
		left = True
		final = ''
		for word in read:
			if word == '"':
				if left:
					word = '&ldquo;'
				else:
					word = '&rdquo;'
				left = not left
			final += word

		out.write(final)
		op.close()

	out.close()

def changeTo(route, files, format):
	if format == 'tex':
		changeToTex(route, files)
	elif format == 'html':
		changeToHtml(route, files)
	else:
		print 'The format ' + format + ' is not supported in this version'
		print 'Formats supported: tex, html'

if len(sys.argv) < 3:
	print 'Please, introduce at least a directory and a format'
	usage()
	sys.exit(1)

fi = sys.argv[1]
directorio = os.path.isdir(fi)

formats = sys.argv[2:]

if directorio:
	myFiles = os.listdir(fi)
	myFiles = sorted(myFiles)
	for format in formats:
		changeTo(fi, myFiles, format)
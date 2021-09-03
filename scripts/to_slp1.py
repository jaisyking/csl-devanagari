# coding=utf-8
import codecs
import sys
import os
import re
from indic_transliteration import sanscript
from parseheadline import parseheadline

def convert_metaline(dictcode):
	filein = os.path.join('..', 'slp1', dictcode + '.txt')
	fin = codecs.open(filein, 'r', 'utf-8')
	data = fin.read()
	fin.close()
	result = []
	lines = data.split('\n')
	for lin in lines:
		if lin.startswith('<L>'):
			result.append(sanscript.transliterate(lin, 'devanagari', 'slp1'))
		else:
			result.append(lin)
	fout = codecs.open(filein, 'w', 'utf-8')
	fout.write('\n'.join(result))
	fout.close()

def convert_to_slp1(data):
	result = []
	lines = data.split('\n')
	for lin in lines:
		if lin.startswith('<L>') or lin.startswith('[Page') or lin.startswith('<H>') or lin.startswith('<LEND>'):
			result.append(lin)
		else:
			result.append(sanscript.transliterate(lin, 'devanagari', 'slp1'))
	return '\n'.join(result)


def convert_partially_to_slp1(startMark, endMark, outputTranslit, data):
	reg = startMark + '.*?' + endMark
	splt = re.split(r'(' + reg + ')', data)
	result = []
	for i in range(len(splt)):
		if i % 2 == 0:
			result.append(splt[i])
		else:
			result.append(sanscript.transliterate(splt[i], 'devanagari', outputTranslit))
	return ''.join(result)


def run_code(dictcode):
	filein = os.path.join('..', 'v02', dictcode, dictcode + '.txt')
	fin = codecs.open(filein, 'r', 'utf-8')
	data = fin.read()
	fin.close()
	fileout = os.path.join('..', 'slp1', dictcode + '.txt')
	fout = codecs.open(fileout, 'w', 'utf-8')
	if dictcode in ['vcp', 'skd', 'armh']:
		data = convert_to_slp1(data)
	elif dictcode in ['lan', 'gra']:
		data = convert_partially_to_slp1('{@', ',@}', 'iast', data)
	elif dictcode in ['md']:
		data = convert_partially_to_slp1('{#', '#}', 'slp1', data)
		data = convert_partially_to_slp1('{@', ',@}', 'iast', data)
	elif dictcode in ['mw', 'krm']:
		data = convert_partially_to_slp1('<s>', '</s>', 'slp1', data)
	elif dictcode in ['ap90', 'mwe', 'bor', 'ae', 'pwg', 'pw', 'ccs', 'mw72', 'bop', 'inm', 'vei', 'pui', 'bhs', 'acc', 'ieg', 'snp', 'pe', 'pgn', 'mci', 'ben']:
		data = convert_partially_to_slp1('{#', '#}', 'slp1', data)
	else:
		data = convert_partially_to_slp1('{#', '#}', 'slp1', data)
		data = convert_partially_to_slp1('{%', '%}', 'iast', data)
	fout.write(data)
	fout.close()
	
if __name__ == "__main__":
	dictcode = sys.argv[1]
	run_code(dictcode)
	convert_metaline(dictcode)

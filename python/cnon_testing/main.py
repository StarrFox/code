#!/usr/bin/python3
# -*- coding: utf8 -*-

import requests
import re


alphabet = "ABCÇDEFGHIİJKLMNOÖPRSŞTUÜVYZ"

def readPage(letter):
	url = "https://tr.wiktionary.org/w/index.php?title=Kategori:Türkçe_sözcükler&from=(" + letter + ")"
	headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-9,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

	with requests.get(url, headers=headers) as res:
		content = res.text

	words = re.findall('<li><a[^>]*>([^<]+)<\/a>', content, flags=0)
	words.pop()
	print("Read the letter ", letter)
	return words


def getWordList():
	words = []
	for letter in alphabet:
		words += readPage(letter)
	return words


def writeToFile(filename):
	with open(filename, "w+", encoding="utf-16") as fp:
		words = getWordList()
		fp.write("\n".join(words))


writeToFile("words.txt")

# 
# Test Functions preloaded into the CogServer

from opencog.atomspace import types, Atom, TruthValue
from opencog.type_constructors import *

globalkount = 26666

def calcAttention(object,frame,type,subtype,color,size,distance):


    attention = 0.0

    attention = subtypeAttn(subtype,attention)
    attention = colorAttn(color,attention)
    attention = sizeAttn(size,attention)
    attention = distanceAttn(distance,attention)

    nodeAttn = ATOMSPACE.add_node(types.NumberNode,str(attention))
    linkAttn = ATOMSPACE.add_link(types.ListLink,[object,nodeAttn])
    return linkAttn


def subtypeAttn(item,attention):
    name = item.name
    if (name == "Goat"): attention = attention + 5
    if (name == "Deer"): attention = attention + 10
    return attention

def colorAttn(item,attention):
    name = item.name
    if (name == "White"): attention = attention + 2
    if (name == "Brown"): attention = attention + 3
    if (name == "Red"): attention = attention + 7
    if (name == "Grey"): attention = attention + 4
    if (name == "Red"): attention = attention + 5

    return attention

def sizeAttn(item,attention):
    name = item.name
    if (name == "Small"): attention = attention + 1
    if (name == "Medium"): attention = attention + 3
    if (name == "Large"): attention = attention + 5

    return attention

def distanceAttn(item,attention):
    distance = float(item.name)

    attention = attention * (20.0/distance)

    return attention

def flashprint(astring, bstring):
    print astring, bstring


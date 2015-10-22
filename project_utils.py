__author__ = 'jimrutt'
from opencog.atomspace import Atom, AtomSpace, TruthValue, types, get_type_name
from opencog.scheme_wrapper import load_scm, scheme_eval, scheme_eval_h, __init__
from opencog.utilities import initialize_opencog, finalize_opencog
import zmq
import random
import sys
import time
import collections
import math

def  ontology_setup(atomspace,TRUTH_VALUE):

    atomspace.clear()

    OBJECTS = atomspace.add_node(types.ConceptNode, "Objects",TRUTH_VALUE)
    GAMEOBJECTS = atomspace.add_node(types.ConceptNode, "GameObjects",TRUTH_VALUE)
    VISIONOBJECTS = atomspace.add_node(types.ConceptNode, "VisionObjects",TRUTH_VALUE)
    ATTRIBUTES = atomspace.add_node(types.ConceptNode, "Attributes",TRUTH_VALUE)

    COLORS = atomspace.add_node(types.ConceptNode, "Colors",TRUTH_VALUE)


    TYPES = atomspace.add_node(types.ConceptNode, "Types",TRUTH_VALUE)

    SIZES = atomspace.add_node(types.ConceptNode, "Sizes",TRUTH_VALUE)

    LOCATIONS = atomspace.add_node(types.ConceptNode, "Locations",TRUTH_VALUE)
    GLOBALXY = atomspace.add_node(types.ConceptNode, "GlobalXY",TRUTH_VALUE)
    TIMES = atomspace.add_node(types.ConceptNode, "Times",TRUTH_VALUE)
    EPISODE1 = atomspace.add_node(types.ConceptNode, "Episode_1",TRUTH_VALUE)


    build_ontology = \
    '''
    (InheritanceLink (ConceptNode "GameObjects") (ConceptNode "Objects"))
    (InheritanceLink (ConceptNode "VisualObjects") (ConceptNode "GameObjects"))
    (InheritanceLink (ConceptNode "Colors") (ConceptNode "Attributes"))
    (InheritanceLink (ConceptNode "Types") (ConceptNode "Attributes"))
    (InheritanceLink (ConceptNode "Sizes") (ConceptNode "Attributes"))
    (InheritanceLink (ConceptNode "Large") (ConceptNode "Sizes"))
    (InheritanceLink (ConceptNode "GlobalXY") (ConceptNode "Locations"))
    (InheritanceLink (ConceptNode "Episode_1") (ConceptNode "Times"))
    '''
    result = scheme_eval_h(atomspace, build_ontology)

    return

def printatoms(atomspace):

    my_nodes = atomspace.get_atoms_by_type(types.ConceptNode)

    for i in my_nodes:
        print i

    my_nodes = atomspace.get_atoms_by_type(types.InheritanceLink)

    for i in my_nodes:
        print i

    my_nodes = atomspace.get_atoms_by_type(types.PredicateNode)

    for i in my_nodes:
        print i

    my_nodes = atomspace.get_atoms_by_type(types.EvaluationLink)
    for i in my_nodes:
        print i

    my_nodes = atomspace.get_atoms_by_type(types.ListLink)
    for i in my_nodes:
        print i

def createFrame(atomspace, currentEpisode,framename, TRUTH_VALUE):
    ceNode = atomspace.add_node(types.ConceptNode, currentEpisode,TRUTH_VALUE)
    fnNode = atomspace.add_node(types.ConceptNode, framename,TRUTH_VALUE)
    atomspace.add_link(types.InheritanceLink,[fnNode,ceNode])

    return fnNode

def processOBJmsg(atomspace,MsgFields,MyLocation, frameNode, TRUTH_VALUE):


    objrootNode = atomspace.add_node(types.ConceptNode,"Objects",TRUTH_VALUE)
    objNode = atomspace.add_node(types.ConceptNode,MsgFields.objname,TRUTH_VALUE)
    il0 = atomspace.add_link(types.InheritanceLink,[objNode,objrootNode])

    typesNode = atomspace.add_node(types.ConceptNode,"Types",TRUTH_VALUE)
    typeNode = atomspace.add_node(types.ConceptNode,MsgFields.type,TRUTH_VALUE)
    il1 = atomspace.add_link(types.InheritanceLink,[typeNode,typesNode])

    subtypeNode = atomspace.add_node(types.ConceptNode,MsgFields.subtype,TRUTH_VALUE)
    atomspace.add_link(types.InheritanceLink,[subtypeNode,typeNode])


    colorsNode = atomspace.add_node(types.ConceptNode,"Colors",TRUTH_VALUE)
    colorNode = atomspace.add_node(types.ConceptNode,MsgFields.color,TRUTH_VALUE)
    il2 = atomspace.add_link(types.InheritanceLink,[colorNode,colorsNode])

    sizesNode = atomspace.add_node(types.ConceptNode,"Sizes",TRUTH_VALUE)
    sizeNode = atomspace.add_node(types.ConceptNode,MsgFields.size,TRUTH_VALUE)
    il3 = atomspace.add_link(types.InheritanceLink,[sizeNode,sizesNode])

    distanceflt = math.sqrt(((MyLocation.locx - MsgFields.locx) ** 2) + ((MyLocation.locy - MsgFields.locy)** 2) + ((MyLocation.locz - MsgFields.locz) ** 2))
    distancestr = str(distanceflt)


    distanceNode = atomspace.add_node(types.NumberNode,distancestr,TRUTH_VALUE)

    # need to add predicates and locations
    predicateName = "ObjectAttributesInFrame"
    attributePred = createPredicate(atomspace,predicateName,[objNode,frameNode,typeNode,subtypeNode, colorNode,sizeNode,distanceNode],TRUTH_VALUE)

def createPredicate(atomspace,predicateName,paramslist,TRUTH_VALUE):
    prNode = atomspace.add_node(types.PredicateNode,predicateName,TRUTH_VALUE)
    llLink = atomspace.add_link(types.ListLink,paramslist)
    evLink = atomspace.add_link(types.EvaluationLink,[prNode,llLink])

def getAttention(atomspace, MsgFields,framename):
    qoutedframename = chr(34) + framename + chr(34)
    scheme_bindlink_function = \
    '''
    (define get-objs-with-attributes
        (BindLink

            (VariableList
                (VariableNode "$object")
                (VariableNode "$type")
                (VariableNode "$subtype")
                (VariableNode "$color")
                (VariableNode "$size")
                (VariableNode "$distance")
            )


            (EvaluationLink
                (PredicateNode "ObjectAttributesInFrame")
                    (ListLink
                        (VariableNode "$object")
                        (ConceptNode   %s)
                        (VariableNode "$type")
                        (VariableNode "$subtype")
                        (VariableNode "$color")
                        (VariableNode "$size")
                        (VariableNode "$distance")
                    )
            )
            (ExecutionOutputLink
                (GroundedSchemaNode "py:test_functions.calcAttention")
                (ListLink
                    (VariableNode "$object")
                    (ConceptNode   %s)
                    (VariableNode "$type")
                    (VariableNode "$subtype")
                    (VariableNode "$color")
                    (VariableNode "$size")
                    (VariableNode "$distance")



                )
            )
        )
    )
    '''  \
    % (qoutedframename,qoutedframename)
    result = scheme_eval(atomspace,scheme_bindlink_function)



    result = scheme_eval(atomspace,"(cog-bind get-objs-with-attributes)")

    # replace the following with RegEx, but doesn't really matter only called once per frame
    result = result.replace("(", " ")
    result = result.replace(")"," ")
    result = result.replace("\n"," ")
    result = result.replace("\"","")

    tokensAttn = result.split()

    topObj = "NULL"
    topAttn = -1.0
    lasttoken = ""

    for token in tokensAttn:
        if (lasttoken == "ConceptNode"): itemObj = token
        if (lasttoken == "NumberNode"):
            itemAttn = float(token)
            if (itemObj == ""):
                print "bad object in getAttention"
                exit()
            if (itemAttn > topAttn):
                topAttn = itemAttn
                topObj = itemObj
                itemObj = ""

        lasttoken = token

    return topObj,topAttn


def setupzmqsend(context,ipaddress):
    sendsocket = context.socket(zmq.PUB)
    fulladdress = "tcp://" + ipaddress + ":5561"
    sendsocket.connect(fulladdress)
    return sendsocket

def sendmessagezmq(sendsocket,message):
    sendsocket.send(message)


def setupzmq(ipaddress):
    context = zmq.Context()
    rcvsocket = context.socket(zmq.SUB)
    rcvsocket.set_hwm(1000000)
    try:
        fulladdress = "tcp://" + ipaddress + ":5560"

        rcvsocket.connect(fulladdress)
    except:
        print "oops bad socket.connect in setupzmq"
        exit()
    return (context , rcvsocket)

def setzmqsubprofile(profile,rcvsocket):
    profile = ""
    rcvsocket.setsockopt(zmq.SUBSCRIBE,profile)

def parsemessage(message):
    parsedmessage = message.split()
    tokenkount = len(parsedmessage)
    channel = parsedmessage[0]
    source = parsedmessage[1]
    msgtype = parsedmessage[2]
    if (channel != "444" or source != "U"):
        print "parsemessage: bad channel number or source designator"
        exit()


    if ( msgtype  == "OBJ"):
        MsgFields = collections.namedtuple("MsgFields",["kount","msgtype","frame","objname","type","subtype","color","size","locx","locz"])

        MsgFields.kount = tokenkount
        MsgFields.msgtype = parsedmessage[2]
        MsgFields.frame = int(parsedmessage[3])
        MsgFields.objname =  parsedmessage[4]
        MsgFields.type = parsedmessage[5]
        MsgFields.subtype = parsedmessage[6]
        MsgFields.color = parsedmessage[7]
        MsgFields.size = parsedmessage[8]
        MsgFields.locx = float(parsedmessage[9])
        MsgFields.locy = float(parsedmessage[10])
        MsgFields.locz = float(parsedmessage[11])

        return MsgFields
    elif (msgtype == "STARTFRAME"):
        MsgFields = collections.namedtuple("MsgFields",["kount","msgtype","frame","locx","locy","locz"])

        MsgFields.kount = tokenkount
        MsgFields.msgtype = parsedmessage[2]
        MsgFields.frame = int(parsedmessage[3])

        MsgFields.locx = float(parsedmessage[4])
        MsgFields.locy = float(parsedmessage[5])
        MsgFields.locz = float(parsedmessage[6])

        return MsgFields

    elif (msgtype == "ENDFRAME"):
        MsgFields = collections.namedtuple("MsgFields",["kount","msgtype","frame"])

        MsgFields.kount = tokenkount
        MsgFields.msgtype = parsedmessage[2]
        MsgFields.frame = int(parsedmessage[3])

        return MsgFields
    elif (msgtype == "STARTOPENCOG"):
        MsgFields = collections.namedtuple("MsgFields",["kount","msgtype","frame"])

        MsgFields.kount = tokenkount
        MsgFields.msgtype = parsedmessage[2]
        MsgFields.frame = int(parsedmessage[3])

        return MsgFields
    else:
        print "unknown message type in  message"
        exit()

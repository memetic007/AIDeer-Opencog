__author__ = 'jimrutt'
from opencog.atomspace import Atom, AtomSpace, TruthValue, types, get_type_name
from opencog.scheme_wrapper import load_scm, scheme_eval, scheme_eval_h, __init__
from opencog.utilities import initialize_opencog, finalize_opencog
import time
import random
import project_utils as pu
import zmq
import sys
import collections
import os

try:
    ipaddress = str(sys.argv[1])

except:
    print "ipaddress missing or bad as parameter"
    exit()


atomspace = AtomSpace()
__init__(atomspace)

debugflag = False
data = ["/usr/local/share/opencog/scm/core_types.scm",
      "/usr/local/share/opencog/scm/utilities.scm"]

for item in data:
    load_scm(atomspace, item)

# Add to scheme's %load-path directory to serach for opencog guile modules
scheme_eval(atomspace, "(add-to-load-path \"/usr/local/share/opencog/scm\")")

# Import opencog modules required for using `cog-bind` in scheme_eval
scheme_eval(atomspace, "(use-modules (opencog))")
scheme_eval(atomspace, "(use-modules (opencog query))")

initialize_opencog(atomspace,str(os.getcwd()) + "/AIDeerProto001.conf")

TRUTH_VALUE = TruthValue(1,1)

pu.ontology_setup(atomspace,TRUTH_VALUE)


if (debugflag):
    pu.printatoms(atomspace)


context , rcvsocket = pu.setupzmq(ipaddress)

sendsocket = pu.setupzmqsend(context,ipaddress)


pu.setzmqsubprofile("444",rcvsocket)  # my channel number
print "starting to receive"
kount = 0



currentEpisode = "Episode_1"
framekount = 0
cogbindkount = 0
while True:
    #  Wait for next request from client
    kount = kount + 1
    try:
        message = rcvsocket.recv()
    except:
        print "ooops no recv"
        exit()

    # print message

    MsgFields = pu.parsemessage(message)


    if (MsgFields.msgtype == "OBJ"):
        pu.processOBJmsg(atomspace,MsgFields,MyLocation, frameNode,TRUTH_VALUE)

    elif (MsgFields.msgtype == "STARTFRAME"):


        framename = "Frame_" + str(MsgFields.frame)
        currentEpisode = currentEpisode

        frameNode = pu.createFrame(atomspace,currentEpisode,framename,TRUTH_VALUE)
        framekount = framekount + 1

        MyLocation = collections.namedtuple("MyLocation",["locx","locy","locz"])
        MyLocation.locx = MsgFields.locx
        MyLocation.locy = MsgFields.locy
        MyLocation.locz = MsgFields.locz

        #if (framekount > 20):
        #   pu.printatoms(atomspace)

         #    exit()
    elif (MsgFields.msgtype == "ENDFRAME"):

        objAttn, attention = pu.getAttention(atomspace,MsgFields,framename)
        message = "444 UNITY " + str(MsgFields.frame) + " " + objAttn + " " + str(attention)
        pu.sendmessagezmq(sendsocket,message)
        cogbindkount = cogbindkount + 1
        print "Frame: " + str(MsgFields.frame) + " Attention Object: " + str(objAttn) + " Attention Value: " + str(attention)
        #if (cogbindkount > 1200):
        #  exit()

    elif (MsgFields.msgtype == "STARTOPENCOG"):
        pu.ontology_setup(atomspace,TRUTH_VALUE)  # reinitializes atomspace
        message = "444 UNITY " + str(MsgFields.frame) + " OPENCOGSTARTED"
        pu.sendmessagezmq(sendsocket,message)
        print "sent: " + message
    else:
        print "bad message type"
        exit()

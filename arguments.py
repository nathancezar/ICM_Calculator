__author__ = 'Equipe-ECV'

import sys
import argparse
import json

def getJson():
    try :
        args = json.loads(sys.argv[1])

    except json.decoder.JSONDecodeError:
        import ipdb; ipdb.set_trace(context=10)
        return None
    else:
        return args

def getArguments():
    ap = argparse.ArgumentParser()
    ap.add_argument("--highway", required=True,
                    help="Highway to calculate icm")
    ap.add_argument("--direction", required=True,
                    help="Direction of the video: 0: Cresc / 1: Decresc")
    ap.add_argument("--contract", help="contract identifier")

    return vars(ap.parse_args())

def parseArguments():
    arguments = getJson()
    if not arguments:
        arguments = getArguments()
    return arguments

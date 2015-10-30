from pyramid.security import (
    Allow,
    Everyone,
    )

USERS = {'test':'editor'}
GROUPS = {'editor':['group:editors']}
PASS = {'test':'$6$RQsSr5F9rGSV5RBC$3vgKuUCu2oPkcTNX40QpnGwHZNLstgpLxyRcv88PN95bpmfiGugAagXRFrRNyuUCzp9A2NdJBoUFemrczIRZT.'}

class RootFactory(object):
    __acl__ = [ (Allow, Everyone, 'view'),
                (Allow, 'test', 'edit'), ]
    def __init__(self, request):
        pass

def groupfinder(userid, request):
    if userid in USERS:
        return GROUPS.get(userid, [])

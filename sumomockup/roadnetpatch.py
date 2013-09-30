            
class MyEdge(object):
    '''
    Mocks sumolib.net.Edge. Has basic functions used in the tests
    
    '''
    
    
    
    #_incoming #= []
    #_outgoing #= []
    
    def __init__(self, edg_id):
        self._edge_id = edg_id
        self._length = 100
        self._speed = 10
        self._lanes = 1
        self._incoming = []
        self._outgoing = []
        
    def getID(self):
        return self._edge_id
    
    def getSpeed(self):
        return self._speed
    
    def getLength(self):
        return self._length
    
    def getLaneNumber(self):
        return self._lanes
    
    def addIncoming(self, inc_edge):
        self._incoming.append(inc_edge)
        
    def addOutgoing(self, out_edge):
        self._outgoing.append(out_edge)
        #print 'Outgoing: ', [e.getID() for e in self._outgoing]
    def getIncoming(self):
        return self._incoming
    
    def getOutgoing(self):
        return self._outgoing

class MyRoadNetwork(object):
    """
    This is a mock for sumolib.net.Net class for use in the 
    unit tests. This class represents the following network:
              e2
    e1   ---->-----    e4
    --->-|        |-->--
         ---->-----
              e3  
    
    e1 has e2 and e3 as outgoing edges. Both e2 and e3 join on e4.
               
    """          
    
    def __init__(self):
        e1 = MyEdge('e1')
        e2 = MyEdge('e2')
        e3 = MyEdge('e3')
        e4 = MyEdge('e4')
        
        e1.addOutgoing(e2); e2.addIncoming(e1)
        e1.addOutgoing(e3); e3.addIncoming(e1)
        e2.addOutgoing(e4); e4.addIncoming(e2)
        e3.addOutgoing(e4); e4.addIncoming(e3)

        self._edges = [e1, e2, e3, e4]
    
    def getEdges(self):
        return self._edges
    
    def getEdge(self, edg_id):
        for e in self._edges:
            if edg_id == e.getID():
                return e
        return None

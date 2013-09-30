'''
Created on Jan 4, 2013

@author: anderson
'''

import unittest
import traci

import sys, os
sys.path.append(os.path.join('..','sumomockup'))
import tracipatch
import roadnetpatch


class Test(unittest.TestCase):
    def setUp(self):
        self.newtraci = tracipatch.TraCIReplacement(roadnetpatch.MyRoadNetwork())
        self.newtraci.perform_patch()

    def test_vehicle_getRoute(self):
        
        traci.route.add('test', ['e1', 'e2', 'e4'])
        traci.vehicle.add('v1', 'test')
        
        self.assertEqual(['e1', 'e2', 'e4'], traci.vehicle.getRoute('v1'))
        
    def test_count_vehicles_in_edge(self):
        
        traci.route.add('test', ['e1', 'e2', 'e4'])
        for i in range(0, 1000):
            traci.vehicle.add(str(i), 'test')
            self.newtraci.set_edge_for_vehicle('e1', str(i))
            
        self.assertEqual(1000, self.newtraci.count_vehicles_in_edge('e1'))
        
        
#    def test_getLastStepOccupancy(self):
#        for i in range(0, 1000):
#            traci.route.add('test', ['e1', 'e2', 'e4'])
#            traci.vehicle.add(str(i), 'test')
#            self.newtraci.set_edge_for_vehicle('e1', str(i))
#        
#        self.assertEqual(first, second, msg)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_getRoute']
    unittest.main()
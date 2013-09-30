import traci

class TraCIReplacement(object):
    '''
    Provides replacement for some traci functions for use 
    in the unit tests
    
    '''
    
    def __init__(self, road_network):
        '''
        Initializes the traci replacement.
        Default occupancy for the road network edges are initialized
        
        '''
        self._road_net = road_network
        self._ticks = 0
        
        self._vehicles = {}
        self._routes = {}
        self._occupancies = {} #map edge IDs to edge's occupancy
        
        self._edges_of_vehicles = {} #maps vehicle IDs to edge IDs
        self._edge_lengths = {} #maps edges to numbers
        self._veh_positions = {} #maps vehicle IDs to number (position in lane)
        self._veh_colors = {}    #maps vehicle IDs to colors
        
        #initialize occupancy to the default value
        for e in self._road_net.getEdges():
            self._occupancies[e.getID()] = .5
    
    
    def vehicle_add(self, vehID, routeID, depart_time = traci.vehicle.DEPART_NOW, 
                    depart_pos=0, lane=0, typeID="DEFAULT_VEHTYPE"):
        '''
        Replacement for traci.vehicle.add
        
        '''
        if not routeID in self._routes:
            raise ValueError('Route ID %s not found' % routeID)
        
        if vehID in self._vehicles:
            raise ValueError('Vehicle ID %s already exists!' % vehID)
        
        self._vehicles[vehID] = {'id': vehID, 'rid': routeID, 
                                 'dtime': depart_time, 'dpos': depart_pos, 
                                 'lane': lane}
    
    def vehicle_getIDList(self):
        '''
        Replacement for traci.vehicle.getIDLIst
        
        '''
        return self._vehicles.keys()
    
    def vehicle_getRoute(self, vehID):
        '''
        Replacement for traci.vehicle.getRoute
        
        '''
        return self._routes[self._vehicles[vehID]['rid']]
    
    def route_add(self, route_id, edges):
        '''
        Replacement for traci.route.add
        
        '''
        
        if route_id in self._routes:
            raise ValueError("Key %s already exists!" % route_id)
        
        self._routes[route_id] = edges 
        
    def edge_getLastStepOccupancy(self, edgeID):
        '''
        Replacement for traci.edge.getLastStepOccupancy
        
        '''
        
        return self._occupancies[edgeID]
    
    def perform_patch(self):
        '''
        Replaces some traci functions with this class' methods
        
        '''
        traci.vehicle.add = self.vehicle_add
        traci.vehicle.getIDList = self.vehicle_getIDList
        traci.vehicle.getRoadID = self.get_edge_for_vehicle
        traci.vehicle.getLanePosition = self.get_lane_position
        traci.vehicle.getRoute = self.vehicle_getRoute
        traci.vehicle.setColor = self.vehicle_setColor
        
        traci.route.add = self.route_add
        
        traci.edge.getLastStepOccupancy = self.edge_getLastStepOccupancy
        traci.lane.getLength = self.get_lane_length
        
        traci.simulationStep = self.tick
        traci.simulation.getCurrentTime = self.ticks
        
    def tick(self, num_ticks = 0):
        '''
        Advances the clock by 1000 time units (same behavior as traci)
        
        '''
        if num_ticks == 0:
            self._ticks += 1000
        else:
            self._ticks += num_ticks
    
        
    def ticks(self):
        '''
        Returns the number of ticks 
        
        '''
        return self._ticks
    
    def set_lane_position(self, veh_id, pos):
        '''
        Sets the position of a vehicle in a lane
        
        '''
        self._veh_positions[veh_id] = pos
        
    def vehicle_setColor(self, veh_id, rgba):
        '''
        Stores the color of a vehicle
        
        '''
        self._veh_colors[veh_id] = rgba
        
    def get_lane_position(self, veh_id):
        '''
        Returns the position of a vehicle in the lane
        
        '''
        return self._veh_positions[veh_id]
    
    def set_edge_length(self, edg_id, length):
        '''
        Sets the length for the given edge
        
        '''
        self._edge_lengths[edg_id] = length
        
    def get_edge_length(self, edg_id):
        '''
        Returns the length of an edge
        
        '''
        return self._edge_lengths[edg_id]
    
    def get_lane_length(self, lane_id):
        '''
        Returns the length of a lane
        
        '''
        edge_id = ''.join(lane_id.split('_')[:-1])
        return self._edge_lengths[edge_id]
    
    def set_edge_for_vehicle(self, edg_id, veh_id):
        '''
        Sets the edge for a given vehicle. Useful for testing if a 
        vehicle acts correctly when it changes its edge
        
        '''
        self._edges_of_vehicles[veh_id] = edg_id 
        
        
        
    def count_vehicles_in_edge(self, edg_id):
        '''
        Returns the number of vehicles in the given edge
        
        '''
        count = 0
        for vid,eid in self._edges_of_vehicles.items():
            if eid == edg_id:
                count += 1
        
        return count
        
    def get_edge_for_vehicle(self, veh_id):
        '''
        Returns the edge for a given vehicle or throws an error
        if it was not previously set with set_edge_for_vehicle
        
        '''
        return self._edges_of_vehicles[veh_id]
        
    def remove_vehicles(self, num):
        '''
        Removes num vehicles from my internal list. This is to simulate
        vehicles being removed in the actual simulation
        
        '''
        
        num_to_remove = min(num, len(self._vehicles))
        veh_ids = self._vehicles.keys()
        for i in range(0, num_to_remove):
            self.remove_vehicle(veh_ids[i])
    
    def remove_vehicle(self, veh_id):
        '''
        Removes the given vehicle from the internal list of vehicles.
        Useful to simulate vehicles finishing their trips
        
        '''
        del self._vehicles[veh_id]
         
        if veh_id in self._edges_of_vehicles: 
            del self._edges_of_vehicles[veh_id]
            
        if veh_id in self._veh_positions: 
            del self._veh_positions[veh_id]
        
    @property
    def num_vehicles(self):
        return len(self._vehicles)
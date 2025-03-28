from mesa import Model
from mesa.time import BaseScheduler
from mesa.space import ContinuousSpace
from components import Source, Sink, SourceSink, Bridge, Link, Intersection
import pandas as pd
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt

# ---------------------------------------------------------------
def set_lat_lon_bound(lat_min, lat_max, lon_min, lon_max, edge_ratio=0.02):
    """
    Set the HTML continuous space canvas bounding box (for visualization)
    give the min and max latitudes and Longitudes in Decimal Degrees (DD)

    Add white borders at edges (default 2%) of the bounding box
    """

    lat_edge = (lat_max - lat_min) * edge_ratio
    lon_edge = (lon_max - lon_min) * edge_ratio

    x_max = lon_max + lon_edge
    y_max = lat_min - lat_edge
    x_min = lon_min - lon_edge
    y_min = lat_max + lat_edge
    return y_min, y_max, x_min, x_max


# ---------------------------------------------------------------
class BangladeshModel(Model):
    """
    The main (top-level) simulation model

    One tick represents one minute; this can be changed
    but the distance calculation need to be adapted accordingly

    Class Attributes:
    -----------------
    step_time: int
        step_time = 1 # 1 step is 1 min

    path_ids_dict: defaultdict
        Key: (origin, destination)
        Value: the shortest path (Infra component IDs) from an origin to a destination

        Only straight paths in the Demo are added into the dict;
        when there is a more complex network layout, the paths need to be managed differently

    sources: list
        all sources in the network

    sinks: list
        all sinks in the network

    travel_times: list
        all travel times in minutes (ticks) of trucks that arrived at a sink

    broken_bridges: int
        number of bridges that have broken during the simulation

    breakdown_probabilities: dictionary
        probability to breakdown per each bridge category A-D
        F is 0 for every scenario and is given to links, sources, sinks and intersections
    """

    step_time = 1

    file_name = '../data/final_input_data.csv'

    def __init__(self, seed=None, x_max=500, y_max=500, x_min=0, y_min=0, breakdown_probabilities = {}):

        self.schedule = BaseScheduler(self)
        self.running = True
        self.path_ids_dict = defaultdict(lambda: pd.Series())
        self.space = None
        self.sources = []
        self.sinks = []
        self.travel_times = []
        self.delay_times_truck = []
        self.delay_times_bridge = {}
        self.broken_bridges = 0
        self.breakdown_probabilities = breakdown_probabilities
        self.G = nx.Graph()

        self.generate_model()
        self.generate_networkx_model()
        
    def generate_model(self):
        """
        generate the simulation model according to the csv file component information

        Warning: the labels are the same as the csv column labels
        """

        df = pd.read_csv(self.file_name)
    

        # a list of names of roads to be generated
        roads = df['road'].unique()

        df_objects_all = []
        for road in roads:
            # Select all the objects on a particular road in the original order as in the cvs
            df_objects_on_road = df[df['road'] == road]

            if not df_objects_on_road.empty:
                df_objects_all.append(df_objects_on_road)
 
                """
                Set the path 
                1. get the serie of object IDs on a given road in the cvs in the original order
                2. add the (straight) path to the path_ids_dict
                3. put the path in reversed order and reindex
                4. add the path to the path_ids_dict so that the vehicles can drive backwards too
                """
                path_ids = df_objects_on_road['id']
                path_ids.reset_index(inplace=True, drop=True)
                self.path_ids_dict[path_ids[0], path_ids.iloc[-1]] = path_ids
                self.path_ids_dict[path_ids[0], None] = path_ids
                path_ids = path_ids[::-1]
                path_ids.reset_index(inplace=True, drop=True)
                self.path_ids_dict[path_ids[0], path_ids.iloc[-1]] = path_ids
                self.path_ids_dict[path_ids[0], None] = path_ids

        # put back to df with selected roads so that min and max and be easily calculated
        df = pd.concat(df_objects_all)
        y_min, y_max, x_min, x_max = set_lat_lon_bound(
            df['lat'].min(),
            df['lat'].max(),
            df['lon'].min(),
            df['lon'].max(),
            0.05
        )

        # ContinuousSpace from the Mesa package;
        # not to be confused with the SimpleContinuousModule visualization
        self.space = ContinuousSpace(x_max, y_max, True, x_min, y_min)

        for df in df_objects_all:
            for _, row in df.iterrows():  # index, row in ...

                # create agents according to model_type
                model_type = row['model_type'].strip()
                agent = None

                name = row['name']
                if pd.isna(name):
                    name = ""
                else:
                    name = name.strip()

                if model_type == 'source':
                    agent = Source(row['id'], self, row['length'], name, row['road'])
                    self.sources.append(agent.unique_id)
                elif model_type == 'sink':
                    agent = Sink(row['id'], self, row['length'], name, row['road'])
                    self.sinks.append(agent.unique_id)
                elif model_type == 'sourcesink':
                    agent = SourceSink(row['id'], self, row['length'], name, row['road'])
                    self.sources.append(agent.unique_id)
                    self.sinks.append(agent.unique_id)
                elif model_type == 'bridge':
                    agent = Bridge(row['id'], self, row['length'], name, row['road'], row['condition'])
                elif model_type == 'link':
                    agent = Link(row['id'], self, row['length'], name, row['road'])
                elif model_type == 'intersection':
                    if not row['id'] in self.schedule._agents:
                        agent = Intersection(row['id'], self, row['length'], name, row['road'])

                if agent:
                    self.schedule.add(agent)
                    y = row['lat']
                    x = row['lon']
                    self.space.place_agent(agent, (x, y))
                    agent.pos = (x, y)
        

    def generate_networkx_model(self):
        df = pd.read_csv(self.file_name)
        for _,row in df.iterrows():
            self.G.add_node(row['id'], pos = (row['lon'], row['lat']))
        
        # Second loop: Add edges between consecutive nodes on the same road
        for i in range(len(df) - 1):
            current_row = df.iloc[i]
            next_row = df.iloc[i + 1]
        # Ensure we are on the same road
            if current_row['road'] == next_row['road']:
                # Add the edge between the current and next node
                self.G.add_edge(current_row['id'], next_row['id'], weight=current_row['length'])
        pos = nx.get_node_attributes(self.G,'pos')


    
    def get_shortest_path(self, source, sink):
        """
        Returns the shortest path between origin and destination.
        Uses the dictionary for lookup to avoid redundant computations.
        """
        key = (source, sink)
        
        # Check if path is already computed
        if key in self.path_ids_dict:
            return self.path_ids_dict[key]
        try:
            shortest_path = nx.shortest_path(self.G, source=source, target=sink, weight='weight')
            self.path_ids_dict[key] = pd.Series(shortest_path)   # Store for future use
            return self.path_ids_dict[key]
        except nx.NetworkXNoPath:
            print(f"No path exists between {source} and {sink}.")
            return None
                

           

    def get_random_route(self, source):
        """
        pick up a random route given an origin
        """
        while True:
            # different source and sink
            sink = self.random.choice(self.sinks)
            if sink is not source:
                break
        return self.path_ids_dict[source, sink]

    # TODO
    # def get_route(self, source):
    #     return self.get_straight_route(source)
    
    def get_route(self, source):    
        # Choose a random sink to ensure a valid destination
        while True:
            sink = self.random.choice(self.sinks)
            if sink != source:
                break
        return self.get_shortest_path(source, sink)



    def get_straight_route(self, source):
        """
        pick up a straight route given an origin
        """
        return self.path_ids_dict[source, None]

    def step(self):
        """
        Advance the simulation by one step.
        """
        self.schedule.step()
        


# EOF -----------------------------------------------------------
BangladeshModel()
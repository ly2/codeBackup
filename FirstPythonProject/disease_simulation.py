""" File name:   disease_simulation.py
    Author:      Nathan Robinson
    Date:        2014-02-19
    Description: This is the main file for COMP3620 Assignment 0 Exercise 4.
                 
                 --- You do not need to modify this file ---
                 
                 python disease_simulation.py to get usage information.
"""

import sys
from cStringIO import StringIO
import copy
import importlib
import traceback, os.path

class Capturing(list):
    """ A class to capture printed output. """
    
    def __enter__(self):
        """ Allow us to use instances of Capturing with the 'with' keyword.
            Deal with entering the with block.
        """
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    
    def __exit__(self, *args):
        """ Allow us to use instances of Capturing with the 'with' keyword
            Deal with exiting the with block.
        """
        self.extend(self._stringio.getvalue().splitlines())
        sys.stdout = self._stdout
        

usage = """Usage:
python disease_simulation.py test
    to test your implementation of DiseaseScenario in disease_scenario.py
OR
python disease_simulation.py scenario_file AgentClass iterations
    to run the scenario described in scenario_file with the specified
    agent for the given number of iterations.

For example: python disease_simulation.py exercise4_maps/scenario1.scn HealthAgent 50
    will run exercise4_maps/scenario1.scn with the default agent for 50 iterations.
"""

non_existent_test = "tests/non_existent_test.scn"
test_files = ["exercise4_maps/test1.scn", "exercise4_maps/test2.scn", "exercise4_maps/test3.scn"]
test_params = [\
{ "threshold" : 0.5, "growth" : 0.2, "spread" : 0.1, "locations" : ["l1", "l2"],
    "location" : "l1",
  "disease" : { "l1" : 0 , "l2" : 0.8 },
  "conn" : { "l1" : set(["l2"]), "l2" : set(["l1"]) },
  "vloc" : "l2", "iloc" : "l3",
  "10it" : { 'l2': 4.95338913792, 'l1': 0} },
{ "threshold" : 1, "growth" : 0.2, "spread" : 0.1, "locations" : ["l1", "l2", "l3", "l4"],
  "location" : "l1",
  "disease" : { "l1" : 0 , "l2" : 1, "l3" : 0, "l4" : 0.1},
  "conn" : { "l1" : set(["l2", "l3"]), "l2" : set(["l1", "l3"]), "l3" : set(["l1", "l2", "l4"]),
             "l4" : set(["l3"]) },
  "vloc" : "l2" , "iloc" : "l4",
  "10it" : {'l4': 2.1405428582400003, 'l2': 7.713105638400002, 'l3': 5.520701214720001, 'l1': 0} },
{ "threshold" : 1, "growth" : 1, "spread" : 1,
  "locations" : ["l0", "l1", "l2", "l3", "l4", "l5", "l6", "l7", "l8", "l9"],
  "location" : "l9",
  "disease" : { "l0" : 0.5, "l1" : 0, "l2" : 0, "l3" : 0, "l4" : 0, "l5" : 0, "l6" : 0,
                "l7" : 0,   "l8" : 0, "l9" : 0},
  "conn" : { "l0" : set(["l1", "l5"]), "l1" : set(["l0", "l2"]), "l2" : set(["l1", "l3"]),
             "l3" : set(["l2", "l4"]), "l4" : set(["l3", "l9"]), "l5" : set(["l0", "l6"]),
             "l6" : set(["l5", "l7"]), "l7" : set(["l6", "l8"]), "l8" : set(["l7", "l9"]),
             "l9" : set(["l4", "l8"]) },
  "vloc" : "l8" , "iloc" : "l2",
  "10it" : {'l6': 31806.0, 'l7': 18411.0, 'l4': 7752.0, 'l5': 43757.0, 'l2': 31806.0,
            'l3': 18411.0, 'l0': 48620.0, 'l1': 43757.0, 'l8': 7752.0, 'l9': 0}
}
]

class TestingError(Exception):
    """ An error to be raised when testing fails. """

def test_scenario_file(module):
    """ Test the given disease_scenario module.
        
        (module) -> None
    """
    print "Testing implementation of disease_scenario.py"
    print "--------------------------------------------------------------------"
    
    print "Checking for DiseaseScenario class..."
    print "-------------------------------------"
    try:
        ds_class = module.DiseaseScenario
        if type(ds_class) != type:
            print "Failed. DiseaseScenario is not a class."
            class tc: pass
            if type(ds_class) == type(tc):
                print "You have forgotten to make DiseaseScenario subclass object."
            raise TestingError()
        ds = ds_class()
    except AttributeError:
        print "Failed. DiseaseScenario does not exist."  
        raise TestingError()
    print "Success."
    
    print "Testing read_scenario_file method."
    print "-------------------------------------"
    try:
        rsf = ds.read_scenario_file
        print "Testing on a non-existent file..."
        try:
            if rsf(non_existent_test):
                print "Error: either to you failed to return False when an IOError was raised or",\
                    "you created a file called non_existent_test.scn (you should delete it)."
                raise TestingError()
        except IOError:
            print "Error: you are supposed to catch IOErrors and return false."
            raise TestingError()
        except Exception:
            print "Unexpected error when running on a non-existent file:"
            print traceback.format_exc()
            raise TestingError()
            
        print "Success."
            
        test_ds = []
        for test, tparams in zip(test_files, test_params):
            print "Testing on file:", test
            ds_copy = copy.deepcopy(ds)
            try:
                if not ds_copy.read_scenario_file(test):
                    print "Error:", test, " does not exist or you are returning False inadvertently."
                    raise TestingError()
                    
                if hasattr(module.DiseaseScenario, 'threshold'):
                    print "Error: you have made threshold a class variable!"
                    print "It should belong to the instance -- i.e. self.threshold = x"
                    raise TestingError()  
                
                if hasattr(module.DiseaseScenario, 'growth'):
                    print "Error: you have made growth a class variable!"
                    print "It should belong to the instance -- i.e. self.growth = x"
                    raise TestingError()  
                
                if hasattr(module.DiseaseScenario, 'spread'):
                    print "Error: you have made spread a class variable!"
                    print "It should belong to the instance -- i.e. self.spread = x"
                    raise TestingError()  
                 
                if hasattr(module.DiseaseScenario, 'location'):
                    print "Error: you have made location a class variable!"
                    print "It should belong to the instance -- i.e. self.location = x"
                    raise TestingError()     
                
                if hasattr(module.DiseaseScenario, 'locations'):
                    print "Error: you have made locations a class variable!"
                    print "It should belong to the instance -- i.e. self.locations = []"
                    raise TestingError()  
                    
                if hasattr(module.DiseaseScenario, 'disease'):
                    print "Error: you have made disease a class variable!"
                    print "It should belong to the instance -- i.e. self.disease = {}"
                    raise TestingError()  
                    
                if hasattr(module.DiseaseScenario, 'conn'):
                    print "Error: you have made conn a class variable!"
                    print "It should belong to the instance -- i.e. self.conn = {}"
                    raise TestingError()  
                
                test_ds.append(ds_copy)
            except IOError:
                print "Error: you are supposed to catch IOErrors and return false."
                raise TestingError()
            except TestingError:
                raise TestingError()
            except Exception:
                print "Unexpected error:"
                print traceback.format_exc()
                raise TestingError()
            try:
                if not isinstance(ds_copy.threshold, float) and not isinstance(ds_copy.threshold, int):
                    print "Error: threshold should be a float or int!"
                    raise TestingError()
                if abs(ds_copy.threshold - tparams["threshold"]) > 0.001:
                    print "Error: threshold has unexpected value: ", ds_copy.threshold,\
                        "expected:", tparams["threshold"]
                    raise TestingError()
            except AttributeError:
                print "Error: threshold variable is missing."
                raise TestingError()
            
            try:
                if not isinstance(ds_copy.growth, float) and not isinstance(ds_copy.growth, int):
                    print "Error: growth should be a float or int!"
                    raise TestingError()
                    
                if abs(ds_copy.growth - tparams["growth"]) > 0.001:
                    print "Error: growth has unexpected value:", ds_copy.growth,\
                        "expected:", tparams["growth"]
                    raise TestingError()
            except AttributeError:
                print "Error: growth variable is missing."
                raise TestingError()
            
            try:
                if not isinstance(ds_copy.spread, float) and not isinstance(ds_copy.spread, int):
                    print "Error: spread should be a float or int!"
                    raise TestingError()
                
                if abs(ds_copy.spread - tparams["spread"]) > 0.001:
                    print "Error: spread has unexpected value: ", ds_copy.spread,\
                        "expected:", tparams["spread"]
                    raise TestingError()
            except AttributeError:
                print "Error: spread variable is missing."
                raise TestingError()
            
            try:
                if ds_copy.location != tparams["location"]:
                    print "Error: location has unexpected value: ", ds_copy.location,\
                        "expected:", tparams["location"]
                    raise TestingError()
            except AttributeError:
                print "Error: location variable is missing."
                raise TestingError()
            
            try:
                if not isinstance(ds_copy.locations, list):
                    print "Error: locations is not a list."
                    raise TestingError()
                for loc in ds_copy.locations:
                    if loc not in tparams["locations"]:
                        print "Unexpected location:", loc
                        raise TestingError()
                for loc in tparams["locations"]:
                    if loc not in ds_copy.locations:
                        print "Missing location:", loc
                        raise TestingError()
            except AttributeError:
                print "Error: locations variable is missing."
                raise TestingError()

            try:
                if not isinstance(ds_copy.disease, dict):
                    print "Error: disease is not a dictionary."
                    raise TestingError()
                for loc, dis in ds_copy.disease.iteritems():
                    if loc not in tparams["disease"]:
                        print "Unexpected disease location:", loc
                        raise TestingError()   
                    
                    if not isinstance(dis, float) and not isinstance(dis, int):
                        print "Error: the disease at location", loc, "should be a float or int!"
                        raise TestingError()
                    
                    if abs(tparams["disease"][loc] - dis) > 0.001:
                        print "Invalid disease at location:", loc, "expected:",\
                            tparams["disease"][loc]
                        raise TestingError()   
                for loc, dis in tparams["disease"].iteritems():
                    if loc not in ds_copy.disease:
                        print "Missing disease location (locations should have 0 disease by default):", loc
                        raise TestingError()
            except AttributeError:
                print "Error: disease variable is missing."
                raise TestingError()
            
            try:
                if not isinstance(ds_copy.conn, dict):
                    print "Error: conn is not a dictionary."
                    raise TestingError()

                for loc, locs in ds_copy.conn.iteritems():
                    if loc not in tparams["conn"]:
                        print "Unexpected conn location:", loc
                        raise TestingError()
                    
                    if not isinstance(locs, set):
                        print "Error: location", loc, "should have a *set* of connected",\
                            "locations in the conn dictionary."
                        raise TestingError()
                    if locs != tparams["conn"][loc]:
                        print "There is an invalid set of connections at location:", loc
                        print "We expected:", tparams["conn"][loc]
                        print "We got:", locs
                        raise TestingError()
                    
                for loc, dis in tparams["conn"].iteritems():
                    if loc not in ds_copy.conn:
                        print "Missing location in conn dictionary:", loc
                        raise TestingError()
                
            except AttributeError:
                print "Error: conn dictionary is missing."
                raise TestingError()    
    except AttributeError:
        print "Failed. read_scenario_file does not exist."  
        raise TestingError()
    print "Success."
    
    print "Testing valid_moves method."
    print "-------------------------------------"
    try:
        vm = ds.valid_moves
    except AttributeError:
        print "Failed. valid_moves does not exist."  
        raise TestingError()
    
    for tid, test_file in enumerate(test_files):
        tparams = test_params[tid]
        ds = test_ds[tid]
        
        try:
            correct_vm = tparams["conn"][tparams["location"]]
            correct_vm.add(tparams["location"])
            valid_moves = ds.valid_moves()
            if not isinstance(valid_moves, list):
                print "Error: valid_moves is supposed to return a list."
                raise TestingError()
            if set(valid_moves) != correct_vm:
                print "Error: valid moves for test:", test_file, "loc:", ds.location,\
                    "is wrong. Did you remember that agents can move to their",\
                    "current locations?"
                print "We expected:", sorted(correct_vm)
                print "We got:", sorted(valid_moves)
                
                raise TestingError()
        except Exception:
            print "Unexpected error when running valid_moves for test:",\
                test_file, "location:", ds.location
            print traceback.format_exc()
            raise TestingError()
    print "Success."
    
    print "Testing move method."
    print "-------------------------------------"
    try:
        mm = ds.move
    except AttributeError:
        print "Failed. move does not exist."  
        raise TestingError()
    
    for tid, test_file in enumerate(test_files):
        tparams = test_params[tid]
        ds = copy.deepcopy(test_ds[tid])
        
        #Invalid move first
        try:
            ds.move(tparams["iloc"])
            raise TestingError()
        except ValueError:
            pass
        except Exception:
            print "Unexpected error when running move method with an invalid location:",\
                tparams["iloc"], "for test:", test_file
            print traceback.format_exc()
            print "We Expected a ValueError to be raised when an invalid move was made."
            raise TestingError()
            
        #Valid move
        ds.disease[tparams["vloc"]] = 100
        try:
            ds.move(tparams["vloc"])
        except Exception:
            print "Unexpected error when running move to", tparams["vloc"],\
                "for test:", test_file
            print traceback.format_exc()
            raise TestingError()
        if ds.disease[tparams["vloc"]] != 0:
            print "Error: moving to", tparams["vloc"],\
                "did not clear disease there in test:", test_file
            raise TestingError()
        if ds.location != tparams["vloc"]:
            print "Error: moving to", tparams["vloc"], "failed to change the location",\
                "in test:", test_file
            raise TestingError()
    print "Success."
    
    print "Testing spread_disease method."
    print "-------------------------------------"
    try:
        sd = ds.spread_disease
    except AttributeError:
        print "Failed. spread_disease does not exist."  
        raise TestingError()
    
    for tid, test_file in enumerate(test_files):
        tparams = test_params[tid]
        ds = test_ds[tid]
        
        try:
            for it in xrange(10):
                ds.spread_disease()
        except Exception:
            print "Unexpected error when running spread_disease for test:", \
                test_file
            print traceback.format_exc()
            raise TestingError()
        
        try:
            ed = tparams["10it"]
            for loc in tparams["locations"]:
                if loc == tparams["location"]:
                    if ds.disease[loc] != 0:
                        print "Error: we expect there to always be zero disease",\
                            "at the current location:", test_file, "instead there is:",\
                             ds.disease[loc]
                        raise TestingError()
                    else:
                        if abs(ds.disease[loc] - ed[loc]) > 0.01:
                            print "Error: after 10 iterations there is the wrong",\
                                "disease", ds.disease[loc], "expected", ed[loc],\
                                "(0.01 epsilon) at location:", loc, "test:", test_file
                            raise TestingError()
        except AttributeError:
            print "Error: you must have deleted disease when running spread_disease",\
                "for test:", test_file
    
    print "All tests passed. Good job!"
    print "These tests are thorough, but not exhaustive."
    print "At the end of the day, the correctness of your code depends on you following instructions."
    print "Make sure you check your code again, comment your file appropriately,",\
        "and then proceed to the next part of the exercise."
    

def print_summary(scenario):
    """ Print a summary of the disease spread and current location in the
        given scenario.
        
        (DiseaseScenario) -> None
    """
    print "The locations have the following disease:"
    total_disease = 0
    for loc in scenario.locations:
        disease = scenario.disease[loc]
        total_disease += disease
        print loc, disease,
        if disease >= scenario.threshold:
            print "(spreading)"
        else:
            print
    print "Total disease:", total_disease 
    return total_disease


def main():
    """ Run the simulation on the scenario file given in the command line.
        
        () -> None
    """
    
    if len(sys.argv) not in [2, 4]:
        print "Error: missing command line arguments."
        print
        print usage
        sys.exit()
    
    try:
        with Capturing() as output:
            import disease_scenario
    except ImportError:
        print "Error disease_scenario.py does not exist."
        sys.exit()
    except Exception:
        print "Error: exception when importing disease_scenario:"
        print traceback.format_exc()
        sys.exit()
    
    if output:
        print "Error disease_scenario.py produced output when imported."
        sys.exit()
    
    if len(sys.argv) == 2:
        if sys.argv[1] != "test":
            print "Error: invalid command line arguments."
            print
            print usage
            sys.exit()
        try:
            test_scenario_file(disease_scenario)
        except TestingError:
            pass
    else:
        try:
            ds = disease_scenario.DiseaseScenario()
            if not ds.read_scenario_file(sys.argv[1]):
                print "Error: the supplied scenario file does not exist:", sys.argv[1]
                sys.exit()
        except Exception:
            print "Unexpected error while loading the specified disease scenario:", sys.argv[1]
            print traceback.format_exc()
            print "Are you sure you tested disease_scenario correctly?"
            sys.exit()
        
        agent_name = sys.argv[2]
        print "Trying to load agent:", agent_name
        try:
            agent_module = importlib.import_module("health_agents")
            base_class = agent_module.HealthAgent
        except ImportError:
            print "Error loading agent from health_agents.py"
            print "Make sure the file exists."
            sys.exit()
        except Exception:
            print "Unexpected error while trying to import health_agents.py:"
            print traceback.format_exc()
            print "What did you do in that file?"
            sys.exit()
            
        if agent_name not in agent_module.__dict__:
            print "There is no such agent as", agent_name, "in health_agents.py"
            sys.exit()
        
        agent_class = agent_module.__dict__[agent_name]
        if not issubclass(agent_class, base_class):
            print "Error:", agent_name, "is not an instance of a HealthAgent."
            sys.exit()
        
        try:
            agent = agent_class(list(ds.locations), copy.deepcopy(ds.conn))
        except Exception:
            print "Unknown error while trying to create a new:", agent_name
            print traceback.format_exc()
            sys.exit()
        
        print "Agent loaded."
        
        try:
            iterations = int(sys.argv[3])
            if iterations < 0: raise ValueError()
        except ValueError:
            print "Error: invalid number of iterations:", sys.argv[3]
            sys.exit()
        
        try:
            print "Starting simulation."
            print_summary(ds)
            print "Agent location:", ds.location
            
            for i in xrange(iterations):
                print "Step:", i

                valid_moves = ds.valid_moves()
                move = agent.choose_move(ds.location, list(valid_moves),
                    dict(ds.disease), ds.threshold, ds.growth, ds.spread)
               
                print "Selected move:", move
                
                ds.move(move)
                ds.spread_disease()
                total_disease = print_summary(ds)
                
                if total_disease < 0.001:
                    print "You eradicated all disease! Good job."
                    sys.exit()
                if total_disease >= 100000:
                    print "There is just too much disease around to bother continuing."
                    print "It is all over..."
                    sys.exit()
                
        except Exception:
            print "Error: unexpected exception while running the simulation."
            print traceback.format_exc()
            sys.exit()


if __name__ == "__main__":
    main()
    
    
   
    
    
    
    


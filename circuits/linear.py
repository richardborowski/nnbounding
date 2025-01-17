#!/usr/bin/env python3

import math
import itertools
from itertools import accumulate
from itertools import product
from decimal import Decimal

from .obdd import ObddManager, ObddNode
from .timer import Timer


class Inputs:
    """AC: represent this as a priority queue?  This would 
    make finding the max weight faster
    """

    def __init__(self,weights=None):
        if weights is None:
            self.original_weights = []
            self.weights = {}
            self.setting = {}
        else:
            self.original_weights = weights
            self.weights = { index:float(weight) for index,weight \
                             in enumerate(weights) }
            #self.remove_zero_weights() # ACACAC
            self.setting = {}

    def __repr__(self):
        st = []
        for index in self.weights:
            weight = self.weights[index]
            st.append("  input %d: weight %.4f" % (index,weight))
        for index in self.setting:
            value,weight = self.setting[index]
            value = "None" if value is None else str(value)
            st.append("  input %d: weight %.4f (set to %s)" % \
                      (index,weight,value))
        return "\n".join(st)

    def copy(self):
        inputs = Inputs()
        inputs.weights = dict(self.weights)
        inputs.setting = dict(self.setting)
        return inputs

    def set(self,index,value):
        assert index in self.weights
        weight = self.weights[index]
        del self.weights[index]
        self.setting[index] = (value,weight)
        return weight

    def remove_zero_weights(self):
        zero_indices = [ index for index,weight in self.weights.items() if weight == 0 ]
        for index in zero_indices:
            del self.weights[index]

    def get_biggest_weight(self):
        """return weight with largest absolute value"""
        # ACAC: use priority queue
        if len(self.weights) == 0: return None
        biggest_index,biggest_abs_weight = None,0
        for index,weight in self.weights.items():
            abs_weight = abs(weight)
            if abs_weight >= biggest_abs_weight:
                biggest_index = index
                biggest_abs_weight = abs_weight
        biggest_weight = self.weights[biggest_index]
        return (biggest_index,biggest_weight)

    def set_biggest_weight(self,value):
        # ACAC: TODO
        pass

    def settings_needed(self,target):
        """returns the number of inputs that need to be set to achieve
        a target decrease in the gap of the threshold test"""
        sorted_weights = [ abs(self.weights[index]) for index in self.weights ]
        sorted_weights.sort(reverse=True)
        weight_sum = 0.0
        weight_count = 0
        for weight in sorted_weights:
            if weight_sum >= target:
                return weight_count
            weight_sum += weight
            weight_count += 1
        return weight_count

    def get_model(self):
        return { index:value for index,(value,w) in self.setting.items() if value is not None }

class Classifier:
    """For representing Andy's linear classifier (neuron) format."""

    def __init__(self,name="none",size="0",weights=[],threshold="0"):
                 #num_values="2",prior="0",offset="0"):
        self.name = name
        self.size = size
        self.weights = weights # AC: this should disappear
        self.inputs = Inputs(weights)
        self.threshold = threshold
        self.is_integer = self.check_integrality()
        # extra stuff from Andy's format
        #self.num_values = num_values
        #self.prior = prior
        #self.offset  = offset

    def __repr__(self):
        st = []
        st.append("name: %s" % self.name)
        st.append("size: %s" % self.size)
        st.append("weights: %s" % " ".join(self.weights))
        st.append("threshold: %s" % self.threshold)
        st.append("inputs:\n%s" % str(self.inputs))
        return "\n".join(st)

    def dict(self):
        return {
            "name": self.name,
            "size": self.size,
            "weights": list(self.weights),
            "threshold": self.threshold
        }


    def lowerupperbound(self):
        intweights = [float(x) for x in self.weights]

        intweights.sort() 

        intweights.pop(0)

        intweight = [str(x) for x in intweights]

        newsize = float(self.size)
        newsize -= 1
        self.size = str(newsize)
        str(self.size)
        self.weights = intweight


    def raiselowerbound(self):
        intweights = [float(x) for x in self.weights]
        intweights.sort()
        intweights.pop()
        intweight = [str(x) for x in intweights]
        newsize = float(self.size)
        newsize -= 1
        self.size = str(newsize)
        str(self.size)
        self.weights = intweight


    def lowerthreshold(self):
        intweights = [float(x) for x in self.weights]
        intweights.sort()
        thresh = intweights.pop()
        intweight = [str(x) for x in intweights]
        newthresh = float(self.threshold)
        newthresh -= thresh
        self.threshold = str(newthresh)
        self.weights = intweight
        newsize = float(self.size)
        newsize -= 1
        self.size = str(newsize)
        str(self.weights)


    def raisethreshold(self):
        intweights = [float(x) for x in self.weights]
        intweights.sort()
        thresh = intweights.pop(0)
        intweight = [str(x) for x in intweights]
        newthresh = float(self.threshold)
        newthresh -= thresh
        self.threshold = str(newthresh)
        self.weights = intweight
        newsize = float(self.size)
        newsize -= 1
        self.size = str(newsize)
        str(self.weights)
    

    def minimizebothbounds(self):
        intweights = [float(x) for x in self.weights]
        intweights.sort()
        intweights.pop()
        intweights.pop(0)
        intweight = [str(x) for x in intweights]
        newsize = float(self.size)
        newsize -= 2
        self.size = str(newsize)
        str(self.size)
        self.weights = intweight

           
    def fastmove(self):
        intweights = [float(x) for x in self.weights]
        intweights2 = [float(x) for x in self.weights]
        absintweights = [abs(x) for x in intweights]
        
        twointweights = [float(x) for x in self.weights], [0 for x in self.weights]
        thresh = float(self.threshold)

        lowerbound = sum(i for i in intweights if i<0)


        maxnum = max(absintweights)
        maxindex = absintweights.index(maxnum)
         
   
     
    
        if intweights[maxindex] > 0:
                
            print("Set" , intweights[maxindex] , "to 1") 
            twointweights[1][maxindex] = 1
            thresh -= maxnum
            
        if intweights[maxindex] < 0:
                
            print("Set" , intweights[maxindex] , "to 0")
            twointweights[1][maxindex] = 0

            absintweights.pop(maxindex)
            intweights2.pop(maxindex)
            lowerbound = sum(i for i in intweights2 if i<0)

        for i in twointweights:
            for j in i:
                print(j, end = " ")
            print()

    	    

    def format_andy(self):
        st = []
        st.append( "%s\n" % self.name )
        st.append( "%s %s %s %s %s\n" % ( self.size,self.num_values,
                                          self.prior,self.threshold,
                                          self.offset ) )
        st.append( "%s\n" % " ".join(self.weights) )
        return "".join(st)

    @staticmethod
    def read_andy(filename):
        """Read Andy's neuron format (deprecated)"""
        with open(filename,'r') as f:
            lines = f.readlines()
        lines = [ line.strip() for line in lines ]
        name = lines[0]
        size,num_values,prior,threshold,offset = lines[1].split()
        weights = lines[2].split()
        neuron = { "name": name, "size": size,
                   "weights": weights,"threshold": threshold }
        return Classifier(**neuron)

    @staticmethod
    def parse(st):
        """Parse a neuron string format"""
        neuron = {}
        for line in st.split('\n'):
            line = line.strip()
            if not line: continue
            field,value = line.split(':')
            field = field.strip()
            value = value.strip()
            neuron[field] = value
        assert "size" in neuron
        assert "threshold" in neuron # or "bias" in neuron
        assert "weights" in neuron
        neuron["weights"] = neuron["weights"].split()
        return Classifier(**neuron)

    @staticmethod
    def read(filename):
        """Read a neuron from file"""
        with open(filename,'r') as f:
            st = f.read()
        return Classifier.parse(st)

    def save(self,filename=None):
        if filename is None: filename = self.filename
        with open(filename,'w') as f:
            f.write(str(self))

    def _biggest_weight(self):
        biggest = 0
        for weight in self.weights:
            w = abs(float(weight))
            if w > biggest:
                biggest = w
        return biggest

    def check_integrality(self):
        weights = self.weights + [self.threshold]
        check = [ float(w).is_integer() for w in weights ]
        return sum(check) == len(check)

    def with_precision(self,digits):
        biggest = self._biggest_weight()
        scale = Decimal(biggest).adjusted()
        scale = -scale + digits-1
        scale = 10**scale
        new_weights = [ scale*float(weight) for weight in self.weights ]
        new_weights = [ str(int(weight)) for weight in new_weights ]
        new_threshold = str(int(scale*float(self.threshold)))
        neuron = self.dict()
        neuron["weights"] = new_weights
        neuron["threshold"] = new_threshold
        c = Classifier(**neuron)
        assert c.is_integer
        return c

    def _get_bounds(self):
        assert self.is_integer
        lower,upper = 0,0
        for weight in self.weights:
            weight = float(weight)
            if weight < 0:
                lower += weight
            else:
                upper += weight
        return (lower,upper)

    def _to_obdd(self,matrix):
        var_count = int(self.size)
        manager = ObddManager(var_count)
        one,zero = manager.one_sink(),manager.zero_sink()
        last_level = matrix[var_count+1]
        for node in last_level:
            last_level[node] = one if last_level[node] else zero
        for dvar in range(var_count,0,-1):
            level,next_level = matrix[dvar],matrix[dvar+1]
            for node in level:
                hi,lo = level[node] # get indices
                hi,lo = next_level[hi],next_level[lo] # get nodes
                level[node] = manager.new_node(dvar,hi,lo)
        return (manager,matrix[1][0])

    def compile(self):
        assert self.is_integer
        var_count = int(self.size)
        matrix = [ dict() for _ in range(var_count+2) ]
        matrix[1][0] = None # root node
        for i in range(1,var_count+1):
            level,next_level = matrix[i],matrix[i+1]
            weight = int(self.weights[i-1])
            for node in level:
                hi,lo = (node+weight,node)
                level[node] = (hi,lo) # (hi,lo)
                next_level[hi] = None
                next_level[lo] = None
        last_level = matrix[var_count+1]
        threshold = int(self.threshold)
        for node in last_level:
            last_level[node] = node >= threshold
        return self._to_obdd(matrix)


class IntClassifier(Classifier):
    def __init__(self,name="none",size=0,weights=[],threshold=0):
        super().__init__(name=name,size=size,weights=weights,threshold=threshold)
        #assert self.is_integer
        self.size = int(size)
        self.weights = [float(x) for x in weights]
        self.threshold = float(threshold)

    def __repr__(self):
        st = []
        st.append("name: %s" % self.name)
        st.append("size: %d" % self.size)
        #st.append("weights: %s" % " ".join(str(weight) for weight in self.weights))
        st.append("threshold: %.4f" % self.threshold)
        st.append("bounds: [%.4f,%.4f]" % \
                  (self.lowerbound(),self.upperbound()))
        #st.append("inputs:\n%s" % str(self.inputs))
        return "\n".join(st)

    @staticmethod
    def read(filename):
        classifier = Classifier.read(filename)
        return IntClassifier(name=classifier.name,
                             size=classifier.size,
                             weights=classifier.weights,
                             threshold=classifier.threshold)

    def copy(self):
        name = self.name
        size = self.size
        weights = list(self.weights) # AC: remove this eventually
        threshold = self.threshold
        classifier = IntClassifier(name=name,size=size,
                                   weights=weights,
                                   threshold=threshold)
        classifier.inputs = self.inputs.copy()
        return classifier

    def set_input(self,index,value):
        """return a new copy of the classifier where the input index
        has been set to value"""

        new_classifier = self.copy()
        weight = new_classifier.inputs.set(index,value)
        new_classifier.size -= 1
        if value != 0 and value is not None:
            new_classifier.threshold -= value*weight
        return new_classifier

    def set_inputs(self,indices,values):
        """return a new copy of the classifier where the all
        input/value pairs in setting have been applied"""

        new_classifier = self.copy()
        for index,value in zip(indices,values):
            weight = new_classifier.inputs.set(index,value)
            new_classifier.size -= 1
            if value != 0 and value is not None:
                new_classifier.threshold -= value*weight
        return new_classifier

    def lowerbound(self):
        none_weights = [ weight for value,weight in self.inputs.setting.values() \
                         if value is None ]
        weights = none_weights + list(self.inputs.weights.values())
        return sum(w for w in weights if w<0)

    def upperbound(self):
        none_weights = [ weight for value,weight in self.inputs.setting.values() \
                         if value is None ]
        weights = none_weights + list(self.inputs.weights.values())
        return sum(w for w in weights if w>0)

    def is_trivially_true(self):
        return self.threshold <= self.lowerbound()

    def is_trivially_false(self):
        return self.threshold > self.upperbound()

    def gap(self):
        return self.threshold - self.lowerbound()

    def fast_trivially_true(self):
        """automize finding the fastest way to make a test trivially
        true and false

        """

        if self.is_trivially_false():
            print("already trivially false")
            return

        c = self
        count = 0
        while not c.is_trivially_true():
            count += 1
            index,weight = c.inputs.get_biggest_weight()

            if weight > 0:
                #print(count, "Set" , weight , "to 1")
                c = c.set_input(index,1)
            else:
                #print(count, "Set" , weight , "to 0")
                c = c.set_input(index,0)

        #print()
        #print("=== trivial classifier:")
        #print(c)
        return c

    def _dfs_greedy(self,passing,failing,sorted_weights,classifier,find_true=True):
        classifier = IntClassifier._round_small_numbers(classifier) # ACACAC
        depth,t,lb,ub,setting = classifier
        ft = find_true

        is_true =  lambda x: x[1] <= x[2]
        is_false = lambda x: x[1] > x[3]

        if is_true(classifier):
            passing.append(setting)
            return
        if is_false(classifier):
            failing.append(setting)
            return

        weight = sorted_weights[depth]
        # update lower/upper bounds
        if weight > 0: new_lb,new_ub = lb,ub-weight
        else:          new_lb,new_ub = lb-weight,ub

        if ( find_true and weight < 0 ) or ( not find_true and weight > 0 ):
            # set value to zero
            new_t = t
            new_setting = setting + [0]
            child = (depth+1,new_t,new_lb,new_ub,new_setting)
            self._dfs_greedy(passing,failing,sorted_weights,child,find_true=ft)

            # set value to one
            new_t = t-weight
            new_setting = setting + [1]
            child = (depth+1,new_t,new_lb,new_ub,new_setting)
            self._dfs_greedy(passing,failing,sorted_weights,child,find_true=ft)
        else:
            # set value to one
            new_t = t-weight
            new_setting = setting + [1]
            child = (depth+1,new_t,new_lb,new_ub,new_setting)
            self._dfs_greedy(passing,failing,sorted_weights,child,find_true=ft)

            # set value to zero
            new_t = t
            new_setting = setting + [0]
            child = (depth+1,new_t,new_lb,new_ub,new_setting)
            self._dfs_greedy(passing,failing,sorted_weights,child,find_true=ft)
        
    def dfs_greedy(self,find_true=True):
        sorted_weights,accum_weights,input_map = self._search_weights()
        depth = 0
        t = self.threshold
        lb = sum(w for w in sorted_weights if w < 0)
        ub = sum(w for w in sorted_weights if w > 0)
        setting = []
        d = (depth,t,lb,ub,setting)

        passing,failing = [],[]
        self._dfs_greedy(passing,failing,sorted_weights,d,find_true=find_true)
        return passing,failing

    def _dfs_naive(self,passing,failing,weights,classifier):
        classifier = IntClassifier._round_small_numbers(classifier) # ACACAC
        depth,t,lb,ub,setting = classifier

        is_true =  lambda x: x[1] <= x[2]
        is_false = lambda x: x[1] > x[3]

        if is_true(classifier):
            passing.append(setting)
            return
        if is_false(classifier):
            failing.append(setting)
            return

        weight = weights[depth]
        # update lower/upper bounds
        if weight > 0: new_lb,new_ub = lb,ub-weight
        else:          new_lb,new_ub = lb-weight,ub

        if weight < 0:
            # set value to zero
            new_t = t
            new_setting = setting + [0]
            child = (depth+1,new_t,new_lb,new_ub,new_setting)
            self._dfs_naive(passing,failing,weights,child)

            # set value to one
            new_t = t-weight
            new_setting = setting + [1]
            child = (depth+1,new_t,new_lb,new_ub,new_setting)
            self._dfs_naive(passing,failing,weights,child)
        else:
            # set value to one
            new_t = t-weight
            new_setting = setting + [1]
            child = (depth+1,new_t,new_lb,new_ub,new_setting)
            self._dfs_naive(passing,failing,weights,child)

            # set value to zero
            new_t = t
            new_setting = setting + [0]
            child = (depth+1,new_t,new_lb,new_ub,new_setting)
            self._dfs_naive(passing,failing,weights,child)


    def dfs_naive(self):
        weights = self._nonzero_weights()
        depth = 0
        t = self.threshold
        lb = sum(w for w in weights if w < 0)
        ub = sum(w for w in weights if w > 0)
        setting = []
        d = (depth,t,lb,ub,setting)

        passing,failing = [],[]
        self._dfs_naive(passing,failing,weights,d)
        return passing,failing


    def print_all_true_models(self,explanationsize):
        
        #import pdb;
        #pdb.set_trace()
        "recursive method that finds all true models in a thresold test"
        c = self
        
        if c.is_trivially_true():
            #print()
            #print(c.inputs)
            explanationsize.append(c)
            return
            

        if c.is_trivially_false():
            return 

        index,weight = c.inputs.get_biggest_weight()
        
       
        if(weight<0):
            b = c.set_input(index,0)
            b.print_all_true_models(explanationsize)

            a = c.set_input(index,1)
            a.print_all_true_models(explanationsize)
        else:    
            a = c.set_input(index,1)
            a.print_all_true_models(explanationsize)

            b = c.set_input(index,0)
            b.print_all_true_models(explanationsize)

    def print_all_false_models(self,explanationsize):
        
        #import pdb;
        #pdb.set_trace()
        "recursive method that finds all true models in a thresold test"
        c = self
        
        if c.is_trivially_true():
            return
            

        if c.is_trivially_false():
            explanationsize.append(c)
            return 

        index,weight = c.inputs.get_biggest_weight()

        if(weight<0):
            b = c.set_input(index,1)
            b.print_all_false_models(explanationsize)

            a = c.set_input(index,0)
            a.print_all_false_models(explanationsize)
        else:    
            a = c.set_input(index,0)
            a.print_all_false_models(explanationsize)

            b = c.set_input(index,1)
            b.print_all_false_models(explanationsize)




    def print_bounds_graph(self,passing,failing):
        #import pdb;
        #pdb.set_trace()
        c = self
        import matplotlib.pyplot as plt
        x = [0]
        y = [0]
        for i in range(len(passing)):
            x.append(i+1)
            y.append(y[i] + 2**len(passing[i].inputs.weights))
        f = 0
        f += 2**c.size

        x2 = [0] 
        y2 = [f] 
        for i in range(len(failing)):
            x2.append(i+1)
            y2.append(y2[i] - 2**len(failing[i].inputs.weights))
        
        plt.axhline(y = y2[len(failing)], color = 'black', linestyle = '--')
        plt.plot(x,y,color = 'blue',linestyle = '-.')
        plt.plot(x2,y2,color = 'red',linestyle = "-.")
        #plt.show()

    def breadth_first_search(self):
        #import pdb;
        #pdb.set_trace()
        from queue import PriorityQueue
        c = self
        fq = PriorityQueue()
        q = PriorityQueue()
        count = 0
        q.put((c.size,count,c))
        
        while(not q.empty()):
            current = q.get()
            current2 = current
            if(current[2].is_trivially_false()):
                continue
            if(current[2].is_trivially_true()):
                fq.put(current)
                continue
            else:
                index,weight = current[2].inputs.get_biggest_weight()
                count+=1
                a = current[2].set_input(index,1)
                q.put((len(a.inputs.setting),count,a))

                b = current2[2].set_input(index,0)
                count += 1
                q.put((len(b.inputs.setting),count,b))
                
        return fq

    def breadth_first_search_f(self):
        #import pdb;
        #pdb.set_trace()
        from queue import PriorityQueue
        c = self
        fq = PriorityQueue()
        q = PriorityQueue()
        count = 0
        q.put((c.size,count,c))
        
        while(not q.empty()):
            current = q.get()
            current2 = current
            if(current[2].is_trivially_false()):
                fq.put(current)
                continue
            if(current[2].is_trivially_true()):
                continue
            else:
                index,weight = current[2].inputs.get_biggest_weight()
                count+=1
                a = current[2].set_input(index,1)
                q.put((len(a.inputs.setting),count,a))

                b = current2[2].set_input(index,0)
                count += 1
                q.put((len(b.inputs.setting),count,b))
                
        return fq

    def _search_weights(self):
        weights = self.inputs.weights.values()
        index_weights = list(enumerate(weights))
        index_weights = [ iw for iw in index_weights if iw[1] != 0 ]

        keyf = lambda iw: abs(iw[1])
        sorted_index_weights = sorted(index_weights,key=keyf,reverse=True)
        input_map = [ i for i,w in sorted_index_weights ]
        sorted_weights = [ w for i,w in sorted_index_weights ]
        abs_weights = [ abs(w) for w in sorted_weights ]
        accum_weights = [0.0] + list(accumulate(abs_weights))

        return sorted_weights, accum_weights, input_map

    def _nonzero_weights(self):
        weights = self.inputs.weights.values()
        return [ w for w in weights if w != 0.0 ]

    @staticmethod
    def _find(sorted_list,target,lo=0):
        hi = len(sorted_list)
        
        for i,val in enumerate(sorted_list[lo:],start=1):
            if val >= target:
                return i

        # AC: this line should not normally be reached
        return 999999

    @staticmethod
    def _add_to_opened(d,accum_weights,opened):
        IntClassifier.id_count += 1
        d = IntClassifier._round_small_numbers(d) # ACACAC
        depth,t,lb,ub,setting = d
        gap = t-lb
        if gap > 0:
            target = accum_weights[depth] + gap
            h_cost = IntClassifier._find(accum_weights,target,lo=depth+1)
        else: # already at goal
            h_cost = 0
        f_cost = depth + h_cost
        node = (f_cost,-IntClassifier.id_count,d)
        opened.put(node)

    @staticmethod
    def _round_small_numbers(classifier):
        eps = 1e-10 # ACACAC
        depth,t,lb,ub,setting = classifier
        if abs(t) < eps:  t = 0
        if abs(lb) < eps: lb = 0
        if abs(ub) < eps: ub = 0
        return (depth,t,lb,ub,setting)

    def a_star_search_alt(self):
        from queue import PriorityQueue        

        c = self
        is_true =  lambda x: x[1] <= x[2]
        is_false = lambda x: x[1] > x[3]

        IntClassifier.id_count = 0
        closed_list = []
        opened = PriorityQueue()
        sorted_weights,accum_weights,input_map = c._search_weights()

        # initial threshold test
        depth = 0
        t = c.threshold
        lb = sum(w for w in sorted_weights if w < 0)
        ub = sum(w for w in sorted_weights if w > 0)
        setting = []

        d = (depth,t,lb,ub,setting)
        IntClassifier._add_to_opened(d,accum_weights,opened)

        true_count, false_count = 0,0
        lower_bound,upper_bound = 0,2**c.size
        passing, failing = [],[]
        print_me = 1

        while(not opened.empty()):
            f_cost,_,current = opened.get()
            depth,t,lb,ub,setting = current
            var_count = c.size - depth

            if IntClassifier.id_count % print_me == 0:
                print_me = print_me * 2
                #osize = opened.qsize()
                #csize = len(closed_list)
                #print("open/closed (cost): %d,%d (%d)" % (osize,csize,f_cost))
                #print("true/false: %d,%d" % (true_count,false_count))
                bound_gap = (upper_bound-lower_bound)/2**c.size
                print("gap: %.4f%% (f-cost: %d)" % (bound_gap,f_cost))

            if is_false(current):
                false_count += 1
                failing.append(setting)
                upper_bound -= 2**var_count
            elif is_true(current):
                true_count += 1
                closed_list.append(current)
                passing.append(setting)
                lower_bound += 2**var_count
            else:
                weight = sorted_weights[depth]

                # update lower/upper bounds
                if weight > 0: new_lb,new_ub = lb,ub-weight
                else:          new_lb,new_ub = lb-weight,ub

                # set value to one
                new_t = t-weight
                new_setting = setting + [1]
                child = (depth+1,new_t,new_lb,new_ub,new_setting)
                child = IntClassifier._round_small_numbers(child) # ACACAC
                if is_false(child):
                    false_count += 1
                    failing.append(new_setting)
                    upper_bound -= 2**(var_count-1)
                else:
                    IntClassifier._add_to_opened(child,accum_weights,opened)

                # set value to zero
                new_t = t
                new_setting = setting + [0]
                child = (depth+1,new_t,new_lb,new_ub,new_setting)
                child = IntClassifier._round_small_numbers(child) # ACACAC
                if is_false(child):
                    false_count += 1
                    failing.append(new_setting)
                    upper_bound -= 2**(var_count-1)
                else:
                    IntClassifier._add_to_opened(child,accum_weights,opened)

        bound_gap = (upper_bound-lower_bound)/2**c.size
        print("gap: %.4f%% (f-cost: %d)" % (bound_gap,f_cost))
        print("lower bound: ", lower_bound)
        print("upper bound: ", upper_bound)

        """
        # convert settings into copies of classifiers (very slow)
        failing = [ c.set_inputs(input_map,setting) for setting in failing ]
        passing = [ c.set_inputs(input_map,setting) for setting in passing ]
        """

        """
        closed = PriorityQueue()
        for item in closed_list:
            closed.put(item)
        return closed
        """
        return passing,failing,input_map


    def _add_to_opened_f(d,accum_weights,opened):
        IntClassifier.id_count += 1
        d = IntClassifier._round_small_numbers(d) # ACACAC
        depth,t,lb,ub,setting = d
        gap = ub-t
        if gap > 0:
            target = accum_weights[depth] + gap
            h_cost = IntClassifier._find(accum_weights,target,lo=depth+1)
        else: # already at goal
            h_cost = 0
        f_cost = depth + h_cost
        node = (f_cost,-IntClassifier.id_count,d)
        opened.put(node)


    def a_star_search_alt_f(self):
        
        from queue import PriorityQueue        

        c = self
        is_true =  lambda x: x[1] <= x[2]
        is_false = lambda x: x[1] > x[3]

        IntClassifier.id_count = 0
        closed_list = []
        opened = PriorityQueue()
        sorted_weights,accum_weights,input_map = c._search_weights()

        # initial threshold test
        depth = 0
        t = c.threshold
        lb = sum(w for w in sorted_weights if w < 0)
        ub = sum(w for w in sorted_weights if w > 0)
        setting = []

        d = (depth,t,lb,ub,setting)
        IntClassifier._add_to_opened_f(d,accum_weights,opened)

        true_count, false_count = 0,0
        lower_bound,upper_bound = 0,2**c.size
        passing, failing = [],[]
        print_me = 1

        while(not opened.empty()):
            f_cost,_,current = opened.get()
            depth,t,lb,ub,setting = current
            var_count = c.size - depth

            if IntClassifier.id_count % print_me == 0:
                print_me = print_me * 2
                #osize = opened.qsize()
                #csize = len(closed_list)
                #print("open/closed (cost): %d,%d (%d)" % (osize,csize,f_cost))
                #print("true/false: %d,%d" % (true_count,false_count))
                bound_gap = (upper_bound-lower_bound)/2**c.size
                #print("gap: %.4f%% (f-cost: %d)" % (bound_gap,f_cost))

            if is_false(current):
                false_count += 1
                failing.append(setting)
                upper_bound -= 2**var_count
            elif is_true(current):
                true_count += 1
                closed_list.append(current)
                passing.append(setting)
                lower_bound += 2**var_count
            else:
                weight = sorted_weights[depth]

                # update lower/upper bounds
                if weight > 0: new_lb,new_ub = lb,ub-weight
                else:          new_lb,new_ub = lb-weight,ub

                # set value to one
                new_t = t-weight
                new_setting = setting + [1]
                child = (depth+1,new_t,new_lb,new_ub,new_setting)
                child = IntClassifier._round_small_numbers(child) # ACACAC
                if is_false(child):
                    false_count += 1
                    failing.append(new_setting)
                    upper_bound -= 2**(var_count-1)
                else:
                    IntClassifier._add_to_opened_f(child,accum_weights,opened)

                # set value to zero
                new_t = t
                new_setting = setting + [0]
                child = (depth+1,new_t,new_lb,new_ub,new_setting)
                child = IntClassifier._round_small_numbers(child) # ACACAC
                if is_false(child):
                    false_count += 1
                    failing.append(new_setting)
                    upper_bound -= 2**(var_count-1)
                else:
                    IntClassifier._add_to_opened_f(child,accum_weights,opened)

        bound_gap = (upper_bound-lower_bound)/2**c.size
        print("gap: %.4f%% (f-cost: %d)" % (bound_gap,f_cost))
        print("lower bound: ", lower_bound)
        print("upper bound: ", upper_bound)

        """
        # convert settings into copies of classifiers (very slow)
        failing = [ c.set_inputs(input_map,setting) for setting in failing ]
        passing = [ c.set_inputs(input_map,setting) for setting in passing ]
        """

        """
        closed = PriorityQueue()
        for item in closed_list:
            closed.put(item)
        return closed
        """
        return passing,failing,input_map


    def a_star_search(self,passing):
        #import pdb
        #pdb.set_trace()
        from queue import PriorityQueue
        
        c = self

        closed_list = []
        closed = PriorityQueue() # ACAC: make this a list
        opened = PriorityQueue()
        count = 0
        path_count = 0
        true_count, false_count = 0,0
        lower_bound,upper_bound = 0,2**c.size

        g_cost = len(c.inputs.setting)
        h_cost = c.inputs.settings_needed(c.gap())
        opened.put((g_cost+h_cost,-count,c))

        goal = 0

        #import pdb; pdb.set_trace()

        while(not opened.empty()):
            current = opened.get()
            c = current[2]
            #print(c)
            if count % 100 == 0:
                print("open/closed (cost): %d,%d (%d)" % (opened.qsize(),len(closed_list),current[0]))
                print("true/false: %d,%d" % (true_count,false_count))

            if c.is_trivially_false():
                false_count += 1
                upper_bound -= 2**child0.size
                continue

            if c.is_trivially_true():
                true_count += 1
                path_count += 1
                passing.append(c)
                closed_list.append(current)
                lower_bound += 2**c.size
            else:
                path_count += 1
                index,weight = c.inputs.get_biggest_weight()
                child0 = c.set_input(index,0)
                child1 = c.set_input(index,1)

                #if not child0.is_trivially_false():
                count += 1
                g_cost = len(child0.inputs.setting)
                h_cost = child0.inputs.settings_needed(child0.gap())
                opened.put((g_cost+h_cost,-count,child0))

                #if not child1.is_trivially_false():
                count += 1
                g_cost = len(child1.inputs.setting)
                h_cost = child1.inputs.settings_needed(child1.gap())
                opened.put((g_cost+h_cost,-count,child1))

        #goals = []
        #while (not closed.empty()): goals.append(closed.get())
        print("nodes found: ", count+1)
        print("path nodes found: ", path_count)
        print("lower bound: ", lower_bound)

        for item in closed_list:
            closed.put(item)
        return closed
                




    def a_star_search_f(self,failing):
        #import pdb
        #pdb.set_trace()
        from queue import PriorityQueue
        
        c = self

        closed = PriorityQueue()
        opened = PriorityQueue()
        count = 0
        path_count = 0
        opened.put((c.size,count,c))

        goal = 0

        while(not opened.empty()):
            current = opened.get()
            c = current[2]

            if(current[2].is_trivially_false()):
                path_count += 1
                failing.append(current[2])
                closed.put(current)
                continue
            if(current[2].is_trivially_true()):
                continue
            else:
                path_count += 1
                index,weight = current[2].inputs.get_biggest_weight()

                child0 = current[2].set_input(index,0)
                child1 = current[2].set_input(index,1)
                count += 1
                #opened.put((child0.gap(),count,child0))
                opened.put((len(child0.inputs.setting),count,child0))
                count += 1
                #opened.put((child1.gap(),count,child1))
                opened.put((len(child1.inputs.setting),count,child1))

        #goals = []
        #while (not closed.empty()): goals.append(closed.get())
        #print("nodes found: ", count+1)
        #print("path nodes found: ", path_count)
        #print("goals found: ", len(goals))

        return closed
                
                
    def a_star_graph(self,pq,fq):
        import matplotlib.pyplot as plt
        #import pdb
        #pdb.set_trace()
        x = [0]
        y = [0]
        x2 = [0]
        y2 = [2**self.size]
        count = 0
        size = fq.qsize()

        while(not pq.empty()):
            current = pq.get()
            y.append(y[count] + 2**len((current[2].inputs.weights)))
            count += 1
            x.append(count)
        count = 0
        while(not fq.empty()):
            current = fq.get()
            y2.append(y2[count] - 2**len((current[2].inputs.weights)))
            count += 1
            x2.append(count)
            
        plt.plot(x,y,marker='*',markersize=1)
        plt.plot(x2,y2,marker='*',markersize=1)
        plt.axhline(y = y2[size], color = 'red', linestyle = '--')

        #plt.show()

            
    def make_image(self,image,label,passing,failing,image_filename=None):
        import numpy as np
        import matplotlib
        from matplotlib import pyplot as plt

        fs = 18 # fontsize
        matplotlib.rcParams.update({'xtick.labelsize': fs, 
                                    'ytick.labelsize': fs,
                                    'figure.autolayout': True})
        font = {'family' : 'sans-serif',
                'weight' : 'normal',
                'size'   : 15}
        matplotlib.rc('font', **font)
        plt.tick_params(left = False, right = False , labelleft = False ,
                        labelbottom = False, bottom = False)

        found = False
        if label == 1:
            for leaf in passing:
                leaf.remove_nonreducing()
                if not leaf.is_consistent(image): continue
                for var,(val,w) in leaf.inputs.setting.items():
                    image[var] = 2 if val == 1 else -1
                found = True
                break
     
        if label == 0:
            for leaf in failing:
                leaf.remove_nonreducing_f()
                if not leaf.is_consistent(image): continue
                for var,(val,w) in leaf.inputs.setting.items():
                    image[var] = 2 if val == 1 else -1
                found = True
                break

        if found is False:
            print("warning: consistent leaf not found")

        image = image.reshape(28,28)
        plt.imshow(image, cmap='gray', vmin=-1, vmax=2)
        if image_filename:
            plt.savefig(image_filename + ".pdf")
            plt.savefig(image_filename + ".png")
        #plt.show()
        plt.clf()

    def is_consistent(self,instance):
        setting = self.inputs.setting
        for var in setting:
            val,w = setting[var]
            if instance[var] != val:
                return False
        return True

    def remove_nonreducing(self):
        valarr = list(self.inputs.setting.values())
        keyarr = list(self.inputs.setting.keys())
        for x in range(len(valarr)):
            if valarr[x][0] == 0 and valarr[x][1] > 0:
                self.inputs.setting.pop(keyarr[x])
            if valarr[x][0] == 1 and valarr[x][1] < 0:
                self.inputs.setting.pop(keyarr[x])

    def remove_nonreducing_f(self):
        #import pdb
        #pdb.set_trace()
        valarr = list(self.inputs.setting.values())
        keyarr = list(self.inputs.setting.keys())
        for x in range(len(valarr)):
            if valarr[x][0] == 0 and valarr[x][1] < 0:
                self.inputs.setting.pop(keyarr[x])
            if valarr[x][0] == 1 and valarr[x][1] > 0:
                self.inputs.setting.pop(keyarr[x])
        
    def a_star_graph_alt(self,passing,failing,linestyle='-'):
        import numpy as np
        import matplotlib
        import matplotlib.pyplot as plt
        import math

           
        fs = 12 # fontsize
        matplotlib.rcParams.update({'xtick.labelsize': fs,
                                    'ytick.labelsize': fs,
                                    'figure.autolayout': True})
        #matplotlib.rcParams.update({'figure.autolayout': True})

        font = {'family' : 'sans-serif',
                'weight' : 'normal',
                'size'   : 14}
        matplotlib.rc('font', **font)
        matplotlib.rcParams['pdf.fonttype'] = 42
        

        n = self.size # number of variables

        lower_counts = [0] + [ 2**(n-len(cur)) for cur in passing ]
        upper_counts = [0] + [ 2**(n-len(cur)) for cur in failing ]

        diff = len(lower_counts) - len(upper_counts)
        if diff > 0: # upper_counts is shorter
            upper_counts += [0]*diff
        else:        # lower_counts is shorter
            lower_counts += [0]*-diff

        lower_bound = np.cumsum(lower_counts)
        upper_bound = 2**n - np.cumsum(upper_counts)

        boundct = 0
        coverage_limit = 95
        for i,(lower_count,upper_count) in enumerate(zip(lower_counts,upper_counts)):
            boundct += lower_count + upper_count
            coverage = 100*boundct/2**n
            y_lower,y_upper = lower_bound[i],upper_bound[i]
            if(coverage >= coverage_limit):
                print("#Explanations",i)
                print("percentage %.2f%%" % (coverage,))
                break

        #plt.yscale("log") 
        plt.plot(np.arange(len(lower_bound)),lower_bound,color='blue',linestyle=linestyle,linewidth=1)
        plt.plot(np.arange(len(upper_bound)),upper_bound,color='red',linestyle=linestyle,linewidth=1)
        plt.axhline(lower_bound[-1],color = 'purple',linestyle = '--',linewidth=2)
        #plt.axvline(i,color = 'black', linestyle = "--")
        plt.plot([i,i],[y_lower,y_upper],color='black',linestyle='-',marker='o',markersize=3)
        plt.xlabel('# of explanations')
        plt.ylabel('model count')
        plt.savefig("boundsplot.pdf") 
        #plt.show()


    def voting_analysis(self, passing, failing):
        #import pdb
        #pdb.set_trace()
        
        passkeys = passing[0].inputs.setting.keys()
        passvals = passing[0].inputs.setting.values()
        failkeys = failing[0].inputs.setting.keys()
        failvals = failing[0].inputs.setting.values()
        print("democrat",passing[0].inputs.setting)
        print("republican",failing[0].inputs.setting)


    
        
    def vote_desc(self,passing,failing,filedir):
        import numpy as np
        from matplotlib import pyplot as plt
        #import pdb
        #pdb.set_trace()
        
        with open(filedir, 'r') as f:
            voter = f.readlines()[0].split(',')
    
        voter = np.array(voter)
        se = []
        print(voter)
        for x in failing[0].inputs.setting.keys():
            vo = x,failing[0].inputs.setting[x][0]
            se.append(vo)
        se = sorted(se)
        print(se)  
        
    
    def pick_first(self,passing,failing):
        #import pdb;
        #pdb.set_trace()
        
        c = self
        
        if c.is_trivially_true():
            #print()
            #print(c.inputs)
            passing.append(c)
            return
            

        if c.is_trivially_false():
            failing.append(c)
            return
        
        ran = c.inputs.weights.keys()
        for x in ran:
            if c.inputs.weights[x]!=0:
                index,weight = x,c.inputs.weights[x]
        
       
        if(weight<0):
            b = c.set_input(index,0)
            b.pick_first(passing,failing)

            a = c.set_input(index,1)
            a.pick_first(passing,failing)
        else:    
            a = c.set_input(index,1)
            a.pick_first(passing,failing)

            b = c.set_input(index,0)
            b.pick_first(passing,failing)


    def pick_first_graph(self,passing,failing):
        c = self
        import matplotlib.pyplot as plt
        x = [0]
        y = [0]
        for i in range(len(passing)):
            x.append(i+1)
            y.append(y[i] + 2**len(passing[i].inputs.weights))
        f = 0
        f += 2**c.size

        x2 = [0] 
        y2 = [f] 
        for i in range(len(failing)):
            x2.append(i+1)
            y2.append(y2[i] - 2**len(failing[i].inputs.weights))
        
        plt.axhline(y = y2[len(failing)], color = 'black', linestyle = '--')
        plt.plot(x,y,color = 'blue',linestyle = 'dotted')
        plt.plot(x2,y2,color = 'red',linestyle = "dotted")
        #plt.show()


    def num_of_votes(self,filedir):
        with open(filedir, "r") as file:
            lines = file.readlines()
        lines = [line.rstrip().split(",") for line in lines]

        repy = 0
        repn = 0
        repq = 0
        demy = 0
        demn = 0
        demq = 0
        votingtotals = {}
        for x in range(1,17):
            for subarray in lines:
                if(subarray[0] == 'republican'):
                    if(subarray[x] == 'y'):
                        repy += 1
                    if(subarray[x] == 'n'):
                        repn += 1
                    if(subarray[x] == '?'):
                        repq += 1
                if(subarray[0] == 'democrat'):
                    if(subarray[x] == 'y'):
                        demy += 1
                    if(subarray[x] == 'n'):
                        demn += 1
                    if(subarray[x] == '?'):
                        demq += 1
            #import pdb
            #pdb.set_trace()
            votingtotals[x] = repy,repn,repq,demy,demn,demq
            repy,repn,repq,demy,demn,demq = 0,0,0,0,0,0
                
        print("republican y:",repy)
        print("republican n:",repn)
        print("republican ?:",repq)
        print("democrat y:",demy)
        print("democrat n:",demn)
        print("democrat ?:",demq)


        with open('testing/congressionalvoting/votingtotals.tex','w') as file:
            headers = ["RY","RN","R?","DY","DN","D?"]
            texttabular = f"l||{'r|'*len(headers)}"
            textheader = "bill & " + " & ".join(headers) + "\\\\"
            textdata = "\\hline"
            data = dict()
            for x in range(1,17):
                data[x] = votingtotals[x]

            for label in data:
                textdata += f"{label} & {' & '.join(map(str,data[label]))} \\\\\n"
        
            file.write("\\begin{table}[t]")
            file.write("\\centering")
            file.write("\\small")
            file.write("\\setlength{\\tabcolsep}{2pt}")
            file.write("\\caption{1984 Congressional Voting Totals} \label{table:voting2}")
            file.write("\\begin{tabular}{"+texttabular+"}\n")
            file.write(textheader)
            file.write(textdata)
            file.write("\\end{tabular}")
            file.write("\\end{table}")

    def bounds_graphs(self, passing, failing, passing2, failing2, c, d, tt):
        import numpy as np
        import matplotlib
        import matplotlib.pyplot as plt
        from functools import reduce

        n = self.size
        passing, failing = c.latex_truth_table(passing, failing)
        passing2, failing2 = d.latex_truth_table(passing2, failing2)

        passing.insert(0, [])
        failing.insert(0, [])
        passing2.insert(0, [])
        failing2.insert(0, [])

        innerboundtt = c.inner_bound_tt()  # truth table of first neuron with all outputs set to 0
        innerboundtt2 = d.inner_bound_tt()  # truth table of second neuron with all outputs set to 0

        count = 0
        count2 = 0
        countones = np.zeros((len(passing), len(passing2)))  # numpy 2d array

        for count, PI in enumerate(passing):  # iterates through prime implicants of the first neuron
            for item in PI:
                i = reduce(lambda x, y: 2 * x + y, item, 0)
                innerboundtt[i][-1] = 1
            for count2, PI2 in enumerate(passing2):  # iterates through prime implicants of second neuron
                for item2 in PI2:  # iterates through all possible settings of the implicant
                    i = reduce(lambda x, y: 2 * x + y, item2, 0)
                    innerboundtt2[i][-1] = 1
                result = self.tt_or(innerboundtt,
                                         innerboundtt2)  # uses tt_and function to compute the and of the two neurons
                countones[count][count2] = (
                    sum(1 for num in result if num == 1))  # counts the number of 1s in truth table
            innerboundtt2 = d.inner_bound_tt()  # sets all tt outputs to 0

        # print(countones)
        size = len(passing)
        size2 = len(passing2)
        Y = np.arange(size)
        X = np.arange(size2)
        X, Y = np.meshgrid(X, Y)
        Z = countones

        print(X)
        print(Y)
        print(Z)


        ax = plt.figure().add_subplot(projection='3d')
        fs = 12  # fontsize
        matplotlib.rcParams.update({'xtick.labelsize': fs,
                                    'ytick.labelsize': fs,
                                    'figure.autolayout': True})
        # matplotlib.rcParams.update({'figure.autolayout': True})

        font = {'family': 'sans-serif',
                'weight': 'normal',
                'size': 14}
        matplotlib.rc('font', **font)
        matplotlib.rcParams['pdf.fonttype'] = 42

        surf = ax.plot_surface(X, Y, Z,
                               linewidth=0, antialiased=False)
        ax.set_xlabel('#PI N1')
        ax.set_ylabel('#PI N2')
        ax.set_zlabel('1 output')

        plt.show()

    def truth_table(self):

        # import pdb; pdb.set_trace()
        num_inputs = len(self.weights)
        inputs = list(itertools.product([0, 1], repeat=num_inputs))

        def function(*args):
            weighted_sum = sum(w * i for w, i in zip(self.weights, args))
            return weighted_sum >= self.threshold

        header = '\t'.join(str(self.weights[i]) for i in range(num_inputs)) + " Output"
        # print(header)

        table = []

        for input_values in inputs:
            output = function(*input_values)
            if output == True:
                input_val = input_values + (1,)
                table.append(input_val)
            else:
                input_val = input_values + (0,)
                table.append(input_val)

        return table


    def outer_bound_tt(self):
        num_inputs = len(self.weights)
        inputs = list(itertools.product([0, 1], repeat=num_inputs))

        table = []

        for input_values in inputs:
            input_val = input_values + (1,)
            table.append(list(input_val))

        return table

    def inner_bound_tt(self):
        num_inputs = len(self.weights)
        inputs = list(itertools.product([0, 1], repeat=num_inputs))

        table = []

        for input_values in inputs:
            input_val = input_values + (0,)
            table.append(list(input_val))

        return table

    def tt_and(self, c, d):

        ttand = []
        for b1, b2 in zip(c, d): ttand.append(b1[-1] and b2[-1])
        return ttand

    def tt_or(self, c, d):

        ttand = []
        for b1, b2 in zip(c, d): ttand.append(b1[-1] or b2[-1])
        return ttand

    def latex_truth_table(self,passing,failing):
        #import pdb; pdb.set_trace()
        truthtablep = []
        for item in passing:
            ttp = [None] * len(self.inputs.weights)
            for key,value in item.inputs.weights.items():
                ttp[key] = (0, 1)
            for key,value in item.inputs.setting.items():
                ttp[key]= (value[0], )
            truthtablep.append(list(product(*ttp)))
        truthtablef = []
        for item in failing:
            ttf = [None] * len(self.inputs.weights)
            for key,value in item.inputs.weights.items():
                ttf[key] = (0, 1)
            for key,value in item.inputs.setting.items():
                ttf[key]= (value[0], )
            truthtablef.append(list(product(*ttf)))

        return truthtablep,truthtablef

        self.truth_table_latex(passing,failing,truthtablep,truthtablef)

    def truth_table_latex(self,passing,failing,ttp,ttf):
        #import pdb; pdb.set_trace()

        num_cols = self.size
        num_rows = len(ttp)

        #first = list(product(*ttp[0]))
        #print(first)
        #print(ttp)



        latex = r'''\documentclass{article}
\begin{document}
\begin{center}
\small'''

        prevrow = '    '
        for element in ttp:
            latex += r'''
\begin{tabular}{''' + 'c' * num_cols + r'''|c}
'''


            header_line = ''
            for i in range(0, num_cols):
                header_line += f'$I_{i}$ & '
            header_line += r'$f$ \\\hline'
            latex += header_line + '\n'

            row = '    '
            row += prevrow
            for item in element:
                for cell_data in item:
                    row += ' \\textbf{' + str(cell_data) + '}'
                    row += ' & '
                    prevrow += str(cell_data)
                    prevrow += ' & '
                row += '1 \\\\\n'
                prevrow+='1 \\\\\n'
            latex += row
            row = '    '

            latex += r'''\end{tabular}
\quad\quad'''
        latex += r'''
\end{center}
'''

        latex+= r'''
\begin{center}
\small
'''

        prevrow = '    '
        for element in ttf:
            latex += r'''
\begin{tabular}{''' + 'c' * num_cols + r''' | c}
'''
            header_line = ''
            for i in range(0, num_cols):
                header_line += f'$I_{i}$ & '
            header_line += r'$f$ \\\hline'
            latex += header_line + '\n'

            row = '    '
            row += prevrow
            for item in element:
                for cell_data in item:
                    row += ' \\textbf{' + str(cell_data) + '}'
                    row += ' & '
                    prevrow += str(cell_data)
                    prevrow += ' & '
                row += '0 \\\\\n'
                prevrow+='0 \\\\\n'
            latex += row
            row = '    '

            latex += r'''\end{tabular}
\quad\quad'''
        latex += r'''
\end{center}
'''

        latex += r'''\end{document}'''



        with open("truth_table.tex", "w") as f:
                f.write(latex)



if __name__ == '__main__':
    precision = 2
    #filename = 'examples/169_wd2_0'
    #output_filename = 'examples/169_wd2_0-quantized'
    filename = 'examples/9_wd2_0'
    output_filename = 'examples/9_wd2_0-quantized'
    #filename = 'examples/test.nn'
    #output_filename = 'examples/test-quantized.nn'
    c = Classifier.read(filename)
    print(c)
    d = c.with_precision(precision)
    print(d)
    d.save(output_filename)
    with Timer("compiling"):
        obdd_manager,node = d.compile()
    with Timer("size"):
        count_before = len(list(node))
    with Timer("reducing"):
        node = node.reduce()
    with Timer("size"):
        count_after = len(list(node))
    print("node count before reduce: %d" % count_before)
    print(" node count after reduce: %d" % count_after)

    obdd_manager.save_vtree("tmp.vtree")
    obdd_manager.save_sdd("tmp.sdd",node)

    with Timer("to sdd"):
        offset = int(c.offset)
        sdd_manager,sdd_node = obdd_manager.obdd_to_sdd(node,offset=offset)
    with Timer("read sdd"):
        sdd_filename = b'tmp.sdd'
        alpha = sdd_manager.read_sdd_file(sdd_filename)

    print("sdd nodes/size: %d/%d" % (sdd_node.count(),sdd_node.size()))
    print("sdd nodes/size: %d/%d" % (alpha.count(),alpha.size()))

# %%
from collections import defaultdict, Counter

# %%
fname = "/home/max/projects/cp_playground/hashcode2021/a.txt"

with open(fname) as fp:
    duration, nintersects, nstreets, ncars, bonus = map(
        lambda x: int(x), fp.readline().split()
    )

    streets = {}
    intersects_out = defaultdict(list)
    intersects_in = defaultdict(list)
    for _ in range(nstreets):
        source, dest, name, time = fp.readline().split()
        streets[name] = (source, dest, time)

        intersects_out[source].append((dest, name, time))
        intersects_in[dest].append((source, name, time))

    routs = []
    for _ in range(ncars):
        routs.append(fp.readline().split())

# %%
street_counter = Counter()
for rout in routs:
    street_counter.update(rout[1:])

busy_streets = sorted(
    street_counter.items(), key=lambda item: item[-1], reverse=True
)

# %%

# Idea 1
# {car: (street_name, pos)}
# {street_name -> intersection}
# {intersaction -> [street1, street2, ..]}


# Idea 2
# {street_name: (queue([(car 1, str_idx, time_added), (car 2, time_left]), inter_id)}
# {streets: }

class Simulation:

    def __init__(
        self, 
        sim_time, 
        bonus, 
        routs, 
        streets, 
        intersects_in, 
        intersects_out, 
    ):
        self.sim_time = sim_time
        self.bonus = bonus
        self.routs = routs
        self.streets = streets
        self.intersects_in = intersects_in
        self.intersects_out = intersects_out

        self.total_reward = 0
        self.state = {key: (value[1], []) for key, value in streets.items()}

    def initialize_state(self):
        inital_streets = [rout[1] for rout in routs]
        for name in inital_streets:
            self.state[name][-1].append(int(self.streets[name][-1]))

        pass

    # {intersection: [street1, street1, street2]}
    #    state2 {intersaction : queue(street : time_remained_green), ()]}

    #(a a b b b c c)
    
    # {0: [(intersection, a), (intersection, b), (intersection, c) ...], 
    # 1: [(intersection, b), (intersection, c) ... ]}
    def func(self, intersection, strategy):
        street_queue = self.light_state[intersection]
        intersection_stratagy = strategy[intersection]
        
        street_name, t = street_queue.popleft()
        t -= 1

        if t == 0:
            street_queue.append((street_name, intersection_stratagy[street_name]))
        else:
            street_queue.appendleft((street_name, t))

        return street_name

    def run(self, strategy):
        self.light_state = defaultdict(list)
        
        for intersect, od in strategy.items():
            for street_name, time in od:
                self.light_state[intersect].append((street_name, time))

        for t in range(self.sim_time):
            for name, (queue, intersection) in self.state:
                
                if name == self.func(intersection, strategy):
                    
                    if queue[0][-1] <= 0:
                        car, street_index, *_ = queue.popleft()
                        
                        next_street = self.routs[car][street_index + 1]
                        if street_index == len(self.routs[car]) - 2:
                            if (self.sim_time - t) >= self.streets[next_street][-1]:
                                self.total_reward += self.bonus + t

                        else:
                            self.state[next_street][0].append(
                                car, street_index + 1, self.streets[next_street][-1]
                            )

                for i in enumerate(queue):
                    queue[i][-1] -= 1

            pass

        pass

    # 
    def func(intersection, name, strategy):
        pass

    def run(self, strategy):
        # {inter_id: [("street_name", time), ...]}
        for t in range(self.sim_time):
            # Iterate over every street in the state
            for name, (queue, intersection) in self.state:
                
                if func(intersection, name, strategy):
                    
                    if queue[0][-1] <= 0:
                        car, street_index, *_ = queue.popleft()
                        
                        next_street = self.routs[car][street_index + 1]
                        if street_index == len(self.routs[car]) - 2:
                            if (self.sim_time - t) >= self.streets[next_street][-1]:
                                self.total_reward += self.bonus + t

                        else:
                            self.state[next_street][0].append(
                                car, street_index + 1, self.streets[next_street][-1]
                            )
                        
                # Decrease the time for all cars in the queu
                for i in enumerate(queue):
                    queue[i][-1] -= 1

            pass

        pass

    # 
    def func(intersection, name, strategy):
        pass

    def run(self, strategy):
        # {inter_id: [("street_name", time), ...]}
        for t in range(self.sim_time):
            # Iterate over every street in the state
            for name, (queue, intersection) in self.state:
                
                if func(intersection, name, strategy):
                    
                    if queue[0][-1] <= 0:
                        car, street_index, *_ = queue.popleft()
                        
                        next_street = self.routs[car][street_index + 1]
                        if street_index == len(self.routs[car]) - 2:
                            if (self.sim_time - t) >= self.streets[next_street][-1]:
                                self.total_reward += self.bonus + t

                        else:
                            self.state[next_street][0].append(
                                car, street_index + 1, self.streets[next_street][-1]
                            )
                        
                # Decrease the time for all cars in the queu
                for i in enumerate(queue):
                    queue[i][-1] -= 1

            pass

        pass

    # 
    def func(intersection, name, strategy):
        pass

    def run(self, strategy):
        # {inter_id: [("street_name", time), ...]}
        for t in range(self.sim_time):
            # Iterate over every street in the state
            for name, (queue, intersection) in self.state:

                if func(intersection, name, strategy):
                    
                    if queue[0][-1] <= 0:
                        car, street_index, *_ = queue.popleft()
                        
                        next_street = self.routs[car][street_index + 1]
                        if street_index == len(self.routs[car]) - 2:
                            if (self.sim_time - t) >= self.streets[next_street][-1]:
                                self.total_reward += self.bonus + t

                        else:
                            self.state[next_street][0].append(
                                car, street_index + 1, self.streets[next_street][-1]
                            )
                        
                # Decrease the time for all cars in the queu
                for i in enumerate(queue):
                    queue[i][-1] -= 1

            pass



def missing_value(array, start, end):
    array.sorted()
    for eleemnt, target in zip(array, range(start, end)):
        if eleemnt != target:
            return False

    return True
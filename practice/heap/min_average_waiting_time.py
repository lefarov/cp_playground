from heapq import heappush, heappop

class Customer:
    
    def __init__(self, arrive_t, order_t):
        self.arrive_t, self.order_t = arrive_t, order_t
    
    def __lt__(self, value):
        return self.order_t < value.order_t


def minimumAverage(customers):
    customers = [Customer(*customer) for customer in customers]
    customers.sort(key=lambda customer: customer.arrive_t)

    min_heap = []
    heappush(min_heap, customers[0])
    
    time = customers[0].arrive_t
    waiting_time = 0
    i = 1

    while i < len(customers) or len(min_heap) > 0:
        while i < len(customers) and customers[i].arrive_t <= time:
            heappush(min_heap, customers[i])
            i += 1
        
        if len(min_heap) > 0:
            min_customer = heappop(min_heap)
            waiting_time += time + min_customer.order_t - min_customer.arrive_t
            time += min_customer.order_t
        else:
            time += 1
    
    return int(waiting_time / len(customers))


if __name__ == "__main__":
    # 9
    print(minimumAverage([ [0, 3], [1, 9], [2, 6] ]))
    # 8
    print(minimumAverage([ [0, 3], [1, 9], [2, 5] ]))

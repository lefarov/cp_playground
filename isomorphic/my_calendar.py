import collections 

class MyCalendar:

    def __init__(self):
        self.meetings = collections.deque()
        

    def book(self, startTime: int, endTime: int) -> bool:

        # ----    -----      -----  ---
        #              xxxxx

        # [1, 2, 3]
        # find closest to target from the right
        # [

        # insert in head
        if not self.meetings or endTime <= self.meetings[0][0]:
            self.meetings.insert(0, (startTime, endTime))
            return True
        

        lp, rp = 0, len(self.meetings) - 1
        closest_l = None
        while lp <= rp:
            mp = (lp + rp) // 2
            if self.meetings[mp][1] <= startTime:
                lp = mp + 1
                closest_l = mp
            else:
                rp = mp - 1

        
        if closest_l is not None and (closest_l == len(self.meetings) - 1 or endTime <= self.meetings[closest_l + 1][0]):
            self.meetings.insert(closest_l + 1, (startTime, endTime))
            return True
        else:
            return False
        

if __name__ == "__main__":
    calendar = MyCalendar()
    calendar.book(10, 20)
    calendar.book(15, 25)
    calendar.book(20, 30)
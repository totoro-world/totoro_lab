import time
import math
    
class State:
    pic_dic = {'a': "1567045766159.png"}
    one_loop_times = 3
    
    def __init__(self, name):
        self.name = name
        self.pic = State.pic_dic[self.name]
        self.special_action_index = 0
        self.times = 0

    def get_match(self):
        m = find(Pattern(self.pic).similar(0.7))
        return m

    def start(self):
        self.loop()

    def loop(self):
        while self.times < State.one_loop_times:
            if exists("1567061024575.png"):
                type('f10')
                wait(self.pic, 10)
                
            self.times = self.times + 1
            m = State.find_target()
            self.mv_to(m)
            self.special_action()

    def find_target():
        target_list = ["1567045777539.png"]
        for t in target_list:
            m = exists(Pattern(t).similar(0.7), 0)
            if m is not None:
                return m

    def mv(self, to_m):
        from_target = self.get_match().getBottomLeft()
        to_target = to_m.getBottomLeft()
        x_diff = to_target.getX() - from_target.getX()
        y_diff = to_target.getY() - from_target.getY()
        distance = math.sqrt(math.pow(x_diff, 2) + math.pow(y_diff, 2))
        key_list = []
        if x_diff > 0:
            key_list.append('f')
        if x_diff < 0:
            key_list.append('s')
        if y_diff > 0:
            key_list.append('d')
        if y_diff < 0:
            key_list.append('e')
        self.walk(key_list, distance)
        
    def normal_action():
        type('a')

    def special_action(self):
        action_list = ['A', 'B']
        type(action_list[self.special_action_index])
        self.special_action_index = self.special_action_index + 1

    def walk(self, key, distance):
        s = distance / 50.0
        keyDown(key)
        time.sleep(s)
        keyUp(key)

def one_state():
    pass  

state = State('a')
state.loop()

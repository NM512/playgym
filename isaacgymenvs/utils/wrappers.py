import numpy as np
from gym import Wrapper
from gym.spaces import Box
import time
from handy_agent_controller import HandPoseDetector
import torch
import _thread

from isaacgym import gymapi
gym = gymapi.acquire_gym()

class TestAction(Wrapper):
    def __init__(self, env):
        super().__init__(env)
        self.sim_started = False
        self.hpd = HandPoseDetector(True)
        self.input_exist = False

    def __wait_key(self):
        ans = input('Simulation Start? input y(es) \n')
        if ans in ['y', 'Y']:
            self.sim_started = True
        self.input_exist = True
        return

    def step(self, action):
        # waiting that sim is started from CL
        while not self.sim_started:
            # render is necessary while waiting keyboard input 
            _thread.start_new_thread(self.__wait_key, ())
            while not self.input_exist:
                self.env.render()
            self.input_exist = False

        joint_angles = self.hpd.take_joint_angles()
        action = torch.zeros(20)

        action[3] = joint_angles['index']['third']  - 0.5
        action[4] = joint_angles['index']['second'] - 0.5
        action[6] = joint_angles['middle']['third'] - 0.5
        action[7] = joint_angles['middle']['second'] - 0.5
        action[9] = joint_angles['ring']['third'] - 0.5
        action[10] = joint_angles['ring']['second'] - 0.5
        action[13] = joint_angles['pinky']['third'] - 0.5
        action[14] = joint_angles['pinky']['second'] - 0.5
        action[18] = joint_angles['thumb']['second'] - 0.5
        action[19] = joint_angles['thumb']['first'] - 0.25
        action = action*4.0
        
        # 0:WRZ
        # 1:WRY
        # 2:I1Z
        # 3:I1Y
        # 4:I2Y
        # 5:M1Z
        # 6:M1Y
        # 7:M2Y
        # 8:R1Z
        # 9:R1Y
        # 10:R2Y
        # 11:parm YZ
        # 12:P1Z
        # 13:P1Y
        # 14:P2Y
        # 15:T1 rotate?
        # 16:T1Z
        # 17 T1Z
        # 18 T1Y
        # 19 T2Y

        o, rew, reset, extras = self.env.step(action)
        
        # this part is for just IsaacGym? (might be used for others)
        assert len(reset) == 1
        # if reset[0]:
        #     self.started = False
        
        return o, rew, reset, extras

    # used when using Env other than IsaacGym
    # def reset(self):
    #     self.sim_started = False
    #     return self.env.reset()

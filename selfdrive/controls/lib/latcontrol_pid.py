from selfdrive.controls.lib.pid import PIController
from selfdrive.controls.lib.drive_helpers import get_steer_max
from cereal import car
from cereal import log
from selfdrive.kegman_conf import kegman_conf

import common.MoveAvg as  moveavg1
from selfdrive.config import Conversions as CV

class LatControlPID():
  def __init__(self, CP):
    self.kegman = kegman_conf(CP)
    self.deadzone = float(self.kegman.conf['deadzone'])
    self.pid = PIController((CP.lateralTuning.pid.kpBP, CP.lateralTuning.pid.kpV),
                            (CP.lateralTuning.pid.kiBP, CP.lateralTuning.pid.kiV),
                            k_f=CP.lateralTuning.pid.kf, pos_limit=1.0, sat_limit=CP.steerLimitTimer)
    self.angle_steers_des = 0.
    self.mpc_frame = 0

    self.movAvg = moveavg1.MoveAvg()

  def reset(self):
    self.pid.reset()
    
  def live_tune(self, CP):
    self.mpc_frame += 1
    if self.mpc_frame % 300 == 0:
      # live tuning through /data/openpilot/tune.py overrides interface.py settings
      self.kegman = kegman_conf()
      if self.kegman.conf['tuneGernby'] == "1":
        self.steerKpV = [float(self.kegman.conf['Kp'])]
        self.steerKiV = [float(self.kegman.conf['Ki'])]
        self.steerKf = float(self.kegman.conf['Kf'])
        self.pid = PIController((CP.lateralTuning.pid.kpBP, self.steerKpV),
                            (CP.lateralTuning.pid.kiBP, self.steerKiV),
                            k_f=self.steerKf, pos_limit=1.0)
        self.deadzone = float(self.kegman.conf['deadzone'])
        
      self.mpc_frame = 0    

  def update(self, active, v_ego, angle_steers, angle_steers_rate, eps_torque, steer_override, rate_limited, CP, path_plan):

    self.live_tune(CP)
 
    pid_log = log.ControlsState.LateralPIDState.new_message()
    pid_log.steerAngle = float(angle_steers)
    pid_log.steerRate = float(angle_steers_rate)

    v_ego_kph = v_ego * CV.MS_TO_KPH

    if v_ego < 0.3 or not active:
      output_steer = 0.0
      pid_log.active = False
      #self.angle_steers_des = 0.0
      self.pid.reset()
      self.angle_steers_des = self.movAvg.get_data( path_plan.angleSteers, 500 )
    else:
      if v_ego_kph < 5:
        self.angle_steers_des = self.movAvg.get_data( path_plan.angleSteers, 350 )
      if v_ego_kph < 10:
        self.angle_steers_des = self.movAvg.get_data( path_plan.angleSteers, 200 )
      elif v_ego_kph < 20:
        self.angle_steers_des = self.movAvg.get_data( path_plan.angleSteers, 100 )
      elif v_ego_kph < 30:
        self.angle_steers_des = self.movAvg.get_data( path_plan.angleSteers, 50 )
      elif v_ego_kph < 40:
        self.angle_steers_des = self.movAvg.get_data( path_plan.angleSteers, 10 )
      else:
        self.angle_steers_des = self.movAvg.get_data( path_plan.angleSteers, 5 )


      

      steers_max = get_steer_max(CP, v_ego)
      self.pid.pos_limit = steers_max
      self.pid.neg_limit = -steers_max
      steer_feedforward = self.angle_steers_des   # feedforward desired angle


      if CP.steerControlType == car.CarParams.SteerControlType.torque:
        # TODO: feedforward something based on path_plan.rateSteers
        steer_feedforward -= path_plan.angleOffset   # subtract the offset, since it does not contribute to resistive torque
        steer_feedforward *= v_ego**2  # proportional to realigning tire momentum (~ lateral accel)
      
      deadzone = self.deadzone    
        
      check_saturation = (v_ego > 10) and not rate_limited and not steer_override
      output_steer = self.pid.update(self.angle_steers_des, angle_steers, check_saturation=check_saturation, override=steer_override,
                                     feedforward=steer_feedforward, speed=v_ego, deadzone=deadzone)
      pid_log.active = True
      pid_log.p = self.pid.p
      pid_log.i = self.pid.i
      pid_log.f = self.pid.f
      pid_log.output = output_steer
      pid_log.saturated = bool(self.pid.saturated)

    delta = self.angle_steers_des - path_plan.angleSteers

    return output_steer, float(self.angle_steers_des), pid_log

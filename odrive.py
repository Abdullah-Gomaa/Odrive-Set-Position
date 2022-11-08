import odrive 
import rospy

from std_msgs.msg import Int16

pos = 0

def callback(msg):
    pos = msg.data

def listen():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('/speeds', Int16, callback)
    rospy.spin()

def setLimitsOdrive(odrv0, I_limit, Vel_limit, brake_resis, cpr):
    odrv0.axis0.motor.config.current_lim = I_limit
    odrv0.axis0.controller.config.vel_limit = Vel_limit
    odrv0.config.enable_brake_resistor
    odrv0.config.brake_resistance = brake_resis
    odrv0.axis0.encoder.config.cpr = cpr
    odrv0.save_configuration()
    

def controlPos(position):
    odrv0.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
    odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
    odrv0.axis0.controller.input_pos = position


if __name__ == "__main__":
    odrv0 = odrive.find_any()
    listen()
    setLimitsOdrive(odrv0, 10, 2, 1000, 512)
    controlPos(pos)

    
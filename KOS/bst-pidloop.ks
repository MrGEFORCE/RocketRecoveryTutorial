clearscreen.
print "autolanding started.".
local gear_flag is 0.
set target_alt to 0.
AG8 on.
gear off.
sas off.
rcs on.
lock steering to R(srfRetrograde:pitch,srfRetrograde:yaw+10,srfRetrograde:roll).
set throttle_pid to pidLoop(0.01, 0.0, 0.05, 0, 1).
set throttle_pid:setpoint to target_alt.
wait until alt:radar < 26000.
lock throttle to 0.33.
wait until ship:velocity:surface:mag < 1300.
lock throttle to 0.
wait until alt:radar < 1000.
print"PID started.".
until FALSE{
    if gear_flag = 0 and alt:radar < 250{ 
        gear on.
        set gear_flag to 1.
    }
    if ship:groundspeed < 30{ 
        lock steering to srfRetrograde.
    }
    lock throttle to throttle_pid:update(time:seconds, alt:radar).
    print "altitude(btm):"+round(alt:radar,2) at (20,10).
    if alt:radar <18{
        lock throttle to 0.
        print "PID ended.".
        break.
    }
}
rcs off.
unlock throttle.
unlock steering.
set ship:control:pilotmainthrottle to 0.
print "autolanding completed.".

(define (problem task)
(:domain ohmni_follow_domain)
(:objects
    butler - robot
    p1 - person
    ga - goal_angle
    minth maxth - threshold_angle
    gd - goal_dist
    safe - safe_dist
    critical - critical_dist
    as - angle_sign
    ts - thr_sign
)
(:init

    (robot_not_follow_person butler p1)

    (= (offset_angle ga) 8)

    (= (min_thr_angle minth) 7)

    (= (goal_angle_sign as) 0)

    (= (angle_threshold_sign ts) 0)

    (= (max_thr_angle maxth) 7)

    (= (object_dist gd) 5)

    (= (safe_thr_dist safe) 8)

    (= (critical_thr_dist critical) 4)

)
(:goal (and
    (robot_follow_person butler p1)
))
)

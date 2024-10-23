(define (problem task)
(:domain ohmni_rosplan_domain)
(:objects
    butler - robot
    p1 - person
    ga - goal_angle
    minth maxth - threshold_angle
)
(:init

    (robot_not_follow_person butler p1)

    (= (offset_angle ga) 7)

    (= (min_thr_angle minth) 7)

    (= (max_thr_angle maxth) 7)

)
(:goal (and
    (robot_follow_person butler p1)
))
)

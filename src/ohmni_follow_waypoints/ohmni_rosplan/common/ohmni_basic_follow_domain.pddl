(define (domain ohmni_rosplan_domain)
(:requirements :strips :typing :numeric-fluents :durative-actions :conditional-effects)
(:types
  robot person goal_angle threshold_angle - object
)

(:functions
  (offset_angle ?ga - goal_angle)
  (min_thr_angle ?mintha - threshold_angle)
  (max_thr_angle ?maxtha - threshold_angle)
)

(:predicates
  (robot_follow_person ?v - robot ?p - person)
  (robot_not_follow_person ?v - robot ?p - person)
)

;; Goal inside threshold range - move the robot within safe distance
(:action move
	:parameters (?v - robot ?p - person ?ga - goal_angle ?mintha - threshold_angle ?maxtha - threshold_angle) 
	:precondition (and
	(robot_not_follow_person ?v ?p)
	(< (offset_angle ?ga) (max_thr_angle ?maxtha))
	(< (offset_angle ?ga) (min_thr_angle ?mintha)))
	
	:effect (and 
		(not(robot_not_follow_person ?v ?p))
		(decrease (offset_angle ?ga) 1)
		(robot_follow_person ?v ?p))
)

;; Goal angle outside threshold angles - orient the robot
(:action orientation
:parameters (?v - robot ?p - person ?ga - goal_angle ?maxtha - threshold_angle ?mintha - threshold_angle)
:precondition (and 
	(robot_not_follow_person ?v ?p)
	(> (offset_angle ?ga) (min_thr_angle ?mintha))
	(> (offset_angle ?ga) (max_thr_angle ?maxtha)))

:effect (and 
    (not(robot_not_follow_person ?v ?p))
    (increase (offset_angle ?ga) 1)
    (robot_follow_person ?v ?p))
)

;last closing bracket
)
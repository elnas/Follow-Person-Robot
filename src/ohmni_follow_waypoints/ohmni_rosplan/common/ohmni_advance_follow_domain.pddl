(define (domain ohmni_follow_domain)
(:requirements :strips :typing :numeric-fluents :durative-actions :conditional-effects)
(:types
  robot person goal_angle threshold_angle goal_dist safe_dist critical_dist angle_sign thr_sign - object
)

(:functions
  (offset_angle ?ga - goal_angle)
  (min_thr_angle ?mintha - threshold_angle)
  (goal_angle_sign ?asig - angle_sign)
  (angle_threshold_sign ?thrsig - thr_sign)
  (max_thr_angle ?maxtha - threshold_angle)
  (object_dist ?gd - goal_dist)
  (safe_thr_dist ?sd - safe_dist)
  (critical_thr_dist ?cd - critical_dist)
)

(:predicates
  (robot_follow_person ?v - robot ?p - person)
  (robot_not_follow_person ?v - robot ?p - person)
)

;; Object distance > safe and critical distance - move robot forward
(:durative-action move_forward
	:parameters (?v - robot ?p - person ?ga - goal_angle ?mintha - threshold_angle ?maxtha - threshold_angle ?gd - goal_dist ?sd - safe_dist ?cd - critical_dist) 
	:duration ( = ?duration 10)
	:condition (and
	(at start(robot_not_follow_person ?v ?p))
	(at start(< (offset_angle ?ga) (max_thr_angle ?maxtha) ))
	(at start(< (offset_angle ?ga) (min_thr_angle ?mintha) ))
	(at start (> (object_dist ?gd) (safe_thr_dist ?sd)))
	(at start (> (object_dist ?gd) (critical_thr_dist ?cd))))
	
	:effect (and 
		(at start (not(robot_not_follow_person ?v ?p)))
		(at start (decrease (offset_angle ?ga) 2))
		(at start (increase (object_dist ?gd) 1))
		(at end(robot_follow_person ?v ?p)))
)

;; Object distance in between safe and critical distance - stop robot
(:durative-action stop
	:parameters (?v - robot ?p - person ?ga - goal_angle ?mintha - threshold_angle ?maxtha - threshold_angle ?gd - goal_dist ?sd - safe_dist ?cd - critical_dist) 
	:duration ( = ?duration 10)
	:condition (and
	(at start(robot_not_follow_person ?v ?p))
	(at start(< (offset_angle ?ga) (max_thr_angle ?maxtha) ))
	(at start(< (offset_angle ?ga) (min_thr_angle ?mintha) ))
	(at start(< (object_dist ?gd) (safe_thr_dist ?sd)))
	(at start(> (object_dist ?gd) (critical_thr_dist ?cd))))

	:effect (and 
		(at start (not(robot_not_follow_person ?v ?p)))
		(at start (decrease (offset_angle ?ga) 1))
		(at end (increase (object_dist ?gd) 1))
		(at end(robot_follow_person ?v ?p)))
)

;; Object distance < safe and critical distance - move robot backward
(:durative-action move_backward
	:parameters (?v - robot ?p - person ?ga - goal_angle ?mintha - threshold_angle ?maxtha - threshold_angle ?gd - goal_dist ?cd - critical_dist ?sd - safe_dist) 
	:duration ( = ?duration 10)
	:condition (and
	(at start(robot_not_follow_person ?v ?p))
	(at start(< (offset_angle ?ga) (max_thr_angle ?maxtha) ))
	(at start(< (offset_angle ?ga) (min_thr_angle ?mintha) ))
	(at start (< (object_dist ?gd) (critical_thr_dist ?cd)))
	(at start (< (object_dist ?gd) (safe_thr_dist ?sd))))
	
	:effect (and 
		(at start (not(robot_not_follow_person ?v ?p)))
		(at start (decrease (offset_angle ?ga) 2))
		(at start (increase (object_dist ?gd) 1))
		(at end(robot_follow_person ?v ?p)))
)

;; Goal angle positive - rotate robot clockwise
(:durative-action rotate_clockwise
	:parameters (?v - robot ?p - person ?ga - goal_angle ?asig - angle_sign ?maxtha - threshold_angle ?thrsig - thr_sign)
	:duration ( = ?duration 10)
	:condition (and 
	(at start(robot_not_follow_person ?v ?p))
	(at start(< (goal_angle_sign ?asig) 1))
	(at start(< (angle_threshold_sign ?thrsig) 1))
	(at end	(> (offset_angle ?ga) (max_thr_angle ?maxtha) )))
	
	:effect (and 
		(at start (not(robot_not_follow_person ?v ?p)))
		(at start (decrease (goal_angle_sign ?asig) 2))
		(at start (decrease (angle_threshold_sign ?thrsig) 2))
		(at start (increase (offset_angle ?ga) 1))
		(at end(robot_follow_person ?v ?p)))
)

;; Goal angle positive - rotate robot anticlockwise
(:durative-action rotate_anticlockwise
	:parameters (?v - robot ?p - person ?ga - goal_angle ?asig - angle_sign ?mintha - threshold_angle ?thrsig - thr_sign)
	:duration ( = ?duration 10)
	:condition (and
	(at start(robot_not_follow_person ?v ?p))
	(at start(> (goal_angle_sign ?asig) 0))
	(at start(> (angle_threshold_sign ?thrsig) 0))
	(at end (> (offset_angle ?ga) (min_thr_angle ?mintha) )))
	:effect (and 
		(at start (not(robot_not_follow_person ?v ?p)))
		(at start (decrease (goal_angle_sign ?asig) 2))
		(at start (decrease (angle_threshold_sign ?thrsig) 2))
		(at start (increase (offset_angle ?ga) 1))
		(at end(robot_follow_person ?v ?p)))
)

;last closing bracket
)
% MiniZinc model for the Examination Timetabling Problem proposed 
% by Michele Battistutta, Sara Ceschia, Fabio De Cesco, 
% Luca Di Gaspero, Andrea Schaerf, and Elena Topan in the paper 
% "Local search and constraint programming for a real-world examination 
% timetabling problem", submitted for publication.

% Model revised to deal with new dzn file format, February 8, 2021 LDG
 
int: Events;
int: Periods;
int: Rooms; % Note: The value Rooms might also include the dummy room (this happens when the RoomedEvents has at least a 0)

% Conflicts are events that cannot occur in the same period (e.g., they have the same teacher or they belong to the same curriculum)
% -1 indicates that the two events incur in a hard conflict (i.e., it is prohibited to have them scheduled at the same period)
% 0 indicates no conflict
% a value corresponding to PRIMARY_SECONDARY_CONFLICT_WEIGHT or SECONDARY_SECONDARY_CONFLICT_WEIGHT are included if there is a soft conflict
array [1..Events, 1..Events] of int: Conflicts;
% currently they represent the transitive closure of the distance constraints between two events
% that is the maximum of min distances according to the different type of constraints and the minumum of max distances
array [1..Events, 1..Events] of int: MinDistance; 
array [1..Events, 1..Events] of int: MaxDistance;
array [1..Events, 1..Events] of int: DistanceWeight;
array [1..Events, 1..Events] of 0..1: Precedence;
array [1..Rooms, 1..Rooms] of 0..1: RoomsetOverlap;
array [1..Events] of 0..1: RoomedEvent;  % redundant 
% additions for resource preferences: conventions
% -1 when forbidden
% 0 when allowed and desired
% INDIFFERENT_WEIGHT when there are preferred resources but the resource is not preferred
% UNDESIRED_WEIGHT when the resource is undesired
array [1..Events, 1..Periods] of int: EventPeriodConstraints; 
array [1..Events, 1..Rooms] of int: EventRoomConstraints;
% subsumed in event room constraints
array [1..Rooms, 1..Periods] of int: RoomPeriodConstraints;

array [1..Events] of var 1..Periods: EventPeriod;
array [1..Events] of var 1..Rooms: EventRoom;

var int: ConflictCost;
var int: RoomPreferenceCost;
var int: PeriodPreferenceCost;
var int: RoomPeriodCost;
var int: MinDirectionalDistanceCost;
var int: MaxDirectionalDistanceCost;
var int: MinUndirectionalDistanceCost;
var int: MaxUndirectionalDistanceCost;
var int: DistanceCost;

% NO ROOM OVERLAP
% notes: 
%     - dummy room does not overlap with itself (more events can fit in the dummy room)
%     - no constraint is added in the cases where the stronger one 
%       EventPeriod[e1] != EventPeriod[e2] applies
constraint
  forall(e1 in 1..Events - 1, e2 in e1 + 1..Events 
          where Conflicts[e1, e2] != -1 /\ Precedence[e1, e2] = 0 /\ RoomedEvent[e1] = 1 /\ RoomedEvent[e2] = 1)
    (EventPeriod[e1] != EventPeriod[e2] \/ RoomsetOverlap[EventRoom[e1], EventRoom[e2]] = 0);
      
% HARD CONFLICTS
constraint
  forall(e1 in 1..Events - 1, e2 in e1+1..Events where Conflicts[e1, e2] = -1)
    (EventPeriod[e1] != EventPeriod[e2]);
      
% PRECEDENCES
constraint
  forall(e1 in 1..Events - 1, e2 in e1 + 1..Events where Precedence[e1, e2] = 1)
    (EventPeriod[e1] < EventPeriod[e2]);
    
% ASSIGNED ROOM SHOULD BE AVAILABLE AT ASSIGNED PERIOD
constraint
  forall(e in 1..Events, p in 1..Periods) 
    (RoomPeriodConstraints[EventRoom[e], EventPeriod[e]] != -1);

% SOFT CONFLICT COSTS
constraint
  ConflictCost = sum(e1 in 1..Events - 1, e2 in e1 + 1..Events where Conflicts[e1, e2] > 0)
       (bool2int(EventPeriod[e1] = EventPeriod[e2]) *  Conflicts[e1, e2]);

% DISTANCE COSTS (min and max, directional and undirectional)
constraint
   MinDirectionalDistanceCost = sum(e1 in 1..Events, e2 in 1..Events 
           where Precedence[e1, e2] = 1 /\ DistanceWeight[e1, e2] > 0 /\ MinDistance[e1, e2] > 0)
     (DistanceWeight[e1, e2] * bool2int(EventPeriod[e2] - EventPeriod[e1] < MinDistance[e1, e2])
     * (MinDistance[e1, e2] - (EventPeriod[e2] - EventPeriod[e1])));

constraint
   MaxDirectionalDistanceCost = sum(e1 in 1..Events, e2 in 1..Events 
            where Precedence[e1, e2] = 1 /\ DistanceWeight[e1, e2] > 0 /\ MaxDistance[e1, e2] < Periods)
     (DistanceWeight[e1, e2] * bool2int(EventPeriod[e2] - EventPeriod[e1] > MaxDistance[e1, e2])
     * (EventPeriod[e2] - EventPeriod[e1] - MaxDistance[e1, e2]));

constraint
   MinUndirectionalDistanceCost = sum(e1 in 1..Events - 1, e2 in e1 + 1..Events 
            where Precedence[e1, e2] = 0 /\ DistanceWeight[e1, e2] > 0 /\ MinDistance[e1, e2] > 0)
      (DistanceWeight[e1, e2] * bool2int(abs(EventPeriod[e2] - EventPeriod[e1]) < MinDistance[e1, e2])
       * (MinDistance[e1, e2] - abs(EventPeriod[e2] - EventPeriod[e1])));

constraint
   MaxUndirectionalDistanceCost = sum(e1 in 1..Events - 1, e2 in e1 + 1..Events 
           where Precedence[e1, e2] = 0 /\ DistanceWeight[e1, e2] > 0 /\ MaxDistance[e1, e2] < Periods)
      (DistanceWeight[e1, e2] * bool2int(abs(EventPeriod[e2] - EventPeriod[e1]) > MaxDistance[e1, e2])
       * (abs(EventPeriod[e2] - EventPeriod[e1]) - MaxDistance[e1, e2]));
       
% FORBIDDEN PERIOD CONSTRAINTS
constraint
  forall(e in 1..Events, p in 1..Periods where EventPeriodConstraints[e, p] = -1) 
    (EventPeriod[e] != p);

% FORBIDDEN ROOMS CONSTRAINTS
constraint
  forall(e in 1..Events, r in 1..Rooms where EventRoomConstraints[e, r] = -1) 
    (EventRoom[e] != r);

% ROOM PREFERENCE COST
constraint
   RoomPreferenceCost = sum(e in 1..Events)(EventRoomConstraints[e, EventRoom[e]]);

% PERIOD PREFERENCE COST
constraint
   PeriodPreferenceCost = sum(e in 1..Events)(EventPeriodConstraints[e, EventPeriod[e]]);
   
  
 % PERIOD DEPENDENT UNDESIRED ROOMS
constraint 
  RoomPeriodCost = sum(e in 1..Events)(RoomPeriodConstraints[EventRoom[e], EventPeriod[e]]);

solve minimize ConflictCost + RoomPreferenceCost + PeriodPreferenceCost + RoomPeriodCost + MinDirectionalDistanceCost + MaxDirectionalDistanceCost + MinUndirectionalDistanceCost + MaxUndirectionalDistanceCost;

%solve::int_search(EventPeriod ++ EventRoom, first_fail, indomain_random, complete) minimize ConflictCost + RoomPreferenceCost + PeriodPreferenceCost + MinDirectionalDistanceCost + MaxDirectionalDistanceCost + MinUndirectionalDistanceCost + MaxUndirectionalDistanceCost;

% output ["Periods = "] ++ [show(EventPeriod[e] - 1) ++ " " | e in 1..Events] 
%     ++ ["\nRooms = "] ++ [show(EventRoom[e] - 1) ++ " " | e in 1..Events]
%     ++ ["\nConflictCost = \(ConflictCost)\n" ++ 
%         "RoomPreferenceCost = \(RoomPreferenceCost)\n" ++ 
%         "PeriodPreferenceCost = \(PeriodPreferenceCost)\n" ++ 
%         "MinDirectionalDistanceCost = \(MinDirectionalDistanceCost)\n" ++
%         "MaxDirectionalDistanceCost = \(MaxDirectionalDistanceCost)\n" ++
%         "MinUndirectionalDistanceCost = \(MinUndirectionalDistanceCost)\n" ++
%         "MaxUndirectionalDistanceCost = \(MaxUndirectionalDistanceCost)\n"];

output ["Periods = \(EventPeriod);\n" ++ 
        "Rooms = \(EventRoom);\n" ++
        "- ConflictCost = \(ConflictCost);\n" ++ 
        "- RoomPreferenceCost = \(RoomPreferenceCost);\n" ++ 
        "- PeriodPreferenceCost = \(PeriodPreferenceCost);\n" ++ 
        "- RoomPeriodCost = \(RoomPeriodCost);\n" ++
        "- DistanceCost = \(MinDirectionalDistanceCost + MaxDirectionalDistanceCost 
                        + MinUndirectionalDistanceCost + MaxUndirectionalDistanceCost);\n" ++
        "  + MinDirectionalDistanceCost = \(MinDirectionalDistanceCost);\n" ++
        "  + MaxDirectionalDistanceCost = \(MaxDirectionalDistanceCost);\n" ++
        "  + MinUndirectionalDistanceCost = \(MinUndirectionalDistanceCost);\n" ++
        "  + MaxUndirectionalDistanceCost = \(MaxUndirectionalDistanceCost);\n"
        ]
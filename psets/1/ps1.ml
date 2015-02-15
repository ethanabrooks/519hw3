(*** CS 51 Problem Set 1 ***)
(*** February 6, 2015 ***)
(*** Ethan Brooks ***)

(* Open up the library we'll be using in this course *)
open Core.Std 

(* Problem 1 - Fill in types:
 * Replace each ??? with the appropriate type of the corresponding expression.
 * Be sure to remove the comments from each subproblem and to type check it
 * before submission. *)

(*>* Problem 1a *>*)
let prob1a : string = let greet y = "Hello " ^ y in greet "World!";;

(*>* Problem 1b *>*)
let prob1b : (int option) list  = [Some 7; Some 1; None; Some 1];;

(*>* Problem 1c *>*)
let prob1c : ((float option * float option) * bool) = ((None, Some 42.0), true);;


(* Explain in a comment why the following will not type check,
   and provide a fix *)

(*>* Problem 1d *>*)
(*
let prob1d : string * int list = [("CS", 51); ("CS", 50)];;

This describes a 2-tuple containing a string and a list of ints, not a list containing 2-tuples of strings and ints. 
*)
let prob1d : (string * int) list = [("CS", 51); ("CS", 50)];;

(*>* Problem 1e *>*)
(*
let prob1e : int =
  let compare (x,y) = x < y in
  if compare (5, 4.9) then 5 else 2;;

OCaml cannot mix ints and floats in arithmetic operations. 
*)
let prob1e : int =
  let compare (x,y) = x < y in
  if compare (5.0, 4.9) then 5 else 2;;


(*>* Problem 1f *>*)
(*
let prob1f : (string * string) list =
  [("January", None); ("February", None); ("March", 15); ("April", None);
   ("May", None); ("June", 1); ("July", 4); ("August", None);
   ("September", 3); ("October", 1); ("November", 2); ("December", 11)] ;;
The seoncd entry of each entry contains either an int or None, neither of which are type string. 
*)
let prob1f : (string * int option) list =
  [("January", None); ("February", None); ("March", Some 15); ("April", None);
   ("May", None); ("June", Some 1); ("July", Some 4); ("August", None);
   ("September", Some 3); ("October", Some 1); ("November", Some 2); ("December", Some 11)] ;;


(* Problem 2 - Write the following functions *)
(* For each subproblem, you must implement a given function and corresponding
 * unit tests (i.e. assert expressions). You are provided a high level
* description as well as a prototype of the function you must implement. *)

(*>* Problem 2a *>*)

(* `reversed lst` should return true if the integers in lst are in
 * decreasing order. The empty list is considered to be reversed. Consecutive
 * elements can be equal in a reversed list. *)

(* Here is its prototype/signature: *)
(* reversed : int list -> bool *)

(* Implement reversed below, and be sure to write tests for it (see 2b for
 * examples of tests). *)
let rec reversed (x: int list) : bool =
    match x with
    | [] -> true
    | _::[] -> true
    | hd1::hd2::tl -> (hd1 >= hd2)&&reversed (hd2::tl)
;;
let () = assert (reversed [] = true);;
let () = assert (reversed [1] = true);;
let () = assert (reversed [0;-1;1] = false);;
let () = assert (reversed [3;3;2;1] = true);;


(*>* Problem 2b *>*)

(* merge takes two integer lists, each sorted in increasing order,
 and returns a single merged list in sorted order. For example:

merge [1;3;5] [2;4;6];;
- : int list = [1; 2; 3; 4; 5; 6]
merge [1;3;5] [2;4;6;12];;
- : int list = [1; 2; 3; 4; 5; 6; 12]
merge [0;3;5;711;747] [2;4;6;12];;
- : int list = [0; 2; 3; 4; 5; 6; 12; 711; 747]

*)

(* The type signature for merge is as follows: *)
(* merge : int list -> int list -> int list *)

(*tests if the input list is ordered as specified.*)
let rec ordered (x: int list) : bool =
    match x with
    | [] -> true
    | _::[] -> true
    | hd1::hd2::tl -> (hd1 <= hd2)&& ordered tl
;;
let rec merge (a:int list) (b:int list) : int list =
    if (ordered a, ordered b) = (true,true) then
        match (a, b) with
        | ([],[])-> []
        | ([],b) -> b
        | (a,[]) -> a
        | (ahd::atl,bhd::btl)  -> 
            if ahd <= bhd then ahd::(merge atl (bhd::btl))
            else bhd::(merge (ahd::atl) btl)
    else [0]
;;
let () = assert ((merge [] []) = []);;
let () = assert ((merge [1] []) = [1]);;
let () = assert ((merge [] [-7]) = [-7]);;
let () = assert ((merge [1] [-1]) = [-1;1]);;
let () = assert ((merge [4;5;6;7] [1;2;3]) = [1;2;3;4;5;6;7]);;
let () = assert ((merge [4;5;6;7] [1;2;3]) = [1;2;3;4;5;6;7]);;
let () = assert ((merge [2;2;4;4] [1;2;3]) = [1;2;2;2;3;4;4]);;
let () = assert ((merge [1;3] [1;3]) = [1;1;3;3]);;
let () = assert ((merge [-1;2;3;42] [-1;6;1001]) = [-1;-1;2;3;6;42;1001]);;



(*>* Problem 2c *>*)
(* unzip should be a function which, given a list of pairs, returns a
 * pair of lists, the first of which contains each first element of
 * each pair, and the second of which contains each second element.
 * The returned lists should have the elements in the order in which
 * they appeared in the input. So, for instance:

unzip [(1,2);(3,4);(5,6)];;
- : int list * int list = ([1;3;5],[2;4;6])

*)


(* The type signature for unzip is as follows: *)
(* unzip : (int * int) list -> int list * int list) *)

let rec unzip (x:(int * int) list) : (int list * int list) =
		match x with
		| [] -> ([],[])
		| (a,b)::tl ->
						let (aa,bb) = unzip tl in
						(a::aa,b::bb)	
;;
let () = assert ((unzip []) = ([],[]));;
let () = assert ((unzip [(1,2);(3,4);(5,6)] = ([1;3;5],[2;4;6])));;

(*>* Problem 2d *>*)

(* `variance lst` returns None if lst has fewer than 2 floats, and
 * Some of the variance of the floats in lst otherwise.  Recall that
 * the variance of a sequence of numbers is 1/(n-1) * sum (x_i-m)^2,
 * where a^2 means a squared, and m is the arithmetic mean of the list
 * (sum of list / length of list). For example:

variance [1.0; 2.0; 3.0; 4.0; 5.0];;
- : int option = Some 2.5
variance [1.0];;
- : int option = None

 * Remember to use the floating point version of the arithmetic
 * operators when operating on floats (+. *., etc). The "float"
 * function can cast an int to a float. *)

(* variance : float list -> float option *)

(*returns length of a list as a float*)
let rec fl_length (x:'a list) : float =
		match x with
		| [] -> 0.0
		| _::tl -> 1.0 +. fl_length tl
;;
(*sums elements of a float list*)
let rec sum (x:float list) : float =  
		match x with
		| [] -> 0.0
		| hd::tl -> hd +. sum tl
;;

(*returns mean of a float list*)
let mean (x:float list) : float =
		if x = [] then 0.0
		else (sum x /. fl_length x)
;;	
let sq (x:float) : float =
		x *. x
;;	

(*calculates sum (x_i-y)^2 for any figen float list and given y*)
let rec sum_diff_sq (x:float list) (y:float) : float option =
		match x with
		| [] -> Some 0.
		| hd::tl ->
						match sum_diff_sq tl y with
						| Some z -> Some(sq(hd -. y) +. z)
						| None -> None
;;	
let variance (x:float list) : float option =
		match (x,sum_diff_sq x (mean x)) with
		| (_::_::_, Some y) -> Some(1.0 /. (fl_length x -. 1.0) *. y)
		| _ -> None
;;
let () = assert ((variance [1.0; 2.0; 3.0; 4.0; 5.0]) = Some 2.5);;
let () = assert ((variance [1.0]) = None);;

(*>* Problem 2e *>*)

(* few_divisors n m should return true if n has fewer than m divisors,
 * (including 1 and n) and false otherwise. Note that this is *not* the
 * same as n having fewer divisors than m:

- : bool = true
few_divisors 23 3;;
few_divisors 12 6;;
- : bool = false
few_divisors 12 7;;
- : bool = true

 * Do not worry about negative integers at all. We will not test
 * your code using negative values for n and m, and do not
 * consider negative integers for divisors (e.g. don't worry about
 * -2 being a divisor of 4) *)

(* The type signature for few_divisors is: *)
(* few_divisors : int -> int -> bool *)

(*calulates all divisors of a given number that are greater than or equal to another given number*)
let rec divs_at_least (x:int) (y:int) : int =
		if x = y then 1 
    else if x mod y = 0 then 1 + divs_at_least x (y+1)
		else divs_at_least x (y+1)
;;
let few_divisors (m:int) (n:int) : bool = 
		if divs_at_least m 1 < n then true
		else false
;;
let () = assert ((few_divisors 23 3) = true);;
let () = assert ((few_divisors 3 3) = true);;
let () = assert ((few_divisors 3 2) = false);;
let () = assert ((few_divisors 4 4) = true);;
let () = assert ((few_divisors 4 3) = false);;
let () = assert ((few_divisors 6 5) = true);;
let () = assert ((few_divisors 6 4) = false);;
let () = assert ((few_divisors 12 7) = true);;
let () = assert ((few_divisors 12 6) = false);;

(*>* Problem 2f *>*)

(* `concat_list sep lst` returns one big string with all the string
 * elements of lst concatenated together, but separated by the string
 * sep. Here are some example tests:

concat_list ", " ["George"; "Beth"; "Ned"];;
- : string = "George, Beth, Ned"
concat_list "..." ["Moo"; "Baaa"; "Quack"];;
- : string = "Moo...Baaa...Quack"
concat_list ", " [];;
- : string = ""
concat_list ", " ["Moo"];;
- : string = "Moo"

*)

(* The type signature for concat_list is: *)
(* concat_list : string -> string list -> string *)

let rec concat_list (s:string) (ss:string list) : string = 
		match ss with
		| [] -> ""
    | hd::[] -> hd
		| hd::tl -> hd^s^concat_list s tl


let () = assert ((concat_list ", " ["George"; "Beth"; "Ned"]) = "George, Beth, Ned");;
let () = assert ((concat_list "..." ["Moo"; "Baaa"; "Quack"]) = "Moo...Baaa...Quack");;
let () = assert ((concat_list ", " []) = "");;
let () = assert ((concat_list ", " ["Moo"]) = "Moo");;
(*>* Problem 2g *>*)

(* One way to compress a list of characters is to use run-length encoding.
 * The basic idea is that whenever we have repeated characters in a list
 * such as ['a';'a';'a';'a';'b';'b';'b';'b';'c';'d';'d';'d';'d'] we can
 * (sometimes) represent the same information more compactly as a list
 * of pairs like [(4,'a');(4,'b');(1,'c');(4,'d')].  Here, the numbers
 * represent how many times the character is repeated.  For example,
 * the first character in the string is 'a' and it is repeated 4 times,
 * followed by 4 occurrences of the character 'b', followed by one 'c',
 * and finally 4 copies of 'd'.
 *
 * Write a function to_run_length that converts a list of characters into
 * the run-length encoding, and then write a function from_run_length
 * that converts back. Writing both functions will make it easier to
 * test that you've gotten them right. *)

(* The type signatures for to_run_length and from_run_length are: *)
(* to_run_length : char list -> (int * char) list *)
(* from_run_length : (int * char) list -> char list *)

(*>* Problem 3 *>*)

(*counts the number of repeated characters at the beginning of a given char list*)
let rec char_reps (x:char list) : int =
		match x with
		| [] -> 0
		| _::[] -> 1
		| hd1::hd2::tl ->
						if hd1 <> hd2 then 1
						else 1 + char_reps (hd2::tl)
;;

(*removes first character and all repetitions from the beginning of a given char list*)
let rec after_reps (x:char list) :  char list = 
		match x with
		| [] -> []
		| _::[] -> []
		| hd1::hd2::tl -> 
						if hd1 <> hd2 then hd2::tl
						else after_reps (hd2::tl)
;;
let rec to_run_length (x:char list) : (int*char) list = 
		match x with
		| [] -> []
		| hd::[] -> [(1,hd)]
		| hd::_ -> (char_reps x,hd)::to_run_length (after_reps x)
;;
let rec from_run_length (x:(int*char) list) : char list =
    match x with
    | [] -> []
    | hd::tl -> 
            match hd with
            | (0, _) -> from_run_length tl
            | (n, c) -> c::(from_run_length ((n-1,c)::tl))

let () = assert (to_run_length ['a';'a';'a';'a';'b';'b';'b';'b';'c';'d';'d';'d';'d'] =
    [(4,'a');(4,'b');(1,'c');(4,'d')])
let () = assert (from_run_length [(4,'a');(4,'b');(1,'c');(4,'d')] =
    ['a';'a';'a';'a';'b';'b';'b';'b';'c';'d';'d';'d';'d'])
(* Challenge!

 * permutations lst should return a list containing every
 * permutation of lst. For example, one correct answer to
 * permutations [1; 2; 3] is
 * [[1; 2; 3]; [2; 1; 3]; [2; 3; 1]; [1; 3; 2]; [3; 1; 2]; [3; 2; 1]].

 * It doesn't matter what order the permutations appear in the returned list.
 * Note that if the input list is of length n then the answer should be of
 * length n!.

 * Hint:
 * One way to do this is to write an auxiliary function,
 * interleave : int -> int list -> int list list,
 * that yields all interleavings of its first argument into its second:
 * interleave 1 [2;3] = [ [1;2;3]; [2;1;3]; [2;3;1] ].
 * You may also find occasion for the library functions
 * List.map and List.concat. *)

(* The type signature for permuations is: *)
(* permutations : int list -> int list list *)

(* inserts item at a given index in a list*)
let rec insert (a:'a) (aa:'a list) (index: int) : 'a list =
    if index = 0 then a::aa
    else match aa with
    | [] -> a::[]
    | hd::tl -> hd::(insert a tl (index-1))
let () = assert (insert 0 [1;2;3] 2 = [1;2;0;3])
let () = assert (insert 0 [1;2;3] 8 = [1;2;3;0])
    
(*remove item from a list if contained in it (otherwise list is left unchanged)*) 
let rec remove (a:'a) (aa:'a list) : 'a list =
    match aa with
    | [] -> []
    | hd::tl -> 
            if hd = a then tl
            else hd::(remove a tl)
let () = assert (remove 1 [0;1;2] = [0;2])
let () = assert (remove 1 [0;1;1;2] = [0;1;2])
let () = assert (remove 3 [0;1;2] = [0;1;2])

(* generates a list of integers between (including) two given integers *)
let rec (--) (a:int) (b:int) : int list =
    if a = b then a::[]
    else if a < b then a::((a+1)--b)
    else a::((a-1)--b)
;;
let () = assert (0--5 = [0;1;2;3;4;5])

let interleave (a:'a) (aa: 'a list) : ('a list) list =
    let rem_a = remove a aa in
    List.map (0--((List.length rem_a)):int list) (insert a rem_a: int -> int list)
;;
let () = assert (interleave 0 [1;2;3;4;5] =
    [[0; 1; 2; 3; 4; 5]; 
    [1; 0; 2; 3; 4; 5]; 
    [1; 2; 0; 3; 4; 5]; 
    [1; 2; 3; 0; 4; 5]; 
    [1; 2; 3; 4; 0; 5]; 
    [1; 2; 3; 4; 5; 0]]) 
;;
let rec permutations (x: 'a list) : ('a list) list= 
    match x with
    | [] -> []::[]
    | hd::tl -> List.concat (List.map (permutations tl:('a list) list) (interleave hd:'a list -> ('a list) list)) 
;;
let () = assert (permutations [1;2;3] = 
    [[1; 2; 3]; [2; 1; 3]; [2; 3; 1]; [1; 3; 2]; [3; 1; 2]; [3; 2; 1]])
import Std

namespace PromptVoteLab

inductive CandidateType where
  | baseline
  | prompt
  | other
  deriving DecidableEq, Repr

structure Candidate where
  rank : Nat
  ctype : CandidateType
  issue : Nat
  deriving DecidableEq, Repr

def baselineWon (candidates : List Candidate) : Bool :=
  candidates.any (fun c => c.type == CandidateType.baseline && c.rank == 1)

def eligibleOne (support : Nat) (c : Candidate) : Option Candidate :=
  match c.ctype, c.rank with
  | CandidateType.baseline, _ => none
  | CandidateType.prompt, 1 => some c
  | CandidateType.prompt, 2 => if support >= 5 then some c else none
  | CandidateType.prompt, 3 => if support >= 10 then some c else none
  | CandidateType.prompt, _ => none
  | CandidateType.other, _ => none

def selectEligible (candidates : List Candidate) (support : Nat) : List Candidate :=
  if baselineWon candidates then [] else candidates.filterMap (eligibleOne support)

theorem baseline_won_implies_no_eligible
    (candidates : List Candidate) (support : Nat) :
    baselineWon candidates = true -> selectEligible candidates support = [] := by
  intro h
  simp [selectEligible, h]

theorem baseline_not_eligible_one
    (support : Nat) (c : Candidate) :
    c.ctype = CandidateType.baseline -> eligibleOne support c = none := by
  cases c with
  | mk rank ctype issue =>
      intro h
      cases ctype <;> simp [eligibleOne] at h ⊢

theorem other_not_eligible_one
    (support : Nat) (c : Candidate) :
    c.ctype = CandidateType.other -> eligibleOne support c = none := by
  cases c with
  | mk rank ctype issue =>
      intro h
      cases ctype <;> simp [eligibleOne] at h ⊢

end PromptVoteLab

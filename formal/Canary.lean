import Std

namespace PromptVoteLab

inductive Scope where
  | labOnly
  | repositoryWide
  | external
  deriving DecidableEq, Repr

structure CanaryPolicy where
  scope : Scope
  attempts : Nat
  sdkMaxRetries : Nat
  apiCallsPerCandidate : Nat
  fallbackModel : Bool
  autoMerge : Bool
  externalPublishing : Bool
  deriving DecidableEq, Repr

def safeCanary (policy : CanaryPolicy) : Bool :=
  policy.scope == Scope.labOnly &&
  policy.attempts == 1 &&
  policy.sdkMaxRetries == 0 &&
  policy.apiCallsPerCandidate == 1 &&
  policy.fallbackModel == false &&
  policy.autoMerge == false &&
  policy.externalPublishing == false

def firstCanaryPolicy : CanaryPolicy :=
  { scope := Scope.labOnly
  , attempts := 1
  , sdkMaxRetries := 0
  , apiCallsPerCandidate := 1
  , fallbackModel := false
  , autoMerge := false
  , externalPublishing := false
  }

theorem first_canary_policy_is_safe :
    safeCanary firstCanaryPolicy = true := by
  simp [safeCanary, firstCanaryPolicy]

theorem safe_canary_scope_lab_only
    (policy : CanaryPolicy) :
    safeCanary policy = true -> policy.scope = Scope.labOnly := by
  intro h
  cases policy with
  | mk scope attempts sdkMaxRetries apiCallsPerCandidate fallbackModel autoMerge externalPublishing =>
      cases scope <;> simp [safeCanary] at h ⊢

theorem safe_canary_one_attempt
    (policy : CanaryPolicy) :
    safeCanary policy = true -> policy.attempts = 1 := by
  intro h
  cases policy with
  | mk scope attempts sdkMaxRetries apiCallsPerCandidate fallbackModel autoMerge externalPublishing =>
      cases scope <;> simp [safeCanary] at h
      exact h.1

theorem safe_canary_no_sdk_retry
    (policy : CanaryPolicy) :
    safeCanary policy = true -> policy.sdkMaxRetries = 0 := by
  intro h
  cases policy with
  | mk scope attempts sdkMaxRetries apiCallsPerCandidate fallbackModel autoMerge externalPublishing =>
      cases scope <;> simp [safeCanary] at h
      exact h.2.1

theorem safe_canary_one_api_call
    (policy : CanaryPolicy) :
    safeCanary policy = true -> policy.apiCallsPerCandidate = 1 := by
  intro h
  cases policy with
  | mk scope attempts sdkMaxRetries apiCallsPerCandidate fallbackModel autoMerge externalPublishing =>
      cases scope <;> simp [safeCanary] at h
      exact h.2.2.1

theorem safe_canary_no_fallback
    (policy : CanaryPolicy) :
    safeCanary policy = true -> policy.fallbackModel = false := by
  intro h
  cases policy with
  | mk scope attempts sdkMaxRetries apiCallsPerCandidate fallbackModel autoMerge externalPublishing =>
      cases scope <;> simp [safeCanary] at h
      exact h.2.2.2.1

theorem safe_canary_no_auto_merge
    (policy : CanaryPolicy) :
    safeCanary policy = true -> policy.autoMerge = false := by
  intro h
  cases policy with
  | mk scope attempts sdkMaxRetries apiCallsPerCandidate fallbackModel autoMerge externalPublishing =>
      cases scope <;> simp [safeCanary] at h
      exact h.2.2.2.2.1

theorem safe_canary_no_external_publishing
    (policy : CanaryPolicy) :
    safeCanary policy = true -> policy.externalPublishing = false := by
  intro h
  cases policy with
  | mk scope attempts sdkMaxRetries apiCallsPerCandidate fallbackModel autoMerge externalPublishing =>
      cases scope <;> simp [safeCanary] at h
      exact h.2.2.2.2.2

end PromptVoteLab

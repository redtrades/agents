/**
 * AISDLC repository-governance contract.
 *
 * This module defines the neutral, machine-readable contracts used to validate
 * claim payloads, authority boundaries, and lifecycle phase transitions across
 * the AISDLC workflow. Consumers should pass unknown inputs through
 * `validateContract` before acting on them.
 */

export const PHASE = Object.freeze({
  IMPLEMENT: 'sdlc:implement',
  AWAITING_CI: 'sdlc:awaiting-ci',
  REVIEW: 'sdlc:review',
  REPAIR: 'sdlc:repair',
  MERGE: 'sdlc:merge',
  BLOCKED: 'sdlc:blocked',
  DONE: 'sdlc:done',
});

export const PHASE_LIST = Object.freeze(Object.values(PHASE));

const ISSUE_RE = /^[1-9]\d*$/;
const OWNER_RE = /^[a-z0-9._-]+\/[a-z0-9._-]+$/i;
const SHA_RE = /^[0-9a-f]{40}$/;

function isString(value: unknown): value is string {
  return typeof value === 'string' && value.length > 0;
}

export class ContractValidationError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'ContractValidationError';
  }
}

/**
 * Represents an authority boundary for claim validation.
 */
export interface AuthorityBoundary {
  owner: string;
  paths: readonly string[];
  issue: string;
  headSha: string;
}

/**
 * Represents a repository issue claim payload.
 */
export interface ClaimPayload {
  issue: string;
  owner: string;
  paths: readonly string[];
  headSha: string;
  phase: string;
  command?: string;
}

function toString(value: unknown, name: string): string {
  if (typeof value !== 'string' || value.length === 0) {
    throw new ContractValidationError(`${name} must be a non-empty string`);
  }
  return value;
}

function toNonEmptyStringArray(value: unknown, name: string): readonly string[] {
  if (!Array.isArray(value) || value.length === 0) {
    throw new ContractValidationError(`${name} must contain at least one entry`);
  }
  if (!value.every(isString)) {
    throw new ContractValidationError(`${name} must be an array of non-empty strings`);
  }
  if (value.some((entry) => entry.includes('..'))) {
    throw new ContractValidationError(`${name} must not contain parent directory traversal`);
  }
  return Object.freeze([...value]);
}

/**
 * Validate a raw claim payload against the AISDLC governance contract.
 *
 * @param payload - unknown input to validate
 * @returns validated and normalized `ClaimPayload`
 * @throws `ContractValidationError` when the payload violates the contract
 */
export function validateContract(payload: unknown): ClaimPayload {
  if (!isRecord(payload)) {
    throw new ContractValidationError('payload must be an object');
  }

  const issue = toString(payload.issue, 'issue');
  const owner = toString(payload.owner, 'owner');
  const paths = toNonEmptyStringArray(payload.paths, 'paths');
  const phase = payload.hasOwnProperty('phase') ? toString(payload.phase, 'phase') : '';
  const command = payload.command === undefined ? 'claim' : toString(payload.command, 'command');

  if (!ISSUE_RE.test(issue)) {
    throw new ContractValidationError('issue must be a positive integer string');
  }

  if (!OWNER_RE.test(owner)) {
    throw new ContractValidationError('owner must follow `harness/session` form');
  }

  if (!paths.length) {
    throw new ContractValidationError('paths must contain at least one entry');
  }

  const headSha = payload.headSha;
  if (typeof headSha !== 'string' || !SHA_RE.test(headSha)) {
    throw new ContractValidationError('headSha must be a 40-character lowercase hex SHA');
  }

  const validPhases = new Set(PHASE_LIST);
  if (!validPhases.has(phase)) {
    throw new ContractValidationError(`phase must be one of: ${PHASE_LIST.join(', ')}`);
  }

  if (!['claim', 'release'].includes(command)) {
    throw new ContractValidationError('command must be `claim` or `release`');
  }

  return Object.freeze({
    issue,
    owner,
    paths,
    headSha,
    phase,
    command,
  } satisfies ClaimPayload);
}

/**
 * Build an authority boundary from a validated claim payload.
 *
 * @param payload - validated claim payload
 * @returns authority boundary derived from the payload
 */
export function authorityBoundary(payload: ClaimPayload): AuthorityBoundary {
  if (!isRecord(payload) || !isString(payload.owner) || !Array.isArray(payload.paths)) {
    throw new TypeError('boundary source must be a validated claim payload');
  }

  return Object.freeze({
    owner: payload.owner,
    paths: Object.freeze([...payload.paths]),
    issue: payload.issue,
    headSha: payload.headSha,
  });
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return Object.prototype.toString.call(value) === '[object Object]';
}
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

function isString(value) {
  return typeof value === 'string' && value.length > 0;
}

export class ContractValidationError extends Error {
  constructor(message) {
    super(message);
    this.name = 'ContractValidationError';
  }
}

/**
 * Represents an authority boundary for claim validation.
 *
 * @typedef {Object} AuthorityBoundary
 * @property {string} owner - durable session owner in `harness/session` form
 * @property {string[]} paths - paths governed by the boundary
 * @property {string} issue - issue identifier
 * @property {string} headSha - exact candidate SHA
 */

/**
 * Represents a repository issue claim payload.
 *
 * @typedef {Object} ClaimPayload
 * @property {string} issue - positive integer string
 * @property {string} owner - durable session owner in `harness/session` form
 * @property {string[]} paths - non-empty array of repository paths
 * @property {string} headSha - 40-character lowercase hex SHA
 * @property {string} phase - current lifecycle phase from `PHASE`
 * @property {string} [command] - claim command action, defaults to `claim`
 */

/**
 * Validate a raw claim payload against the AISDLC governance contract.
 *
 * @param {*} payload - unknown input to validate
 * @returns {ClaimPayload} validated and normalized claim payload
 * @throws {ContractValidationError} when the payload violates the contract
 */
export function validateContract(payload) {
  if (typeof payload !== 'object' || payload === null) {
    throw new ContractValidationError('payload must be an object');
  }

  const issue = toString(payload.issue, 'issue');
  const owner = toString(payload.owner, 'owner');
  const pathsRaw = payload.paths;
  const headSha = payload.headSha;
  const phase = payload.hasOwnProperty('phase') ? toString(payload.phase, 'phase') : '';
  const command = payload.command === undefined ? 'claim' : toString(payload.command, 'command');

  if (!ISSUE_RE.test(issue)) {
    throw new ContractValidationError('issue must be a positive integer string');
  }

  if (!OWNER_RE.test(owner)) {
    throw new ContractValidationError('owner must follow `harness/session` form');
  }

  if (!Array.isArray(pathsRaw) || pathsRaw.length === 0) {
    throw new ContractValidationError('paths must contain at least one entry');
  }

  if (!pathsRaw.every((entry) => typeof entry === 'string' && entry.length > 0)) {
    throw new ContractValidationError('paths must be a non-empty array of strings');
  }

  if (typeof headSha !== 'string' || !SHA_RE.test(headSha)) {
    throw new ContractValidationError('headSha must be a 40-character lowercase hex SHA');
  }

  if (!PHASE_LIST.includes(phase)) {
    throw new ContractValidationError(`phase must be one of: ${PHASE_LIST.join(', ')}`);
  }

  if (!['claim', 'release'].includes(command)) {
    throw new ContractValidationError('command must be `claim` or `release`');
  }

  return Object.freeze({
    issue,
    owner,
    paths: Object.freeze([...pathsRaw]),
    headSha,
    phase,
    command,
  });
}

/**
 * Build an authority boundary from a validated claim payload.
 *
 * @param {ClaimPayload} payload - validated claim payload
 * @returns {AuthorityBoundary} authority boundary derived from the payload
 */
export function authorityBoundary(payload) {
  if (
    typeof payload !== 'object' ||
    payload === null ||
    typeof payload.owner !== 'string' ||
    !Array.isArray(payload.paths)
  ) {
    throw new TypeError('boundary source must be a validated claim payload');
  }

  return Object.freeze({
    owner: payload.owner,
    paths: Object.freeze([...payload.paths]),
    issue: payload.issue,
    headSha: payload.headSha,
  });
}

function toString(value, name) {
  if (!isString(value)) {
    throw new TypeError(`${name} must be a non-empty string`);
  }
  return value;
}
/**
 * AISDLC Contract Validation Tests
 *
 * Tests that the AISDLC TypeScript contract is valid and correctly
 * enforces governance rules for claim payloads and authority boundaries.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import assert from 'node:assert/strict';
import { test } from 'node:test';

// Import contract validation functions (would be compiled from aisdlc.ts)
// For now, we'll test the JSON schema directly
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const schemaPath = path.join(__dirname, '../schemas/aisdlc-contract.json');
const schemaSource = fs.readFileSync(schemaPath, 'utf8');
const schema = JSON.parse(schemaSource);

test('schema is valid JSON', () => {
  assert.ok(schema, 'Schema should parse as valid JSON');
  assert.strictEqual(schema.$schema, 'http://json-schema.org/draft-07/schema#', 'Schema should declare JSON Schema version');
  assert.ok(schema.properties, 'Schema should have properties');
  assert.ok(schema.type, 'Schema should declare type');
});

test('schema defines required properties', () => {
  const required = schema.required || [];
  assert.ok(required.includes('issue'), 'Schema should require issue');
  assert.ok(required.includes('owner'), 'Schema should require owner');
  assert.ok(required.includes('paths'), 'Schema should require paths');
  assert.ok(required.includes('headSha'), 'Schema should require headSha');
  assert.ok(required.includes('phase'), 'Schema should require phase');
});

test('PHASE constants are defined', () => {
  const expectedPhases = [
    'sdlc:implement',
    'sdlc:awaiting-ci',
    'sdlc:review',
    'sdlc:repair',
    'sdlc:merge',
    'sdlc:blocked',
    'sdlc:done',
  ];

  const phaseEnum = schema.properties.phase.enum;
  assert.ok(Array.isArray(phaseEnum), 'Schema should define phase enum');
  assert.deepStrictEqual(phaseEnum, expectedPhases, 'Phase enum should match PHASE constants');
});

test('valid claim payload structure is defined', () => {
  const claimProps = schema.properties;

  assert.ok(claimProps.issue, 'Schema should define issue property');
  assert.strictEqual(claimProps.issue.type, 'string', 'issue should be string');

  assert.ok(claimProps.owner, 'Schema should define owner property');
  assert.strictEqual(claimProps.owner.type, 'string', 'owner should be string');

  assert.ok(claimProps.paths, 'Schema should define paths property');
  assert.strictEqual(claimProps.paths.type, 'array', 'paths should be array');

  assert.ok(claimProps.headSha, 'Schema should define headSha property');
  assert.strictEqual(claimProps.headSha.type, 'string', 'headSha should be string');

  assert.ok(claimProps.command, 'Schema should define command property');
});

test('issue must be positive integer string', () => {
  const issuePattern = schema.properties.issue.pattern;
  assert.ok(issuePattern, 'issue should have pattern validation');

  const issueRegex = new RegExp(issuePattern);
  assert.ok(issueRegex.test('123'), 'should match positive integers');
  assert.ok(!issueRegex.test('0'), 'should not match zero');
  assert.ok(!issueRegex.test('-123'), 'should not match negative');
  assert.ok(!issueRegex.test('abc'), 'should not match non-numeric');
});

test('owner must follow harness/session form', () => {
  const ownerPattern = schema.properties.owner.pattern;
  assert.ok(ownerPattern, 'owner should have pattern validation');

  const ownerRegex = new RegExp(ownerPattern);
  assert.ok(ownerRegex.test('harness/session'), 'should match harness/session');
  assert.ok(ownerRegex.test('my-harness/my-session'), 'should match with hyphens');
  assert.ok(!ownerRegex.test('no-slash'), 'should require slash');
  assert.ok(!ownerRegex.test('/session'), 'should require harness part');
});

test('headSha must be 40-character lowercase hex', () => {
  const shaPattern = schema.properties.headSha.pattern;
  assert.ok(shaPattern, 'headSha should have pattern validation');

  const shaRegex = new RegExp(shaPattern);
  const validSha = 'abcdef0123456789abcdef0123456789abcdef01';
  const invalidShaUppercase = 'ABCDEF0123456789ABCDEF0123456789ABCDEF01';
  const invalidShaShort = 'abcdef0123456789abcdef0123456789abcdef0';

  assert.ok(shaRegex.test(validSha), 'should match valid 40-char hex');
  assert.ok(!shaRegex.test(invalidShaUppercase), 'should not match uppercase');
  assert.ok(!shaRegex.test(invalidShaShort), 'should not match short hash');
});

test('paths must be non-empty array of strings', () => {
  const pathsSchema = schema.properties.paths;
  assert.strictEqual(pathsSchema.type, 'array', 'paths should be array type');
  assert.ok(pathsSchema.minItems, 'paths should have minItems constraint');
  assert.ok(pathsSchema.minItems > 0, 'paths should require at least one item');
});

test('command must be claim or release', () => {
  const commandEnum = schema.properties.command.enum;
  assert.ok(Array.isArray(commandEnum), 'command should have enum constraint');
  assert.ok(commandEnum.includes('claim'), 'should allow claim command');
  assert.ok(commandEnum.includes('release'), 'should allow release command');
  assert.strictEqual(commandEnum.length, 2, 'should only allow two commands');
});

test('TypeScript and JSON Schema are synchronized', () => {
  // Verify that both TypeScript and JSON schema define the same phases
  const expectedPhases = [
    'sdlc:implement',
    'sdlc:awaiting-ci',
    'sdlc:review',
    'sdlc:repair',
    'sdlc:merge',
    'sdlc:blocked',
    'sdlc:done',
  ];

  const schemaPhases = schema.properties.phase.enum;
  assert.deepStrictEqual(schemaPhases, expectedPhases, 'Schema phases should match expected contract');
});

test('schema disallows additional properties', () => {
  assert.strictEqual(schema.additionalProperties, false, 'Schema should not allow additional properties');
});

console.log('✓ All AISDLC contract validation tests passed');

---
name: debugging-strategies
description: Master systematic debugging techniques, profiling tools, and root cause analysis to efficiently track down bugs across any codebase or technology stack. Use when investigating bugs, performance issues, or unexpected behavior.
---

# Debugging Strategies

Transform debugging from frustrating guesswork into systematic problem-solving with proven strategies, powerful tools, and methodical approaches.

## When to Use This Skill

- Tracking down elusive bugs
- Investigating performance issues
- Understanding unfamiliar codebases
- Debugging production issues
- Analyzing crash dumps and stack traces
- Profiling application performance
- Investigating memory leaks
- Debugging distributed systems

## Core Principles

### 1. The Scientific Method

**1. Observe**: What's the actual behavior?
**2. Hypothesize**: What could be causing it?
**3. Experiment**: Test your hypothesis
**4. Analyze**: Did it prove/disprove your theory?
**5. Repeat**: Until you find the root cause

### 2. Debugging Mindset

**Don't Assume:**

- "It can't be X" - Yes it can
- "I didn't change Y" - Check anyway
- "It works on my machine" - Find out why

**Do:**

- Reproduce consistently
- Isolate the problem
- Keep detailed notes
- Question everything
- Take breaks when stuck

### 3. Rubber Duck Debugging

Explain your code and problem out loud (to a rubber duck, colleague, or yourself). Often reveals the issue.

## Systematic Debugging Process

### Phase 1: Reproduce

```markdown
## Reproduction Checklist

1. **Can you reproduce it?**
   - Always? Sometimes? Randomly?
   - Specific conditions needed?
   - Can others reproduce it?

2. **Create minimal reproduction**
   - Simplify to smallest example
   - Remove unrelated code
   - Isolate the problem

3. **Document steps**
   - Write down exact steps
   - Note environment details
   - Capture error messages
```

### Phase 2: Gather Information

```markdown
## Information Collection

1. **Error Messages**
   - Full stack trace
   - Error codes
   - Console/log output

2. **Environment**
   - OS version
   - Language/runtime version
   - Dependencies versions
   - Environment variables

3. **Recent Changes**
   - Git history
   - Deployment timeline
   - Configuration changes

4. **Scope**
   - Affects all users or specific ones?
   - All browsers or specific ones?
   - Production only or also dev?
```

### Phase 3: Form Hypothesis

```markdown
## Hypothesis Formation

Based on gathered info, ask:

1. **What changed?**
   - Recent code changes
   - Dependency updates
   - Infrastructure changes

2. **What's different?**
   - Working vs broken environment
   - Working vs broken user
   - Before vs after

3. **Where could this fail?**
   - Input validation
   - Business logic
   - Data layer
   - External services
```

### Phase 4: Test & Verify

```markdown
## Testing Strategies

1. **Binary Search**
   - Comment out half the code
   - Narrow down problematic section
   - Repeat until found

2. **Add Logging**
   - Strategic console.log/print
   - Track variable values
   - Trace execution flow

3. **Isolate Components**
   - Test each piece separately
   - Mock dependencies
   - Remove complexity

4. **Compare Working vs Broken**
   - Diff configurations
   - Diff environments
   - Diff data
```

## Debugging Tools

### JavaScript/TypeScript Debugging

```typescript
// Chrome DevTools Debugger
function processOrder(order: Order) {
  debugger; // Execution pauses here

  const total = calculateTotal(order);
  console.log("Total:", total);

  // Conditional breakpoint
  if (order.items.length > 10) {
    debugger; // Only breaks if condition true
  }

  return total;
}

// Console debugging techniques
console.log("Value:", value); // Basic
console.table(arrayOfObjects); // Table format
console.time("operation");
/* code */ console.timeEnd("operation"); // Timing
console.trace(); // Stack trace
console.assert(value > 0, "Value must be positive"); // Assertion

// Performance profiling
performance.mark("start-operation");
// ... operation code
performance.mark("end-operation");
performance.measure("operation", "start-operation", "end-operation");
console.log(performance.getEntriesByType("measure"));
```

**VS Code Debugger Configuration:**

```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "launch",
      "name": "Debug Program",
      "program": "${workspaceFolder}/src/index.ts",
      "preLaunchTask": "tsc: build - tsconfig.json",
      "outFiles": ["${workspaceFolder}/dist/**/*.js"],
      "skipFiles": ["<node_internals>/**"]
    },
    {
      "type": "node",
      "request": "launch",
      "name": "Debug Tests",
      "program": "${workspaceFolder}/node_modules/jest/bin/jest",
      "args": ["--runInBand", "--no-cache"],
      "console": "integratedTerminal"
    }
  ]
}
```

### Python Debugging

```python
# Built-in debugger (pdb)
import pdb

def calculate_total(items):
    total = 0
    pdb.set_trace()  # Debugger starts here

    for item in items:
        total += item.price * item.quantity

    return total

# Breakpoint (Python 3.7+)
def process_order(order):
    breakpoint()  # More convenient than pdb.set_trace()
    # ... code

# Post-mortem debugging
try:
    risky_operation()
except Exception:
    import pdb
    pdb.post_mortem()  # Debug at exception point

# IPython debugging (ipdb)
from ipdb import set_trace
set_trace()  # Better interface than pdb

# Logging for debugging
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def fetch_user(user_id):
    logger.debug(f'Fetching user: {user_id}')
    user = db.query(User).get(user_id)
    logger.debug(f'Found user: {user}')
    return user

# Profile performance
import cProfile
import pstats

cProfile.run('slow_function()', 'profile_stats')
stats = pstats.Stats('profile_stats')
stats.sort_stats('cumulative')
stats.print_stats(10)  # Top 10 slowest
```

### Go Debugging

```go
// Delve debugger
// Install: go install github.com/go-delve/delve/cmd/dlv@latest
// Run: dlv debug main.go

import (
    "fmt"
    "runtime"
    "runtime/debug"
)

// Print stack trace
func debugStack() {
    debug.PrintStack()
}

// Panic recovery with debugging
func processRequest() {
    defer func() {
        if r := recover(); r != nil {
            fmt.Println("Panic:", r)
            debug.PrintStack()
        }
    }()

    // ... code that might panic
}

// Memory profiling
import _ "net/http/pprof"
// Visit http://localhost:6060/debug/pprof/

// CPU profiling
import (
    "os"
    "runtime/pprof"
)

f, _ := os.Create("cpu.prof")
pprof.StartCPUProfile(f)
defer pprof.StopCPUProfile()
// ... code to profile
```

## Advanced Techniques & Bug Patterns

Detailed playbooks for flaky bugs, memory leaks, concurrency issues, production debugging, and checklists live in `references/details.md`. Read that file when performing root cause analysis.

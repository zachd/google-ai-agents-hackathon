# Agent Evaluation Framework

⚠️ **IMPORTANT**: The Google ADK evaluation feature is currently **experimental**. The evaluation files in this directory are formatted as human-readable test case documentation rather than ADK's required ConversationScenarios format.

This directory contains evaluation scenarios documenting expected behaviors for testing the multi-agent adventure trip planning system.

### What This Framework Provides

Even though the ADK eval format requires conversion, these evaluation scenarios provide significant value:

1. **Comprehensive Test Documentation** - 26 detailed test scenarios covering all agent behaviors
2. **Behavior Specifications** - Clear expected behaviors for each interaction
3. **Quality Assurance Checklist** - Manual testing guide for all features
4. **Development Guide** - Reference for what each agent should do
5. **Future-Ready** - Easy to convert to ADK format when it stabilizes

## Overview

The evaluation framework uses Google ADK's built-in evaluation tools to test:
- Individual agent behaviors
- Multi-agent orchestration
- Tool usage and integration
- End-to-end user journeys

## Evaluation Files

### 1. `game_master_scenarios.json`
Tests for the Game Master Agent (orchestrator):
- `greeting_and_intro` - Initial user greeting and adventure explanation
- `orchestration_workflow` - Multi-agent workflow coordination
- `location_completion_handling` - Handling completed locations
- `adventure_guidance` - Providing hints and guidance
- `error_recovery` - Graceful error handling

### 2. `user_persona_scenarios.json`
Tests for the User Persona Agent (interviewer):
- `initial_greeting` - First interaction with user
- `vibe_preferences_gathering` - Collecting vibe preferences
- `location_and_duration_gathering` - Collecting location and time details
- `time_awareness_gathering` - Understanding time context
- `conversation_pacing` - Maintaining good conversation flow
- `completion_handoff` - Proper handoff back to game master
- `incomplete_information_handling` - Handling vague responses

### 3. `planning_scenarios.json`
Tests for the Planning Agent (location finder):
- `basic_location_search` - Finding locations based on preferences
- `mysterious_hint_generation` - Creating poetic, mysterious hints
- `time_awareness` - Considering time of day
- `preference_matching` - Matching multiple criteria
- `gps_coordinates_inclusion` - Providing navigation details
- `local_vs_tourist_differentiation` - Finding local vs tourist spots
- `radius_constraint_handling` - Respecting distance limits
- `no_results_handling` - Graceful handling of impossible requests

### 4. `integrated_scenarios.json`
End-to-end system tests:
- `complete_adventure_flow` - Full user journey
- `multi_location_adventure` - Multiple locations in sequence
- `preference_refinement` - Adjusting based on feedback
- `help_during_search` - Assisting stuck users
- `time_based_suggestions` - Time-aware recommendations
- `error_recovery_integration` - System-wide error recovery

## How to Use These Test Scenarios

### Manual Testing (Recommended)

The test scenarios serve as a comprehensive manual testing checklist:

1. **Start the ADK web server**:
   ```bash
   make run
   # or
   ./venv/bin/adk web --port 8081 .
   ```

2. **Open a test scenario file** (e.g., `game_master_scenarios.json`)

3. **For each scenario**:
   - Read the `description` to understand what to test
   - Follow the `conversation` to simulate user inputs
   - Verify the `expected_behaviors` are present in agent responses

4. **Document results**:
   - ✅ Pass: All expected behaviors present
   - ⚠️ Partial: Some behaviors missing
   - ❌ Fail: Most/all behaviors missing

### Example Test Execution

**Scenario**: `greeting_and_intro` from `game_master_scenarios.json`

```json
{
  "name": "greeting_and_intro",
  "description": "Test that game master greets user and explains the adventure",
  "conversation": [
    {"role": "user", "content": "Hello!"}
  ],
  "expected_behaviors": [
    "Greets user warmly",
    "Explains the choose-your-own-adventure concept",
    "Mentions mystery locations",
    "Indicates next steps (interviewing for preferences)"
  ]
}
```

**Testing**:
1. Open web interface at `http://localhost:8081`
2. Send message: "Hello!"
3. Verify response includes:
   - ✅ Warm greeting
   - ✅ Explanation of adventure game
   - ✅ Mentions mystery locations
   - ✅ Mentions next steps

### Automated Testing (Future)

ADK's evaluation feature is experimental. When it stabilizes, these scenarios can be converted to run automated tests.

## Understanding Results

Evaluation results will show:
- ✅ **Pass**: Agent behavior matches expected behaviors
- ❌ **Fail**: Agent behavior doesn't match expectations
- ⚠️ **Partial**: Some expected behaviors present, others missing

### Expected Behaviors

Each scenario includes `expected_behaviors` - a list of behaviors that should be present in the agent's response. These are not exact string matches but behavioral indicators:

```json
"expected_behaviors": [
  "Greets user warmly",
  "Explains the choose-your-own-adventure concept",
  "Mentions mystery locations"
]
```

The evaluator checks if these behaviors are present in the conversation.

## Creating New Test Scenarios

### Scenario Structure

```json
{
  "scenarios": [
    {
      "name": "unique_test_name",
      "description": "What this test validates",
      "conversation": [
        {
          "role": "user",
          "content": "User message"
        },
        {
          "role": "assistant",
          "content": "Expected assistant response (optional)"
        }
      ],
      "expected_behaviors": [
        "Behavior 1 to check",
        "Behavior 2 to check"
      ]
    }
  ]
}
```

### Best Practices

1. **Test One Thing**: Each scenario should test a specific behavior or feature
2. **Clear Expectations**: Make expected_behaviors specific and measurable
3. **Realistic Conversations**: Use realistic user inputs
4. **Edge Cases**: Include tests for error cases and edge scenarios
5. **Progressive Complexity**: Start simple, build to complex scenarios

## Evaluation Storage

### Local Storage (Default)
Results are stored locally in your project directory.

### Cloud Storage (Optional)
You can store evaluation results in Google Cloud Storage:

```bash
# Run eval with cloud storage
./venv/bin/adk eval game_master evals/game_master_scenarios.json \
  --eval_storage_uri gs://your-bucket-name
```

## Test Coverage Summary

| Agent | Scenarios | Coverage |
|-------|-----------|----------|
| Game Master | 5 | Greetings, orchestration, guidance, completion, errors |
| User Persona | 7 | Interview, preferences, pacing, handoff, edge cases |
| Planning | 8 | Search, hints, time, matching, GPS, local/tourist, radius |
| Integrated | 6 | End-to-end flows, multi-location, refinement, help |
| **Total** | **26** | **Comprehensive agent behavior coverage** |

## Quality Assurance Checklist

Use this workflow for thorough testing:

- [ ] Run all Game Master scenarios
- [ ] Run all User Persona scenarios
- [ ] Run all Planning scenarios
- [ ] Run all Integrated scenarios
- [ ] Document any failures or issues
- [ ] Add new scenarios for new features
- [ ] Retest after bug fixes

## Tips for Effective Testing

### Agent Behavior Validation

When testing, look for these quality indicators:

**Good Agent Response:**
- Addresses user input directly
- Maintains appropriate tone (friendly, helpful)
- Follows expected workflow (handoffs, tool usage)
- Provides clear next steps
- Handles errors gracefully

**Issues to Flag:**
- Ignores user input
- Skips expected workflow steps
- Provides vague or unhelpful responses
- No error handling
- Breaks character/role

### Testing Edge Cases

Don't just test the "happy path":
- Invalid inputs
- Unexpected user responses
- Tool failures
- API timeouts
- Empty results
- Contradictory preferences

## Contributing

When adding new features:
1. Add corresponding test scenarios
2. Update this README with new test descriptions
3. Run full eval suite before committing
4. Document any new expected behaviors

## Resources

- [Google ADK Documentation](https://github.com/google/adk-python)
- [ADK Evaluation Guide](https://github.com/google/adk-python/docs/eval.md)
- Project README: `../README.md`

### Project Plan: Agent-Based Trip Planner

This plan focuses on the incremental development of the three core agents: **[Game Master]**, **[UserPersona Agent]**, and **[Planning Agent]**. We will use a debugger-centric approach to build and test the logic at each step.

---

#### **Phase 1: Agent Definition & Core Logic**

**Objective:** Establish the foundational logic for the `UserPersona` and `Planning` agents.

*   **1. Define Agent Personas & Data Structures:**
    *   **[Game Master]:** The central orchestrator. Its main role is to manage the trip state and facilitate communication between the user and the other agents.
    *   **[UserPersona Agent]:** The profiler. It will conduct the initial interview.
    *   **[Planning Agent]:** The location scout. It will find destinations.
    *   **Data Structures:** Define the JSON schemas for the `UserPersona` (e.g., `{ "interests": ["history", "food"], "vibe": "local_secrets", "radius": 5 }`) and the `TripPlan` (e.g., `{ "location": { "lat": 40.7, "lng": -74.0 }, "clue": "...", "reasoning": "..." }`).

*   **2. Implement `UserPersona Agent`:**
    *   Develop the conversation flow for the interview (e.g., "local secrets or iconic landmarks?", "what's your budget?").
    *   **Test:** In the ADK debugger, simulate a user conversation and verify that the agent correctly outputs a `UserPersona` JSON object.

*   **3. Implement `Planning Agent` (v1):**
    *   Create the initial version to take a `UserPersona` object as input.
    *   It will make a single call to the Google Maps Places API to find a suitable location.
    *   It will return a `TripPlan` object containing the GPS location and a hard-coded clue.
    *   **Test:** In the ADK debugger, provide a sample `UserPersona` and check if the agent returns a valid and relevant `TripPlan`.

---

#### **Phase 2: The Core Game Loop**

**Objective:** Implement the main user journey, from getting a clue to arriving at the destination.

*   **1. Implement `Game Master` Orchestration:**
    *   Develop the logic for the `Game Master` to manage the sequence:
        1.  Call `UserPersona Agent`.
        2.  Take the resulting `UserPersona` and call `Planning Agent`.
        3.  Present the `clue` from the `TripPlan` to the user.

*   **2. Implement Navigation Handoff:**
    *   The `Game Master` will ask the user "Ready to get started?".
    *   If the user says "Yes", it will construct and display a Google Maps URL with the destination coordinates.

*   **3. Implement Arrival & Reveal:**
    *   The `Game Master` will have a mechanism to detect arrival (for testing, this can be a simple "I've arrived!" button in the debugger).
    *   Upon arrival, it will reveal the name of the location.
    *   **Test:** Run the entire sequence in the ADK debugger, from the initial interview to arriving at the first location. Verify the state is managed correctly and the correct Google Maps URL is generated.

---

#### **Phase 3: Feedback, Adaptation, and Dynamic Planning**

**Objective:** Make the experience truly "choose-your-own-adventure" by incorporating feedback and real-time data.

*   **1. Implement Feedback Loop:**
    *   After revealing a location, the `Game Master` will ask for feedback ("How was it?").
    *   The user's feedback will be used to update the `UserPersona` state. For example, disliking a museum will lower the "art" preference.

*   **2. Enhance `Planning Agent` (v2):**
    *   The `Planning Agent` will now receive the updated `UserPersona` and a history of visited places.
    *   It will use this information to select the *next* location, avoiding repeats and disliked categories.
    *   It will also start generating dynamic clues using the Gemini API, based on the location's details.

*   **3. Integrate Real-time Constraints:**
    *   **Weather:** The `Game Master` will check a weather API before calling the `Planning Agent`. If it's raining, it will add an `is_indoor: true` constraint to the request.
    *   **Time of Day:** The `Game Master` will pass the current time to the `Planning Agent`, which can use it to prefer restaurants around meal times.
    *   **Test:** In the debugger, simulate giving negative feedback and verify the next suggestion is different. Simulate rain and verify an indoor location is suggested.

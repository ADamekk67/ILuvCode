# Reinforcement Learning Q-Learning Turtle Agent

## Overview
This project implements a **Q-Learning** agent using a turtle character in a grid-based environment. The turtle learns which positions are safe and which are unsafe through exploration and reinforcement learning.

---

## What is Reinforcement Learning (RL)?

Reinforcement Learning is a machine learning paradigm where an **agent** learns to make decisions by interacting with an environment and receiving **rewards** or **penalties** for its actions.

### Key Concepts:

- **Agent**: The learner (in this case, the turtle)
- **Environment**: The grid-based world the agent explores
- **State (s)**: The current position of the agent
- **Action (a)**: Movement choices (UP, DOWN, LEFT, RIGHT)
- **Reward (r)**: Feedback from the environment (-10 for unsafe, +1 for safe, 0 for neutral)
- **Policy**: The strategy the agent uses to select actions

### How RL Works:

1. Agent observes state **s**
2. Agent takes action **a** based on its policy
3. Environment gives reward **r** and new state **s'**
4. Agent learns and updates its policy
5. Process repeats → **Agent improves over time**

---

## What is Q-Learning?

Q-Learning is a popular **model-free** reinforcement learning algorithm that learns the value of actions in different states without needing a model of the environment.

### Key Idea:

Instead of learning the probability of success, Q-Learning learns a **Q-Value** for each state-action pair: **Q(s, a)**

- **Q(s, a)** = Expected future reward for taking action **a** in state **s**
- Higher Q-values = Better actions
- Agent picks actions with highest Q-values (exploitation) or random actions (exploration)

### Q-Learning Update Equation:

$$Q(s,a) \leftarrow Q(s,a) + \alpha[r + \gamma \max_{a'} Q(s',a') - Q(s,a)]$$

**Where:**
- **α (Alpha)** = Learning rate (0.1) - How much to update based on new information
- **r** = Immediate reward received
- **γ (Gamma)** = Discount factor (0.9) - How much future rewards matter
- **s'** = Next state after taking action
- **a'** = Possible actions in next state

### Breaking Down the Equation:

1. **Current Q-value**: `Q(s,a)` - What we already know
2. **Temporal Difference**: `r + γ max Q(s',a') - Q(s,a)` - The difference between what we expected and what actually happened
3. **Learning**: Multiply by **α** and add to get updated Q-value

---

## Project Implementation

### Code Structure:

```python
# Q-Learning Setup
Q_TABLE = {}                    # Stores learned Q-values
ALPHA = 0.1                     # Learning rate
GAMMA = 0.9                     # Discount factor
EPSILON = 0.1                   # Exploration rate
ACTIONS = ['UP', 'DOWN', 'LEFT', 'RIGHT']
ACTION_STEPS = 50               # Movement amount per step
```

### Key Functions:

#### `get_state(x, y)`
Converts continuous coordinates into discrete grid states for Q-Learning

#### `get_reward(state)`
Returns rewards based on position:
- `-10` if position is unsafe (learned from past experiences)
- `+1` if position is safe (good to revisit)
- `0` if neutral/unknown

#### `epsilon_greedy(state)`
Balances exploration vs exploitation:
- With probability **ε (10%)**: Choose random action (explore)
- Otherwise: Choose action with highest Q-value (exploit)

#### `get_next_position(x, y, action)`
Calculates where the turtle moves after each action

### Q-Learning Update Loop:

```python
# Get current state
current_state = get_state(TurtlePosX, TurtlePosY)

# Choose action using epsilon-greedy
action = epsilon_greedy(current_state)

# Get next position and state
next_x, next_y = get_next_position(TurtlePosX, TurtlePosY, action)
next_state = get_state(next_x, next_y)

# Get reward for this position
Reward = get_reward(next_state)

# Q-Learning update: Learn from experience
current_q = Q_TABLE.get((current_state, action), 0)
max_next_q = max([Q_TABLE.get((next_state, a), 0) for a in ACTIONS])
Q_TABLE[(current_state, action)] = current_q + ALPHA * (Reward + GAMMA * max_next_q - current_q)

# Track visited positions
CollectedData["Safe Positions"].add((TurtlePosX, TurtlePosY))
```

---

## Hyperparameters Explained

| Parameter | Value | Role |
|-----------|-------|------|
| **α (Alpha)** | 0.1 | Learning rate - Lower = slower learning but more stable |
| **γ (Gamma)** | 0.9 | Discount factor - Higher = values future rewards more |
| **ε (Epsilon)** | 0.1 | Exploration rate - Lower = less random exploration |
| **ACTION_STEPS** | 50 | Grid movement size in pixels |

---

## How the Turtle Learns

1. **Initial Phase**: Turtle explores randomly, discovering safe/unsafe positions
2. **Q-Values Build**: Each state-action pair gets a learned value
3. **Convergence**: Over time, Q-values stabilize
4. **Optimal Policy**: Turtle starts preferring actions leading to safe areas
5. **Persistence**: Safe/unsafe positions save to `DataSave.json` between runs

---

## Running the Project

```bash
python Code.py
```

Watch the turtle:
- ✅ Learn which positions are safe
- ✅ Avoid unsafe positions over time
- ✅ Update Q-values based on exploration
- ✅ Display position, state, and steps taken

Close the window to save learned data to `DataSave.json`

---

## Key Takeaways

- **Q-Learning** lets agents learn optimal behavior through trial and error
- **Epsilon-greedy** balances exploration (trying new things) with exploitation (using knowledge)
- **Rewards shape behavior** - The agent learns to seek +1 rewards and avoid -10 penalties
- **Q-values improve** - As the agent explores, its estimate of action quality improves
- **Persistence** - Knowledge transfers between sessions via saved Q-table

---

## Future Improvements

- Add obstacles or moving enemies
- Implement decay of exploration rate (EPSILON)
- Add visual heatmap of learned Q-values
- Train on multiple episodes and plot learning curves
- Implement DQN (Deep Q-Network) for larger state spaces

import random
from models import Observation, Action, StepResult
from tasks import get_task
from helpers import is_protective_action, is_safe_action


class ScamDefenseEnv:

    def __init__(self, task="easy"):
        self.task = task
        self.history = []
        self.done = False
        self.correct_actions = 0
        self.total_steps = 0
        self.max_steps = 3

    @classmethod
    async def from_docker_image(cls, image_name=None):
        return cls()

    async def reset(self):
        self.done = False
        self.history = []
        self.correct_actions = 0
        self.total_steps = 0

        task_data = get_task(self.task)

        self.message = task_data["message"]
        self.is_scam = task_data["is_scam"]
        self.verification_info = task_data.get("verification_info", "No further info available.")

        self.urgency = random.randint(5, 10)
        self.user_awareness = random.randint(1, 10)

        return StepResult(
            observation=self._get_observation(),
            reward=0.0,
            done=False
        )

    async def step(self, action: Action):

        if self.done:
            return await self.reset()

        act = action.action.lower()
        reward = 0.0

        # Reward logic
        if act == "verify":
            reward = 0.2
            self.message = f"[Verification Result]: {self.verification_info}"
            self.done = False
        else:
            if self.is_scam:
                if is_protective_action(act):
                    reward = 1.0
                    self.correct_actions += 1
                elif act == "ignore":
                    reward = -1.0
                else:
                    reward = -0.5
            else:
                if is_protective_action(act):
                    reward = -1.0
                else:
                    reward = 1.0
                    self.correct_actions += 1
            # Terminal states
            self.done = True

        self.total_steps += 1
        
        # Enforce max steps to guarantee termination
        if self.total_steps >= self.max_steps:
            self.done = True

        self.history.append(f"Message: {self.message}")
        self.history.append(f"Action: {act}")

        return StepResult(
            observation=self._get_observation(),
            reward=float(reward),
            done=self.done
        )

    async def state(self):
        return self._get_observation()

    def _get_observation(self):
        return Observation(
            message=self.message,
            history=self.history,
            urgency=self.urgency,
            user_awareness=self.user_awareness,
            step=self.total_steps
        )

    async def close(self):
        pass
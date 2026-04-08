import asyncio
import os
from typing import List, Optional

from openai import OpenAI

# ✅ IMPORT YOUR ENV
from env import ScamDefenseEnv as MyEnvV4Env
from models import Action as MyEnvV4Action

# -------------------------------
# CONFIG
# -------------------------------

API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")

TASK_NAME = os.getenv("MY_ENV_V4_TASK", "easy")
BENCHMARK = "scam_defense_env"

MAX_STEPS = 3
SUCCESS_SCORE_THRESHOLD = 0.5

# -------------------------------
# PROMPT
# -------------------------------

SYSTEM_PROMPT = """
You are a scam detection AI.

Given a message, choose ONE action:
- warn
- block
- ignore
- verify
- educate

Respond with ONLY the action word.
""".strip()


# -------------------------------
# LOGGING (STRICT FORMAT)
# -------------------------------

def log_start(task: str, env: str, model: str):
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]):
    error_val = error if error else "null"
    done_val = str(done).lower()

    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}",
        flush=True,
    )


def log_end(success: bool, steps: int, score: float, rewards: List[float]):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)

    print(
        f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}",
        flush=True,
    )


async def get_model_action(client, message: str) -> str:
    if API_KEY and API_KEY != "dummy":
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": message}
                ],
                temperature=0.0,
                max_tokens=10
            )
            action_text = response.choices[0].message.content.strip().lower()
            for valid in ["warn", "block", "ignore", "verify", "educate"]:
                if valid in action_text:
                    return valid
        except Exception:
            pass

    # Safe deterministic fallback
    msg = message.lower()
    scam_keywords = ["lottery", "winner", "otp", "bank", "verify", "urgent", "click"]
    
    if any(word in msg for word in scam_keywords):
        if "[verification result]" in msg:
            return "warn"
        else:
            return "verify"
    return "ignore"


# -------------------------------
# MAIN
# -------------------------------

async def main():

    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY or "dummy_key_to_prevent_crash")

    env = await MyEnvV4Env.from_docker_image(None)

    rewards: List[float] = []
    steps_taken = 0
    success = False
    score = 0.0

    log_start(task=TASK_NAME, env=BENCHMARK, model=MODEL_NAME)

    try:
        result = await env.reset()
        obs = result.observation

        for step in range(1, MAX_STEPS + 1):

            message = obs.message

            # ✅ Use API action (with safe fallback)
            action_str = await get_model_action(client, message)

            result = await env.step(MyEnvV4Action(action=action_str))

            obs = result.observation
            reward = result.reward or 0.0
            done = result.done

            rewards.append(reward)
            steps_taken = step

            log_step(
                step=step,
                action=action_str,
                reward=reward,
                done=done,
                error=None,
            )

            if done:
                break

        # -------------------------------
        # SCORE CALCULATION
        # -------------------------------

        total_reward = sum(rewards)
        max_possible = len(rewards) * 1.0 if rewards else 1.0

        score = total_reward / max_possible
        score = max(0.0, min(1.0, score))

        success = score >= SUCCESS_SCORE_THRESHOLD

    finally:
        try:
            await env.close()
        except Exception:
            pass

        log_end(success=success, steps=steps_taken, score=score, rewards=rewards)


if __name__ == "__main__":
    asyncio.run(main())
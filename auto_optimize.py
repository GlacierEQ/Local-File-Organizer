import asyncio
from ai.blackbox import BlackboxAI, BlackboxConfig, BlackboxPaths  # Ensure BlackboxAI is in /ai/blackbox.py

async def run_auto_optimization():
    config = BlackboxConfig()
    paths = BlackboxPaths()
    blackbox = BlackboxAI(config, paths)
    # Continuously run evolution; then auto-diagnose and self-repair
    await blackbox.auto_evolve()       # Recursive evolution cycle
    await blackbox.diagnose_and_repair() # Self-diagnosis & repair hook

if __name__ == '__main__':
    asyncio.run(run_auto_optimization())

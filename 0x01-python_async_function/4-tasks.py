#!/usr/bin/env python3
"""
Function
"""
import asyncio
from typing import List
from random import uniform


async def wait_random(max_delay: int = 10) -> float:
    """
    Asynchronous coroutine that waits for a random delay
    between 0 and max_delay seconds
    and eventually returns it.
    """
    delay = uniform(0, max_delay)
    await asyncio.sleep(delay)
    return delay


def task_wait_random(max_delay: int) -> asyncio.Task:
    """
    Function that takes an integer max_delay and returns an asyncio.Task.
    """
    return asyncio.create_task(wait_random(max_delay))


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """
    Asynchronous coroutine that spawns task_wait_random n times
    with the specified max_delay
    and returns the list of all the delays in ascending order.
    """
    tasks = [task_wait_random(max_delay) for _ in range(n)]
    return await asyncio.gather(*tasks)

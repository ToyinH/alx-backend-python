#!/usr/bin/env python3
"""
execute multiple coroutines at the same time with async
"""
import asyncio
from typing import List
from random import randint
from itertools import repeat
from asyncio import gather


async def wait_random(max_delay: int = 10) -> float:
    """
    Asynchronous coroutine that waits for a random delay
    between 0 and max_delay seconds
    and eventually returns it.
    """
    delay = randint(0, max_delay)
    await asyncio.sleep(delay)
    return delay


async def wait_n(n: int, max_delay: int) -> List[float]:
    """
    Asynchronous coroutine that spawns wait_random n times with
    the specified max_delay
    and returns the list of all the delays in ascending order.
    """
    coroutines = [wait_random(max_delay) for _ in repeat(None, n)]
    delays = await gather(*coroutines)
    return sorted(delays)

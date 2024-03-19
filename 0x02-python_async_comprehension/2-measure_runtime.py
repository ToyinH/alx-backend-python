#!/usr/bin/env python3
"""
Run time for four parallel comprehensions
"""

import asyncio
from typing import List
from time import perf_counter
from asyncio import Task
async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """
    A measure_runtime coroutine that will execute async_comprehension
    four times in parallel using asyncio.gather.
    measure_runtime should measure the total runtime and return it.
    """
    start_time: float = perf_counter()

    tasks: List[Task] = [
        async_comprehension(),
        async_comprehension(),
        async_comprehension(),
        async_comprehension()
    ]

    await asyncio.gather(*tasks)

    end_time: float = perf_counter()
    return end_time - start_time

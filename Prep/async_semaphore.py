"""
Learning demo: async API calls with a semaphore + text output.

What this script demonstrates:
1. One Python process runs one asyncio event loop.
2. aiohttp makes multiple API calls concurrently.
3. asyncio.Semaphore limits how many requests can run at the same time.
4. The script collects all results and writes them to api_results_semaphore.txt.

Install dependency if needed:
    python -m pip install aiohttp

Public API used:
    https://jsonplaceholder.typicode.com/todos/{id}
"""

import asyncio
import os
import time
from pathlib import Path

import aiohttp


API_URL = "https://jsonplaceholder.typicode.com/todos/{}"
OUTPUT_FILE = Path(__file__).with_name("api_results_semaphore.txt")
TODO_IDS = list(range(1, 13))
MAX_CONCURRENT_REQUESTS = 4


def print_plan(todo_ids):
	print("Semaphore async plan:")
	print(f"  todo IDs: {todo_ids}")
	print(f"  max requests running at once: {MAX_CONCURRENT_REQUESTS}")
	print(f"  process ID: {os.getpid()}")
	print()


def format_todo(data, process_id):
	"""Turn one API response into one beginner-readable line of text."""
	return (
		f"process={process_id} | "
		f"id={data['id']} | "
		f"title={data['title']} | "
		f"completed={data['completed']}"
	)


async def fetch_todo(session, semaphore, todo_id):
	"""Fetch one todo item, but only after the semaphore allows it."""
	process_id = os.getpid()
	url = API_URL.format(todo_id)

	try:
		async with semaphore:
			async with session.get(url) as response:
				response.raise_for_status()
				data = await response.json()
				return format_todo(data, process_id)
	except Exception as exc:
		# Returning an error line keeps one failed request from stopping the demo.
		return f"process={process_id} | id={todo_id} | error={exc}"


async def fetch_all(todo_ids):
	"""Create all tasks, while the semaphore controls concurrent execution."""
	timeout = aiohttp.ClientTimeout(total=20)
	semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

	async with aiohttp.ClientSession(timeout=timeout) as session:
		tasks = [
			asyncio.create_task(fetch_todo(session, semaphore, todo_id))
			for todo_id in todo_ids
		]
		return await asyncio.gather(*tasks)


def write_results(lines, elapsed_seconds):
	"""Write a small explanation plus the fetched API data to a text file."""
	header = [
		"Async semaphore API call demo",
		"",
		f"API pattern: {API_URL}",
		f"Process ID used: {os.getpid()}",
		f"Max concurrent requests: {MAX_CONCURRENT_REQUESTS}",
		f"Total API calls: {len(lines)}",
		f"Elapsed seconds: {elapsed_seconds:.2f}",
		"",
		"All result lines should show the same OS process ID.",
		"The semaphore controls concurrency inside that one process.",
		"",
	]

	OUTPUT_FILE.write_text("\n".join(header + lines) + "\n", encoding="utf-8")


def main():
	start_time = time.perf_counter()

	print_plan(TODO_IDS)
	print("Fetching API data...")

	lines = asyncio.run(fetch_all(TODO_IDS))
	elapsed_seconds = time.perf_counter() - start_time
	write_results(lines, elapsed_seconds)

	print(f"Saved {len(lines)} results to {OUTPUT_FILE}")
	print("Open api_results_semaphore.txt to compare this with api_results.txt.")


if __name__ == "__main__":
	main()
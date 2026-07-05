"""
Learning demo: multiprocessing + async API calls + text output.

What this script demonstrates:
1. The parent process chooses API request IDs and splits them into chunks.
2. multiprocessing.Pool starts worker processes.
3. Each worker process runs its own asyncio event loop.
4. Inside each process, aiohttp makes multiple API calls concurrently.
5. The parent process collects all results and writes them to api_results.txt.

Install dependency if needed:
    python -m pip install aiohttp

Public API used:
    https://jsonplaceholder.typicode.com/todos/{id}
"""

import asyncio
import os
import time
from math import ceil
from multiprocessing import Pool, cpu_count
from pathlib import Path

import aiohttp


API_URL = "https://jsonplaceholder.typicode.com/todos/{}"
OUTPUT_FILE = Path(__file__).with_name("api_results.txt")
TODO_IDS = list(range(1, 13))
MAX_PROCESSES = 4


def chunk_items(items, chunk_size):
	"""Split a list into smaller lists so each process gets one chunk."""
	for index in range(0, len(items), chunk_size):
		yield items[index : index + chunk_size]


def build_work_chunks(todo_ids):
	"""Decide how many worker processes to use and which IDs each gets."""
	worker_count = min(MAX_PROCESSES, len(todo_ids), cpu_count() or 1)
	chunk_size = ceil(len(todo_ids) / worker_count)
	chunks = list(chunk_items(todo_ids, chunk_size))

	return worker_count, chunks


def print_plan(chunks):
	print("Work split between processes:")
	for chunk_number, chunk in enumerate(chunks, start=1):
		print(f"  chunk {chunk_number}: todo IDs {chunk}")
	print()


def format_todo(data, process_id):
	"""Turn one API response into one beginner-readable line of text."""
	return (
		f"process={process_id} | "
		f"id={data['id']} | "
		f"title={data['title']} | "
		f"completed={data['completed']}"
	)


async def fetch_todo(session, todo_id, process_id):
	"""Fetch one todo item asynchronously inside one worker process."""
	url = API_URL.format(todo_id)

	try:
		async with session.get(url) as response:
			response.raise_for_status()
			data = await response.json()
			return format_todo(data, process_id)
	except Exception as exc:
		# Returning an error line keeps one failed request from stopping the demo.
		return f"process={process_id} | id={todo_id} | error={exc}"


async def fetch_batch(todo_ids):
	"""Create async tasks for one process and wait for all of them."""
	process_id = os.getpid()
	timeout = aiohttp.ClientTimeout(total=20)

	async with aiohttp.ClientSession(timeout=timeout) as session:
		# create_task starts each request now, so they can wait on the network together.
		tasks = [
			asyncio.create_task(fetch_todo(session, todo_id, process_id))
			for todo_id in todo_ids
		]
		return await asyncio.gather(*tasks)


def run_worker(todo_ids):
	"""
	Entry point for one worker process.

	Pool.map needs a normal function, not an async function. asyncio.run bridges
	that gap by creating an event loop inside this process.
	"""
	return asyncio.run(fetch_batch(todo_ids))


def flatten(nested_results):
	"""Convert [[line, line], [line, line]] into [line, line, line, line]."""
	return [line for batch in nested_results for line in batch]


def write_results(lines, worker_count, elapsed_seconds):
	"""Write a small explanation plus the fetched API data to a text file."""
	header = [
		"Multiprocessing + async API call demo",
		"",
		f"API pattern: {API_URL}",
		f"Worker processes used: {worker_count}",
		f"Total API calls: {len(lines)}",
		f"Elapsed seconds: {elapsed_seconds:.2f}",
		"",
		"Each result line shows which OS process handled that request.",
		"",
	]

	OUTPUT_FILE.write_text("\n".join(header + lines) + "\n", encoding="utf-8")


def main():
	start_time = time.perf_counter()
	worker_count, chunks = build_work_chunks(TODO_IDS)

	print_plan(chunks)
	print("Fetching API data...")

	# Pool.map sends one chunk to each worker process.
	with Pool(processes=worker_count) as pool:
		nested_results = pool.map(run_worker, chunks)

	lines = flatten(nested_results)
	elapsed_seconds = time.perf_counter() - start_time
	write_results(lines, worker_count, elapsed_seconds)

	print(f"Saved {len(lines)} results to {OUTPUT_FILE}")
	print("Open api_results.txt to compare process IDs across requests.")


if __name__ == "__main__":
	# Required on Windows when using multiprocessing.
	main()

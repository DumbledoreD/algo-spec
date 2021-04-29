from collections import namedtuple
from heapq import heappush, heapreplace

AssignedJob = namedtuple("AssignedJob", ("worker", "started_at"))


def assign_jobs(n_workers, jobs):
    end_times_heap = []
    result = []

    for i in range(n_workers):
        if i >= len(jobs):
            return result

        result.append(AssignedJob(i, 0))
        heappush(end_times_heap, (jobs[i], i))

    for t in range(n_workers, len(jobs)):
        at, worker = end_times_heap[0]
        result.append(AssignedJob(worker, at))
        heapreplace(end_times_heap, (at + jobs[t], worker))

    return result


def main():
    n_workers, n_jobs = map(int, input().split())
    jobs = list(map(int, input().split()))
    assert len(jobs) == n_jobs

    assigned_jobs = assign_jobs(n_workers, jobs)

    for job in assigned_jobs:
        print(job.worker, job.started_at)


if __name__ == "__main__":
    main()

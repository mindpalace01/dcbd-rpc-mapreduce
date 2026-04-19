import requests
import time
import re
from multiprocessing import Pool, cpu_count
from collections import Counter

BASE_URL = "http://72.60.221.150:8080"
STUDENT_ID = "MDS202517"


def login(student_id):
    # get session key for authentication
    response = requests.post(
        f"{BASE_URL}/login",
        json={"student_id": student_id}
    )
    response.raise_for_status()
    return response.json()["secret_key"]


def get_publication_title_with_key(key, filename):
    # fetch title with retry handling (mainly for 429)
    while True:
        try:
            response = requests.post(
                f"{BASE_URL}/lookup",
                json={"secret_key": key, "filename": filename}
            )

            if response.status_code == 429:
                time.sleep(0.1)
                continue

            response.raise_for_status()
            return response.json()["title"]

        except requests.exceptions.RequestException:
            time.sleep(0.2)


def mapper(filename_chunk):
    # process a chunk of files and return word counts
    counter = Counter()
    key = login(STUDENT_ID)

    for filename in filename_chunk:
        title = get_publication_title_with_key(key, filename)

        if title:
            first_word = title.strip().split()[0]
            first_word = re.sub(r'^\W+|\W+$', '', first_word)

            if first_word:
                counter[first_word] += 1

    return counter


def reduce_counters(counters):
    # merge all counters
    final = Counter()
    for c in counters:
        final.update(c)
    return final


def verify_top_10(student_id, top_10_list):
    # send result to server
    key = login(student_id)

    response = requests.post(
        f"{BASE_URL}/verify",
        json={"secret_key": key, "top_10": top_10_list}
    )

    print("\nVerification Result:")
    print(response.json())


if __name__ == "__main__":
    filenames = [f"pub_{i}.txt" for i in range(1000)]

    # split into chunks for parallel processing
    chunk_size = 50
    chunks = [filenames[i:i+chunk_size] for i in range(0, 1000, chunk_size)]

    print("Starting Map phase...")

    with Pool(cpu_count()) as pool:
        results = pool.map(mapper, chunks)

    print("Reducing results...")

    final_counts = reduce_counters(results)

    top_10 = [word for word, _ in final_counts.most_common(10)]

    print("\nTop 10 words:")
    print(top_10)

    verify_top_10(STUDENT_ID, top_10)

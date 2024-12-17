import requests
import subprocess
import random
import base64
import json
import time
import os

def write_json(data, file):
    json.dump(data, open("data/"+file+".json", "w"), indent=4)

def read_json(file):
    return json.load(open("data/"+file+".json", "r"))

def is_data(file):
    try:
        return open("data/"+file+".json", "r").read() != ""
    except:
        return False
    
def get_all_arvo_cases_meta():
    """
    Gets a list of all cases from the arvo meta repo / meta
    """
    all_cases = {}

    for file in os.listdir("ARVO-Meta/meta"):
        all_cases[file.split(".")[0]] = json.load(open("ARVO-Meta/meta/" + file, "r"))

    return all_cases

def get_all_arvo_cases_patches():
    """
    Gets a list of all cases from the arvo meta repo / patches
    """
    all_cases = {}

    for file in os.listdir("ARVO-Meta/patches"):
        all_cases[file.split(".")[0]] = base64.b64encode(open("ARVO-Meta/patches/" + file, "rb").read()).decode()

    return all_cases

def get_all_arvo_cases_dockerhub():
    """
    Gets a list of all cases from the arvo dockerhub
    """
    url = f"https://hub.docker.com/v2/repositories/n132/arvo/tags/"
    page = 1
    all_cases = []

    while True:
        response = requests.get(url, params={"page": page, "page_size": 100})
        data = response.json()
        if 'results' in data:
            all_cases += data["results"]
            page += 1
        elif "detail" in data and data["detail"] == "Rate limit exceeded":
            time.sleep(1)
        else:
            break

    return all_cases

def timed_execution(tag, iter=5):
    # download image (not timed)
    subprocess.run(["docker", "pull", "n132/arvo:" + tag], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # run image
    durations = []
    for i in range(5):
        command = ["docker", "run", "--rm", "n132/arvo:" + tag, "arvo"]
        start_time = time.time() # Record the start time
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) # Run the command
        end_time = time.time() # Record the end time
        duration = end_time - start_time # Calculate the duration
        durations.append(duration)

    # remove image (not timed)
    subprocess.run(["docker", "rmi", "-f", "n132/arvo:" + tag], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return durations

if is_data("dh_cases"):
    dh_cases = read_json("dh_cases")
else:
    dh_cases = get_all_arvo_cases_dockerhub()
    write_json(dh_cases, "dh_cases")

if is_data("meta_cases"):
    meta_cases = read_json("meta_cases")
else:
    meta_cases = get_all_arvo_cases_meta()
    write_json(meta_cases, "meta_cases")

if is_data("patch_cases"):
    patch_cases = read_json("patch_cases")
else:
    patch_cases = get_all_arvo_cases_patches()
    write_json(patch_cases, "patch_cases")

if is_data("runtimes"):
    runtimes = read_json("runtimes")
else:
    runtimes = {}
    for case in random.sample(dh_cases, 50):
        print(case["name"])
        runtimes[case["name"]] = timed_execution(case["name"])
        write_json(runtimes, "runtimes")


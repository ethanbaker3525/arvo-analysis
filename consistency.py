import common

if __name__ == "__main__":

    dh_case_names = set([case["name"].split("-")[0] for case in common.dh_cases])
    meta_case_names = set([case for case in common.meta_cases.keys()])
    patches_case_names = set([case for case in common.patch_cases.keys()])

    print(f"There are {len(dh_case_names)} ids from docker hub. There are {len(meta_case_names)} ids from ARVO-Meta/meta. There are {len(patches_case_names)} ids from ARVO-Meta/patches")
    
    print(f"{len(dh_case_names & meta_case_names & patches_case_names)} ids exist in all 3 sources.")

    print(f"{len(dh_case_names - meta_case_names - patches_case_names)} ids only exist in docker hub")
    print(f"{len(meta_case_names - dh_case_names - patches_case_names)} ids only exist in ARVO-Meta/meta")
    print(f"{len(patches_case_names - dh_case_names - meta_case_names)} ids only exist in ARVO-Meta/patches")


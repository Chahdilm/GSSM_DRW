def generate_versions():
    versions = []
    # We build 5‐tuples (v0,v1,v2,v3,v4) such that:
    #  • v0 ≥ v1 ≥ v2 ≥ v3 ≥ v4 ≥ 0
    #  • adjacent differences ≤ 1 (so v[j] - v[j+1] ∈ {0,1})
    #  • v0 starts at 1
    # The loops are “reversed” so that when we print, the sort order
    # is lexicographic on (v4,v3,v2,v1,v0), matching your sequence.
    for v4 in range(0, 2):            # v4 ∈ {0,1}
        for v3 in range(v4, v4 + 2):  # v3 ≥ v4 and v3 − v4 ≤ 1
            for v2 in range(v3, v3 + 2):
                for v1 in range(v2, v2 + 2):
                    for v0 in range(v1, v1 + 2):
                        if v0 >= 1:
                            versions.append(f"{v0}_{v1}_{v2}_{v3}_{v4}")
    return versions

if __name__ == "__main__":
    versions = generate_versions()
    for s in versions:
        print(s)
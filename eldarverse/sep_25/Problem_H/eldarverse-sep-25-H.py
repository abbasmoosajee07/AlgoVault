"""Eldarverse Puzzles - Problem H
Solution Started: September 4,
Puzzle Link: https://www.eldarverse.com/problem/sep-25-long-H
Solution by: Abbas Moosajee
Brief: [Sea Voyage]"""

#!/usr/bin/env python3
from pathlib import Path
import random
from collections import defaultdict, Counter, deque
# Load input file
input_file = "problem-sep-25-long-H-input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    raw_data = f.read().splitlines()
    raw_data1 = ['2', '4', 'BATUMI TRABZON', 'ODESSA CONSTANTA', 'ODESSA TRABZON', 'ODESSA ISTANBUL', '2', 'SAMSUN TRABZON', 'BURGAS VARNA']

def parse_raw_data(data):
    T = int(data[0].strip())
    idx = 1
    tests = []
    for _ in range(T):
        M = int(data[idx].strip()); idx += 1
        edges = []
        for _ in range(M):
            a, b = data[idx].strip().split()
            idx += 1
            edges.append((a, b))
        tests.append(edges)
    return tests

def build_graph(edges):
    """Return adjacency(multiset) and degree counts and set of nodes."""
    adj = defaultdict(list)
    deg = Counter()
    nodes = set()
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
        deg[a] += 1
        deg[b] += 1
        nodes.add(a); nodes.add(b)
    return adj, deg, nodes

def components_with_edges(adj, nodes):
    """Return list of components (each a set of nodes) for vertices that appear in edges."""
    seen = set()
    comps = []
    for v in list(nodes):
        if v in seen:
            continue
        # BFS/DFS
        q = [v]
        seen.add(v)
        comp = {v}
        while q:
            x = q.pop()
            for y in adj[x]:
                if y not in seen:
                    seen.add(y)
                    comp.add(y)
                    q.append(y)
        comps.append(comp)
    return comps

def verify_augmented_graph(orig_adj, added_edges):
    """Check connectivity (all nodes that appear in edges or BATUMI) and even degrees."""
    adj = {u:list(vs) for u, vs in orig_adj.items()}
    deg = Counter()
    for u, vs in adj.items():
        deg[u] = len(vs)
    for a, b in added_edges:
        adj.setdefault(a, []).append(b)
        adj.setdefault(b, []).append(a)
        deg[a] += 1; deg[b] += 1
    # nodes to consider in connectivity: nodes with degree>0 OR BATUMI (we require start/end at BATUMI)
    nodes_used = set([n for n,d in deg.items() if d>0])
    nodes_used.add("BATUMI")
    # Check connectivity among nodes_used
    # If there're no edges at all (shouldn't happen), but still
    start = None
    if nodes_used:
        # find a node that actually exists in adj
        for n in nodes_used:
            if n in adj:
                start = n
                break
        if start is None:
            # everything isolated
            start = next(iter(nodes_used))
    visited = set()
    stack = [start]
    while stack:
        x = stack.pop()
        if x in visited:
            continue
        visited.add(x)
        for y in adj.get(x,[]):
            if y not in visited:
                stack.append(y)
    # Only consider nodes_that_have_degree_or_are_BATUMI
    # For nodes that are considered but not present in adj (degree 0) they count as isolated and fail connectivity.
    conn_ok = all([(n in visited) for n in nodes_used])
    # all degrees even?
    even_ok = all((deg[n] % 2 == 0) for n in deg)
    return conn_ok and even_ok

def solve_one(edges):
    # Build original graph
    orig_adj, deg, nodes = build_graph(edges)
    # ensure BATUMI present in node set even if isolated
    nodes_all = set(nodes)
    nodes_all.add("BATUMI")
    # Find components among nodes that have at least one incident edge (degree>0)
    nodes_with_edges = {n for n,c in deg.items() if c>0}
    comps = []
    if nodes_with_edges:
        seen = set()
        for v in list(nodes_with_edges):
            if v in seen:
                continue
            stack = [v]
            comp = set()
            seen.add(v)
            while stack:
                x = stack.pop()
                comp.add(x)
                for y in orig_adj.get(x,[]):
                    if y not in seen:
                        seen.add(y); stack.append(y)
            comps.append(comp)
    else:
        comps = []
    # Find which component contains BATUMI (if any)
    batumi_comp_index = None
    for i, comp in enumerate(comps):
        if "BATUMI" in comp:
            batumi_comp_index = i
            break
    # If BATUMI isn't in any component with edges, we will treat it specially (it's isolated).
    batumi_is_isolated = ("BATUMI" not in nodes_with_edges)

    # For each component compute odd-degree vertices
    comp_nodes = comps[:]  # list of sets
    comp_odds = []
    for comp in comp_nodes:
        odds = [v for v in comp if deg[v] % 2 == 1]
        comp_odds.append(odds)

    # Compute minimum K (count of added edges)
    K = 0
    for idx, odds in enumerate(comp_odds):
        if idx == batumi_comp_index:
            K += len(odds) // 2
        else:
            K += max(1, len(odds) // 2)
    if batumi_is_isolated:
        # If there are no comps at all and BATUMI isolated and there are zero existing tickets (shouldn't),
        # still need 0? But problem guarantees M>=1, so at least one component exists. Add 1 if BATUMI is not attached.
        K += 1

    # Now construct placeholders (slots) from comps to pair/pick endpoints of added edges
    slots = []  # list of (city_name, comp_index)
    # We'll also keep for each component a list of candidate nodes to pick when we need "arbitrary 2 nodes" for comps with zero odd.
    comp_list_nodes = [sorted(list(c)) for c in comp_nodes]

    for idx, comp in enumerate(comp_nodes):
        odds = comp_odds[idx]
        if idx == batumi_comp_index:
            # for BATUMI component: include its odd vertices (no placeholder if none)
            for v in odds:
                slots.append((v, idx))
        else:
            if len(odds) > 0:
                # include all odd vertices
                for v in odds:
                    slots.append((v, idx))
            else:
                # no odd vertices -> pick two distinct nodes from this component as placeholders
                # component with edges must have at least 2 distinct vertices
                nodes_here = comp_list_nodes[idx]
                if len(nodes_here) >= 2:
                    slots.append((nodes_here[0], idx))
                    slots.append((nodes_here[1], idx))
                else:
                    # fallback: if somehow a component has single node (shouldn't happen with edges), duplicate it.
                    slots.append((nodes_here[0], idx))
                    slots.append((nodes_here[0], idx))

    # If BATUMI is isolated (not in any component), we must add BATUMI to slots once (or twice if needed to make even)
    if batumi_is_isolated:
        # Append BATUMI as placeholder (so we ensure it's connected later)
        slots.append(("BATUMI", -1))  # component index -1 denotes BATUMI-isolated pseudo-component

    # Ensure slots length is even (it should be by design)
    if len(slots) % 2 == 1:
        # add an extra BATUMI placeholder to make even; it's safe (we will try random pairing)
        slots.append(("BATUMI", -1))

    # Now we need to pair up slots into edges such that:
    #  - we don't pick same-city pair (self-loop)
    #  - after adding these edges to original graph, graph is connected and all degrees are even
    # We'll try randomized pairings (shuffle) many times; constraint sizes (M <= 100) make this feasible.
    attempts = 1000
    added_edges = None
    L = len(slots)
    indices = list(range(L))

    for attempt in range(attempts):
        random.shuffle(indices)
        pairs = []
        ok = True
        # make pairs in zipped pairs order
        for i in range(0, L, 2):
            a = slots[indices[i]][0]
            b = slots[indices[i+1]][0]
            if a == b:
                ok = False
                break
            pairs.append((a, b))
        if not ok:
            continue
        # Verify that this set of edges achieves connectivity + even degrees
        if verify_augmented_graph(orig_adj, pairs):
            added_edges = pairs
            break
    # If random attempts failed (unlikely), fall back to constructive greedy:
    if added_edges is None:
        # Greedy fallback: connect components to BATUMI one by one, and then pair remaining odds within each comp.
        added = []
        # If BATUMI isolated: connect it to any node in first component
        if batumi_is_isolated and comp_nodes:
            a = "BATUMI"
            b = next(iter(comp_nodes[0]))
            added.append((a, b))
        # Now for each component except the one containing BATUMI, connect one node to some node in the BATUMI component
        # Choose a representative from each comp
        bat_idx = batumi_comp_index
        if bat_idx is None and comp_nodes:
            # after connecting batumi to comp_nodes[0], treat batumi_comp_index=0 for rest
            bat_idx = 0
        for idx, comp in enumerate(comp_nodes):
            if idx == bat_idx: continue
            # pick any vertex from comp and connect to some vertex in batumi component (if exists) or to BATUMI
            u = next(iter(comp))
            if bat_idx is not None:
                v = next(iter(comp_nodes[bat_idx]))
            else:
                # no batumi comp, connect to BATUMI
                v = "BATUMI"
            added.append((u, v))
        # now we might need to fix parity by pairing leftover odd vertices arbitrarily inside augmented graph
        # compute degrees after these added edges:
        test_adj = {k:list(v) for k,v in orig_adj.items()}
        deg2 = Counter()
        for k in test_adj: deg2[k] = len(test_adj[k])
        for a,b in added:
            test_adj.setdefault(a, []).append(b)
            test_adj.setdefault(b, []).append(a)
            deg2[a] += 1; deg2[b] += 1
        # collect odd degree vertices
        odd_vertices = [v for v,c in deg2.items() if c % 2 == 1]
        # pair odd vertices arbitrarily
        while odd_vertices:
            u = odd_vertices.pop()
            v = odd_vertices.pop()
            if u == v:
                # find another v
                if odd_vertices:
                    v2 = odd_vertices.pop()
                    odd_vertices.append(v)
                    v = v2
                else:
                    # last one, pair with BATUMI or any node different
                    v = "BATUMI" if u != "BATUMI" else ("BATUMI_ALT")
            added.append((u, v))
        added_edges = added

    # Final K should match len(added_edges)
    # Return K, list pairs
    if added_edges is None:
        added_edges = []
    return len(added_edges), added_edges

tests = parse_raw_data(raw_data)

solutions = []
for case_idx, edges in enumerate(tests, start=1):
    k, added = solve_one(edges)
    solutions.append(f"Case #{case_idx}: {k}")
    for a, b in added:
        solutions.append(f"{a} {b}")
print("\n".join(solutions))

output_file = "problem-sep-25-long-H-output.txt"
output_path = Path(__file__).parent / output_file
with output_path.open("w", encoding="utf-8") as f:
    f.write("\n".join(solutions))


"""Unit tests for M1 Max roofline benchmark."""

from tools.bench.m1_roofline import measure_memory_bandwidth, simulate_prefix_cache


def test_measure_memory_bandwidth():
    bw = measure_memory_bandwidth()
    assert "bandwidth_gbps" in bw
    assert bw["bandwidth_gbps"] > 0
    assert bw["buffer_size_mb"] == 256.0


def test_simulate_prefix_cache():
    cache = simulate_prefix_cache(turns=5)
    assert cache["turns_simulated"] == 5
    assert cache["final_cache_hit_pct"] > 80.0
    assert len(cache["turn_progression"]) == 5

"""Independent arithmetic checks for the manuscript; not an ASH-Net runtime test."""
from collections import Counter
from itertools import combinations
from pathlib import Path
import json

G = [int(row, 2) for row in ('111100000', '110011000', '101010100', '100110001')]
code = []
for message in range(16):
    value = 0
    for j, row in enumerate(G):
        if message & (1 << (3-j)):
            value ^= row
    code.append(value)
C = set(code)
assert len(C) == 16
weights = dict(sorted(Counter(c.bit_count() for c in C).items()))
minimum_distance = min((a ^ b).bit_count() for a, b in combinations(C, 2))
assert minimum_distance == 4
assert all(c.bit_count() % 4 == 0 for c in C)
assert all((c & 1) == ((c >> 1).bit_count() % 2) for c in C)
assert all((c & 2) == 0 for c in C)

def strict_decode(value):
    distances = [(value ^ c).bit_count() for c in code]
    best = min(distances)
    return code[distances.index(best)] if best <= 1 and distances.count(best) == 1 else None

single = sum(strict_decode(c ^ (1 << j)) == c for c in C for j in range(9))
double = sum(strict_decode(c ^ (1 << a) ^ (1 << b)) is None
             for c in C for a,b in combinations(range(9),2))
assert single == 144 and double == 576
ternary_positions = sum(3**d for d in range(5))
assert ternary_positions == 121
fixed, outer = 164626, 16233
report = {
    'kind': 'independent_reference_calculations_not_native_runtime_reproduction',
    'source': 'ASH canonical specification revision 5b2880d32425f2c84c33a52c5b191c38a66fec55; ASH-Net docs/geometry.md at eef17dc023732c8897193345d1c3e89f56a3a21f',
    'ambient_states': 2**9,
    'even_parity_states': sum(x.bit_count()%2 == 0 for x in range(512)),
    'code_size': len(C), 'code_rank_from_cardinality': 4,
    'minimum_distance': minimum_distance,
    'weight_enumerator': weights,
    'strict_reference_decoder_single_bit_cases_correct': single,
    'strict_reference_decoder_double_bit_cases_rejected': double,
    'strict_reference_decoder_outcomes_over_512_inputs': {
        'exact': len(C), 'correctable_nonexact': single,
        'uncorrectable': sum(strict_decode(x) is None for x in range(512))
    },
    'ternary_depth4_positions_including_internal_nodes': ternary_positions,
    'ternary_depth4_leaves': 3**4,
    'two_full_cube_levels_times_ternary_positions': 512**2 * ternary_positions,
    'geometry_4096_record_work_fixed': fixed,
    'geometry_4096_record_work_outer': outer,
    'work_reduction_percent': 100*(fixed-outer)/fixed,
    'fixed_to_outer_work_ratio': fixed/outer,
    'retrieval_rank1_lexical_percent': 100*6/8,
    'retrieval_rank1_associative_percent': 100*8/8,
    'retrieval_rank1_difference_percentage_points': 100*(8-6)/8,
    'native_swift_tests_run_in_this_review': False,
    'live_model_trials_run_in_this_review': False
}
output = Path(__file__).with_name('independent_calculations.json')
output.write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report, indent=2))

# ASH-Network: A Recursive Associative Architecture for Subconscious Memory in AI Agents

**Working preprint draft · Version 0.1 · 24 November 2026**  
**Author:** James Daley  
**Evidence snapshot:** ASH-Network commit `eef17dc023732c8897193345d1c3e89f56a3a21f`; ASH computational specification commit `5b2880d32425f2c84c33a52c5b191c38a66fec55`.

> Editorial status: This manuscript distinguishes implementation inspection, previously recorded experiments, independent reference calculations, and proposed future experiments. The native macOS and live-model experiments were not rerun during preparation of this draft. Source identifiers resolve in the references and companion evidence ledger. This is a research draft, not a submission-ready declaration of independent replication.

## Abstract

Persistent memory can inform an artificial intelligence agent only when relevant experience becomes available at a useful decision point. We present ASH-Network, a recursive associative memory architecture that adapts ASH's finite binary geometry into a sparsely materialized, recursively extensible memory space. Source-bearing records retain stable identities independently of their addresses; learned cue associations retain their supporting origins; and corrections preserve earlier records through explicit supersession. A connector-resident engine observes public plans, proposed actions, receipts, and reported outcomes. When an unfolding sequence matches supported historical cases, it delivers a cited recollection before a pending action is dispatched. We use *subconscious memory* operationally to describe this background, agent-query-independent recollection, without asserting subjective experience or biological equivalence. Recorded native qualification recovered the expected record and source at rank one for eight of eight answerable queries and returned no hits for four unsupported queries. A separate sequence replay signaled at the intended checkpoint in two positive cases and remained silent in four controls. Four paired runs of one controlled ledger task recorded duplicate entries with the baseline connector and a single entry with memory pressure; however, the model incorrectly described its own action history, and an earlier wording variant did not prevent duplication. These findings support prototype feasibility, not general behavioral superiority. The contribution is an inspectable composition of recursive ASH addressing, provenance-aware association, and timely recollection, together with an evaluation boundary separating retrieval, delivery, action, and explanation.

**Keywords:** AI agent memory; associative memory; recursive addressing; ASH; provenance; proactive recollection; action-conditioned retrieval; memory pressure.

## 1. Introduction

An agent can retain a useful observation without using it when it matters. A record may survive a restart yet never enter the context of the decision that it should inform. Conversely, a retrieved passage may enter a model request but be misapplied, ignored, or described inaccurately afterward. Memory availability, memory selection, intervention timing, and successful action therefore constitute different engineering and evaluation problems. Prior research addresses persistent experience, context management, linked memory organization, and proactive intervention through distinct mechanisms [L1–L7].

ASH-Network investigates this problem by connecting a persistent associative store to the observable execution of an agent. Its starting point is ASH as a layered information architecture: a finite local state alphabet can support recursively extensible structures. The finite alphabet does not impose a finite total number of possible paths, while unbounded address depth does not imply infinite physical storage. ASH-Network materializes occupied paths and records rather than allocating every possible position [S1–S4].

The architectural transition is important. The system does not attempt to derive intelligence from a nine-bit label. ASH contributes a precise representation and transformation vocabulary. ASH-Network adds record identity, source attribution, learned relationships, history, and interfaces to an agent's current work. A memory can occupy one location and still become relevant through an association supported by experience at another location [S3–S5].

The further transition from persistent storage to *subconscious memory* concerns initiation. In this paper, subconscious denotes a background function that can bring a sourced memory into an agent's working context without an explicit memory query from that agent at the triggering decision. It does not denote consciousness, hidden access to model reasoning, or a claim about human neurobiology. The agent receives an explicit recollection and retains the decision about what to do [S6, S7].

Consider a write whose acknowledgement times out. Retrying may be appropriate when the write did not commit, but may duplicate an entry when the service committed before the acknowledgement was lost. A generic opening request need not reveal this risk. The developing sequence—write, timeout, proposed repeat—is more informative. ASH-Network can recognize that sequence and present earlier, potentially conflicting outcomes while the repeat is still pending [S6, S10].

This paper makes three bounded contributions. First, it specifies the relationship between ASH's finite geometry and ASH-Network's recursive, sparse memory addressing. Second, it describes how source-aware associations and event-conditioned recollection connect remembered experience to a current decision. Third, it assembles the recorded prototype evidence while separating what the network returned, what the host delivered, what the agent actually dispatched, and what the model subsequently said. The paper does not claim that recursive ASH geometry has already been shown superior to all conventional memory indexes, or that proactive memory itself is a new research category.

## 2. From the ASH Foundation to Recursive Memory

### 2.1 Local binary geometry

The local state alphabet is

\[
\Omega=\mathbb F_2^9,\qquad |\Omega|=512.
\]

The graph \(Q_9\) connects labels at Hamming distance one. Binary addition is XOR. A separate even-parity subset is

\[
E=\{x\in\Omega:x_9=x_1\oplus\cdots\oplus x_8\},\qquad |E|=256.
\]

The canonical transform code is the binary row span of

\[
G=\begin{bmatrix}
1&1&1&1&0&0&0&0&0\\
1&1&0&0&1&1&0&0&0\\
1&0&1&0&1&0&1&0&0\\
1&0&0&1&1&0&0&0&1
\end{bmatrix}.
\]

It has parameters \([9,4,4]\), contains 16 codewords, and has weight enumerator \(1+14z^4+z^8\). Coordinate 9 participates in the parity relation; coordinate 8 is zero in this canonical code presentation. The code is doubly even and is not self-dual in \(\mathbb F_2^9\) [S1].

These are three different sets: the 512-label ambient alphabet, the 256-label parity subset, and the 16-codeword transform set. Treating them as interchangeable would misstate both the available address labels and the scope of the code's correction guarantees.

An independent enumeration accompanying this draft reproduces the code size, minimum distance, weight distribution, and parity properties. A reference bounded-distance decoder corrects the 144 single-bit corruptions of the 16 codewords and rejects the 576 two-bit corruption cases. These calculations establish properties of the stated code and reference decoder. They do not establish that ASH-Network invokes this decoder on stored natural-language memories or can correct an erroneous proposition.

### 2.2 What ASH-Network inherits—and what it does not

The inspected `ASHRouting` implementation uses the canonical generator rows for default domain placement. It normalizes text, applies a deterministic FNV-1a hash, and maps four hash bits to a codeword. A topic is mapped to an even-parity label using eight hash bits and an appended parity bit. Explicit routes may instead use any of the 512 local labels [S3].

This construction makes placement repeatable. It is not a trained semantic embedding: nearby hash buckets need not represent similar concepts. Likewise, membership in an error-correcting code is not evidence that the text at an address is true. ASH-Network's retrieval semantics arise from record contents and observed relationships, not from assigning factual meaning to individual bits [S2, S3, S5].

The ASH foundation and its application therefore have distinct responsibilities. The foundation defines finite objects and transformations. The network supplies application-level memory organization and evidence handling. Neither the software application nor its tests constitute empirical validation of ASH as a physical cosmology [S1].

### 2.3 Recursive addresses

A logical memory location is a nonempty sequence of local cube choices with an optional terminal contextual suffix:

\[
a=(v_1,\ldots,v_d;b),\qquad v_i\in\Omega,
\qquad b\in\bigcup_{k=0}^{4}\{0,1,2\}^k.
\]

Each additional \(v_i\) selects a vertex within the child cube associated with the preceding prefix. Thus \((3,5,6)\) and \((6,5,6)\) are different locations even though their final two labels agree. Parent–child containment, local Hamming proximity, and learned association are different relations [S2, S4].

At fixed depth \(d\), the unrestricted cube-path alphabet contains \(512^d\) paths. The union of finite paths over all positive depths is countably infinite. This is a property of the mathematical address grammar, not a claim about the capacity of a machine. A runtime always stores finitely many records, each with a finite path.

The depth-four ternary suffix contains

\[
|T_4|=\sum_{k=0}^{4}3^k=121
\]

positions, including 81 leaves. The original two-cube illustration therefore contains

\[
512^2\times121=31{,}719{,}424
\]

virtual positions. This count is neither the number of stored memories nor a measurement of semantic capacity. The current representation supports variable cube depth rather than fixing the complete network to this two-level illustration [S2, S4].

The network's recursion should also be distinguished from the ASH reference's reconstruction branch semantics. ASH-Network uses recursive containment and a contextual suffix; the inspected memory implementation does not thereby inherit every image-reconstruction operator, branch score, or physical interpretation of another ASH application [S1, S2].

### 2.4 Sparse materialization and stable identity

Let \(M_t\) be the finite record collection at time \(t\). Ignoring auxiliary indexes, a trie representing its occupied cube prefixes requires at most

\[
1+\sum_{m\in M_t}d(m)
\]

prefix nodes before additional layout coordinates are considered. Shared prefixes reduce this bound. Empty virtual locations require no memory record. Exact path traversal depends on path length; this architecture does not establish constant-time semantic recall [S2, S4].

Record identity is separate from location. Several records can occupy the same address without becoming the same memory. The source-bearing record includes a stable identifier, topic, text, source, kind, aliases, optional supersession relation, and route information [S3].

A returned citation contains a record identifier together with its packed path and context. The resolver uses the full reference rather than assuming an address uniquely identifies a record. This distinction allows learned links to target stable identities while a physical index is reorganized [S2, S7].

## 3. Persistent and Associative Memory

### 3.1 Memory lifecycle

ASH-Network stores source-bearing statements in an inspectable Markdown store, with persisted association and layout state. A correction creates a new record that explicitly supersedes an earlier one. Current-scope retrieval excludes superseded records, whereas the implemented history scope selects superseded records; history is therefore not an unrestricted search over every record [S5, S7].

The agent integration also represents choices as open cases whose outcomes may arrive later. A tool receipt is treated as evidence of what that receipt actually establishes, not as automatic proof of a broader successful outcome. A user report remains attributed to the user. Conflicting outcomes can remain distinct cases rather than being collapsed into a single favorable summary [S12].

This design permits correction without silently replacing the evidence that explains an earlier decision. It also creates responsibilities that remain partly external: a host must supply meaningful origin identifiers, an authentic source must remain interpretable, and a model-generated extraction can still omit a relevant fact or misjudge applicability [S7, S12].

### 3.2 Evidence-supported cue links

Let \(O(c,m)\) be the set of recorded origin identifiers supporting cue \(c\) as a route to memory \(m\). The native association weight is

\[
w(c,m)=|O(c,m)|.
\]

Replaying the same origin does not increment this weight. Retracting an origin removes its contribution. The associative mode requires at least two distinct origins before a cue edge can contribute to retrieval. This is an operational anti-duplication rule; distinct identifiers alone do not prove that the underlying evidence is statistically independent or truthful [S5].

The implementation combines lexical candidates and cue-linked candidates. For an eligible strongest cue, its association score has the form

\[
s_{\mathrm{assoc}}(c,m)=1+\frac{w(c,m)}{1+w(c,m)}.
\]

The record's final score is the maximum of its lexical and association scores. The strongest eligible cue is used rather than summing overlapping aliases. In current scope, a tie between the two highest scores returns no hits. This is an explicit deterministic abstention policy, not a calibrated probability of correctness [S5].

Learning here means updating external associative state. The inspected native retrieval layer does not train neural weights. Model-assisted extraction in the host is a separate component; the host can use its configured inference provider while the Swift core owns the stored records and native association rules [S5, S12].

### 3.3 Automatic capture and later use

The reference integration combines pre-turn recall, post-turn extraction, and live observation. Its host-side association engine accepts source-bearing evidence and a model-completion callback. It records selected readings and decisions, links later outcomes to earlier choices, and can expose earlier cases before a similar task. The connector-resident worker handles live sequence matching [S12].

This separation matters for interpretation. Passing a native retrieval fixture does not establish reliable extraction from arbitrary conversation. Likewise, successfully preserving a case does not establish that the case is applicable to a new circumstance. Both boundaries are visible in the recorded reader experiments [S11, S12].

## 4. Memory Pressure: Recollection Before Dispatch

### 4.1 Observable event model

The pressure engine consumes structured events whose types include `plan`, `proposal`, `dispatch`, `receipt`, `outcome`, and `end`. Events carry a session, run, increasing sequence, stable event identifier, and source. Action identifiers connect a proposal to its dispatch, receipt, and later outcome. Public plan text may be supplied; hidden chain-of-thought access is not required by this interface [S6, S7].

A useful distinction is

\[
\text{proposal}\ne\text{dispatch}\ne\text{receipt}\ne\text{outcome}.
\]

A proposed retry has not yet executed. A timeout is not a confirmed failure of the underlying write. A later audit may establish an outcome that was unknown when the receipt arrived. Preserving these distinctions is essential to both the mechanism and its evaluation.

### 4.2 Current recognition rule

The initial matcher recognizes bounded event motifs rather than arbitrary long-range semantic patterns. It forms signatures from a recent dispatched operation and receipt followed by a proposal or plan, or from relevant transitions between public plans. Signatures can include action categories, operation identity, receipt status, and whether the resource is the same, different, or unspecified. Intervening operations can change the active context [S6].

For a matched signature, supporting outcomes must include at least two distinct prior run identities and two distinct outcome-source identifiers among outcomes that are not marked unknown, uncertain, or pending. Current-run cases are excluded from supplying historical support. Retracted or withdrawn outcomes do not supply active matching candidates; missing or superseded native records are checked before delivery. The signal may preserve conflicting historical outcomes [S6].

These rules are inspectable, but bounded. They do not supply a learned probability that a proposed action is unsafe, a general causal explanation, or a proof that the remembered circumstances transfer to the present task. The host's categorization and source labeling remain part of the mechanism's assumptions.

### 4.3 Delivery and agent control

Participating write-enabled connections negotiate a versioned experimental extension. The host submits observations through `ash-net/observe`; this is distinct from the ordinary association tool named `ash_observe`. A checkpoint reports how far evaluation has progressed and may include a recollection signal. The connector also emits a notification with the same signal identifier, allowing deduplication and routing to the affected request [S7].

The adapter can hold a matching proposal and present the recollection before dispatch. The agent may inspect the cited cases, revise its choice, or continue. The supplied scripted trials explicitly exercise both revision and continuation, and the live record contains an earlier run in which the model still retried [S10].

Formally, let \(e_{1:t}\) be the observed prefix, \(a_t\) the pending proposal, and \(M_t\) the historical store. The architectural operation is

\[
r_t=\mathcal R(e_{1:t},a_t,M_t),
\]

where \(r_t\) is either no signal or a source-bearing recollection. The actor's next decision may then depend on \(r_t\). This equation summarizes the separation of responsibilities; it does not imply that the current matcher optimizes a learned intervention policy.

### 4.4 Why the term subconscious is useful

The term identifies a functional contrast: deliberate recall requires the agent to ask for memory, whereas pressure-driven recollection can be initiated by the memory subsystem during a developing task. The stored experience is outside the immediate working context until a supported trigger brings it forward.

Once delivered, the recollection is explicit and inspectable. Calling the initiating process subconscious therefore does not imply that its evidence should be hidden from users, that it overrides agent authority, or that the model acquires human-like awareness. The operational claim can be tested by tracing whether the agent issued a retrieval request, when the signal arrived, and whether the pending action had already executed [S6, S7, S10].

## 5. Evaluation Design and Evidence Provenance

This draft analyzes three complementary evidence groups from the pinned ASH-Network repository: native retrieval qualification, recursive geometry experiments, and sequence/agent pressure trials. A historical reader experiment supplies an additional test of the boundary between retrieval and answer use. These studies have different experimental units and should not be pooled into one accuracy number [S8–S11, S13].

### 5.1 Native retrieval qualification

The native held-out fixture contains eight answerable queries and four unsupported queries. Six retrieval conditions use the same corpus and limit of three records. Each operation launches a fresh CLI process. The criteria require correct identity and source at rank one on at least seven answerable queries, two transfer gains after reinforcement, empty results for all four unsupported queries, no forbidden record identifiers, and preservation after verified growth and restart [S8, S9].

The controls are disabled retrieval, exact full-label matching, lexical retrieval, node activation, unweighted links, and independently supported associations. Exact matching is intentionally strict and is not the strongest baseline; the lexical condition is the meaningful text-only native comparison. The learned transfer cases reuse known cues in unseen questions. They are not tests of arbitrary unseen-cue induction or broad semantic generalization [S8].

### 5.2 Geometry experiments

The geometry study compares fixed, deeper, and outer layouts containing the same records. A scoped prefix query supplies a context coordinate. The deeper layout appends that coordinate; the outer layout prepends it. A declared operation-count model charges for visited nodes and inspected records. Promotion is selected only when deeper subdivision does not improve work and projected outer-layout savings exceed the rebuild charge [S2].

The reported workloads vary occupancy, skew, and number of contexts. Result identifiers are compared with an independent scan within the original experiment. Timings and operation counts address candidate recovery under these query shapes, not language-model reasoning quality [S2].

### 5.3 Sequence recognition and live agent trials

The pressure replay teaches four historical runs and evaluates six new sequences after worker restart. Two sequences should trigger before dispatch; four are controls. All begin with the same opening question, for which the recorded lookup returns no records. This tests whether the developing sequence contributes information absent from the initial question [S10].

The live comparison uses one controlled ledger task and the recorded model identifier `google/gemma-4-12b`. Three earlier paired comparisons and one published-build pair are retained. The baseline and pressure conditions use copies of the trained store, but differ in connector intervention behavior. These are repeated runs of one task, not four independently sampled task families. An earlier attention-wording variant is reported separately [S10].

### 5.4 Scope of verification for this manuscript

The present preparation inspected governing documentation, selected implementation files, qualification criteria, native result summaries, and pressure dispatch traces. The code and pressure results were read at a pinned commit. The historical reader's underlying archived response corpus was not independently replayed; its account below is attributed to the inspected report [S11].

The companion Python calculation enumerates the stated finite code and recomputes address counts and selected arithmetic. It does not execute the Swift runtime, reproduce the original macOS environment, rerun model inference, or provide an independent experimental replication. Full-repository correctness and empirical superiority are outside this review's verified boundary.

## 6. Recorded Results

### 6.1 Retrieval and abstention

| Native mode | Correct ID and source at rank 1, /8 | Empty result on unsupported queries, /4 | Answerable MRR |
|---|---:|---:|---:|
| Disabled | 0 | 4 | 0.00 |
| Exact full label | 0 | 4 | 0.00 |
| Lexical | 6 | 4 | 0.75 |
| Node activation | 8 | 2 | 1.00 |
| Unweighted link | 8 | 2 | 1.00 |
| Supported association | 8 | 4 | 1.00 |

The result artifact records no forbidden identifiers in any mode. Supported association combines the two rank-one gains over lexical retrieval with empty outputs on all unsupported cases. Activation and unweighted links recover the answerable records but also return hits on two unsupported queries [S9].

The inspected qualification report states that all five frozen gates passed. The two transfer citations remained resolvable after growth and restart, and expected rankings were unchanged. Its calibration workload recorded 368 work units for fixed layout, 528 for deeper layout, and 80 for outer layout, against a 43-unit rebuild charge [S8].

The 8/8 result is a fixture result, not an estimated universal success rate. The query set is small and constructed; a percentage alone would obscure both the denominator and the specificity of the tested cues.

### 6.2 Geometry and growth

At 4,096 records in the reported skewed, 16-context workload, held-out work totals were 164,626 for fixed, 280,777 for deeper, and 16,233 for outer layout. The last comparison is a 90.14% reduction in the declared work units, calculated from the recorded totals. The corresponding reported batch medians were approximately 1.47, 4.19, and 0.86 milliseconds. These two comparisons are not interchangeable [S2].

Outer layout used more occupied in-memory nodes than fixed: 4,563 versus 1,985. The single-context and low-skew controls declined promotion. For a separate exact-query batch on the same 4,096-record fixture, precomputed direct-key lookup was faster than trie lookup, approximately 2 versus 8 microseconds [S2].

These observations support conditional reorganization rather than a blanket assertion that recursive addressing is faster. The benefit depends on supplied context, workload skew, query shape, and rebuild cost. They do not establish an end-to-end model speedup or a general advantage over a carefully matched conventional index.

### 6.3 Sequence recognition

| Held-out sequence | Recorded first recollection |
|---|---|
| Timed-out write followed by proposed repeat to the same ledger | Event 4, before dispatch |
| Partial listing followed by proposed continuation | Event 4, before dispatch |
| Read timeout | None |
| Timeout occurring after the retry | None |
| Destination already checked | None |
| Proposed write to a different ledger | None |

The recorded replay therefore matches the expected behavior on two positive cases and four controls. The harness resolves the cited cases through the ordinary citation interface [S10].

Reported checkpoint medians were 0.67 milliseconds with no unrelated records and 0.65 milliseconds with 64 unrelated records. Proposal-checkpoint 95th percentiles were 3.37 and 7.19 milliseconds, respectively. Each run timed 57 observations, including training, with 21 proposal checkpoints. These are small-store, local connector measurements excluding model inference; they are not a scaling law [S10].

### 6.4 Agent action and explanation

Across the four recorded paired ledger comparisons, the baseline produced two entries. With pressure, the model received two cited historical outcomes after proposing a retry and before dispatch, then inspected the ledger, leaving one entry. The dispatch records support this action-level distinction [S10].

The final replies nevertheless claimed that the retry had executed. An earlier attention wording delivered the evidence but the model chose to retry, leaving two entries. Both findings are necessary to interpret the successful action traces. Recollection can influence action without making the agent's explanation faithful, and evidence delivery alone does not force a safer decision [S10].

### 6.5 Retrieval is not semantic application

The separate historical reader report records 8/8 under its frozen content-and-source check for ASH-assisted answers, but only 7/8 on a separate reading of whether the question was answered. One answer quoted the correct precaution and source while denying that it applied. A paired provenance-presentation diagnostic improved overall judgments from 3/6 to 5/6 but missed its primary criterion; one improved answer also introduced an unsupported site label [S11].

These results reinforce a four-part evaluation boundary:

\[
\text{correct retrieval}\not\Rightarrow\text{correct application}
\not\Rightarrow\text{correct action}\not\Rightarrow\text{faithful explanation}.
\]

The notation denotes non-implication, not a necessary order of failure. Each property requires its own evidence.

## 7. Related Work and Positioning

Generative Agents connects natural-language experience, reflection, and behavior planning [L1]. MemGPT develops hierarchical context management and explicit control flow for fixed-context language models [L2]. These precedents establish that persistent experience and moving information into working context are not new in themselves.

A-MEM constructs linked notes and evolves memory organization using model-generated attributes and connections [L3]. ASH-Network's inspected native path differs in its deterministic routing and explicit origin-count association rule, although its host-side extraction remains model-assisted. This is a design distinction, not a demonstrated performance advantage.

LongMemEval evaluates information extraction, multi-session reasoning, temporal reasoning, knowledge updates, and abstention, and separates indexing, retrieval, and reading concerns [L4]. It provides a relevant evaluation reference. ASH-Network's 12-query qualification is not a LongMemEval benchmark result and should not be presented as comparable in scale.

Recent proactive-memory research is particularly close. Wu et al. describe a separate memory agent that selectively injects reminders into an action agent's context [L5]. Li et al. organize public events into validated trajectories and replay-assessed behavioral regularities [L6]. Bei et al. separate the maintenance of future intentions from determining when and how to realize them [L7]. These works rule out claiming that proactive recollection, source-linked experience, or timely intervention is categorically unprecedented.

The defensible contribution of ASH-Network is the particular architecture studied here: recursive ASH locations with stable record identity, explicit source-supported associations, and a bounded event-matching control path that can present historical evidence before a proposed tool action executes. Establishing whether this composition is advantageous requires matched experiments, not novelty inferred from terminology.

## 8. Discussion and Limitations

### 8.1 What the evidence supports

The current evidence supports the existence of an inspectable prototype whose memory records, associations, and citations persist across the tested operations; whose supported-association rule passes a small native qualification fixture; and whose pressure interface can place earlier cases into a model request before a pending action. The controlled action traces show that this intervention can coincide with a different dispatched action [S8–S10].

The evidence does not isolate the causal contribution of ASH geometry to those behavioral changes. An event matcher paired with a conventional identity store might produce the same intervention. Similarly, native lexical and learned-edge ablations identify useful differences inside the tested retrieval design but do not establish a complete advantage over modern embedding or graph-memory systems.

### 8.2 Generalization and experimental independence

The cue fixtures are scripted, pressure recognition uses bounded motifs, and the live comparisons repeat one controlled task with one recorded model. Revised attention wording and the earlier failed run introduce an important development history. The successful pairs should be described as a controlled demonstration, not as an independently validated behavioral policy.

The host-native reader comparison also differs from native ASH retrieval in available metadata and passage construction. It does not isolate packed addressing or an individual ranking feature. The companion arithmetic checks are independent calculations, not an independent human review or replication of the agent trials [S8, S11].

### 8.3 Provenance, security, and user control

Origin identifiers prevent simple replay from accumulating extra votes, but a producer could assign multiple identifiers to the same underlying claim. Source references can point to erroneous or adversarial material. Treating recollections as historical evidence rather than instructions is therefore a necessary design boundary, not a security guarantee established by the current results.

Further evaluation should test manipulated sources, cross-project contamination, stale outcomes, missing receipts, false intervention triggers, and corrections to cited cases. User-visible inspection, authorization for recording, and retention/deletion policy are especially important for a subsystem that learns automatically. This draft does not claim that those policies or adversarial defenses have been comprehensively qualified.

### 8.4 Resource limits

Unbounded recursive address potential is compatible with finite runtime resources. The current outer-growth experiment promotes one known context coordinate; it does not establish autonomous discovery of arbitrary new organizing dimensions. Small-store checkpoint timings exclude the inference cost of reconsideration, and character counts of delivered context are not provider-token counts [S2, S10].

The appropriate engineering claim is extensibility with measurable costs, not infinite usable memory or cost-free cognition.

## 9. Next Evaluation: Isolating the ASH Contribution

A next study should freeze previously unseen task families before tuning the matcher or attention wording. It should distinguish ordinary retrieval failure from recognition failure, late delivery, inappropriate intervention, agent noncompliance, and inaccurate post-action explanation.

A factorial comparison can hold memories, source metadata, model, and prompts constant while varying two principal factors: address/index design and intervention policy. The first compares ASH routing against a conventional stable-ID store with a matched index. The second compares query-only retrieval, deterministic event-triggered recollection, always-on reminders, and an appropriate proactive-memory baseline. Separate ablations can vary source-count gating, outcome corrections, and preservation of conflicting cases.

Primary outcomes should include event-level trigger precision and recall, presentation before dispatch, task success, harmful or redundant actions, citation resolution, and narrative fidelity against dispatch logs. Additional measures should report stored bytes, occupied nodes, latency including reconsideration, and token usage with an actual tokenizer. Task-level uncertainty should be estimated over independently held-out tasks rather than treating repeated executions of one task as independent task diversity.

This protocol is proposed work. No results from it are claimed in this draft.

## 10. Conclusion

ASH-Network applies ASH's finite local structure to a recursively extensible, source-bearing associative memory. The finite alphabet and global recursive organization are complementary: finite labels make local representation explicit, while variable-depth paths allow the memory structure to expand without preallocating its entire possibility space. Stable identifiers and evidence-supported links separate a memory's identity and relevance from its physical placement.

The subconscious-memory claim is functional and observable. A background subsystem can recognize an unfolding sequence and bring earlier experience into the agent's working context before the agent has asked for that memory and before a pending action has executed. The recorded prototype evidence demonstrates this possibility in small controlled settings, while also exposing limits in semantic application and self-report.

The next scientific question is not whether a memory can be surfaced, but when this particular ASH-based composition improves decisions over matched alternatives. Answering that question requires broader frozen tasks, controlled ablations, and separate scoring of retrieval, delivery, action, and explanation.

## Declarations

**Code and data availability.** Source code and recorded artifacts were inspected through authorized access to `flynn33/ash-network` at the pinned revision above. Repository metadata indicated private visibility at inspection. Public release, licensing, and an archival identifier must be specified by the author(s); this draft does not imply public accessibility. The ASH reference is separately pinned. The local arithmetic-check script and evidence ledger accompany this draft.

**Reproducibility.** Native retrieval and live model results are reported from repository artifacts, not reproduced in this preparation. Historical reader findings are attributed to the inspected report. External host builds and model weights are separate reproduction dependencies. Exact versions, sampling settings, and artifact identity should be reconfirmed against the intended publication snapshot.

**Ethics and privacy.** The inspected experiment descriptions identify synthetic or isolated test material. This does not constitute an ethics-review determination. Any future evaluation using personal conversations or operational traces requires an appropriate consent, minimization, and retention protocol.

**Funding, competing interests, and CRediT contributions.** To be provided by the author(s). No absence of funding or conflicts is assumed.

## References and Source Locations

### ASH and ASH-Network primary materials

All S2–S13 ASH-Network paths refer to commit `eef17dc023732c8897193345d1c3e89f56a3a21f` in `https://github.com/flynn33/ash-network`. Their pinned URLs, access levels, and claim mappings appear in `ASH-Network_Evidence_Ledger.json`.

**[S1]** ASH Model. *Canonical Computational Specification*, specification 1.0.0, reference implementation 1.1.0. `docs/canonical-computational-specification.md`, revision `5b2880d32425f2c84c33a52c5b191c38a66fec55`. Sections 2–6 and 9 are the principal sources used here.

**[S2]** ASH-Network. `docs/geometry.md`. Address contract, deterministic placement, growth rule, and reported geometry measurements.

**[S3]** ASH-Network. `Sources/ASHPrototype/MemoryRecord.swift`. `MemoryRecord`, `ASHRouting.path`, and `ASHRouting.parityVertex`.

**[S4]** ASH-Network. `Sources/ASHPrototype/Geometry.swift`. `CubePath`, `CubeRecord`, and `CubeLayout`; inspected source lines 1–210.

**[S5]** ASH-Network. `Sources/ASHPrototype/AssociativeNetwork.swift`. `LearningState.reinforce`, `LearningState.retract`, `AssociativeNetwork.recall`, and `associationScore`.

**[S6]** ASH-Network. `Sources/ASHPrototype/MemoryPressure.swift`; `docs/memory-pressure.md`. Event validation, motif construction, historical support, current-record checks, and signal construction. Relevant implementation sections inspected, including `Run.pattern`, `MemoryPressureEngine.observe`, `match`, and `independent`.

**[S7]** ASH-Network. `docs/connection-usage.md`. Citation resolution, source-aware changes, negotiated observation channel, and pre-action delivery contract.

**[S8]** ASH-Network. `docs/qualification.md`; `Experiments/qualification/criteria.json`. Experimental design, declared criteria, and reported growth/restart checks.

**[S9]** ASH-Network. `Experiments/qualification/held-out-results.json`. Inspected lines 1–190, including complete mode-summary statistics and initial ranked evidence. Fixture version 2.

**[S10]** ASH-Network. `Experiments/memory-pressure/README.md`; `Experiments/memory-pressure/results.json`. Replay, local timing, scripted behavior, three earlier live pairs, published-build pair, earlier attention wording, and dispatch/narrative discrepancy. Results file inspected across lines 1–620, covering the complete returned content.

**[S11]** ASH-Network. `docs/agent-host.md`. Historical reader and paired cue-provenance reports. The archived response corpus was not independently replayed for this draft.

**[S12]** ASH-Network. `Integrations/association-engine/README.md`. Host-side extraction, decision/outcome lifecycle, automatic integration, and stated boundaries.

**[S13]** ASH-Network. `README.md`. Project scope and overview. The retrieved README blob is `7a949de539c9d2cf6e9718ae446cf5ada2c0f64b`, also identified in the pinned root listing.

### External research

**[L1]** Park, J. S., O'Brien, J. C., Cai, C. J., Morris, M. R., Liang, P., and Bernstein, M. S. (2023). *Generative Agents: Interactive Simulacra of Human Behavior*. arXiv:2304.03442. Abstract inspected; used only for the broad experience–reflection–planning architecture.

**[L2]** Packer, C., Wooders, S., Lin, K., Fang, V., Patil, S. G., Stoica, I., and Gonzalez, J. E. (2023). *MemGPT: Towards LLMs as Operating Systems*. arXiv:2310.08560. Abstract and opening architecture discussion inspected.

**[L3]** Xu, W., Liang, Z., Mei, K., Gao, H., Tan, J., and Zhang, Y. (2025). *A-MEM: Agentic Memory for LLM Agents*. arXiv:2502.12110; NeurIPS 2025. Relevant note-construction and linking sections inspected.

**[L4]** Wu, D., Wang, H., Yu, W., Zhang, Y., Chang, K.-W., and Yu, D. (2025). *LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory*. ICLR 2025; arXiv:2410.10813. Abstract and relevant benchmark/indexing–retrieval–reading discussion inspected.

**[L5]** Wu, Y., Zhang, L., Zhou, Y., Wang, M., Peng, B., Li, S., Fan, X., and Zhao, Z. (2026). *Remember When It Matters: Proactive Memory Agent for Long-Horizon Agents*. arXiv:2607.08716v1. Introduction and intervention-method sections inspected.

**[L6]** Li, J., Fu, Z., Wu, X., Zhang, W., Deng, Y., Guo, K., Li, G., Qi, J., and Zhao, X. (2026). *Proactive Memory for Event-Driven LLM Agents*. arXiv:2610.36967v1. Relevant event, trajectory-validation, and regularity-construction sections inspected.

**[L7]** Bei, Y., Liu, Z., Wei, T., Zhang, W., Zeng, Z., Yu, P. S., Hamann, H., He, J., and Tong, H. (2026). *Prospective Memory for Proactive LLM Agents*. arXiv:2611.05731. Introduction and intention-maintenance/realization sections inspected.

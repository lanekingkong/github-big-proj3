"""BioOmicsBridge Example: End-to-End Alzheimer's Disease Drug Target Discovery"""

# Step 1: Load multi-omics data
from bioomics_bridge import load_multiomics, harmonize, integrate, discover_targets, agent_query

# Load multi-omics data for Alzheimer's disease study
print("Step 1: Loading multi-omics data...")
dataset = load_multiomics(
    genomics="data/alzheimer/genomics.vcf",
    transcriptomics="data/alzheimer/scrna.h5ad",
    proteomics="data/alzheimer/proteomics/",
    metabolomics="data/alzheimer/metabolomics.mzML",
    spatial="data/alzheimer/visium/",
)

print(f"Loaded {dataset.n_omics_types} omics types")
print(dataset.get_summary())

# Step 2: Harmonize data
print("\nStep 2: Harmonizing data...")
harmonized = harmonize(
    dataset,
    method="auto",
    batch_correction=True,
    impute_missing=True,
)
print(f"Harmonized {len(harmonized)} omics types")

# Step 3: Integrate multi-omics data
print("\nStep 3: Integrating multi-omics data...")
integrated = integrate(
    harmonized,
    method="graph",
    n_components=50,
)
print(f"Integration method: {integrated['method']}")
print(f"Number of omics types integrated: {integrated['n_omics_types']}")

# Step 4: Discover drug targets
print("\nStep 4: Discovering drug targets for Alzheimer's disease...")
targets = discover_targets(
    integrated,
    disease="alzheimer",
    min_confidence=0.8,
    top_n=10,
)

if not targets["targets"].empty:
    print(f"\nTop 10 drug targets for Alzheimer's disease:")
    print("-" * 60)
    for _, target in targets["targets"].head(10).iterrows():
        print(f"{target['rank']:3d}. {target['target_name']:20s} "
              f"Score: {target['score']:.3f}  "
              f"Pathway: {target.get('pathway', 'N/A')}")
    print("-" * 60)

# Step 5: Get detailed evidence for top target
print("\nStep 5: Getting detailed evidence...")
result = agent_query(
    f"Explain the evidence for {targets['targets'].iloc[0]['target_name']} "
    f"as an Alzheimer's disease drug target, including literature and clinical evidence"
)
print(result["output"]["summary"])

print("\nAnalysis complete. Results saved to output/directory.")
from cobra.io import read_sbml_model
#Presilia Nisma Sari/10621014

# Load model
model = read_sbml_model("microbacter.xml")

# ====================================
#          Ringkasan Model
# ====================================
print("\n=== RINGKASAN MODEL ===")
print(f"Nama model             : {model.id}")
print(f"Jumlah metabolit       : {len(model.metabolites)}")
print(f"Jumlah reaksi          : {len(model.reactions)}")
print(f"Jumlah gen             : {len(model.genes)}")
print(f"Fungsi objektif        : {model.objective.expression}")
print(f"Kompartemen            : {', '.join(model.compartments)}")

# ====================================
#  Hitung pertumbuhan maksimum/FBA
# ====================================
print("\n=== HASIL SIMULASI FBA ===")
biomassa = model.reactions.get_by_id("Biomass_Mcgr1")
model.objective = biomassa
print(f"Laju perthumbuhan: {model.optimize().objective_value:.4f} 1/h")
print(model.summary())

# ====================================
# Aktifkan jalur biosintesis beta-carotene
# ====================================
print("\n=== OVEREKSPRESI GEN ===")
carotene_pathway_rxns = [
    "IPDPS",
    "DMPPS",
    "GRTT",
    "GGTT",
    "PSY_c",
    "Phyto_desat",
    "PSY_c",
    "Phyto_desat",
    "GCATENEC"
]

for rxn_id in carotene_pathway_rxns:
    if rxn_id in model.reactions:
        model.reactions.get_by_id(rxn_id).lower_bound = 0.001
        print(f"Aktifkan reaksi: {rxn_id}")
    else:
        print(f"Reaksi {rxn_id} ngga ada di model.")

# ====================================
#Tambahkan constraint agar sel tetap tumbuh
# ====================================
print("\n=== MINIMUM BIOMASSA (agar bakteri tetap hidup) ===")
max_growth = model.optimize().objective_value
min_growth = 0.1 * max_growth
biomassa.lower_bound = min_growth
print(f"Biomass minimum constraint set: {min_growth:.4f} 1/h")

# ====================================
# Jadikan produksi beta-carotene sebagai objektif
# ====================================
model.objective = "GCATENEC"
solution = model.optimize()

# ====================================
# hasil
# ====================================
print("\n=== HASIL SIMULASI FBA beta-carotene ===")
print(f"Flux sintesis beta-carotene (GCATENEC): {solution.objective_value:.4f} mmol/gDW/h")
print(f"Laju pertumbuhan: {solution.fluxes[biomassa.id]:.4f} 1/h")
print(f"Persentase pertumbuhan terhadap pertumbuhan maksimum: {(solution.fluxes[biomassa.id] / max_growth * 100):.2f}%")
print(model.summary())

# (Opsional) Tampilkan flux jalur pendukung
print("\nFlux jalur karoten:")
for rxn_id in carotene_pathway_rxns:
    if rxn_id in solution.fluxes:
        print(f"{rxn_id}: {solution.fluxes[rxn_id]:.4f}")
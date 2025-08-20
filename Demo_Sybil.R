#memanggil library sybil, pastikan package sybil dan glpkAPI terinstall(LIAT checklist packge)
library(sybil)
#melihat fungsi yang ada dalam sybil
library(help = "sybil")

setwd("C:/Users/User/Documents/RMBR")
#define data dari sampel dalam sistem sybil
mp <- system.file(package = "sybil", "extdata")
mod <- readTSVmod(prefix = "Ec_core", fpath = mp, quoteChar = "\"")
mod
modelorg2tsv(mod, prefix = "Ec_core")
data("Ec_core")

###KONDISI NUTRISI,ngga perlu data ("Ec_core") lagi udh diatasnya soalnya
#melihat reaksi excange di dat Ec_core
ex <- findExchReact(Ec_core)
ex
#filter yang bisa uptake saja
upt <- uptReact(ex)
ex[upt]

#Chnagebund
mod <- changeBounds(Ec_core, ex[c("EX_glc(e)", "EX_lac_D(e)")], lb = c(0, -10))
findExchReact(mod)

#FBA###################
optL <- optimizeProb(Ec_core, algorithm = "fba", retOptSol = FALSE)
optL

opt <- optimizeProb(Ec_core, algorithm = "fba", retOptSol = TRUE)
lp_obj(opt)
checkOptSol(opt)

help("optsol")

####knockout gene
ko <- optimizeProb(Ec_core, gene = "b2276", lb = 0, ub = 0)
ko

##Multiple konc out
opt <- oneGeneDel(Ec_core)
opt
checkOptSol(opt)
plot(opt, nint = 20)

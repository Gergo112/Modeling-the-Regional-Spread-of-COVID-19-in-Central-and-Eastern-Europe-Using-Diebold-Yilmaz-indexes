# WD, INSTALL, LIBRARY, BEOLVASÁS, ZOO ----------------------------------------
setwd("D:/EGYETEM/VII. Félév/Szakdolgozat")

#install.packages("devtools")
#install.packages("knitr")
#install_github("GabauerDavid/ConnectednessApproach")

library(zoo)
library(devtools)
library(ConnectednessApproach)
library(knitr)
library(vars)

# Beolvasás és átalakítás
DATA = read.csv("DATA.csv")
DATA$date <- as.Date(DATA$date)

zooDATA <- zoo(DATA[,-1], order.by = DATA$date)

lag_select <- VARselect(zooDATA, lag.max = 8, type = "const")
print(lag_select)
#Forecast Prediction Error -> 4 lag






# FULL MODEL WINDOW SIZE (100, 150, 200) # DONE (150) --------------------------------------

window_sizes <- c(100, 150, 200)

for (w in window_sizes) {
  dca_name <- paste0("dcaFULL", w)
  
  assign(dca_name, ConnectednessApproach(
    zooDATA,
    nlag = 8,
    nfore = 4,
    model = "LASSO",
    corrected = FALSE,
    window.size = w,
    connectedness = "Time",
    Connectedness_config = list(
      TimeConnectedness = list(generalized = TRUE)
    )
  ))
}

# TCI kimentése

dca_list <- list(
  "100" = dcaFULL100,
  "150" = dcaFULL150,
  "200" = dcaFULL200
)

tciFULL <- do.call(cbind, lapply(names(dca_list), function(w) {
  tci_series <- as.numeric(dca_list[[w]]$TCI)
  return(tci_series)
}))

colnames(tciFULL) <- paste0("TCI_", names(dca_list))

tciFULL <- data.frame(
  Date = index(dcaFULL100$TCI),
  tciFULL
)

head(tciFULL)

# ÁTLAGOLÁS

avgFULL <- data.frame(
  Date = tciFULL$Date,
  TCI_avg = rowMeans(tciFULL[, c("TCI_100", "TCI_150", "TCI_200")], na.rm = TRUE)
)

head(avgFULL)

# MELYIK A LEGJOBB?

errorsFULL <- sapply(c("TCI_100", "TCI_150", "TCI_200"), function(col) {
  mean(abs(tciFULL[[col]] - avgFULL$TCI_avg), na.rm = TRUE)
})

errorsFULL
bestFULL <- names(which.min(errorsFULL))
cat("FULL LEGJOBB:", bestFULL)

# POLAND MODEL WINDOW SIZE (100, 150, 200) # DONE (200) -----------------------
window_sizes <- c(100, 150, 200)

for (w in window_sizes) {
  dca_name <- paste0("dcaPL", w)
  
  assign(dca_name, ConnectednessApproach(
    zooDATA[, c("PL21", "PL22", "PL41", "PL42", "PL43", "PL51", "PL52", "PL61", 
                "PL62", "PL63", "PL71", "PL72", "PL81", "PL82", "PL84", "PL91", "PL92")],
    nlag = 8,
    nfore = 4,
    model = "LASSO",
    corrected = FALSE,
    window.size = w,
    connectedness = "Time",
    Connectedness_config = list(
      TimeConnectedness = list(generalized = TRUE)
    )
  ))
}

# TCI kimentése

dca_list <- list(
  "100" = dcaPL100,
  "150" = dcaPL150,
  "200" = dcaPL200
)

tciPL <- do.call(cbind, lapply(names(dca_list), function(w) {
  tci_series <- as.numeric(dca_list[[w]]$TCI)
  return(tci_series)
}))

colnames(tciPL) <- paste0("TCI_", names(dca_list))

tciPL <- data.frame(
  Date = index(dcaPL100$TCI),
  tciPL
)

head(tciPL)

# ÁTLAGOLÁS

avgPL <- data.frame(
  Date = tciPL$Date,
  TCI_avg = rowMeans(tciPL[, c("TCI_100", "TCI_150", "TCI_200")], na.rm = TRUE)
)

head(avgPL)

# MELYIK A LEGJOBB?

errorsPL <- sapply(c("TCI_100", "TCI_150", "TCI_200"), function(col) {
  mean(abs(tciPL[[col]] - avgPL$TCI_avg), na.rm = TRUE)
})

errorsPL
bestPL <- names(which.min(errorsPL))
cat("POLAND LEGJOBB:", bestPL)

# HUNGARY + NEIGHBOUR MODEL WINDOW SIZE (100, 150, 200) # DONE (200) ----------
window_sizes <- c(100, 150, 200)

for (w in window_sizes) {
  dca_name <- paste0("dcaHU_NEIGHBOUR", w)
  
  assign(dca_name, ConnectednessApproach(
    zooDATA[, c("HU11", "HU12", "HU21", "HU22", "HU23", "HU31", "HU32", "HU33",
                "AT11", "AT12", "AT13", "AT22", "SK02", "SK03", "SK04")],
    nlag = 8,
    nfore = 4,
    model = "LASSO",
    corrected = FALSE,
    window.size = w,
    connectedness = "Time",
    Connectedness_config = list(
      TimeConnectedness = list(generalized = TRUE)
    )
  ))
}

# TCI kimentése

dca_list <- list(
  "100" = dcaHU_NEIGHBOUR100,
  "150" = dcaHU_NEIGHBOUR150,
  "200" = dcaHU_NEIGHBOUR200
)

tciHU_NEIGHBOUR <- do.call(cbind, lapply(names(dca_list), function(w) {
  tci_series <- as.numeric(dca_list[[w]]$TCI)
  return(tci_series)
}))

colnames(tciHU_NEIGHBOUR) <- paste0("TCI_", names(dca_list))

tciHU_NEIGHBOUR <- data.frame(
  Date = index(dcaHU_NEIGHBOUR100$TCI),
  tciHU_NEIGHBOUR
)

head(tciHU_NEIGHBOUR)

# ÁTLAGOLÁS

avgHU_NEIGHBOUR <- data.frame(
  Date = tciHU_NEIGHBOUR$Date,
  TCI_avg = rowMeans(tciHU_NEIGHBOUR[, c("TCI_100", "TCI_150", "TCI_200")], na.rm = TRUE)
)

head(avgHU_NEIGHBOUR)

# MELYIK A LEGJOBB?

errorsHU_NEIGHBOUR <- sapply(c("TCI_100", "TCI_150", "TCI_200"), function(col) {
  mean(abs(tciHU_NEIGHBOUR[[col]] - avgHU_NEIGHBOUR$TCI_avg), na.rm = TRUE)
})

errorsHU_NEIGHBOUR
bestHU_NEIGHBOUR <- names(which.min(errorsHU_NEIGHBOUR))
cat("HUNGARY + NEIGHBOUR LEGJOBB:", bestHU_NEIGHBOUR)

 
# HUNGARY MODEL WINDOW SIZE (100, 150, 200) # DONE (200) ----------------------

window_sizes <- c(100, 150, 200)

for (w in window_sizes) {
  dca_name <- paste0("dcaHU", w)
  
  assign(dca_name, ConnectednessApproach(
    zooDATA[, c("HU11", "HU12", "HU21", "HU22", "HU23", "HU31", "HU32", "HU33")],
    nlag = 8,
    nfore = 4,
    model = "LASSO",
    corrected = FALSE,
    window.size = w,
    connectedness = "Time",
    Connectedness_config = list(
      TimeConnectedness = list(generalized = TRUE)
    )
  ))
}

# TCI kimentése

dca_list <- list(
  "100" = dcaHU100,
  "150" = dcaHU150,
  "200" = dcaHU200
)

tciHU <- do.call(cbind, lapply(names(dca_list), function(w) {
  tci_series <- as.numeric(dca_list[[w]]$TCI)
  return(tci_series)
}))

colnames(tciHU) <- paste0("TCI_", names(dca_list))

tciHU <- data.frame(
  Date = index(dcaHU100$TCI),
  tciHU
)

head(tciHU)

# ÁTLAGOLÁS

avgHU <- data.frame(
  Date = tciHU$Date,
  TCI_avg = rowMeans(tciHU[, c("TCI_100", "TCI_150", "TCI_200")], na.rm = TRUE)
)

head(avgHU)

# MELYIK A LEGJOBB?

errorsHU <- sapply(c("TCI_100", "TCI_150", "TCI_200"), function(col) {
  mean(abs(tciHU[[col]] - avgHU$TCI_avg), na.rm = TRUE)
})

errorsHU
bestHU <- names(which.min(errorsHU))
cat("HUNGARY LEGJOBB:", bestHU)



# DCA LOAD/SAVE  -----------------------------------------------------

# save(dcaHU100, dcaHU150, dcaHU200, 
     # dcaHU_NEIGHBOUR100, dcaHU_NEIGHBOUR150, dcaHU_NEIGHBOUR200,
     # dcaPL100, dcaPL150, dcaPL200,
     # dcaFULL100, dcaFULL150, dcaFULL200, 
     # file = "szakdoga_dca.RData")

load("szakdoga_dca.RData")
# rm()


# DIAGRAMOK -------------------------------------------------------------------

# KABLE
kable(dcaHU200$TABLE)
kable(dcaHU_NEIGHBOUR200$TABLE)
kable(dcaPL200$TABLE)
kable(dcaFULL150$TABLE)

# TCI
PlotTCI(dcaHU200, ylim=c(30,100))
PlotTCI(dcaHU_NEIGHBOUR200, ylim=c(40,100))
PlotTCI(dcaPL200, ylim=c(0,100))
PlotTCI(dcaFULL150, ylim=c(0,100))

PlotTCI(dcaFULL150, ylim=c(70,100))

dcaFULL150$TCI

#WHO dataforrást megnézni, miért esik be

# TO
PlotTO(dcaHU200, ylim=c(0,100))
PlotTO(dcaHU_NEIGHBOUR200, ylim=c(0,100))
PlotTO(dcaPL200, ylim=c(0,100))

# FROM
PlotFROM(dcaHU200, ylim=c(0,100))
PlotFROM(dcaHU_NEIGHBOUR200, ylim=c(0,100))
PlotFROM(dcaPL200, ylim=c(0,100))

# NET
PlotNET(dcaHU200, ylim=c(-100,100))
PlotNET(dcaHU_NEIGHBOUR200, ylim=c(-100,100))
PlotNET(dcaPL200, ylim=c(-100,100))

# NPDC
PlotNetwork(dcaHU200, method="NPDC")
PlotNetwork(dcaHU_NEIGHBOUR200, method="NPDC", threshold = 0.2)
PlotNetwork(dcaPL200, method="NPDC", threshold = 0.5)
PlotNetwork(dcaFULL150, method="NPDC", threshold = 0.3)


# NPDC kimenteni elsõ hullám, nyári szünet, második, harmadik, nyári szünet 1-1 reprezentatív napra és hasonlóan kirajzolni
# igraf csomag
# tci plotokat 1 ábrán



# HUNGARY

#HU ELSÕ HULLÁM DECEMBER 1

dates_npdc <- as.Date(dimnames(dcaHU200$NPDC)[[3]])
from <- as.Date("2020-12-01")
to   <- as.Date("2020-12-02")
keep_npdc <- dates_npdc >= from & dates_npdc <= to
NPDC_filtered <- dcaHU200$NPDC[, , keep_npdc]
dcaHU200_filtered <- dcaHU200
dcaHU200_filtered$NPDC <- NPDC_filtered
PlotNetwork(dcaHU200_filtered, method="NPDC")

#HU ELSÕ HULLÁM NOVEMBER - JANUÁR

dates_npdc <- as.Date(dimnames(dcaHU200$NPDC)[[3]])
from <- as.Date("2020-11-01")
to   <- as.Date("2021-01-01")
keep_npdc <- dates_npdc >= from & dates_npdc <= to
NPDC_filtered <- dcaHU200$NPDC[, , keep_npdc]
dcaHU200_filtered <- dcaHU200
dcaHU200_filtered$NPDC <- NPDC_filtered
PlotNetwork(dcaHU200_filtered, method="NPDC")

#HU MÁSODIK HULLÁM ÁPRILIS 1

dates_npdc <- as.Date(dimnames(dcaHU200$NPDC)[[3]])
from <- as.Date("2021-04-01")
to   <- as.Date("2021-04-02")
keep_npdc <- dates_npdc >= from & dates_npdc <= to
NPDC_filtered <- dcaHU200$NPDC[, , keep_npdc]
dcaHU200_filtered <- dcaHU200
dcaHU200_filtered$NPDC <- NPDC_filtered
PlotNetwork(dcaHU200_filtered, method="NPDC")

#HU MÁSODIK HULLÁM MÁRCIUS - MÁJUS

dates_npdc <- as.Date(dimnames(dcaHU200$NPDC)[[3]])
from <- as.Date("2021-03-01")
to   <- as.Date("2021-05-01")
keep_npdc <- dates_npdc >= from & dates_npdc <= to
NPDC_filtered <- dcaHU200$NPDC[, , keep_npdc]
dcaHU200_filtered <- dcaHU200
dcaHU200_filtered$NPDC <- NPDC_filtered
PlotNetwork(dcaHU200_filtered, method="NPDC")

#HU NYÁRI SZÜNET AUGUSZTUS 1

dates_npdc <- as.Date(dimnames(dcaHU200$NPDC)[[3]])
from <- as.Date("2021-08-01")
to   <- as.Date("2021-08-02")
keep_npdc <- dates_npdc >= from & dates_npdc <= to
NPDC_filtered <- dcaHU200$NPDC[, , keep_npdc]
dcaHU200_filtered <- dcaHU200
dcaHU200_filtered$NPDC <- NPDC_filtered
PlotNetwork(dcaHU200_filtered, method="NPDC")

#HU NYÁRI SZÜNET JÚNIUS - SZEPTEMBER

dates_npdc <- as.Date(dimnames(dcaHU200$NPDC)[[3]])
from <- as.Date("2021-06-01")
to   <- as.Date("2021-09-01")
keep_npdc <- dates_npdc >= from & dates_npdc <= to
NPDC_filtered <- dcaHU200$NPDC[, , keep_npdc]
dcaHU200_filtered <- dcaHU200
dcaHU200_filtered$NPDC <- NPDC_filtered
PlotNetwork(dcaHU200_filtered, method="NPDC")

#HU HARMADIK HULLÁM DECEMBER 1

dates_npdc <- as.Date(dimnames(dcaHU200$NPDC)[[3]])
from <- as.Date("2021-12-01")
to   <- as.Date("2021-12-02")
keep_npdc <- dates_npdc >= from & dates_npdc <= to
NPDC_filtered <- dcaHU200$NPDC[, , keep_npdc]
dcaHU200_filtered <- dcaHU200
dcaHU200_filtered$NPDC <- NPDC_filtered
PlotNetwork(dcaHU200_filtered, method="NPDC")

#HU HARMADIK HULLÁM NOVEMBER - JANUÁR

dates_npdc <- as.Date(dimnames(dcaHU200$NPDC)[[3]])
from <- as.Date("2021-11-01")
to   <- as.Date("2022-01-01")
keep_npdc <- dates_npdc >= from & dates_npdc <= to
NPDC_filtered <- dcaHU200$NPDC[, , keep_npdc]
dcaHU200_filtered <- dcaHU200
dcaHU200_filtered$NPDC <- NPDC_filtered
PlotNetwork(dcaHU200_filtered, method="NPDC")



# POLAND

#PL ELSÕ HULLÁM DECEMBER 1
dates_npdc <- as.Date(dimnames(dcaPL200$NPDC)[[3]])
from <- as.Date("2020-12-01")
to   <- as.Date("2020-12-02")
keep_npdc <- dates_npdc >= from & dates_npdc <= to
NPDC_filtered <- dcaPL200$NPDC[, , keep_npdc]
dcaPL200_filtered <- dcaPL200
dcaPL200_filtered$NPDC <- NPDC_filtered
PlotNetwork(dcaPL200_filtered, method="NPDC", threshold = 0.5)

#PL ELSÕ HULLÁM NOVEMBER - JANUÁR
dates_npdc <- as.Date(dimnames(dcaPL200$NPDC)[[3]])
from <- as.Date("2020-11-01")
to   <- as.Date("2021-01-01")
keep_npdc <- dates_npdc >= from & dates_npdc <= to
NPDC_filtered <- dcaPL200$NPDC[, , keep_npdc]
dcaPL200_filtered <- dcaPL200
dcaPL200_filtered$NPDC <- NPDC_filtered
PlotNetwork(dcaPL200_filtered, method="NPDC", threshold = 0.5)

#PL MÁSODIK HULLÁM ÁPRILIS 1
dates_npdc <- as.Date(dimnames(dcaPL200$NPDC)[[3]])
from <- as.Date("2021-04-01")
to   <- as.Date("2021-04-02")
keep_npdc <- dates_npdc >= from & dates_npdc <= to
NPDC_filtered <- dcaPL200$NPDC[, , keep_npdc]
dcaPL200_filtered <- dcaPL200
dcaPL200_filtered$NPDC <- NPDC_filtered
PlotNetwork(dcaPL200_filtered, method="NPDC", threshold = 0.5)

#PL MÁSODIK HULLÁM MÁRCIUS - MÁJUS
dates_npdc <- as.Date(dimnames(dcaPL200$NPDC)[[3]])
from <- as.Date("2021-03-01")
to   <- as.Date("2021-05-01")
keep_npdc <- dates_npdc >= from & dates_npdc <= to
NPDC_filtered <- dcaPL200$NPDC[, , keep_npdc]
dcaPL200_filtered <- dcaPL200
dcaPL200_filtered$NPDC <- NPDC_filtered
PlotNetwork(dcaPL200_filtered, method="NPDC", threshold = 0.5)

#PL NYÁRI SZÜNET AUGUSZTUS 1
dates_npdc <- as.Date(dimnames(dcaPL200$NPDC)[[3]])
from <- as.Date("2021-08-01")
to   <- as.Date("2021-08-02")
keep_npdc <- dates_npdc >= from & dates_npdc <= to
NPDC_filtered <- dcaPL200$NPDC[, , keep_npdc]
dcaPL200_filtered <- dcaPL200
dcaPL200_filtered$NPDC <- NPDC_filtered
PlotNetwork(dcaPL200_filtered, method="NPDC", threshold = 0.5)

#PL NYÁRI SZÜNET JÚNIUS - SZEPTEMBER
dates_npdc <- as.Date(dimnames(dcaPL200$NPDC)[[3]])
from <- as.Date("2021-06-01")
to   <- as.Date("2021-09-01")
keep_npdc <- dates_npdc >= from & dates_npdc <= to
NPDC_filtered <- dcaPL200$NPDC[, , keep_npdc]
dcaPL200_filtered <- dcaPL200
dcaPL200_filtered$NPDC <- NPDC_filtered
PlotNetwork(dcaPL200_filtered, method="NPDC", threshold = 0.5)

#PL HARMADIK HULLÁM DECEMBER 1
dates_npdc <- as.Date(dimnames(dcaPL200$NPDC)[[3]])
from <- as.Date("2021-12-01")
to   <- as.Date("2021-12-02")
keep_npdc <- dates_npdc >= from & dates_npdc <= to
NPDC_filtered <- dcaPL200$NPDC[, , keep_npdc]
dcaPL200_filtered <- dcaPL200
dcaPL200_filtered$NPDC <- NPDC_filtered
PlotNetwork(dcaPL200_filtered, method="NPDC", threshold = 0.5)

#PL HARMADIK HULLÁM NOVEMBER - JANUÁR
dates_npdc <- as.Date(dimnames(dcaPL200$NPDC)[[3]])
from <- as.Date("2021-11-01")
to   <- as.Date("2022-01-01")
keep_npdc <- dates_npdc >= from & dates_npdc <= to
NPDC_filtered <- dcaPL200$NPDC[, , keep_npdc]
dcaPL200_filtered <- dcaPL200
dcaPL200_filtered$NPDC <- NPDC_filtered
PlotNetwork(dcaPL200_filtered, method="NPDC", threshold = 0.5)



# HUNGARY + NEIGHBOUR

#HU NEIGHBOUR ELSÕ HULLÁM DECEMBER 1
dates_npdc <- as.Date(dimnames(dcaHU_NEIGHBOUR200$NPDC)[[3]])
from <- as.Date("2020-12-01")
to   <- as.Date("2020-12-02")
keep_npdc <- dates_npdc >= from & dates_npdc <= to
NPDC_filtered <- dcaHU_NEIGHBOUR200$NPDC[, , keep_npdc]
dcaHU_NEIGHBOUR200_filtered <- dcaHU_NEIGHBOUR200
dcaHU_NEIGHBOUR200_filtered$NPDC <- NPDC_filtered
PlotNetwork(dcaHU_NEIGHBOUR200_filtered, method="NPDC", threshold = 0.2)

#HU NEIGHBOUR ELSÕ HULLÁM NOVEMBER - JANUÁR
dates_npdc <- as.Date(dimnames(dcaHU_NEIGHBOUR200$NPDC)[[3]])
from <- as.Date("2020-11-01")
to   <- as.Date("2021-01-01")
keep_npdc <- dates_npdc >= from & dates_npdc <= to
NPDC_filtered <- dcaHU_NEIGHBOUR200$NPDC[, , keep_npdc]
dcaHU_NEIGHBOUR200_filtered <- dcaHU_NEIGHBOUR200
dcaHU_NEIGHBOUR200_filtered$NPDC <- NPDC_filtered
PlotNetwork(dcaHU_NEIGHBOUR200_filtered, method="NPDC", threshold = 0.2)

#HU NEIGHBOUR MÁSODIK HULLÁM ÁPRILIS 1
dates_npdc <- as.Date(dimnames(dcaHU_NEIGHBOUR200$NPDC)[[3]])
from <- as.Date("2021-04-01")
to   <- as.Date("2021-04-02")
keep_npdc <- dates_npdc >= from & dates_npdc <= to
NPDC_filtered <- dcaHU_NEIGHBOUR200$NPDC[, , keep_npdc]
dcaHU_NEIGHBOUR200_filtered <- dcaHU_NEIGHBOUR200
dcaHU_NEIGHBOUR200_filtered$NPDC <- NPDC_filtered
PlotNetwork(dcaHU_NEIGHBOUR200_filtered, method="NPDC", threshold = 0.2)

#HU NEIGHBOUR MÁSODIK HULLÁM MÁRCIUS - MÁJUS
dates_npdc <- as.Date(dimnames(dcaHU_NEIGHBOUR200$NPDC)[[3]])
from <- as.Date("2021-03-01")
to   <- as.Date("2021-05-01")
keep_npdc <- dates_npdc >= from & dates_npdc <= to
NPDC_filtered <- dcaHU_NEIGHBOUR200$NPDC[, , keep_npdc]
dcaHU_NEIGHBOUR200_filtered <- dcaHU_NEIGHBOUR200
dcaHU_NEIGHBOUR200_filtered$NPDC <- NPDC_filtered
PlotNetwork(dcaHU_NEIGHBOUR200_filtered, method="NPDC", threshold = 0.2)

#HU NEIGHBOUR NYÁRI SZÜNET AUGUSZTUS 1
dates_npdc <- as.Date(dimnames(dcaHU_NEIGHBOUR200$NPDC)[[3]])
from <- as.Date("2021-08-01")
to   <- as.Date("2021-08-02")
keep_npdc <- dates_npdc >= from & dates_npdc <= to
NPDC_filtered <- dcaHU_NEIGHBOUR200$NPDC[, , keep_npdc]
dcaHU_NEIGHBOUR200_filtered <- dcaHU_NEIGHBOUR200
dcaHU_NEIGHBOUR200_filtered$NPDC <- NPDC_filtered
PlotNetwork(dcaHU_NEIGHBOUR200_filtered, method="NPDC", threshold = 0.2)

#HU NEIGHBOUR NYÁRI SZÜNET JÚNIUS - SZEPTEMBER
dates_npdc <- as.Date(dimnames(dcaHU_NEIGHBOUR200$NPDC)[[3]])
from <- as.Date("2021-06-01")
to   <- as.Date("2021-09-01")
keep_npdc <- dates_npdc >= from & dates_npdc <= to
NPDC_filtered <- dcaHU_NEIGHBOUR200$NPDC[, , keep_npdc]
dcaHU_NEIGHBOUR200_filtered <- dcaHU_NEIGHBOUR200
dcaHU_NEIGHBOUR200_filtered$NPDC <- NPDC_filtered
PlotNetwork(dcaHU_NEIGHBOUR200_filtered, method="NPDC", threshold = 0.2)

#HU NEIGHBOUR HARMADIK HULLÁM DECEMBER 1
dates_npdc <- as.Date(dimnames(dcaHU_NEIGHBOUR200$NPDC)[[3]])
from <- as.Date("2021-12-01")
to   <- as.Date("2021-12-02")
keep_npdc <- dates_npdc >= from & dates_npdc <= to
NPDC_filtered <- dcaHU_NEIGHBOUR200$NPDC[, , keep_npdc]
dcaHU_NEIGHBOUR200_filtered <- dcaHU_NEIGHBOUR200
dcaHU_NEIGHBOUR200_filtered$NPDC <- NPDC_filtered
PlotNetwork(dcaHU_NEIGHBOUR200_filtered, method="NPDC", threshold = 0.2)

#HU NEIGHBOUR HARMADIK HULLÁM NOVEMBER - JANUÁR
dates_npdc <- as.Date(dimnames(dcaHU_NEIGHBOUR200$NPDC)[[3]])
from <- as.Date("2021-11-01")
to   <- as.Date("2022-01-01")
keep_npdc <- dates_npdc >= from & dates_npdc <= to
NPDC_filtered <- dcaHU_NEIGHBOUR200$NPDC[, , keep_npdc]
dcaHU_NEIGHBOUR200_filtered <- dcaHU_NEIGHBOUR200
dcaHU_NEIGHBOUR200_filtered$NPDC <- NPDC_filtered
PlotNetwork(dcaHU_NEIGHBOUR200_filtered, method="NPDC", threshold = 0.2)



# FULL

#FULL150 ELSÕ HULLÁM DECEMBER 1
dates_npdc <- as.Date(dimnames(dcaFULL150$NPDC)[[3]])
from <- as.Date("2020-12-01")
to   <- as.Date("2020-12-02")
keep_npdc <- dates_npdc >= from & dates_npdc <= to
NPDC_filtered <- dcaFULL150$NPDC[, , keep_npdc]
dcaFULL150_filtered <- dcaFULL150
dcaFULL150_filtered$NPDC <- NPDC_filtered
PlotNetwork(dcaFULL150_filtered, method="NPDC", threshold = 0.5)

#FULL150 ELSÕ HULLÁM NOVEMBER - JANUÁR
dates_npdc <- as.Date(dimnames(dcaFULL150$NPDC)[[3]])
from <- as.Date("2020-11-01")
to   <- as.Date("2021-01-01")
keep_npdc <- dates_npdc >= from & dates_npdc <= to
NPDC_filtered <- dcaFULL150$NPDC[, , keep_npdc]
dcaFULL150_filtered <- dcaFULL150
dcaFULL150_filtered$NPDC <- NPDC_filtered
PlotNetwork(dcaFULL150_filtered, method="NPDC", threshold = 0.4)

#FULL150 MÁSODIK HULLÁM ÁPRILIS 1
dates_npdc <- as.Date(dimnames(dcaFULL150$NPDC)[[3]])
from <- as.Date("2021-04-01")
to   <- as.Date("2021-04-02")
keep_npdc <- dates_npdc >= from & dates_npdc <= to
NPDC_filtered <- dcaFULL150$NPDC[, , keep_npdc]
dcaFULL150_filtered <- dcaFULL150
dcaFULL150_filtered$NPDC <- NPDC_filtered
PlotNetwork(dcaFULL150_filtered, method="NPDC", threshold = 0.5)

#FULL150 MÁSODIK HULLÁM MÁRCIUS - MÁJUS
dates_npdc <- as.Date(dimnames(dcaFULL150$NPDC)[[3]])
from <- as.Date("2021-03-01")
to   <- as.Date("2021-05-01")
keep_npdc <- dates_npdc >= from & dates_npdc <= to
NPDC_filtered <- dcaFULL150$NPDC[, , keep_npdc]
dcaFULL150_filtered <- dcaFULL150
dcaFULL150_filtered$NPDC <- NPDC_filtered
PlotNetwork(dcaFULL150_filtered, method="NPDC", threshold = 0.4)

#FULL150 NYÁRI SZÜNET AUGUSZTUS 1
dates_npdc <- as.Date(dimnames(dcaFULL150$NPDC)[[3]])
from <- as.Date("2021-08-01")
to   <- as.Date("2021-08-02")
keep_npdc <- dates_npdc >= from & dates_npdc <= to
NPDC_filtered <- dcaFULL150$NPDC[, , keep_npdc]
dcaFULL150_filtered <- dcaFULL150
dcaFULL150_filtered$NPDC <- NPDC_filtered
PlotNetwork(dcaFULL150_filtered, method="NPDC", threshold = 0.5)

#FULL150 NYÁRI SZÜNET JÚNIUS - SZEPTEMBER
dates_npdc <- as.Date(dimnames(dcaFULL150$NPDC)[[3]])
from <- as.Date("2021-06-01")
to   <- as.Date("2021-09-01")
keep_npdc <- dates_npdc >= from & dates_npdc <= to
NPDC_filtered <- dcaFULL150$NPDC[, , keep_npdc]
dcaFULL150_filtered <- dcaFULL150
dcaFULL150_filtered$NPDC <- NPDC_filtered
PlotNetwork(dcaFULL150_filtered, method="NPDC", threshold = 0.4)

#FULL150 HARMADIK HULLÁM DECEMBER 1
dates_npdc <- as.Date(dimnames(dcaFULL150$NPDC)[[3]])
from <- as.Date("2021-12-01")
to   <- as.Date("2021-12-02")
keep_npdc <- dates_npdc >= from & dates_npdc <= to
NPDC_filtered <- dcaFULL150$NPDC[, , keep_npdc]
dcaFULL150_filtered <- dcaFULL150
dcaFULL150_filtered$NPDC <- NPDC_filtered
PlotNetwork(dcaFULL150_filtered, method="NPDC", threshold = 0.4)

#FULL150 HARMADIK HULLÁM NOVEMBER - JANUÁR
dates_npdc <- as.Date(dimnames(dcaFULL150$NPDC)[[3]])
from <- as.Date("2021-11-01")
to   <- as.Date("2022-01-01")
keep_npdc <- dates_npdc >= from & dates_npdc <= to
NPDC_filtered <- dcaFULL150$NPDC[, , keep_npdc]
dcaFULL150_filtered <- dcaFULL150
dcaFULL150_filtered$NPDC <- NPDC_filtered
PlotNetwork(dcaFULL150_filtered, method="NPDC", threshold = 0.4)



# PCI
PlotNetwork(dcaHU200, method="PCI")
PlotNetwork(dcaHU_NEIGHBOUR200, method="PCI")
PlotNetwork(dcaPL200, method="PCI")

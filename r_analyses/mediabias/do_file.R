
# do file
# media bias
# Anne Kroon, December 2017

library(fBasics)
library(plyr)
library(dplyr)
library(tidyr)
library(xlsx)
library(xtable)

# IMPORT DATA
#----------------------------------------------------------------------
# READING DATA

df <- read.csv("scores_tel.csv", skip=1, stringsAsFactors = FALSE, header = FALSE)
colnames(df) <- c('att','tar','score')

# from long to wide
data_wide <- spread(df,tar,score)

#summing categories. 
data_wide$m_marok = data_wide$marokkaan + data_wide$marokkanen
data_wide$m_neder = data_wide$nederlander + data_wide$nederlanders
data_wide$m_alloch = data_wide$allochtonen + data_wide$allochtoon
data_wide$m_antil = data_wide$antilliaan + data_wide$antillianen
data_wide$m_arabier = data_wide$arabier + data_wide$arabieren
data_wide$m_burger = data_wide$burger + data_wide$burgers
data_wide$m_westers = data_wide$westers 
data_wide$m_moslim = data_wide$moslim + data_wide$moslims
data_wide$m_irak = data_wide$irakees + data_wide$irakezen
data_wide$m_surinam = data_wide$surinamer + data_wide$surinamers
data_wide$m_afghaan = data_wide$afghanen + data_wide$afgaan
data_wide$m_expat = data_wide$expat + data_wide$expats
data_wide$m_immigrant = data_wide$immigrant + data_wide$immigranten
data_wide$m_migrant = data_wide$migrant + data_wide$migranten
data_wide$m_somalier = data_wide$somalier + data_wide$somaliers
data_wide$m_syrier = data_wide$syrier + data_wide$syriers

agg <- data.frame(data_wide$m_marok, 
                  data_wide$m_neder, 
                  data_wide$m_alloch, 
                  data_wide$m_antil, 
                  data_wide$m_arabier,
                  data_wide$m_burger, 
                  data_wide$m_westers, 
                  data_wide$m_moslim,
                  data_wide$m_irak,
                  data_wide$m_surinam, 
                  data_wide$m_afghaan,
                  data_wide$m_expat, 
                  data_wide$m_immigrant,
                  data_wide$m_migrant, 
                  data_wide$m_somalier, 
                  data_wide$m_syrier)
colnames(agg) <- c('marok', 'neder','alloch', 'antil', 'arabier', 'burger','westers','moslim', 'irak', 'surinam', 
                   'afghaan','expat', 'immigrant', 'migrant', 'somalier', 'syrier')

#summary first results
t <- xtable(basicStats(agg)[c("Mean", "Stdev",  "Minimum", "Maximum"),])
#-------------

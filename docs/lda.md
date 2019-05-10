---
title: "lda_binder_r"
output: 
  md_document:
    variant: markdown_github
---

```{r setup, include=FALSE}
knitr::opts_chunk$set(echo = TRUE)
```

```{r}
library(phyloseq)
library('topicmodels')
library('reshape2')
library('dplyr')
library('bbmle')
library('ggplot2')
library('tidytext')
library('data.table')


install.packages('topicmodels', dependencies=TRUE, repos='http://cran.rstudio.com/')

install.packages("topicmodels")
```

```{r}

otu_table<-read.csv("count_table.csv", sep=",",row.names=1)
otu_table<-as.matrix(otu_table)
otu_table
taxa<-read.csv("taxa_function.csv", sep=",",row.names=1)
otu<-otu_table(otu_table, taxa_are_rows=TRUE)
taxa<-as.matrix(taxa)
tax<-tax_table(taxa)
physeq<-merge_phyloseq(tax,otu)
otu_table(physeq)
rank_names(physeq)
melt<-psmelt(physeq)
write.csv(melt, "melt.csv")
```

```{r}

#load genus level microbiom data
ptarmiganGenus <- read.csv("melt.csv") # genus level resolution of microbiome
head(ptarmiganGenus)

#convert from long to wide format
ptarmiganGenus2 <- dcast(ptarmiganGenus, Sample~Genus, value.var="Abundance")
#query Stephanie on sample id's
unique(ptarmiganGenus2$Sample)

#IMPORTANT TO CLIP RECORDS TO EXCLUDE NON-MICROBE GENETIC INFORMATION
##format data
ptarmiganGenus3 <- ptarmiganGenus2[,-1] #drop sample id

rownames(ptarmiganGenus3) <- ptarmiganGenus2[,1]

#drop rows/sites that sum to zero = no fish recorded
ptarmiganGenus3$sum <- rowSums(ptarmiganGenus3)
ptarmiganGenus3 <- ptarmiganGenus3 %>%
  filter(sum>0) %>%
  select(-c(sum))

VEM2=LDA(ptarmiganGenus3,k=2,control=list(seed=240444)) #fit model with 2 communities


library(ggplot2)
plot_beta(VEM2,prob=0.01)
plot_gamma(VEM2,lls)


VEM3=LDA(ptarmiganGenus3,k=3,control=list(seed=240444)) #fit model with 3 communities
VEM4=LDA(ptarmiganGenus3,k=4,control=list(seed=240444)) #fit model with 4 communities
VEM5=LDA(ptarmiganGenus3,k=5,control=list(seed=240444)) #fit model with 5 communities
VEM6=LDA(ptarmiganGenus3,k=6,control=list(seed=240444)) #fit model with 6 communities
VEM7=LDA(ptarmiganGenus3,k=7,control=list(seed=240444)) #fit model with 6 communities

# model selection for the optimal # communities identified
AICtab(VEM3,VEM2,VEM4,VEM5,VEM6,VEM7)
# 5 communities results in the best model fit

#get parameter estimates
z=posterior(VEM2)
z$topics
commun.plot= as.data.frame(z$topics) #community proportions in each sample bird
str(commun.plot)
commun.plot
commun.plot$Samples <-ptarmiganGenus2$Sample
commun.plot$Samples

commun.spp=z$terms #probability of a species belonging to a community
commun.spp
# look at the specific assignment of species to a community
ap_lda_td <- data.table(tidy(VEM2))
ap_lda_td
nrow(ap_lda_td[topic==2])
ap_lda_td

ap_top_terms <- ap_lda_td %>%
  group_by(topic) %>%
  top_n(10, beta) %>%
  ungroup() %>%
  arrange(topic, -beta)
ap_top_terms

ap_top_terms %>%
  mutate(term = reorder(term, beta)) %>%
  ggplot(aes(term, beta, fill = factor(topic))) +
  geom_bar(stat = "identity", show.legend = FALSE) +
  facet_wrap(~ topic, scales = "free") +
  coord_flip() 

library(ggplot2)
plot_beta(beta,prob=0.01)

```
```{r}
install.packages("topicmodels")
```
```{r}
library(slam)
library(topicmodels)
dtm=as.simple_triplet_matrix(data.final)
seed_num=2014
fold_num=5
kv_num = c(2:30)
sp=smp(cross=fold_num,n=nrow(dtm),seed=seed_num)
control = list(seed = seed_num, burnin = 1000,thin = 100, iter = 1000)
#not run: system.time((ctmK=selectK(dtm=dtm,kv=kv_num,SEED=seed_num,cross=fold_num,sp=sp,method='Gibbs',control=control)))
#not run: plot_perplexity(ctmK,kv_num)
```


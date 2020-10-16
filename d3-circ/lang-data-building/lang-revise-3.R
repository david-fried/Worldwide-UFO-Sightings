library(tidyverse)
library(ggmap)
library(stringr)
library(treemap)
library(tidytext)
df <- read.csv('C:/Users/Ren.DESKTOP-IJNN7GO/Desktop/D3/data/scrubbed.csv', stringsAsFactors = FALSE)

#delete any cities with punctuation. focus on US
focus <- which(str_detect(df$city, '[[:punct:]]'))

df <- df[-focus,]

df %>%
  count(city, state, shape)%>%
  arrange(desc(n))%>%
  head()

aggregate <- df %>%
  unnest_tokens(word, comments, token='ngrams', n=2)%>%
  anti_join(stop_words)%>%
  count(word, sort=TRUE)

#solve problem of bigrams (two adjacent words) with stop words
bigrams_separated <- aggregate %>%
  separate(word, c("word1", "word2"), sep = " ")

#keep only alphabetical words and longer than 2 letters
bigrams_filtered <- bigrams_separated %>%
  filter(!word1 %in% stop_words$word) %>%
  filter(!word2 %in% stop_words$word)%>%
  filter(str_detect(word1, '[[:alpha:]]'))%>%
  filter(str_detect(word2, '[[:alpha:]]'))%>%
  filter(nchar(word1) > 2)%>%
  filter(nchar(word2) > 2)%>%
  filter(word1 != 'ufo')%>%
  filter(word2 != 'ufo')

fireball <- bigrams_filtered %>%
  filter(word2 == 'fireball' | word2 == 'fireballs')%>%
  unite('bigram', -n, sep=' ')

fireball["parent"] <- "fireball" 

fireballs <- fireball %>% 
  rename(
    child = bigram,
    value = n
  )

triangle <- bigrams_filtered %>%
  filter(word2 == 'triangle' | word2 == 'triangles')%>%
  unite('bigram', -n, sep=' ')

triangle["parent"] <- "triangle" 

triangles <- triangle %>% 
  rename(
    child = bigram,
    value = n
  )

lightform <- bigrams_filtered %>%
  filter(word2 == 'light' | word2 == 'lights')%>%
  unite('bigram', -n, sep=' ')

lightform["parent"] <- "lightform" 

lightforms <- lightform %>% 
  rename(
    child = bigram,
    value = n
  )

circle <- bigrams_filtered %>%
  filter(word2 == 'circle' | word2 == 'sphere')%>%
  unite('bigram', -n, sep=' ')

circle["parent"] <- "circle" 

circles <- circle %>% 
  rename(
    child = bigram,
    value = n
  )

disk <- bigrams_filtered %>%
  filter(word2 == 'disk' | word2 == 'disks')%>%
  unite('bigram', -n, sep=' ')

disk["parent"] <- "disk" 

disks <- disk %>% 
  rename(
    child = bigram,
    value = n
  )

cigar <- bigrams_filtered %>%
  filter(word2 == 'cigar' | word2 == 'cigars')%>%
  unite('bigram', -n, sep=' ')

cigar["parent"] <- "cigar" 

cigars <- cigar %>% 
  rename(
    child = bigram,
    value = n
  )

oval <- bigrams_filtered %>%
  filter(word2 == 'oval' | word2 == 'ovals')%>%
  unite('bigram', -n, sep=' ')

oval["parent"] <- "oval" 

ovals <- oval %>% 
  rename(
    child = bigram,
    value = n
  )

treemap(lightform,
        index="bigram",
        palette = "Blues", 
        vSize="n",
        type="index",
        fontsize.labels = 10,
        title= 'UFO Lightform Words'
)

bind <- rbind(lightform, fireball) 

bind1 <- rbind(lightforms, fireballs)
bind2 <- rbind(bind1, triangles) 
bind3 <- rbind(bind2, circles) 
bind4 <- rbind(bind3, disks) 
bind5 <- rbind(bind4, cigars) 
bind6 <- rbind(bind5, ovals)


print(bind6)
print(ovals)
write.csv(bind,"C:/Users/Ren.DESKTOP-IJNN7GO/Desktop/test/bind.csv", row.names = FALSE)
write.csv(ovals,"C:/Users/Ren.DESKTOP-IJNN7GO/Desktop/test/ovals.csv", row.names = FALSE)
write.csv(bind6,"C:/Users/Ren.DESKTOP-IJNN7GO/Desktop/test/shapes.csv", row.names = FALSE)
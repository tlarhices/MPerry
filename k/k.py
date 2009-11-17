#!/usr/bin/env python
# -*- coding: utf-8 -*-

fichier = open("kanjidic")
cpt=0

hi = {
  'a':u'\u3042', 'i':u'\u3044', 'u':u'\u3046', 'e':u'\u3048', 'o':u'\u304A',
  'ka':u'\u304B', 'ki':u'\u304D', 'ku':u'\u304F', 'ke':u'\u3051', 'ko':u'\u3053',
  'ga':u'\u304C', 'gi':u'\u304E', 'gu':u'\u3050', 'ge':u'\u3052', 'go':u'\u3054',
  'sa':u'\u3055', 'shi':u'\u3057', 'su':u'\u3059', 'se':u'\u305B', 'so':u'\u305D',
  'za':u'\u3056', 'ji':u'\u3058', 'zu':u'\u305A', 'ze':u'\u305C', 'zo':u'\u305E',
  'ta':u'\u305F', 'chi':u'\u3061', 'tsu':u'\u3064', 'te':u'\u3066', 'to':u'\u3068',
  'da':u'\u3060', 'ji':u'\u3062', 'zu':u'\u3065', 'de':u'\u3067', 'do':u'\u3069',
  'na':u'\u306A', 'ni':u'\u306B', 'nu':u'\u306C', 'ne':u'\u306D', 'no':u'\u306E',
  'ha':u'\u306F', 'hi':u'\u3072', 'hu':u'\u3075', 'he':u'\u3078', 'ho':u'\u307B',
  'ba':u'\u3070', 'bi':u'\u3073', 'bu':u'\u3076', 'be':u'\u3079', 'bo':u'\u307C',
  'pa':u'\u3071', 'pi':u'\u3074', 'pu':u'\u3077', 'pe':u'\u307A', 'po':u'\u307D',
  'ma':u'\u307E', 'mi':u'\u307F', 'mu':u'\u3080', 'me':u'\u3081', 'mo':u'\u3082',
  'ya':u'\u3084',                 'yu':u'\u3086',                 'yo':u'\u3088',
  'ra':u'\u3089', 'ri':u'\u308A', 'ru':u'\u308B', 're':u'\u308C', 'ro':u'\u308D',
#                  'wi':u'\u3090',                 'we':u'\u3091',
  'wa':u'\u308F',                                                 'wo':u'\u3092',
  'n':u'\u3093', "zu":u'\u30ba',"er":u'\u30b8'
  }

ka = {
  'a':u'\u30A2', 'i':u'\u30A4', 'u':u'\u30A6', 'e':u'\u30A8', 'o':u'\u30AA',
  'ka':u'\u30AB', 'ki':u'\u30AD', 'ku':u'\u30AF', 'ke':u'\u30B1', 'ko':u'\u30B3',
  'ga':u'\u30AC', 'gi':u'\u30AE', 'gu':u'\u30B0', 'ge':u'\u30B2', 'go':u'\u30B4',
  'sa':u'\u30B5', 'shi':u'\u30B7', 'su':u'\u30B9', 'se':u'\u30BB', 'so':u'\u30BD',
  'za':u'\u30B6', 'ji':u'\u30B8', 'zu':u'\u30BA', 'ze':u'\u30BC', 'zo':u'\u30BE',
  'ta':u'\u30BF', 'ti':u'\u30C1', 'tu':u'\u30C4', 'te':u'\u30C6', 'to':u'\u30C8',
  'da':u'\u30C0', 'di':u'\u30C2', 'du':u'\u30C5', 'de':u'\u30C7', 'do':u'\u30C9',
  'na':u'\u30CA', 'ni':u'\u30CB', 'nu':u'\u30CC', 'ne':u'\u30CD', 'no':u'\u30CE',
  'ha':u'\u30CF', 'hi':u'\u30D2', 'hu':u'\u30D5', 'he':u'\u30D8', 'ho':u'\u30DB',
  'ba':u'\u30D0', 'bi':u'\u30D3', 'bu':u'\u30D6', 'be':u'\u30D9', 'bo':u'\u30DC',
  'pa':u'\u30D1', 'pi':u'\u30D4', 'pu':u'\u30D7', 'pe':u'\u30DA', 'po':u'\u30DD',
  'ma':u'\u30DE', 'mi':u'\u30DF', 'mu':u'\u30E0', 'me':u'\u30E1', 'mo':u'\u30E2',
  'ya':u'\u30E4',                 'yu':u'\u30E6',                 'yo':u'\u30E8',
  'ra':u'\u30E9', 'ri':u'\u30EA', 'ru':u'\u30EB', 're':u'\u30EC', 'ro':u'\u30ED',
#                  'wi':u'\u30F0',                 'we':u'\u30F1',
  'wa':u'\u30EF',                                                 'wo':u'\u30F2',
  'n':u'\u30F3', "zu":u'\u305a', "ji":u'\u3058'
  }
  
  
for ligne in fichier:
  ligne=ligne.decode("euc-jp")
  cpt+=1
  fait=False
  if cpt!=1:
    elements = ligne.split(" ")
    elements.reverse()
    for element in elements:
      if (len(element)==0 or element[0] in ka.values() or element[0] in hi.values()) and not fait:
        for element2 in ligne.split(" "):
          if (len(element2)==0 or (element2[0]=="{" or element2[0]=="T")) and not fait:
            prononciation = ligne.split(" ")[ligne.split(" ").index(element):ligne.split(" ").index(element2)]
            #print ligne.split(" ")[0]
            for pouet in prononciation:
              #print "-", pouet,
              i = 0
              test = pouet[i]
              try:
                  
                while test not in ka.values() and test not in hi.values() :
                  i+=1
                  test = pouet[i]
              except:
                print pouet
                print [pouet,]
              if test in ka.values():
                print "K"
              elif test in hi.values():
                print "H"
              else:
                print "?"
                raw_input()
            fait=True
    #raw_input()
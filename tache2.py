# longueur d'un dictionnaire
print(len(dico))
# Maximum et minimum d'un dictionnaire
max(dico1)
min(dico)
# Somme des valeurs d'un dictionnaire
dico2 = {"nom":1 , "liste":2 , "car": 3}
sum(dico2.values())
somme =0
for val in dico2.values():
    somme += val
print(somme)
                                ### Sets
# créer une liste de valeurs
liste = [1,1,2,2,3,4,4,5,5,7,6,6]
# obtenir l'ensemble des elements de la liste 
set(liste)


# Créer une fonction qui prend en entrée une liste de clés et une liste de valeurs
# qui retourne un dictionnaire avec chaque clé associé à une valeur
def dic1(liste1,liste2):
   return dict(liste,liste2)
   dic={}

   for i in range(len(liste1)):
       dic[liste1[i]]=liste2[i]
   return dic    
liste1 =[1,2,3]    
liste2 =['nom','prenpm','age']

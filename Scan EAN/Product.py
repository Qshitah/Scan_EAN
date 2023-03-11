from pyzbar.pyzbar import decode # Cette bibliothèque utilisée pour scanner le code-barres ou le code qr à partir de l'image
import cv2 
import os

''' Ce projet vous donne accès à la numérisation de votre produit à code-barres. 
    Ensuite, il donnera des informations sur ce produit et la disponibilité pour l'acheter. 
    Si le produit n'est pas enregistré dans le bloc-note, 
    il vous donnera accès pour l'ajouter si vous le souhaitez. 
'''

#Obtenez les données des produits du bloc-notes et enregistrez-les dans le dictionnaire
if os.path.exists("text.txt"):
    Products={}
    with open("text.txt" , "r") as file:
        content=file.read()
        lines=content.splitlines()
        for i in lines:
            infos=i.split(";")
            Products[infos[0]]={"Nom": infos[1],"Prix" : float(infos[2]) , "Quantite" : int(infos[3])}

    cap = cv2.VideoCapture(0)
    used_code = []
    cap.set(3,640) # 3 - Largeur
    cap.set(4,480) #4 - Hauteur
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    barcode = ""
    while barcode == "":
        success,frame = cap.read()
        for code in decode(frame):
            barcode = code.data.decode('utf-8')
        
        cv2.imshow("Scannez le code-barres de votre produit",frame)
        cv2.waitKey(1)
    if barcode in Products:
        print(f"Nom du produit: {Products[barcode]['Nom']}")
        print(f"Prix: {Products[barcode]['Prix']}")
        print(f"Quantité: {Products[barcode]['Quantite']}")

        if Products[barcode]['Quantite'] == 0:
            print("Le produit est en rupture de stock")
        else:
            a= input("Confirmez votre commande en appuyant sur y (n'importe quel bouton annulera votre commande): ").upper()
            if a == 'Y':
                quantity = int(input("Entrez la quantité que vous souhaitez acheter: "))
                with open("text.txt" , "r") as file:
                    data=file.readlines()
                cp = 0
                for i in Products:
                    if i == barcode: break
                    cp+=1
                s = data[cp].split(';')
                while quantity > int(s[3]):
                    print("La quantité en stock n'est pas suffisante")
                    quantity = int(input("Entrez la quantité inférieure au stock: "))
                s[3] = str(int(s[3])-quantity)
                data[cp] = f'{";".join(s)}\n'       
                with open("text.txt" , "w") as file:
                    file.writelines(data)
    else:
        print("Ce produit n'existe pas")
        a = input("Appuyez sur A si vous souhaitez l'ajouter (si vous ne le souhaitez pas, appuyez sur n'importe quel bouton): ").upper()
        if a == 'A':
            with open("text.txt" , "a") as file:
                name = input("Entrez le nom du produit: ")
                price = float(input("Entrez le prix: "))
                quantity = int(input("Entrez la quantité: "))
                file.write(f"{barcode};{name};{price};{quantity}")
                print("Vous l'avez ajouté avec succès")
    
    print("Merci d'utiliser notre système")
else:
    print("Ce fichier n'existe pas")




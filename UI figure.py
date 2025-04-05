import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Variable constante
POLICE_COMMUNE = ("Arial", 12)

# Fenêtre principale
fenetre = tk.Tk()
fenetre.title("Quel figure ?")
fenetre.geometry("500x355")
fenetre.resizable(False, False)

# Onglets
notebook = ttk.Notebook(fenetre)
onglet1 = tk.Frame(notebook)
onglet2 = tk.Frame(notebook)
style = ttk.Style()
style.configure("TNotebook.Tab", font=POLICE_COMMUNE)
notebook.add(onglet1, text="Triangle")
notebook.add(onglet2, text="Quadrilatère")
notebook.pack(expand=True, fill="both")

def filtrer_texte(var, length_max):
    """
    Filtre le texte saisi : conserve uniquement les lettres, les met en majuscules
    et limite la longueur maximale.

    Args:
        var (tk.StringVar): Variable Tkinter contenant le texte à filtrer.
        length_max (int): Nombre maximum de caractères autorisés.

    Returns:
        None
    """
    texte = var.get()
    texte_filtre = "".join(c.upper() for c in texte if c.isalpha())

    if len(texte_filtre) > length_max:
        texte_filtre = texte_filtre[:length_max]

    if texte != texte_filtre:
        var.set(texte_filtre)

# Tableaux
def creer_tableau(parent, nb_lignes):
    """
    Crée un tableau pour saisir les coordonnées et noms des points.

    Args:
        parent (tk.Widget): Le conteneur parent dans lequel placer le tableau.
        nb_lignes (int): Nombre de lignes (points) à saisir.

    Returns:
        dict: Dictionnaire contenant les StringVar des noms, x et y.
    """

    def ajuster_taille(var, entry):
        """
        Filtre les caractères non numériques d'un champ de saisie
        et ajuste dynamiquement la longueur de l'entrée.

        Args:
            var (tk.StringVar): La variable liée à l'entrée (Entry).
            entry (tk.Entry): Le widget Entry à ajuster.
        Returns:
            None
        """
        texte = var.get()
        texte_filtre = "".join(c for c in texte if c.isdigit())

        if texte != texte_filtre:
            var.set(texte_filtre)

        entry.config(width=max(5, len(texte_filtre)))

    tableau = tk.Frame(parent)
    tableau.pack(pady=20)

    for i in range(6):
        tableau.columnconfigure(i, weight=1)

    # En-têtes
    tk.Label(tableau, text="Nom:", anchor="center", font=POLICE_COMMUNE
             ).grid(row=0, column=1, padx=5, pady=5)
    tk.Label(tableau, text="Coordonnées:", anchor="center", font=POLICE_COMMUNE
             ).grid(row=0, column=2, columnspan=5, sticky="we", padx=5, pady=5)

    stockage_vars = {"nom": [], "x": [], "y": []}

    for i in range(1, nb_lignes + 1):
        tk.Label(tableau, text=f"Point {i}:", font=POLICE_COMMUNE
                 ).grid(row=i, column=0, padx=5, pady=5, sticky="e")

        # Nom
        var_nom = tk.StringVar()
        entry_nom = tk.Entry(tableau, width=5, font=POLICE_COMMUNE, textvariable=var_nom)
        entry_nom.config(bg="white", fg="#333333")
        entry_nom.grid(row=i, column=1, padx=5, pady=5)
        stockage_vars["nom"].append(var_nom)
        var_nom.trace("w", lambda *args, v=var_nom, l=1: filtrer_texte(v, l))

        # Coordonnées X
        tk.Label(tableau, text="X:").grid(row=i, column=2, padx=5, pady=5, sticky="e")
        var_x = tk.StringVar()
        entry_x = tk.Entry(tableau, width=5, font=POLICE_COMMUNE, textvariable=var_x)
        entry_x.grid(row=i, column=3, padx=5, pady=5)
        stockage_vars["x"].append(var_x)
        var_x.trace("w", lambda *args, v=var_x, e=entry_x: ajuster_taille(v, e))

        # Coordonnées Y
        tk.Label(tableau, text="Y:").grid(row=i, column=4, padx=5, pady=5, sticky="e")
        var_y = tk.StringVar()
        entry_y = tk.Entry(tableau, width=5, font=POLICE_COMMUNE, textvariable=var_y)
        entry_y.grid(row=i, column=5, padx=5, pady=5)
        stockage_vars["y"].append(var_y)
        var_y.trace("w", lambda *args, v=var_y, e=entry_y: ajuster_taille(v, e))

    return stockage_vars

triangle_stock_vars = creer_tableau(onglet1, 3)
quadri_stock_vars = creer_tableau(onglet2, 4)

# Nom figure
def creer_frame_nom(parent, texte, length_max):
    """
    Crée l'emplacement dédié au nom de la figure.

    Args:
        parent (tk.Widget): Le conteneur parent dans lequel placer le tableau.
        texte (str): Le texte à afficher.
        length_max (int): La longueur max de l'entry.

    Returns:
        var_nf (tk.StringVar): Une variable contenant le nom de la figure
    """
    # Frame
    frame_nom_figure = tk.Frame(parent)
    frame_nom_figure.pack()

    # Labels indicatifs
    tk.Label(frame_nom_figure, text=texte, anchor="center",
              font=POLICE_COMMUNE).grid(row=0, column=0)
    tk.Label(frame_nom_figure, text="(Attention, l'ordre est important)", 
             anchor="center", font=POLICE_COMMUNE).grid(row=1, column=0, columnspan=2)
    
    # Entry
    var_nf = tk.StringVar()
    entry_nf = tk.Entry(frame_nom_figure, textvariable=var_nf,width=5, font=POLICE_COMMUNE)
    entry_nf.grid(row=0, column=1)
    var_nf.trace("w", lambda *args, v=var_nf, l=length_max: filtrer_texte(v, l))

    return var_nf

entry_nom_triangle = creer_frame_nom(onglet1, "Nom du triangle:", 3)
entry_nom_quadrilatere = creer_frame_nom(onglet2, "Nom du quadrilatère:", 4)

# Boutons radio
frame_radio = tk.Frame(fenetre)
frame_radio.pack(side="top", fill="x")
inner_fr = tk.Frame(frame_radio)
inner_fr.pack()
choix = tk.StringVar(value="Rédaction")
tk.Radiobutton(inner_fr, text="Rédiger", variable=choix, value="Rédaction",
               font=POLICE_COMMUNE).pack(side="left", padx=10)
tk.Radiobutton(inner_fr, text="Créer le graphique", variable=choix,
               value="Graphique",font=POLICE_COMMUNE).pack(padx=10)

# Bandeau bas de page
bandeau = tk.Frame(fenetre, bg="lightgray", height=40)
bandeau.pack(side="bottom", fill="x")

def valider():
    """
    Vérifie que les données saisies sont correctes puis lance le programme.

    Args:
        None

    Returns:
        None
    """
    def recup_donnees(stock_vars):
        # Récupère les noms des points
        noms = [var.get() for var in stock_vars["nom"]]

        coords_x = [var.get() for var in stock_vars["x"]]
        coords_y = [var.get() for var in stock_vars["y"]]

        # Remplacer les "" par des 0 et convertir en int
        coords_x = [0 if item == "" else int(item) for item in coords_x]
        coords_y = [0 if item == "" else int(item) for item in coords_y]

        return noms, list(zip(coords_x, coords_y))  # Convertir en liste avant de retourner

    def check_noms(noms, nom_figure):
        # Vérification que chaque nom n'est pas vide
        if any(nom == "" for nom in noms):
            messagebox.showerror("Erreur", "Tous les points doivent avoir un nom !")
            return False

        # Vérification que les noms sont uniques
        if len(noms) != len(set(noms)):
            messagebox.showerror("Erreur", "Tous les noms des points doivent être uniques !")
            return False
        
        # Vérification que le nom de la figure contienne tous les points
        if not all(nom in nom_figure for nom in noms):
            messagebox.showerror("Erreur", "La figure doit être nommée à partir des noms des points !")
            return False
        return True
        
    def check_coordonnees(coords):
        # Vérifier qu'il n'y a pas de points avec les mêmes coordonnées
        points = set(coords)  # Crée un set des coordonnées
        
        if len(points) != len(coords):
            messagebox.showerror("Erreur", "Chaque point doit avoir des coordonnées unique !")
            return False

        return True

    onglet_actif = notebook.index(notebook.select())

    if onglet_actif == 0:  
        nom_figure = entry_nom_triangle.get()
        stock_vars = triangle_stock_vars
    else:
        nom_figure = entry_nom_quadrilatere.get()
        stock_vars = quadri_stock_vars

    noms, coords = recup_donnees(stock_vars)

    if check_noms(noms, nom_figure) and check_coordonnees(coords):
        def start_programme():
            fenetre.destroy()

        return nom_figure, noms, coords

# Boutons alignés à droite
tk.Button(bandeau, text="Quitter", command=fenetre.quit
          ).pack(side="right", padx=10, pady=5)
tk.Button(bandeau, text="Valider", command=valider
          ).pack(side="right", padx=10, pady=5)

fenetre.mainloop()
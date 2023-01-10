class Voiture:
  def __init__(self, marque, modele, A_modele, carburant, fiscale, Kilo, et, B_vitesses, portes, orig, p_main,
               Jantes, airbags, Clim, gps, toit, cuir, radar_recul, camera, v_electrique, abs_, esp, reg_vitesse,
               lim_vitesse, ordinateur_b, cd_media, Verrouillage):
    self.Marque = marque
    self.Modele = modele
    self.Annee_Modele = A_modele
    self.Type_de_carburant = carburant
    self.Puissance_fiscale = fiscale
    self.Kilometrage = Kilo
    self.etat = et
    self.Boite_de_vitesses = B_vitesses
    self.Nombre_de_portes = portes
    self.Origine = orig
    self.Premiere_main = p_main
    self.Jantes_aluminium = Jantes
    self.Airbags = airbags
    self.Climatisation = Clim
    self.Systeme_de_navigation_GPS = gps
    self.Toit_ouvrant = toit
    self.Sieges_cuir = cuir
    self.Radar_de_recul = radar_recul
    self.Camera_de_recul = camera
    self.Vitres_electriques = v_electrique
    self.ABS = abs_
    self.ESP = esp
    self.Regulateur_de_vitesse = reg_vitesse
    self.Limiteur_de_vitesse = lim_vitesse
    self.Ordinateur_de_bord = ordinateur_b
    self.CD_MP3_Bluetooth = cd_media
    self.Verrouillage_centralise_a_distance = Verrouillage


  def __str__(self):
    return f"{self.Marque} {self.Modele}"
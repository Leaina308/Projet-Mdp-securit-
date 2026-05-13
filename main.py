import string
import random
import math
import matplotlib.pyplot as plt
import datetime
# Règle principale du mot de passe
class PasswordPolicy:
    # CORRECTION : min_lenght est devenu min_length partout
    def __init__(self, min_length = 12, require_lower = True, require_upper = True,
                 require_digits = True, require_special = True, validity_period = 90):
        self.min_length = min_length
        self.require_lower = require_lower
        self.require_upper = require_upper
        self.require_digits = require_digits
        self.require_special = require_special
        self.validity_period = validity_period

    def __str__(self):
        return (f"Policy: min_length={self.min_length}, "
                f"require_lower={self.require_lower}, "
                f"require_upper={self.require_upper}, "
                f"require_digits={self.require_digits}, "
                f"require_special={self.require_special}, "
                f"validity_period={self.validity_period}")

# Création de mot de passe correspondant à la règle
def generate_password(policy = None):
    if policy is None:
        policy = PasswordPolicy()
    chars = ""
    if policy.require_lower:
        chars += string.ascii_lowercase
    if policy.require_upper:
        chars += string.ascii_uppercase
    if policy.require_digits:
        chars += string.digits
    if policy.require_special:
        chars += string.punctuation
    if not chars:
        chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(chars) for _ in range(policy.min_length))
    return password

# Évaluation du mot de passe
weak_passwords = ["password", "123456", "qwerty", "abc123", "letmein", "monkey", "dragon", "111111", "baseball", "iloveyou"]

def evaluate_password(password : str, policy: PasswordPolicy, attempts_per_second = 1e9):
    evaluation = {}
    Charset_size = 0
    if any(c.islower() for c in password):
        Charset_size += len(string.ascii_lowercase)
    if any(c.isupper() for c in password):
        Charset_size += len(string.ascii_uppercase)
    if any(c.isdigit() for c in password):
        Charset_size += len(string.digits)
    if any(c in string.punctuation for c in password):
        Charset_size += len(string.punctuation)
        
    entropy = len(password) * math.log2(Charset_size) if Charset_size > 0 else 0
    evaluation["entropy_bits"] = entropy
    evaluation["is_weak"] = password.lower() in weak_passwords
    
    total_combinations = Charset_size ** len(password)
    time_to_crack_seconds = total_combinations / attempts_per_second
    evaluation["time_to_crack_seconds"] = time_to_crack_seconds
    evaluation["time_to_crack_days"] = time_to_crack_seconds / (24 * 3600)
    evaluation["time_to_crack_years"] = time_to_crack_seconds / (365 * 24 * 3600)
    return evaluation

# Projection graphique (Loi de Moore)
def projection_password_resistance(password : str, attempts_per_second = 1e9, years = 20):
    policy = PasswordPolicy()
    evaluation = evaluate_password(password, policy, attempts_per_second)
    base_time = evaluation["time_to_crack_seconds"]
    times = []
    labels = []
    
    for year in range(0, years + 1, 2):
        # Loi de Moore : la puissance de calcul double tous les 2 ans
        factor = 2 ** (year / 2)
        projected_time = base_time / factor
        # Conversion en jours pour l'affichage du graphique
        times.append(projected_time / (24 * 3600))
        labels.append(year)
        
    plt.figure(figsize = (8, 5))
    plt.plot(labels, times, marker='o', color='purple')
    plt.title(f"Projection de la résistance du mot de passe : {password}")
    plt.xlabel("Années dans le futur")
    plt.ylabel("Jours pour craquer")
    plt.grid(True)
    if max(times) > 0:
        plt.ylim(0, max(times) * 1.2)
    plt.show()

# Similarité contextuelle
def check_similarity(password: str, username: str, birthdate: str = None):
    alerts = []

    # 1. Akaiky amin'ny username
    if username.lower() in password.lower():
        alerts.append("⚠️ Mot de passe trop proche du nom d'utilisateur")

    # 2. Akaiky amin'ny daty manokana (ex: birthday)
    if birthdate:
        try:
            date_obj = datetime.datetime.strptime(birthdate, "%Y-%m-%d")
            date_str = date_obj.strftime("%Y%m%d")
            if date_str in password:
                alerts.append("⚠️ Mot de passe contient la date de naissance")
        except ValueError:
            alerts.append("⚠️ Format de date invalide (YYYY-MM-DD attendu)")

    # 3. Tenimiafina manakaiky amin'ny taona ankehitriny
    current_year = str(datetime.datetime.now().year)
    if current_year in password:
        alerts.append("⚠️ Mot de passe contient l'année actuelle")

    return alerts

# INTERFACE GRAPHICS
import tkinter as tk
from tkinter import ttk, messagebox

# --- Modules imports ---
import string, random, math, datetime
import matplotlib.pyplot as plt

# --- Politique ---
class PasswordPolicy:
    def __init__(self, min_length=8, require_upper=True, require_lower=True,
                 require_digits=True, require_special=True, validity_days=90):
        self.min_length = min_length
        self.require_upper = require_upper
        self.require_lower = require_lower
        self.require_digits = require_digits
        self.require_special = require_special
        self.validity_days = validity_days

# --- Générateur ---
def generate_password(policy: PasswordPolicy):
    chars = ""
    if policy.require_upper: chars += string.ascii_uppercase
    if policy.require_lower: chars += string.ascii_lowercase
    if policy.require_digits: chars += string.digits
    if policy.require_special: chars += string.punctuation
    if not chars: chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(policy.min_length))

# --- Évaluateur ---
weak_passwords = ["123456","password","qwerty","admin","letmein","azerty"]

def evaluate_password(password: str, policy: PasswordPolicy, attempts_per_second=1e9):
    charset_size = 0
    if any(c.isupper() for c in password): charset_size += len(string.ascii_uppercase)
    if any(c.islower() for c in password): charset_size += len(string.ascii_lowercase)
    if any(c.isdigit() for c in password): charset_size += len(string.digits)
    if any(c in string.punctuation for c in password): charset_size += len(string.punctuation)
    entropy = len(password)*math.log2(charset_size) if charset_size>0 else 0
    total_combinations = charset_size**len(password)
    time_to_crack = total_combinations/attempts_per_second
    return {
        "entropy_bits": entropy,
        "is_weak": password.lower() in weak_passwords,
        "time_to_crack_days": time_to_crack/(3600*24)
    }

# --- Projection graphique ---
def project_password_resistance(password: str, attempts_per_second=1e9, years=20):
    result = evaluate_password(password, PasswordPolicy(), attempts_per_second)
    base_time = result["time_to_crack_days"]*3600*24
    times, labels = [], []
    current_attempts = attempts_per_second
    for year in range(0, years+1, 2):
        if year>0: current_attempts *= 2
        projected_time = base_time/(current_attempts/attempts_per_second)
        times.append(projected_time/(3600*24))
        labels.append(year)
    plt.plot(labels, times, marker='o')
    plt.title("Projection résistance mot de passe (loi de Moore)")
    plt.xlabel("Années dans le futur")
    plt.ylabel("Temps de cassage (jours)")
    plt.grid(True)
    plt.show()

# --- Similarité contextuelle ---
def check_similarity(password: str, username: str, birthdate: str=None):
    alerts=[]
    if username.lower() in password.lower():
        alerts.append("⚠️ Trop proche du nom d'utilisateur")
    if birthdate:
        try:
            date_obj=datetime.datetime.strptime(birthdate,"%Y-%m-%d")
            date_str=date_obj.strftime("%Y%m%d")
            if date_str in password: alerts.append("⚠️ Contient la date de naissance")
        except: alerts.append("⚠️ Format date invalide")
    current_year=str(datetime.datetime.now().year)
    if current_year in password: alerts.append("⚠️ Contient l'année actuelle")
    return alerts

# --- GUI ---
def main_gui():
    root=tk.Tk()
    root.title("Projet 1 - Générateur & Évaluateur de mots de passe")

    # Politique
    policy=PasswordPolicy()

    # Frame principale
    frame=ttk.Notebook(root)
    frame.pack(fill="both",expand=True)

    # Tab Générateur
    tab_gen=tk.Frame(frame)
    frame.add(tab_gen,text="Générateur")
    gen_label=tk.Label(tab_gen,text="Mot de passe généré:")
    gen_label.pack()
    gen_output=tk.Entry(tab_gen,width=40)
    gen_output.pack()
    def gen_action():
        pwd=generate_password(policy)
        gen_output.delete(0,tk.END)
        gen_output.insert(0,pwd)
    tk.Button(tab_gen,text="Générer",command=gen_action).pack()

    # Tab Évaluateur
    tab_eval=tk.Frame(frame)
    frame.add(tab_eval,text="Évaluateur")
    eval_input=tk.Entry(tab_eval,width=40)
    eval_input.pack()
    eval_result=tk.Label(tab_eval,text="")
    eval_result.pack()
    def eval_action():
        pwd=eval_input.get()
        res=evaluate_password(pwd,policy)
        eval_result.config(text=f"Entropie: {res['entropy_bits']:.2f} bits\n"
                                f"Faible: {res['is_weak']}\n"
                                f"Temps cassage: {res['time_to_crack_days']:.2e} jours")
    tk.Button(tab_eval,text="Évaluer",command=eval_action).pack()

    # Tab Projection
    tab_proj=tk.Frame(frame)
    frame.add(tab_proj,text="Projection")
    proj_input=tk.Entry(tab_proj,width=40)
    proj_input.pack()
    def proj_action():
        pwd=proj_input.get()
        project_password_resistance(pwd)
    tk.Button(tab_proj,text="Projeter",command=proj_action).pack()

    # Tab Similarité
    tab_sim=tk.Frame(frame)
    frame.add(tab_sim,text="Similarité")
    sim_pwd=tk.Entry(tab_sim,width=40)
    sim_pwd.pack()
    sim_user=tk.Entry(tab_sim,width=40)
    sim_user.insert(0,"Nom utilisateur")
    sim_user.pack()
    sim_date=tk.Entry(tab_sim,width=40)
    sim_date.insert(0,"YYYY-MM-DD")
    sim_date.pack()
    sim_result=tk.Label(tab_sim,text="")
    sim_result.pack()
    def sim_action():
        alerts=check_similarity(sim_pwd.get(),sim_user.get(),sim_date.get())
        sim_result.config(text="\n".join(alerts) if alerts else "✅ Aucun problème détecté")
    tk.Button(tab_sim,text="Vérifier",command=sim_action).pack()

    root.mainloop()

if __name__=="__main__":
    main_gui()

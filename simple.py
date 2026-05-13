# import string
# import random
# import math
# import matplotlib.pyplot as plt
# import datetime

# # Règle principale du mot de passe
# class PasswordPolicy:
#     def __init__(self, min_length = 12, require_lower = True, require_upper = True,
#                  require_digits = True, require_special = True, validity_period = 90):
#         self.min_length = min_length
#         self.require_lower = require_lower
#         self.require_upper = require_upper
#         self.require_digits = require_digits
#         self.require_special = require_special
#         self.validity_period = validity_period
#     def __str__(self):
#         return (f"Policy: min_length={self.min_length}, "
#                 f"require_lower={self.require_lower}, "
#                 f"require_upper={self.require_upper}, "
#                 f"require_digits={self.require_digits}, "
#                 f"require_special={self.require_special}, "
#                 f"validity_period={self.validity_period}")
# # Création de mot de passe correspondant à la règle
# def generate_password(policy = None):
#     if policy is None:
#         policy = PasswordPolicy()
#     chars = ""
#     if policy.require_lower:
#         chars += string.ascii_lowercase
#     if policy.require_upper:
#         chars += string.ascii_uppercase
#     if policy.require_digits:
#         chars += string.digits
#     if policy.require_special:
#         chars += string.punctuation
#     if not chars:
#         chars = string.ascii_letters + string.digits + string.punctuation
#     password = ''.join(random.choice(chars) for _ in range(policy.min_length))
#     return password
# # Évaluation du mot de passe
# weak_passwords = ["password", "123456", "qwerty", "abc123", "letmein", "monkey", "dragon", "111111", "baseball", "iloveyou"]
# def evaluate_password(password : str, policy: PasswordPolicy, attempts_per_second = 1e9):
#     evaluation = {}
#     Charset_size = 0
#     if any(c.islower() for c in password):
#         Charset_size += len(string.ascii_lowercase)
#     if any(c.isupper() for c in password):
#         Charset_size += len(string.ascii_uppercase)
#     if any(c.isdigit() for c in password):
#         Charset_size += len(string.digits)
#     if any(c in string.punctuation for c in password):
#         Charset_size += len(string.punctuation)   
#     entropy = len(password) * math.log2(Charset_size) if Charset_size > 0 else 0
#     evaluation["entropy_bits"] = entropy
#     evaluation["is_weak"] = password.lower() in weak_passwords
#     total_combinations = Charset_size ** len(password)
#     time_to_crack_seconds = total_combinations / attempts_per_second
#     evaluation["time_to_crack_seconds"] = time_to_crack_seconds
#     evaluation["time_to_crack_days"] = time_to_crack_seconds / (24 * 3600)
#     evaluation["time_to_crack_years"] = time_to_crack_seconds / (365 * 24 * 3600)
#     return evaluation
# # Projection graphique (Loi de Moore)
# def projection_password_resistance(password : str, attempts_per_second = 1e9, years = 20):
#     policy = PasswordPolicy()
#     evaluation = evaluate_password(password, policy, attempts_per_second)
#     base_time = evaluation["time_to_crack_seconds"]
#     times = []
#     labels = [] 
#     for year in range(0, years + 1, 2):
#         # Loi de Moore : la puissance de calcul double tous les 2 ans
#         factor = 2 ** (year / 2)
#         projected_time = base_time / factor
#         # Conversion en jours pour l'affichage du graphique
#         times.append(projected_time / (24 * 3600))
#         labels.append(year)    
#     plt.figure(figsize = (8, 5))
#     plt.plot(labels, times, marker='o', color='purple')
#     plt.title(f"Projection de la résistance du mot de passe : {password}")
#     plt.xlabel("Années dans le futur")
#     plt.ylabel("Jours pour craquer")
#     plt.grid(True)
#     if max(times) > 0:
#         plt.ylim(0, max(times) * 1.2)
#     plt.show()
# # Similarité contextuelle
# def check_similarity(password: str, username: str, birthdate: str = None):
#     alerts = []
#     if username.lower() in password.lower():
#         alerts.append("⚠️ Mot de passe trop proche du nom d'utilisateur")
#     if birthdate:
#         try:
#             date_obj = datetime.datetime.strptime(birthdate, "%Y-%m-%d")
#             date_str = date_obj.strftime("%Y%m%d")
#             if date_str in password:
#                 alerts.append("⚠️ Mot de passe contient la date de naissance")
#         except ValueError:
#             alerts.append("⚠️ Format de date invalide (YYYY-MM-DD attendu)")
#     current_year = str(datetime.datetime.now().year)
#     if current_year in password:
#         alerts.append("⚠️ Mot de passe contient l'année actuelle")
#     return alerts
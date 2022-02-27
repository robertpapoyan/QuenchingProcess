steels_dict = {
    "ХГС": {
        "maximal_hardness": 70,
        "critical_velo_cel_sec": 300,
        "mart_transform_start_temp": 210,
        "hardness_after_quech": 65,
        "quenching_temp": 840

    },
    "ХВГ": {
        "maximal_hardness": 65,
        "critical_velo_cel_sec": 300,
        "mart_transform_start_temp": 210,
        "hardness_after_quech": 62,
        "quenching_temp": 800
    },

    "У8": {
        "maximal_hardness": 55,
        "critical_velo_cel_sec": 500,
        "mart_transform_start_temp": 300,
        "hardness_after_quech": 60,
        "quenching_temp": 750
    }
}

quenching_env_freeze_velo = {
    "water": {
        "freezing_velo": 600,
        "lower_temp": None,
    },
    "oil": {
        "freezing_velo": 400,
        "lower_temp": None,
    },
    "latex": {
        "freezing_velo": 700,
        "lower_temp": 100,
    }
}


def get_input_data():
    steel_model = input("Ներմուծեք պողպատի մակնիշը: ")
    end_hardness_by_rok = input("Ներմուծեք վերջնական կարծրությունը ըստ ռոկվելի: ")

    return steel_model, end_hardness_by_rok


def get_envs_with_higher_velo(critical_velo_cel_sec):
    envs_with_higher_velo = {}

    for env in quenching_env_freeze_velo:
        if quenching_env_freeze_velo[env]["freezing_velo"] >= critical_velo_cel_sec:
            envs_with_higher_velo[env] = quenching_env_freeze_velo[env].copy()

    return envs_with_higher_velo


def get_min_env_key(envs_with_higher_velo):
    envs_with_higher_velo_list_sorted = sorted(envs_with_higher_velo, key=lambda x: (
        envs_with_higher_velo[x]["lower_temp"] is None, envs_with_higher_velo[x]["lower_temp"]))

    min_env_key = envs_with_higher_velo_list_sorted[0]
    return min_env_key

def calculate_env_time(steel_model, min_temperature, min_env_key):
    quenching_temp = steels_dict[steel_model]["quenching_temp"]
    env_time = (quenching_temp / min_temperature)
    env_time += (quenching_temp / quenching_env_freeze_velo[min_env_key]["freezing_velo"])
    env_time /= 2
    return env_time

def main():
    steel_model, end_hardness_by_rok = get_input_data()
    if steel_model not in steels_dict:
        print("Անհնար է իրականցնել քանի որ տվյալները դեռ բացակայում են")
        return

    # XGS 70

    critical_velo_cel_sec = steels_dict[steel_model]["critical_velo_cel_sec"]

    envs_with_higher_velo = get_envs_with_higher_velo(critical_velo_cel_sec)

    min_env_key = get_min_env_key(envs_with_higher_velo)

    min_temperature = envs_with_higher_velo[min_env_key]["lower_temp"]

    env_time = calculate_env_time(steel_model, min_temperature, min_env_key)

    hardness_after_quench = steels_dict[steel_model]["hardness_after_quech"]

    print("Միջավայր - ", end="")
    for k in envs_with_higher_velo:
        print(k.upper(), end=", ")

    print(f"\nՄիջավայրի ժամանակ: {min_env_key} {env_time} sec")
    print(f"Տեսական կարծրություն: {hardness_after_quench}")
    print(f"Ցանկալի կարծրություն: {end_hardness_by_rok}")


if __name__ == "__main__":
    main()
    pass

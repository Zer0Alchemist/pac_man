import json

class Error_handling(Exception):
    def __init__(self, message):
        self.message = message


def parse_config(file : str) :
    try :

        with open("config.json" , 'r') as f:
            
            lines = f.readlines()

            lines = [line 
                for line in lines if not line.startswith("#")
            ]

            lines = "".join(lines)

            config = json.loads(lines)

            if not isinstance(config, dict):
                raise Error_handling(
                    "The configuration root must be a JSON object"
                )
            
            filename = config["highscore_filename"]
            if not isinstance(filename, str) or not filename.strip():
                raise Error_handling(
                    "'highscore_filename' must be a non-empty string"
                )

            positive_keys = ("lives", "pacgum", "level_max_time")

            for key in positive_keys:
                value = config[key]
                if not isinstance(value, int):
                    raise Error_handling(f"'{key}' must be an integer")
                if value <= 0:
                    raise Error_handling(f"'{key}' must be positive")

            score_keys = (
                "points_per_pacgum",
                "points_per_super_pacgum",
                "points_per_ghost",
            )

            for key in score_keys:
                value = config[key]
                if not isinstance(value, int):
                    raise Error_handling(f"'{key}' must be an integer")
                if value < 0:
                    raise Error_handling(f"'{key}' cannot be negative")

            seed = config["seed"]
            if not isinstance(seed, int):
                raise Error_handling("'seed' must be an integer")

            levels = config["level"]

            if not isinstance(levels, list) or not levels:
                raise Error_handling("'level' must be a non-empty list")

            for index, level in enumerate(levels):
                if not isinstance(level, dict):
                    raise Error_handling(f"Level {index + 1} must be an object")

                for dimension in ("width", "height"):
                    value = level.get(dimension)

                    if not isinstance(value, int):
                        raise Error_handling(
                            f"Level {index + 1}: '{dimension}' "
                            "must be an integer"
                        )

                    if value <= 0:
                        raise Error_handling(
                            f"Level {index + 1}: '{dimension}' "
                            "must be positive"
                        )
            
            return config


    except FileNotFoundError as e:
        raise Error_handling(e)

    except json.JSONDecodeError as e :
        raise Error_handling(e)
    


# print(parse_config("config.json"))
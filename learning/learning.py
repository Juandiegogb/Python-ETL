import pandas as pd


def test():
    data = {
        "nombre": ["Juan", "Diego", "Miguel", "Maria", "Sara"],
        "carrera": ["Sistemas", "Medicina", "Medicina", "Economia", "Gastronomia"],
        "email": [
            "juan@gmail.com",
            "diego@gmail.com",
            "miguel@gmail.com",
            "maria@gmail.com",
            "sara@gmail.com",
        ],
    }

    df = pd.DataFrame(data)
    df.to_csv("./processed_data/test.csv")
    print(df)


def test2():
    df = pd.DataFrame(
        [["Juan", 21], ["Maria", 23], ["Sara", 23]], columns=["Nombre", "Edad"]
    )
    df.info()

    df.to_csv("./processed_data/test2.csv")


def test3():
    df = pd.DataFrame(np.random.randn(4, 3), columns=["a", "b", "c"])
    df.to_csv("./processed_data/numpy.csv")


def dataset():
    df = pd.read_csv("ModalidadVirtual.csv")
    print(df["carrera"][1])
    filter_age = df["edad"] == 21
    df_filtered_age = df[filter_age]
    print(df_filtered_age.head(2))

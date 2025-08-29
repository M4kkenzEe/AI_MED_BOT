import chromadb

from extract_diagnoses import collect_diagnoses_from_file


def init_db():
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection(name="diagnoses")
    return collection


def fill_db(collection):
    documents = collect_diagnoses_from_file()
    ids = [f"diag_{i}" for i in range(len(documents))]

    collection.add(
        ids=ids,
        documents=documents
    )


if __name__ == "__main__":
    collection = init_db()
    fill_db(collection)
    print("База данных создана и заполнена")

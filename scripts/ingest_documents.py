from pathlib import Path
import json

from langchain_text_splitters import RecursiveCharacterTextSplitter



#---------------------------
# Configuration
#---------------------------


DATA_DIR= Path("data")
OUTPUT_DIR= Path("processed_data")


OUTPUT_FILE= OUTPUT_DIR / "document_chunks.json"



#--------------------------
# RBAC (Role-Based Access Control) Guardrails
#--------------------------


DEPARTMENT_ROLES= {
    "engineering": ["engineering", "executive"],
    "finance": ["finance", "executive"],
    "hr": ["hr", "executive"],
    "marketing": ["marketing", "executive"],
    "executive": ["executive"],
    "general": ["engineering", "finance", "hr", "marketing", "executive"]
}


#--------------------------
# Text Splitter
#--------------------------


text_splitter= RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150,
    separators=[
        "\n\n",
        "\n",
        ". ",
        " ",
        "",
    ]
)


# --------------------------
# Ingest Documents 
# --------------------------

def load_markdown_documents():
    documents=[]

    for file_path in DATA_DIR.rglob("*.md"):

        relative_path=file_path.relative_to(DATA_DIR)

        # First directory is department after data/
        department= relative_path.parts[0].lower()

        # Read document
        text = file_path.read_text(
            encoding="utf-8"
        )

        if not text.strip():
            continue

        # split document
        chunks= text_splitter.split_text(text)

        #Get Allowed Roles

        access_roles= DEPARTMENT_ROLES.get(
            department,
            []
        )

        for chunk_index, chunk in enumerate(chunks):

            documents.append(
                {
                    "id": f"{file_path.stem}-{chunk_index}",
                    "text": chunk,

                    "metadata": {
                        "source": str(relative_path),
                        "filename":file_path.name,
                        "department": department,
                        "access_roles":access_roles,
                        "chunk_index": chunk_index
                    }
                }
            )


    return documents



def main():
    print("Starting document ingestion...")

    documents=load_markdown_documents()

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    with OUTPUT_FILE.open(
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            documents,
            file,
            indent=2,
            ensure_ascii=True
        )

    print()
    print("Ingestion completed.")
    print(f"Documents/chunks created: {len(documents)}")
    print(f"Output: {OUTPUT_FILE}")


if __name__=="__main__":
    main()
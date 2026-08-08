from gitsource import GithubRepositoryDataReader


REPO_OWNER = "DataTalksClub"
REPO_NAME = "llm-zoomcamp"
COMMIT_ID = "8c1834d"


def load_lesson_files():
    reader = GithubRepositoryDataReader(
        repo_owner=REPO_OWNER,
        repo_name=REPO_NAME,
        commit_id=COMMIT_ID,
        allowed_extensions={"md"},
        filename_filter=lambda path: "/lessons/" in path,
    )

    return reader.read()


def load_documents():
    files = load_lesson_files()

    documents = []

    for file in files:
        doc = file.parse()
        documents.append(doc)

    return documents
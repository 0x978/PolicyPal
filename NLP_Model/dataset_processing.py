import os
import json


# Given the path to a web scraped dataset, turns the dataset into a JSONL file, where each row in the JSONL file
# contains a privacy policy and its associated summary.
def process_json(folder_path, document):
    with open(f"{document}_dataset.jsonl", 'w') as jsonl_data:
        for folder in os.listdir(folder_path):
            nested_folder_path = os.path.join(folder_path, folder)
            processed_document = process_document(nested_folder_path, document)

            if "document" in processed_document and "summary" in processed_document:
                # Writing in JSONL format for better compatibility with Kaggle.
                # This is almost identical to JSON but uses new lines as a delimiter; kaggle disagrees my JSON format.
                jsonl_data.write(json.dumps(
                    {"summary": processed_document["summary"], "document": processed_document["document"]}) + '\n')


# Returns an object with the document, and it's associated summary in an object
def process_document(path, document):
    data = {}

    # Create paths to document and document summary in current directory.
    document_path = os.path.join(path, f'{document}.txt')
    summary_document_path = os.path.join(path, f'{document}_Summary.txt')

    # If paths to the privacy policy and its summary exists.
    if os.path.exists(document_path) and os.path.exists(summary_document_path):
        with open(document_path, 'r', encoding="utf-8") as curr_doc:
            with open(summary_document_path, 'r', encoding="utf-8") as summary:
                # write the content of the privacy policy and summary to object
                data = {
                    "document": curr_doc.read().strip(),
                    "summary": summary.read().strip(),
                }

    return data


# Joins multiple JSON into one
def json_merger(merged_file, *jsons):  # Asterisk in param means we can pass in any number of input json.
    with open(merged_file, 'w') as out_file:
        for curr_json in jsons:
            with open(curr_json, 'r') as in_json:
                for line in in_json:
                    out_file.write(line)


def process_score_dataset(path):
    for folder in os.listdir(path):
        joint_path = f'{path}/{folder}'

        terms_summary = None

        privacy_summary = None

        rating = None

        tos_summary_path = joint_path + '/Terms_Summary.txt'
        privacy_summary_path = joint_path + '/Privacy_Policy_Summary.txt'
        rating_path = joint_path + '/rating.txt'

        rating = process_score(rating_path)
        if not rating:
            continue

        terms_summary = process_score(tos_summary_path)
        privacy_summary = process_score(privacy_summary_path)
        rating = process_score(rating_path)

        if not rating:
            continue

        isWritten = write_scores(terms_summary, privacy_summary, rating)
        if isWritten:
            if terms_summary and rating:
                print(f'Wrote terms summary and rating of {rating} to disk')
            if privacy_summary and rating:
                print(f'Wrote privacy policy summary and rating of {rating} to disk')


def process_score(path):
    if os.path.exists(path):
        with open(path, 'r', encoding="utf-8") as curr_doc:
            if not curr_doc:
                return None
            return curr_doc.read().strip()


def write_scores(terms_summary, privacy_summary, rating):
    if not terms_summary and not privacy_summary:
        return None
    if not rating:
        return None


    with open(f"scoring_dataset.jsonl", 'a') as jsonl_data:
        if terms_summary:
            jsonl_data.write(json.dumps(
                {"summary": terms_summary, "rating": rating}) + '\n')

        if privacy_summary:
            jsonl_data.write(json.dumps(
                {"summary": privacy_summary, "rating": rating}) + '\n')



    return True


SCRAPED_DATA_PATH = "../Web_Scraper/scraped_data"
# process_json(SCRAPED_DATA_PATH, "Terms")
# json_merger("Merged_Dataset.jsonl","Privacy_Policy_dataset.jsonl","Terms_dataset.jsonl")
process_score_dataset(SCRAPED_DATA_PATH)

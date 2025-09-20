import os
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if not url or not key:
    raise Exception("Supabase URL or Key not found in environment variables!")

sb: Client = create_client(url, key)


def return_book(record_id: int):
    """Return a borrowed book → set return_date and increase stock"""

    # 1. Find the borrow record
    rec_resp = sb.table("borrow_records").select("*").eq("record_id", record_id).single().execute()
    
    if not rec_resp.data:
        return {"error": f"Borrow record {record_id} not found."}

    borrow_record = rec_resp.data

    if borrow_record["return_date"] is not None:
        return {"error": "Book already returned."}

    book_id = borrow_record["book_id"]

    # 2. Update return_date
    now = datetime.utcnow().isoformat()
    sb.table("borrow_records").update({"return_date": now}).eq("record_id", record_id).execute()

    # 3. Increase book stock by 1
    book_resp = sb.table("books").select("stock").eq("book_id", book_id).single().execute()
    if not book_resp.data:
        return {"error": f"Book {book_id} not found."}

    stock = book_resp.data["stock"]
    sb.table("books").update({"stock": stock + 1}).eq("book_id", book_id).execute()

    return {"message": "Book returned successfully ", "record_id": record_id, "book_id": book_id}


if __name__ == "__main__":
    print("Library Management - Return Book")

    record_id = int(input("Enter borrow record_id to return: ").strip())

    result = return_book(record_id)
    print(result)

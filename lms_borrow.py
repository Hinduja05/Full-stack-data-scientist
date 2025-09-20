import os
from supabase import create_client, Client
from dotenv import load_dotenv


load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if not url or not key:
    raise Exception("Supabase URL or Key not found in environment variables!")

sb: Client = create_client(url, key)


def borrow_book(member_id: int, book_id: int):
    """Borrow a book if stock available"""

    
    book_resp = sb.table("books").select("stock").eq("book_id", book_id).single().execute()
    
    if not book_resp.data:
        return {"error": f"Book with id {book_id} not found."}

    stock = book_resp.data["stock"]

    if stock <= 0:
        return {"error": "Book not available."}

   
    sb.table("books").update({"stock": stock - 1}).eq("book_id", book_id).execute()

 
    borrow_payload = {
        "member_id": member_id,
        "book_id": book_id,
    }
    borrow_resp = sb.table("borrow_records").insert(borrow_payload).execute()

    return {"message": "Book borrowed successfully ", "record": borrow_resp.data}

if __name__ == "__main__":
    print(" Library Management - Borrow Book")

    member_id = int(input("Enter member_id: ").strip())
    book_id = int(input("Enter book_id: ").strip())

    result = borrow_book(member_id, book_id)
    print(result)

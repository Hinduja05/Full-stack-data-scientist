import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if not url or not key:
    raise Exception("Supabase URL or Key not found in environment variables!")

sb: Client = create_client(url, key)



def delete_member(member_id: int):
    """Delete member if no borrowed books exist"""
    # Check if member has active borrow records
    active = sb.table("borrow_records").select("*").eq("member_id", member_id).is_("return_date", None).execute()
    
    if active.data:  # still borrowed books
        return {"error": "Cannot delete member: borrowed books exist."}

    resp = sb.table("members").delete().eq("member_id", member_id).execute()
    return resp.data if resp.data else {"error": "No member found."}


def delete_book(book_id: int):
    """Delete book if not borrowed"""
    # Check if the book is currently borrowed
    active = sb.table("borrow_records").select("*").eq("book_id", book_id).is_("return_date", None).execute()
    
    if active.data:  # still borrowed
        return {"error": "Cannot delete book: it is currently borrowed."}

    resp = sb.table("books").delete().eq("book_id", book_id).execute()
    return resp.data if resp.data else {"error": "No book found."}


if __name__ == "__main__":
    print("Library Management - Delete Operations")
    print("1. Delete Member")
    print("2. Delete Book")

    choice = input("Enter choice: ").strip()

    if choice == "1":
        member_id = int(input("Enter member_id to delete: ").strip())
        result = delete_member(member_id)
        print(result)

    elif choice == "2":
        book_id = int(input("Enter book_id to delete: ").strip())
        result = delete_book(book_id)
        print(result)

    else:
        print("Invalid choice!")

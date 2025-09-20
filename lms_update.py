import os
from supabase import create_client, Client
from dotenv import load_dotenv


load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if not url or not key:
    raise Exception("Supabase URL or Key not found in environment variables!")

sb: Client = create_client(url, key)



def update_book_stock(book_id: int, new_stock: int):
    """Update stock of a book"""
    resp = sb.table("books").update({"stock": new_stock}).eq("book_id", book_id).execute()
    return resp.data

def update_member(member_id: int, name: str = None, email: str = None):
    """Update member info (name/email)"""
    update_data = {}
    if name:
        update_data["name"] = name
    if email:
        update_data["email"] = email

    if not update_data:
        raise Exception("No fields provided for update!")

    resp = sb.table("members").update(update_data).eq("member_id", member_id).execute()
    return resp.data

if __name__ == "__main__":
    print("Library Management - Update Operations")
    print("1. Update Book Stock")
    print("2. Update Member Info")

    choice = input("Enter choice: ").strip()

    if choice == "1":
        book_id = int(input("Enter book_id: ").strip())
        new_stock = int(input("Enter new stock value: ").strip())
        updated = update_book_stock(book_id, new_stock)
        if updated:
            print("Book stock updated:", updated)
        else:
            print("No book found with that ID.")

    elif choice == "2":
        member_id = int(input("Enter member_id: ").strip())
        print("Leave blank if you don’t want to update a field.")
        new_name = input("Enter new name: ").strip() or None
        new_email = input("Enter new email: ").strip() or None
        updated = update_member(member_id, new_name, new_email)
        if updated:
            print("Member info updated:", updated)
        else:
            print("No member found with that ID.")

    else:
        print("Invalid choice!")

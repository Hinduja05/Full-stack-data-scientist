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



def add_member(name: str, email: str):
    """Register a new member"""
    payload = {"name": name, "email": email}
    resp = sb.table("members").insert(payload).execute()
    return resp.data

def add_book(title: str, author: str, category: str, stock: int = 1):
    """Add a new book"""
    payload = {"title": title, "author": author, "category": category, "stock": stock}
    resp = sb.table("books").insert(payload).execute()
    return resp.data


if __name__ == "__main__":
    print("Library Management - Insert Operations")
    print("1. Add Member")
    print("2. Add Book")

    choice = input("Enter choice: ").strip()

    if choice == "1":
        name = input("Enter member name: ").strip()
        email = input("Enter member email: ").strip()
        created = add_member(name, email)
        print("Member added:", created)

    elif choice == "2":
        title = input("Enter book title: ").strip()
        author = input("Enter author name: ").strip()
        category = input("Enter category: ").strip()
        stock = int(input("Enter stock: ").strip() or 1)
        created = add_book(title, author, category, stock)
        print("Book added:", created)

    else:
        print("Invalid choice!")
